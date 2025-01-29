import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from core import settings
from django.core.files.storage import default_storage
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

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
        #추가인 부분
        if isinstance(file_obj, InMemoryUploadedFile):
            file_obj.seek(0)  # 파일 읽기 위치를 처음으로 이동
            file_data = io.BytesIO(file_obj.read())  # 파일을 BytesIO 객체로 변환
            content_type = file_obj.content_type  # 파일의 Content-Type 유지
        else:
            file_data = file_obj
            content_type = "application/octet-stream"
        
        
        # S3에 파일 객체 업로드
        s3_client.upload_fileobj(
            file_data,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_name,
            ExtraArgs={'ACL': 'public-read'}#, 'ContentType': content_type}  # ContentType 추가
        )
        
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_name}"
    except NoCredentialsError:
        print("AWS 자격 증명이 설정되지 않았습니다.")
        return None
    except PartialCredentialsError:
        print("AWS 자격 증명이 일부만 설정되었습니다.")
        return None
    except Exception as e:
        print(f"파일 업로드 실패: {str(e)}")
        return None

def s3_delete_file(file_url):
    """
    S3에서 파일 삭제
    :param file_url: 삭제할 파일의 S3 URL
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # S3 URL에서 파일 경로 추출
        file_key = file_url.split(f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/")[-1]
        
        # 파일 삭제
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
        print(f"Deleted old S3 file: {file_key}")
        
    except Exception as e:
        print(f"S3 파일 삭제 실패: {str(e)}")