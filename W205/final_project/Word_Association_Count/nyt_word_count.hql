--Kasane Utsumi
--nyt_word_count.hql 
--Hql file used for EMR word count in new york times corpus table

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
        using '${SCRIPT}/mapperWordCount.py'
        as word, count
        cluster by word) map_output
insert overwrite table word_count
reduce map_output.word, map_output.count
using '${SCRIPT}/reducer.py'
as word,count;
