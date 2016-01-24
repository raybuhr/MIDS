# Using the guide at https://spark.apache.org/docs/1.5.2/ml-guide.html
# we are going to try and predict a reddit comment's controversiality score 
# by the text of comments. The training set will be August 2015 comments
# and test set will be September 2015 comments.

from pyspark import SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.sql import SQLContext
from pyspark.sql import DataFrameWriter

# Module Constants
APP_NAME = "reddit-comment-controversiality-regression"
REDDIT_AUG = "swift://reddit3.sjc01/RC_2010-08"
REDDIT_SEPT = "swift://reddit3.sjc01/RC_2010-09"

if __name__ == "__main__":
    
    # Configure Spark
    sc = SparkContext(appName=APP_NAME)
    sqlContext = SQLContext(sc)

    # Configure an ML pipeline, which consists of tree stages: tokenizer, hashingTF, and lr.
    tokenizer = Tokenizer(inputCol="body", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
    lr = LogisticRegression(maxIter=10, regParam=0.01)
    pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

    # prepare Reddit json files as sql Dataframes for pyspark.ml
    aug_comments =  sqlContext.read.json(REDDIT_AUG)
    sep_comments = sqlContext.read.json(REDDIT_SEPT)

    training = aug_comments.select('id', 'body', (aug_comments.controversiality).cast("double").alias('label'))
    test = sep_comments.select('id', 'body')
    test_actual = sep_comments.select('id', (sep_comments.controversiality).alias('actual'))

    model = pipeline.fit(training)
    prediction = model.transform(test)
    selected = prediction.select("id", "text", "prediction").join(test_actual, prediction.id == test_actual.id)
    selected.write.format('json').save("hdfs://master/usr/hadoop/karma_predictions")
    sc.stop()