import boto3
from decouple import config

# S3 클라이언트 생성
s3 = boto3.client(
    's3',
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
    region_name=config('AWS_S3_REGION_NAME')
)

bucket_name = config('AWS_STORAGE_BUCKET_NAME')

try:
    response = s3.head_bucket(Bucket=bucket_name)
    print(f"'{bucket_name}' 버킷이 존재합니다.")
except Exception as e:
    print(f"'{bucket_name}' 버킷이 존재하지 않거나 접근 권한이 없습니다:", str(e))
    
# 특정 버킷에 파일 업로드

file_name = 'README.md'  # 업로드할 파일 이름
object_name = 'test.txt'  # S3에 저장될 경로

try:
    with open(file_name, 'rb') as file_data:
        s3.upload_fileobj(file_data, bucket_name, object_name)
    print(f"파일이 성공적으로 {bucket_name}/{object_name}에 업로드되었습니다.")
except Exception as e:
    print("파일 업로드 실패:", str(e))
