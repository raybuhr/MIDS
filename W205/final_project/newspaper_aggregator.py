# -*- coding: utf-8 -*- 
import newspaper #Newspaper: Article scraping & curation
import boto.dynamodb #boto: interfaces to Amazon Web Services (AWS)

# Create a connection to AWS NoSQL Database, DynamoDB
# Note you will need to enter your own private keys from AWS
conn = boto.dynamodb.connect_to_region(
       'us-west-2',
       aws_access_key_id="enter key",
       aws_secret_access_key="enter secret")

# To create a new table, we have to set up the schema
# The schema requires a primary hash key and allows a secondary range key
my_schema = conn.create_schema(hash_key_name = 'id', hash_key_proto_value = int)

# Create the table by providing a name, schema and the computing power required by AWS
table = conn.create_table(name="newspaper", schema=my_schema, read_units=10, write_units=5)

# To fill our table, we are going to parse through websites that publish news
# The newspaper package happens to contain a list of over 200 popular news websites
sources = newspaper.popular_urls()

hashkey = 1 # primary key integer to be used for DynamoDB table
source_iterator = 0 # iterator to be increased at end of loop to move to next source

for source in sources:
    parser = sources[source_iterator]
    try:
        collect = newspaper.build(parser) # Build method returns an object with each sub-site url
    except:
        source_iterator += 1 # If the Build method fails, move on to next source

    # Store articles as dict type in a list to iterate through for upload to DynamoDB
    collection = []  
    for article in collect.articles:
        try:
            data = {}
            article.download() # Similar to requests, downloads html
            article.parse() # Uses lxml package to organize html
            data['url'] = article.url
            data['date'] = str(article.publish_date) # Have to store as string because DynamoDB does not recognize python datetime object
            data['text'] = article.text
            collection.append(data)    
        except:
            pass
    
    # Once the list of articles is collected, need to check for any empty text
    for i in collection:
        if len(i['text']) == 0:
            collection.pop(collection.index(i))

    # Get DynamoDB table            
    table = conn.get_table('newspaper')

    # Iterate through list of articles and upload to table
    item_counter = hashkey
    list_counter = 0
    for a in collection:
        try:
            item = table.new_item(hash_key=item_counter,attrs=collection[list_counter])
            item.put()
            item_counter += 1
            list_counter += 1
        except:
            pass

    hashkey += len(collection) # Continue primary key for DynamoDB table
    source_iterator += 1 # Move on to next source
