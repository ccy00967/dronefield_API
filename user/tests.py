from django.test import TestCase
from .models import CustomUser
from datetime import datetime
import uuid
import random

class CreateTestUsersTestCase(TestCase):
    def test_create_test_users(self):
        # Gender, Nation, and Type choices
        gender_choices = ['0', '1'] # 예: 여성, 남성
        nation_choices = ['0', '1'] # 예: 내국인, 외국인인
        type_choices = [1, 2]  # 예: 1=어드민, 2=매니저, 3=드론조종사, 4=고객

        for i in range(50):
            CustomUser.objects.create(
                uuid=uuid.uuid4(),
                name=f"tester{i}",
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
                password="test1234!"
            )
        
        # 검증: 생성된 유저 수 확인
        self.assertEqual(CustomUser.objects.count(), 50)
