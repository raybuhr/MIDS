CREATE EXTERNAL TABLE cnntexts (body string, timestamp string)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
TBLPROPERTIES ("dynamodb.table.name" = "CNN",
"dynamodb.column.mapping" = "body:body,timestamp:timestamp");

DROP TABLE IF EXISTS wc_cnn;

CREATE TABLE wc_cnn (word string, tstamp string, count float);

INSERT OVERWRITE TABLE wc_cnn
SELECT word, timestamp, COUNT(*) FROM cnntexts                     
LATERAL VIEW explode(split(lower(cnntexts.body), '\\W+')) x as word
WHERE word REGEXP "^[A-Za-z+'-]+$"
GROUP BY word, timestamp;

DROP TABLE IF EXISTS wctot_cnn;

CREATE TABLE wctot_cnn (tstamp string, count float);

INSERT OVERWRITE TABLE wctot_cnn
SELECT timestamp, COUNT(*) FROM cnntexts
LATERAL VIEW explode(split(lower(cnntexts.body), '\\W+')) x as word
WHERE word REGEXP "^[A-Za-z+'-]+$"
GROUP BY timestamp;

DROP TABLE IF EXISTS tf_cnn;

CREATE TABLE tf_cnn (word string, tstamp string, tf float);

INSERT OVERWRITE TABLE tf_cnn
SELECT wc_cnn.word, wc_cnn.tstamp,
wc_cnn.count/wctot_cnn.count as tf
FROM wc_cnn JOIN wctot_cnn ON (wc_cnn.tstamp=wctot_cnn.tstamp)
ORDER BY tf desc;

CREATE EXTERNAL TABLE CNN_TF_Index
(word string,tstamp string,count bigint)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
TBLPROPERTIES ("dynamodb.table.name"="CNN_TF_Index","dynamodb.column.mapping" =
"word:word,tstamp:tstamp,count:count");

INSERT OVERWRITE TABLE CNN_TF_Index
SELECT * FROM tf_cnn;

SET dynamodb.throughput.write.percent=1.0;

CREATE TABLE df_cnn (word string, df int);

INSERT OVERWRITE TABLE df_cnn
SELECT word, count(*)
FROM tf_cnn

CREATE TABLE tfidf_cnn
(word string, timestamp string, tfidf float);

select count(distinct tstamp) from tf_cnn;
10309

set hivevar:n_docs_cnn=10309;

INSERT OVERWRITE TABLE tfidf_cnn
SELECT tf_cnn.tstamp, tf_cnn.word,
tf_cnn.count*(log10(CAST(${n_docs_cnn} as FLOAT)/df_cnn.df+1.0)) as tfidf
FROM tf_cnn JOIN df_cnn ON (tf_cnn.word=df_cnn.word)
ORDER BY tfidf desc;

CREATE EXTERNAL TABLE CNN_tfidf
(tstamp string,word string,tfidf double)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
TBLPROPERTIES ("dynamodb.table.name"="CNN_tfidf","dynamodb.column.mapping" =
"tstamp:tstamp,word:word,tfidf:tfidf");

INSERT OVERWRITE TABLE CNN_tfidf
SELECT * FROM tfidf_cnn;

