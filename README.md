드론평야 장고 웹 어플리케이션 서버입니다

현재 JWT를 사용한 로그인 까지만 구현되어 있습니다

* 나중에 서비스 할 때는 settings.py에 있는 SECRET_KEY를 수정해야합니다
* 그리고 깃허브에 secret.json을 올리지 않도록 조치

앞으로 깃헙에 settings 파일은 올리지 않도록 주의하세요 - git ignore사용하기
* settings 파일을 여러 버전으로 관리 시작함
* python manage.py runserver --settings=[세팅폴더의 세팅파일이름]
* ex) 로컬 개발환경에서 사용
* python manage.py runserver --settings=config.settings.local

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
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ ORIG_HEAD
│  ├─ branches
│  ├─ config
│  ├─ description
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  ├─ sendemail-validate.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  ├─ Dev
│  │     │  └─ main
│  │     └─ remotes
│  │        └─ origin
│  │           ├─ Dev
│  │           └─ HEAD
│  ├─ objects
│  │  ├─ 00
│  │  │  └─ 17be41ee0ce29b54d53552e8af9b12b8bf93ca
│  │  ├─ 04
│  │  │  └─ 45d5c1085687c75ba7c9dbf70630d489a75589
│  │  ├─ 09
│  │  │  └─ 58f6c600b5c1315a7c97798d59fd2ada24a0f7
│  │  ├─ 0d
│  │  │  └─ 9cc1c8d3bc6cc522d74d0d087ab93a298b1278
│  │  ├─ 0e
│  │  │  ├─ 4de0aa11972dc63f7ef3052aacd01a7c51aec8
│  │  │  └─ 73b251f3222b61dfbe935bc753b2dfd462dc2b
│  │  ├─ 1a
│  │  │  └─ d3fb7537ad37ddc9bc16cde546a8d9ce57ca2c
│  │  ├─ 1d
│  │  │  └─ 924198da7e28da5d1b859cc358f28e123ac3de
│  │  ├─ 4e
│  │  │  └─ cd02c9151d75f503873df27454f97c8f70f15d
│  │  ├─ 5e
│  │  │  └─ d9ce2cb43105bca63e36d89ca8ceef30671aaa
│  │  ├─ 68
│  │  │  └─ 656d5fc03a69fd987d516c92fc9eb2a294c3e8
│  │  ├─ 69
│  │  │  └─ 2b854a8e689e5e414cfece21472252229d3ed0
│  │  ├─ 73
│  │  │  └─ 67b355aa746d80a15484a8658f7f1084007836
│  │  ├─ 87
│  │  │  └─ 84cafd15ef71e7143b42634acd8bed7065fc94
│  │  ├─ 9d
│  │  │  └─ 1dcfdaf1a6857c5f83dc27019c7600e1ffaff8
│  │  ├─ bc
│  │  │  └─ af305b550de4ffef9fa09e1edf0e03ca57bb6d
│  │  ├─ c6
│  │  │  └─ f3c95641093c190e4a4f3e41899cf7589c23ad
│  │  ├─ c8
│  │  │  └─ baf027badfcf7c337115b3428aaf95062e3759
│  │  ├─ d6
│  │  │  └─ 2b715920e79a7c50474b5c94e3f04a10631c60
│  │  ├─ d8
│  │  │  └─ 04baf2a8091666a8881e031a1a7de74c464a3d
│  │  ├─ de
│  │  │  └─ ad3f7f306b13fc6c277112e902cc31f53a362c
│  │  ├─ e0
│  │  │  └─ e36e6856476373d4afb64943ec5563abb63972
│  │  ├─ e5
│  │  │  └─ f658488637faae8fff884dc074dd6577624c30
│  │  ├─ ff
│  │  │  └─ 96b9ade3a2a6553e6c30b4bc2d758657b93485
│  │  ├─ info
│  │  └─ pack
│  │     ├─ pack-060d9fdba213931fb1485129253415601252ee03.idx
│  │     ├─ pack-060d9fdba213931fb1485129253415601252ee03.pack
│  │     └─ pack-060d9fdba213931fb1485129253415601252ee03.rev
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  ├─ Dev
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     ├─ Dev
│     │     └─ HEAD
│     └─ tags
├─ .gitignore
├─ Dockerfile
├─ README.md
├─ common
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ config
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ customer
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ entrypoint.sh
├─ exterminator
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
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ manage.py
├─ requirements.txt
├─ templates
│  └─ emailvalidation.html
├─ user
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ swagger_doc.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
└─ validation
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ models.py
   ├─ nice_fuc.py
   ├─ permissions.py
   ├─ swagger_doc.py
   ├─ tests.py
   ├─ urls.py
   └─ views.py

```