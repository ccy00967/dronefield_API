드론평야 장고 웹 어플리케이션 서버입니다

현재 JWT를 사용한 로그인 까지만 구현되어 있습니다

* 나중에 서비스 할 때는 settings.py에 있는 SECRET_KEY를 수정해야합니다
* 그리고 깃허브에 secret.json을 올리지 않도록 조치

앞으로 깃헙에 settings 파일은 올리지 않도록 주의하세요 - git ignore사용하기
* settings 파일을 여러 버전으로 관리 시작함
* python manage.py runserver --settings=[세팅폴더의 세팅파일이름]
* ex) 로컬 개발환경에서 사용
* python manage.py runserver --settings=core.settings.local

모듈 한번에 다운받기 - 가상환경을 올리지 않고 소스코드만 올리기 위함
* requirements.txt 위치를 찾아서 실행, 이때 pip실행위치는 가상환경이어야한다 (pwd가 자신의 디렉토리이름 이어야함)
* pip install -r ./[파일이름]./requirements.txt/base.txt

만약 파이썬 패키지를 추가, 제외했다면 다시 작성필요
* pip freeze > requirements.txt 또는 pip list --format=freeze > requirements.txt


# 도커로 실행하기
* 복잡한 설정 없이 도커로 바로 실행가능하다
* 처음 실행시 컨테이너를 만들고 실행필요 - 컨테이너를 만들고 실행까지 바로 된다 -
* docker-compose up -b --build
* 실행 종료하기
* docker-compose down
* 만들어진 컨테이너 실행하기 - 굳이 도커 명령어로 안해도 된다 도커 UI에서 실행가능 -
* docker-compose up# dronefield_API



```
dronefield_API
├─ .dockerignore
├─ .ebextensions
│  ├─ 01_packages.config
│  ├─ 02_gunicorn.config
│  ├─ docker.config
│  └─ nginx.config
├─ .gitignore
├─ Dockerfile
├─ Dockerfile.copy
├─ Dockerrun.aws.json
├─ README.md
├─ application.py
├─ common
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ nice_fuc.py
│  ├─ response.py
│  ├─ serializers.py
│  ├─ tests.py
│  └─ views.py
├─ config
├─ core
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  └─ wsgi.py
├─ customer
│  └─ migrations
│     ├─ 0001_initial.py
│     └─ 0002_initial.py
├─ entrypoint.sh.copy
├─ entypoint.sh
├─ exterminator
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ farmer
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ farmrequest
│  └─ migrations
│     ├─ 0001_initial.py
│     └─ 0002_initial.py
├─ main
│  └─ urls.py
├─ manage.py
├─ payments
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ requirements.txt
├─ templates
│  └─ emailvalidation.html
├─ trade
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
└─ user
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ migrations
   │  ├─ 0001_initial.py
   │  └─ __init__.py
   ├─ models.py
   ├─ permissions.py
   ├─ serializers.py
   ├─ swagger_doc.py
   ├─ test
   │  ├─ nice.html
   │  └─ tests.py
   ├─ urls.py
   └─ views.py

```
