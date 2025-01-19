from django.test import TestCase
from .models import CustomUser
from datetime import datetime
import uuid
import random

from farmer.models import FarmInfo
class CreateTestUsersTestCase(TestCase):
    def test_create_test_users(self):
        # Gender, Nation, and Type choices
        gender_choices = ['0', '1'] # 예: 여성, 남성
        nation_choices = ['0', '1'] # 예: 내국인, 외국인인
        type_choices = [3, 4]  # 예: 1=어드민, 2=매니저, 3=드론조종사, 4=농지소유주

        CustomUser.objects.create(
            uuid=uuid.uuid4(),
            name=f"test_farmer",
            birthdate="19900101",
            gender=random.choice(gender_choices),
            nationalinfo='1',
            mobileno=f"01011111111",
            email=f"test_farmer@test.com",
            type=3,
            road=f"TestRoad_farmer",
            jibun=f"TestJibun_farmer",
            detail=f"TestDetail_farmer",
            is_active=True,
            password="test1234!"
        )
        CustomUser.objects.create(
            uuid=uuid.uuid4(),
            name=f"test_exterminator",
            birthdate="19900101",
            gender=random.choice(gender_choices),
            nationalinfo='1',
            mobileno=f"01011111112",
            email=f"test_exterminator@test.com",
            type=4,
            road=f"TestRoad_exterminator",
            jibun=f"TestJibun_exterminator",
            detail=f"TestDetail_exterminator",
            is_active=True,
            password="test1234@"
        )
        
        for i in range(50):
            FarmInfo.objects.create(
                uuid=uuid.uuid4(),
                owner=CustomUser.objects.get(name='test_farmer'),
                road=f"TestRoad{i}",
                jibun=f"TestJibun{i}",
                detail=f"TestDetail{i}",
                pnu=f"pnu{i}",
                lndpclAr=f"lndpclAr{i}",
                cd=f"cd{i}",
                landNickName=f"landNickName{i}",
                cropsInfo=f"cropsInfo{i}",
                additionalPhoneNum=f"0100000{1000+i:04}"
            )

        for i in range(50):
            CustomUser.objects.create(
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
                password="test1234@"
            )
        
        # 검증: 생성된 유저 수 확인
        self.assertEqual(CustomUser.objects.count(), 50)
