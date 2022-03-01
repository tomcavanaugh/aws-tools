import json
import boto3
import sys


try:
    newTag = sys.argv[1]
    newTagValue = sys.argv[2]
except:
    raise SystemExit(f"Usage: {sys.argv[0]} tag value")
    
print(f'Adding/updating all buckets with tag => {newTag}={newTagValue}')

# session = boto3.session.Session(profile_name='default')
s3_client = boto3.client('s3')
put_bucket_tagging_response = s3_client.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in put_bucket_tagging_response['Buckets']:
    print(f'  {bucket["Name"]}')
    tags_to_write = dict()
    try:
        get_bucket_tagging_response = s3_client.get_bucket_tagging(Bucket=bucket["Name"])      
        for i in get_bucket_tagging_response['TagSet']:
            key = i['Key']
            val = i['Value']
            tags_to_write[key]=val
    except Exception as e:
        print(e)
        print("There was no tag")
    
    print(f'  Existing Tags: {tags_to_write}')

    tags_to_write[newTag]=newTagValue

    put_bucket_tagging_response = s3_client.put_bucket_tagging(
        Bucket=bucket["Name"],
        Tagging={
            'TagSet': [{'Key': str(k), 'Value': str(v)} for k, v in tags_to_write.items()]
        }
    )
