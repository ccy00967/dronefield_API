import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from core import settings
from django.core.files.storage import default_storage
import uuid

def s3_upload_file(file_obj, file_name):
    """
    S3에 파일 업로드
    :param file_obj: 업로드할 파일 객체 (InMemoryUploadedFile)
    :param file_name: S3에 저장될 경로 및 파일 이름
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # S3에 파일 객체 업로드
        s3_client.upload_fileobj(
            file_obj,  # 파일 객체
            settings.AWS_STORAGE_BUCKET_NAME,
            file_name,
            ExtraArgs={'ACL': 'public-read'}  # 퍼블릭 읽기 권한 (옵션)
        )
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_name}"
    except Exception as e:
        print(f"파일 업로드 실패: {str(e)}")
        return None
