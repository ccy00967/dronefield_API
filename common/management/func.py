# generate_insert.py

import os
import django
import uuid
from django.contrib.auth.hashers import make_password

def main():
    # Django 프로젝트의 설정 모듈을 지정합니다.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # 실제 프로젝트 설정 모듈로 변경

    # Django를 초기화합니다.
    django.setup()

    # UUID 생성
    user_uuid = uuid.uuid4()

    # 비밀번호 해싱
    raw_password = 'YourSecureP@ssw0rd!'  # 실제 비밀번호로 변경
    hashed_password = make_password(raw_password)

    # SQL INSERT 문 작성
    insert_query = f"""
    INSERT INTO user_customuser (
        uuid,
        name,
        birthdate,
        gender,
        nationalinfo,
        mobileno,
        email,
        type,
        road,
        jibun,
        detail,
        is_active,
        password,
        created_at,
        updated_at
    ) VALUES (
        '{user_uuid}',                           -- UUID
        'Jane Doe',                              -- name
        '19900515',                              -- birthdate (YYYYMMDD)
        '0',                                     -- gender ('0' = 여성, '1' = 남성)
        '0',                                     -- nationalinfo ('0' = 국내, '1' = 외국인)
        '010-1234-5678',                         -- mobileno
        'jane.doe@example.com',                  -- email
        4,                                       -- type (4 = Customer)
        '456 Elm Street',                        -- road
        'Jibun Info',                            -- jibun
        'Apt 101',                               -- detail
        TRUE,                                    -- is_active
        '{hashed_password}',                     -- password (해시된 비밀번호)
        NOW(),                                   -- created_at
        NOW()                                    -- updated_at
    );
    """

    print("Generated SQL INSERT Query:")
    print(insert_query)

if __name__ == '__main__':
    main()
