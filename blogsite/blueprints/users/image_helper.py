import boto3
import botocore
import os

s3 = boto3.client("s3", 
    aws_access_key_id=os.environ.get("S3_KEY"), 
    aws_secret_access_key=os.environ.get("S3_SECRET"))

my_bucket=os.environ.get('S3_BUCKET')

#UPLOAD FILES TO S3
def upload_file_to_s3(file, bucket_name=my_bucket, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    # This is a catch all exception, edit this part to fit your needs
    except Exception as e:
        print("Algo Paso", e)
        return e

    #Return a URL to the uploaded file
    return "{}{}".format(os.environ.get("S3_LOCATION"), file.filename)

#UPDATE FILE
def delete_file_from_s3(file, bucket_name=my_bucket, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """


    try:
        s3.delete_object(
            Bucket=bucket_name,
            Key=file
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

def allowed_profile_images(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'png', 'jpeg']


def allowed_images(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'png', 'jpeg']
