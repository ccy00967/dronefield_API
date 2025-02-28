import logging
from django.core.files.base import ContentFile
from common.models import TestDocument

# 현재 모듈에 대한 로거 생성
logger = logging.getLogger(__name__)

def test_upload():
    logger.info("테스트 파일 업로드 시작")
    
    try:
        # ContentFile을 이용해 테스트용 텍스트 파일 생성
        content = ContentFile("모델로 업로드 테스트입니다.", name="model_test.txt")
        document = TestDocument.objects.create(file=content)
        logger.info(f"파일 업로드 완료: {document.file.url}")
        print(f"파일 업로드 완료: {document.file.url}")
    except Exception as e:
        logger.error("파일 업로드 중 오류 발생", exc_info=True)
        print(f"에러 발생: {e}")

    return document

