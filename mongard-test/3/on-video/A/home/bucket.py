import boto3
from django.conf import settings
import logging
import logging
from botocore.exceptions import ClientError

try:
   s3_resource = boto3.resource(
       's3',
       endpoint_url='https://s3.ir-thr-at1.arvanstorage.com',
       aws_access_key_id='60850c20bf35fdc12193e7eb2a43380223df51e6ca412e63a8835f35cd7c0479',
       aws_secret_access_key='216643bc-a5e2-432c-a5c3-df7815a3d60c'
   )
except Exception as exc:
   logging.error(exc)
else:
   try:
       bucket_name = 'django-shop-erfan'
       bucket = s3_resource.Bucket(bucket_name)
       bucket.create(ACL='public-read') # ACL='private'|'public-read'
   except ClientError as exc:
       logging.error(exc)