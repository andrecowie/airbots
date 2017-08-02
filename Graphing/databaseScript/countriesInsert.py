
import boto3
import uuid
session = boto3.session.Session(profile_name="autrdproject")
client = session.client('dynamodb')
