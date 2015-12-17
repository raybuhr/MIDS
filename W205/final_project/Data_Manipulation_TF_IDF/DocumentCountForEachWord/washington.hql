--Kasane Utsumi - 05/02/2015
--washington.hql
--Hive script for a mapreduce job to count how many document contains each word in Washington Post article table.

drop table if exists texts;

--create a table from the source DynamoDb table. In this case, source is articles from Washington_Post table and "text" is the column which contains article body. 
CREATE EXTERNAL TABLE texts (text string)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler' 
TBLPROPERTIES ("dynamodb.table.name" = "Washington_Post", 
"dynamodb.column.mapping" = "text:text");     

drop table if exists word_count2;

--create a table that will be used as an output with number of documents that contains each word. "word" column will contain word, and "count" will be the document count.
--In this case, result will be written to an another dynamodb table. 
create external table if not exists word_count2(word string, count bigint)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler' 
TBLPROPERTIES ("dynamodb.table.name" = "Washington_PostWordCount", 
"dynamodb.column.mapping" = "word:word,count:count");  

-- add mapper and reducer python files                    
add file s3://final205/python/mapperDocCount.py;
add file s3://final205/python/reducerDocCount.py;

--run map reduce job and dump result in the word_count3 table created above, which in turn would dump result into the associated DynamoDb table. 
from (
        from texts
        map texts.text
        using 'python mapperDocCount.py'
        as word, count
        cluster by word) map_output
insert overwrite table word_count2
reduce map_output.word, map_output.count
using 'python reducerDocCount.py'
as word,count;



