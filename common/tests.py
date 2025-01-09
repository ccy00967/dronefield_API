from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTest(APITestCase):
    def test_password_validation_success(self):
        # 올바른 비밀번호로 회원가입
        response = self.client.post('/user/register/', {
            'email': 'testuser@example.com',
            'password': 'Passw0rd!',
            'name': 'Test User',
            'birthdate': '1990-01-01',
            'gender': 'M',
            'nationalinfo': 'KR',
            'mobileno': '01012345678'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 데이터베이스에 비밀번호가 해싱된 상태로 저장되었는지 확인
        user = User.objects.get(email='testuser@example.com')
        self.assertNotEqual(user.password, 'Passw0rd!')  # 비밀번호는 원문이 아니어야 함
        self.assertTrue(user.check_password('Passw0rd!'))  # 해싱된 비밀번호와 일치 확인

    def test_password_validation_failure(self):
        # 특수 문자가 없는 비밀번호로 회원가입
        response = self.client.post('/user/register/', {
            'email': 'testuser@example.com',
            'password': 'Password123',
            'name': 'Test User',
            'birthdate': '1990-01-01',
            'gender': 'M',
            'nationalinfo': 'KR',
            'mobileno': '01012345678'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
