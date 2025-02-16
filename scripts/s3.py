import boto3
import os

bucket_name = "vugiau"
s3 = boto3.client('s3')

def download_folder_from_s3(bucket_name, s3_folder, local_dir):
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
        if 'Contents' in result:
            for obj in result['Contents']:
                s3_key = obj['Key']
                local_file_path = os.path.join(local_dir, os.path.relpath(s3_key, s3_folder))
                local_file_dir = os.path.dirname(local_file_path)
                if not os.path.exists(local_file_dir):
                    os.makedirs(local_file_dir)
                s3.download_file(bucket_name, s3_key, local_file_path)

def upload_image_to_s3(file_name, s3_prefix="ml_images", object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    object_name = f"{s3_prefix}/{object_name}"

    s3.upload_file(file_name, bucket_name, object_name)

    response = s3.generate_presigned_url('get_object',
                                         Params={
                                             "Bucket": bucket_name,
                                             "Key": object_name
                                         },
                                         ExpiresIn=3600)
    
    return response
