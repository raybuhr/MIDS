--Kasane Utsumi
--nyt_word_keyword.hql 
--Hql file used for EMR job to count words appearing in a same doc as top 100 words in New York Times corpus table

drop table if exists texts;

CREATE EXTERNAL TABLE texts (snippet string)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler' 
TBLPROPERTIES ("dynamodb.table.name" = "NYT_NOSGI", 
"dynamodb.column.mapping" = "snippet:snippet");     

drop table if exists word_count;

create external table if not exists word_count(word string, count int)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
lines terminated by '\n'
STORED AS TEXTFILE 
LOCATION '${OUTPUT}';

from (
        from texts
        map texts.snippet
        using '${SCRIPT}/mapperKeyword.py'
        as word, count
        cluster by word) map_output
insert overwrite table word_count
reduce map_output.word, map_output.count
using '${SCRIPT}/reducerKeyword.py'
as word,count;
