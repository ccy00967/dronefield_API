from user.models import CustomUser
from farmer.models import FarmInfo
from exterminator.models import ExterminatorLicense, Drone
import uuid
import random
from common.utils.s3 import s3_upload_file, s3_delete_file
from farmer.models import FarmInfo
from django.core.files.uploadedfile import SimpleUploadedFile

gender_choices = ['0', '1'] # 예: 여성, 남성
nation_choices = ['0', '1'] # 예: 내국인, 외국인인
type_choices = [3, 4]  # 예: 1=어드민, 2=매니저, 3=드론조종사, 4=농지소유주
# 🔹 `/media/test.png`을 파일 객체로 변환 후 S3에 업로드

TEST_IMAGE_PATH = "/home/git/dronefield_API/media/test_license.png"
def get_uploaded_file(file_path, file_name="test.png"):
    with open(file_path, "rb") as f:
        return SimpleUploadedFile(name=file_name, content=f.read(), content_type="image/png")
license_file = get_uploaded_file(TEST_IMAGE_PATH)
license_image_url = s3_upload_file(license_file, f"exterminator/images/license/{uuid.uuid4()}.png")
business_file = get_uploaded_file(TEST_IMAGE_PATH)
business_registration_image_url = s3_upload_file(business_file, f"exterminator/images/business/{uuid.uuid4()}.png")
drone_file = get_uploaded_file(TEST_IMAGE_PATH)
drone_image_url = s3_upload_file(drone_file, f"drones/images/{uuid.uuid4()}.png")

  
def create_test():
    #테스트 농민민
    famrmer = CustomUser.objects.create(
        uuid=uuid.uuid4(),
        name=f"test_농민",
        birthdate="19900101",
        gender=random.choice(gender_choices),
        nationalinfo='1',
        mobileno=f"11111111111",
        email=f"test_farmer@test.com",
        type=4,
        road=f"TestRoad_farmer",
        jibun=f"TestJibun_farmer",
        detail=f"TestDetail_farmer",
        is_active=True,
    )
    famrmer.set_password("test1234@")
    famrmer.save() 
    for i in range(20):
        FarmInfo.objects.create(
            uuid=uuid.uuid4(),
            owner=famrmer,
            road=f"TestRoad{i}",
            jibun=f"TestJibun{i}",
            detail=f"TestDetail{i}",
            pnu=f"pnu{i}",
            lndpclAr="20.00",
            cd=f"cd{i}",
            landNickName=f"landNickName{i}",
            cropsInfo=f"cropsInfo{i}",
            additionalPhoneNum=f"0100000{1000+i:04}"
        )
        
        
    #테스트 방제사
    exter = CustomUser.objects.create(
        uuid=uuid.uuid4(),
        name=f"test_방제사",
        birthdate="19900101",
        gender=random.choice(gender_choices),
        nationalinfo='1',
        mobileno=f"22222222222",
        email=f"test_exterminator@test.com",
        type=3,
        road=f"TestRoad_exterminator",
        jibun=f"TestJibun_exterminator",
        detail=f"TestDetail_exterminator",
        is_active=True,
    )
    exter.set_password("test1234@")
    exter.save() 
    for i in range(20):
        ExterminatorLicense.objects.create(
            uuid=uuid.uuid4(),
            license_title=f"license_title{i}",
            license_number=f"license_number{i}",
            lincense_holder_name=f"lincense_holder_name{i}",
            business_registration_type=f"business_registration_type{i}",
            worker_registration_number=f"worker_registration_number{i}",
            owner=exter,
            license_image=license_image_url,  # S3 URL 저장
            business_registration_image=business_registration_image_url,  # S3 URL 저장
        )
        Drone.objects.create(
            uuid=uuid.uuid4(),
            nickname=f"nickname{i}",
            model_number=f"model_number{i}",
            capacity="20.00",
            owner=exter,
            image=drone_image_url,  # S3 URL 저장
        )
     
    for i in range(50):
        user = CustomUser.objects.create(
            uuid=uuid.uuid4(),
            name=f"test{i}",
            birthdate="19900101",
            gender=random.choice(gender_choices),
            nationalinfo=random.choice(nation_choices),
            mobileno=f"0100000{1000+i:04}",
            email=f"test{i}@test.com",
            type=random.choice(type_choices),
            road=f"TestRoad{i}",
            jibun=f"TestJibun{i}",
            detail=f"TestDetail{i}",
            is_active=True,
        )
        user.set_password("test1234@")
        user.save()

        for j in range(20):
            FarmInfo.objects.create(
                uuid=uuid.uuid4(),
                owner=user,  # 기존 `CustomUser.objects.get(name=f"test{i}")` 제거
                road=f"TestRoad{j}",
                jibun=f"TestJibun{j}",
                detail=f"TestDetail{j}",
                pnu=f"pnu{j}",
                lndpclAr="20.00",
                cd=f"cd{j}",
                landNickName=f"landNickName{j}",
                cropsInfo=f"cropsInfo{j}",
                additionalPhoneNum=f"0100000{1000+j:04}"
            )
            ExterminatorLicense.objects.create(
                uuid=uuid.uuid4(),
                license_title=f"license_title{j}",
                license_number=f"license_number{j}",
                lincense_holder_name=f"lincense_holder_name{j}",
                business_registration_type=f"business_registration_type{j}",
                worker_registration_number=f"worker_registration_number{j}",
                owner=user,  # 기존 `CustomUser.objects.get(name=f"test{i}")` 제거
                license_image=license_image_url,  # S3 URL 저장
                business_registration_image=business_registration_image_url,  # S3 URL 저장
            )
            Drone.objects.create(
                uuid=uuid.uuid4(),
                nickname=f"nickname{j}",
                model_number=f"model_number{j}",
                capacity="20.00",
                owner=user,  # 기존 `CustomUser.objects.get(name=f"test{i}")` 제거
                image=drone_image_url,  # S3 URL 저장
            )
            
    user = CustomUser.objects.create(
            uuid=uuid.uuid4(),
            name=f"test50",
            birthdate="19900101",
            gender=random.choice(gender_choices),
            nationalinfo=random.choice(nation_choices),
            mobileno=f"999999999999",
            email=f"test50@test.com",
            type=random.choice(type_choices),
            road=f"TestRoad50",
            jibun=f"TestJibun50",
            detail=f"TestDetail50",
            is_active=True,
    )
    user = CustomUser.objects.get(name=f"test50")
    user.set_password("test1234@")
    user.save()
        
    


create_test()
# 확인 메시지 출력
print("테스트 데이터 생성 완료")
print(f"CustomUser 생성된 유저 수: {CustomUser.objects.count()}")
print(f"FarmInfo 생성된 농지 수: {FarmInfo.objects.count()}")
print(f"ExterminatorLicense 생성된 방제사 면허 수: {ExterminatorLicense.objects.count()}")
print(f"Drone 생성된 드론 수: {Drone.objects.count()}")