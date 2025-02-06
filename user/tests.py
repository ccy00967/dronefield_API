from user.models import CustomUser, BankAccount
from farmer.models import FarmInfo
from exterminator.models import ExterminatorLicense, Drone
from trade.models import Request
from common.models import Alarm, Notice
import uuid
import random
from common.utils.s3 import s3_upload_file, s3_delete_file
from farmer.models import FarmInfo
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
from datetime import timedelta

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
    #테스트 농민민, 농민민
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
        optinal_consent=True,
        marketing_agreement_date=now(),
        required_consent_data=now()
    )
    famrmer.set_password("test1234@")
    famrmer.save()
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
        optinal_consent=True,
        marketing_agreement_date=now(),
        required_consent_data=now()
    )
    exter.set_password("test1234@")
    exter.save()
    BankAccount.objects.create(
        uuid=uuid.uuid4(),
        owner=exter,
        bank_name="농협",
        account_number="3025634745867890",
        account_type = "법인명"
    )
    
    road_list = [
    "경기도 이천시 농원로 12",     # 이천 농지 예시
    "충청북도 청주시 상당구 농업로 45",  # 청주 농지 예시
    "전라남도 순천시 농업대로 78",    # 순천 농지 예시
    "경상북도 영덕군 농촌로 22",      # 영덕 농지 예시
    "강원도 평창군 농로 33"         # 평창 농지 예시
    ]

    jibun_list = [
        "경기도 이천시 부발읍 123-4",    # 이천의 지번 주소 예시
        "충청북도 청주시 상당구 56-7",    # 청주의 지번 주소 예시
        "전라남도 순천시 89-10",         # 순천의 지번 주소 예시
        "경상북도 영덕군 11-12",         # 영덕의 지번 주소 예시
        "강원도 평창군 33-22"           # 평창의 지번 주소 예시
    ]

    detail_list = [
        "농지 A (이천지점)",
        "농지 B (청주지점)",
        "농지 C (순천지점)",
        "농지 D (영덕지점)",
        "농지 E (평창지점)"
    ]
    landNickName_list = [
        "이천지점 농지",
        "청주지점 농지",
        "순천지점 농지",
        "영덕지점 농지",
        "평창지점 농지"
    ]
    cropsInfo = [
        "딸기",
        "사과",
        "배",
        "블루베리",
        "토마토",
    ]
    #테스트 농지 및 거래
    for i in range(2):
        farm_info = FarmInfo.objects.create(
            uuid=uuid.uuid4(),
            owner=famrmer,
            road=road_list[i],
            jibun=jibun_list[i],
            detail= detail_list[i],
            pnu=f"pnu{i:04}",
            lndpclAr="20.00",
            cd=f"cd{i}",
            landNickName=landNickName_list[i],
            cropsInfo=cropsInfo[i],
            additionalPhoneNum=f"0100000{1000+i:04}",
            min_price=25
        )
        for j in range(0,3):
            if j == 0:
                exterminater_user = None
            else:
                exterminater_user = exter
            Request.objects.create(
                orderId=uuid.uuid4(),
                owner=famrmer,
                exterminator=exterminater_user,
                landInfo=farm_info,
                dealmothod=0,
                startDate=now(),
                endDate=now() + timedelta(days=11),
                pesticide=random.choice(["곰팡이살균제", "일본농약", "구형농약"]),
                setAveragePrice=30,
                requestAmount=25,
                reservateDepositAmount=1000,
                requestTosspayments = None,
                reservateTosspayments = None,
                #requestCancelTransactionKey = None,

                # 방제완료-농민
                checkState=0,
                requestDepositState = 0,

                # 방제완료-방제사
                exterminateState= j,#방제상황 0:매칭중, 1:작업준비중, 2:작업중, 3:작업완료
                reservateDepositState= 0,
                depositCancelTransactionKey = "uuid값",

                # 관리자용용
                calculation=0,
                # 신청금액-방제사

            )
    
        license_title_list =["특수드론1종", "경드론2종", "드론정비사", "비행기기운용전문가", "비행기기운용사"]
    for i in range(5):
        ExterminatorLicense.objects.create(
            uuid=uuid.uuid4(),
            license_title=license_title_list[i],
            license_number=f"0100000{1000+i:04}",
            lincense_holder_name=f"lincense_holder_name{i}",
            business_registration_type=random.choice(["개인", "법인"]),
            worker_registration_number=f"0100000{1000+i:04}",
            owner=exter,
            license_image=license_image_url,  # S3 URL 저장
            business_registration_image=business_registration_image_url,  # S3 URL 저장
        )
        Drone.objects.create(
            uuid=uuid.uuid4(),
            nickname=f"대형드론론{i}",
            model_number=f"MSE-{i}",
            capacity="20.00",
            owner=exter,
            image=drone_image_url,  # S3 URL 저장
        )
     
    for i in range(25):
        user = CustomUser.objects.create(
            uuid=uuid.uuid4(),
            name=f"test_farmer{i}",
            birthdate="19900101",
            gender=random.choice(gender_choices),
            nationalinfo=random.choice(nation_choices),
            mobileno=f"0100000{1000+i:04}",
            email=f"test_farmer{i}@test.com",
            type=4,
            road=f"TestRoad{i}",
            jibun=f"TestJibun{i}",
            detail=f"TestDetail{i}",
            is_active=True,
            optinal_consent=True,
            marketing_agreement_date=now(),
        required_consent_data=now()
        )
        user.set_password("test1234@")
        user.save()
        for j in range(10):
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
                additionalPhoneNum=f"0100000{1000+j:04}",
                min_price=25
            )
    for i in range(25):
        user = CustomUser.objects.create(
            uuid=uuid.uuid4(),
            name=f"test_exter{i}",
            birthdate="19900101",
            gender=random.choice(gender_choices),
            nationalinfo=random.choice(nation_choices),
            mobileno=f"1100000{1100+i:04}",
            email=f"test_exter{i}@test.com",
            type=3,
            road=f"TestRoad{i}",
            jibun=f"TestJibun{i}",
            detail=f"TestDetail{i}",
            is_active=True,
            optinal_consent=True,
            marketing_agreement_date=now(),
        required_consent_data=now()
        )    
        user.set_password("test1234@")
        user.save()
        BankAccount.objects.create(
            uuid=uuid.uuid4(),
            owner=user,
            bank_name="test_은행명칭",
            account_number="1234567890",
            account_type = "법인명"
        )
        for j in range(10):
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
        
    Alarm.objects.create(
        uuid=uuid.uuid4(),
        title="매칭이 완료되었습니다.",
        content=f"{now()}에 매칭이 완료되었습니다.",
        created_at=now(),
    ).save()
    
    Notice.objects.create(
        uuid=uuid.uuid4(),
        title="2월 폭설로 인한 방제 지연 안내",
        content="2월 폭설로 전남권 대규모 폭설로 인해 방제를 2월 3일까지 연기합니다.",
        created_at=now(),
    ).save()

    
#=========비어있는 계정================    
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
            optinal_consent=True,
            marketing_agreement_date=now(),
            required_consent_data=now()
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