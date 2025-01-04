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

```
dronefield_API
├─ .dockerignore
├─ .ebextensions
│  ├─ 01_amazon-linux-extras.config
│  ├─ 01_packages.config
│  ├─ 02_django_commands.config
│  ├─ django.config
│  ├─ nginx.config
│  ├─ postgres.config
│  └─ wsgi.config
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
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  ├─ Dev
│  │     │  ├─ Dev_Ref
│  │     │  └─ main
│  │     ├─ remotes
│  │     │  └─ origin
│  │     │     ├─ Dev
│  │     │     ├─ Dev_Deploy_AWS
│  │     │     ├─ Dev_Ref
│  │     │     ├─ Dev_exterminator
│  │     │     ├─ Dev_user
│  │     │     ├─ HEAD
│  │     │     └─ main
│  │     └─ stash
│  ├─ objects
│  │  ├─ 03
│  │  │  └─ 3bb1c5ea24ad5f6930a12a587e4c035f9c19d0
│  │  ├─ 05
│  │  │  └─ 9a2c35a36493822650eb84e0abc119f0f5fee0
│  │  ├─ 07
│  │  │  └─ 683f9a5f524d5afd9c1d31d560054042c42321
│  │  ├─ 08
│  │  │  └─ 86bc50ab25341330e2d0fd2f1f12cd27bf78cd
│  │  ├─ 0b
│  │  │  └─ ed24ea724386be7a633f5c61d23c4fb387b7db
│  │  ├─ 0e
│  │  │  └─ 7c7d2beca6e3e77fe7f86966d510f417e79849
│  │  ├─ 0f
│  │  │  └─ 06c4e5d2849b58a9a1486b8f8bc751998144d6
│  │  ├─ 10
│  │  │  └─ 52989599a2147285d7209c72d422ada5afeac2
│  │  ├─ 12
│  │  │  └─ 1568b07b1c0daefbe6d548d98ea93f2b49ef79
│  │  ├─ 13
│  │  │  └─ facfa7c11cb4fe6840f5a3a48382a5153ea464
│  │  ├─ 14
│  │  │  └─ efc655d4cb438d2a1b160037dac0d1c68622c3
│  │  ├─ 15
│  │  │  └─ 1ba855188496a0f0510011f8537ce4c1881cf0
│  │  ├─ 17
│  │  │  └─ fb6b2018dc223d40b221aa3db38659752d90c8
│  │  ├─ 18
│  │  │  └─ b550419cf78a26677d0c4a825494dfb9362322
│  │  ├─ 1a
│  │  │  └─ 89b5db2b581cf32dac5218d620ec412d3aa647
│  │  ├─ 22
│  │  │  ├─ 46806a9c984f267342b727fb44769857951616
│  │  │  ├─ 4bc1f4169967edd42a69d8345c9acd6b275724
│  │  │  └─ 7d3995523f2b5e2471d25db17c81c0eb72007a
│  │  ├─ 26
│  │  │  └─ eaebfce42f82fc45b17dcc5d197b564b7b7406
│  │  ├─ 28
│  │  │  └─ 64877094edc1e887a2e9e0ed5f996ababecb5a
│  │  ├─ 2b
│  │  │  └─ 23c47a4366ff428347d479387e0250a3d4afd7
│  │  ├─ 31
│  │  │  ├─ 5e037fbf2c4e8ea8f37ef5eb1f6890a551fb1e
│  │  │  └─ 9a75adafc45d5ba5e7b19e6a0093cb20cab55e
│  │  ├─ 32
│  │  │  └─ 5cfdef97ccb1a03495a083404b41f4978f013d
│  │  ├─ 33
│  │  │  └─ a66fc942d9025dc942cc47095ea94511a1d0e1
│  │  ├─ 37
│  │  │  └─ f63deb16824c34cbdb3a5daf1d623df5419fdc
│  │  ├─ 3a
│  │  │  └─ f8329f8bcba5d5573e71865cc3266232f79ce1
│  │  ├─ 3b
│  │  │  └─ ad9be1b8ca4bfdc6b586e08791999e873a0562
│  │  ├─ 3f
│  │  │  └─ 2539714d8666a534cfb3d880063bce68c9bf5a
│  │  ├─ 42
│  │  │  └─ 53ac0bed900a0b7115e838edf5b7a3dea46bb0
│  │  ├─ 43
│  │  │  ├─ 0b637499941dc81bbc997e51dae9d75e573109
│  │  │  └─ cb82a7bd8bf56a9671133c380ab2d7bdb748b6
│  │  ├─ 46
│  │  │  └─ 867df86ecd757dc72a3015d9be2e309b33ac99
│  │  ├─ 47
│  │  │  ├─ 8a5854a80720e29ce5073dcebbc022059f9bfd
│  │  │  └─ d99f75938fc7b3aa4af3bc10365068430c37e6
│  │  ├─ 49
│  │  │  └─ 377c8579321361f148008a01dc7528ae2a0932
│  │  ├─ 4e
│  │  │  └─ 90b48a16cbf57eac0167e5a057994551d56bf2
│  │  ├─ 50
│  │  │  └─ 21ded9b523f401996a949353f55085d7e43dc7
│  │  ├─ 51
│  │  │  └─ 02afc9a3ce3f23bd53e40ae5291533fc544aa9
│  │  ├─ 52
│  │  │  └─ 0de9a46fe78dcf4566007de558f133f74f31d7
│  │  ├─ 56
│  │  │  └─ 47510bfd1c6d4d08cfb8e008cab4ac7ee7a626
│  │  ├─ 58
│  │  │  └─ 25f49f4c88f3dc7a831ab6b558fa02abd82cdf
│  │  ├─ 59
│  │  │  └─ 9723aa9f74eaa912827b75fb02cee62462deb4
│  │  ├─ 5b
│  │  │  └─ 8acd2c2c226d5bb8a792a4977e18c07aeceb8a
│  │  ├─ 5d
│  │  │  └─ 39654940e8373d6af01a8183f6a3fa4b9a592c
│  │  ├─ 5e
│  │  │  └─ 25977fe81b226ad7c7a9874eaee6ce80544a2f
│  │  ├─ 65
│  │  │  └─ 5a9eccf6f41e597c0cf7f757b7dfba42d4230d
│  │  ├─ 66
│  │  │  └─ ed4a36d20656cac3573d2bb4e1bc3911f60432
│  │  ├─ 68
│  │  │  └─ 0ec56332f6eda01dbd1d53b932da566d0397b9
│  │  ├─ 69
│  │  │  ├─ 0118993d7d6c348b24872d4c46abf1f3c91913
│  │  │  └─ 93d010e61def8579c9f7ba25079bd4c11f2e1e
│  │  ├─ 6b
│  │  │  └─ c26a5a844fc356619860fe6556b79d8b5dc390
│  │  ├─ 6c
│  │  │  ├─ 853eafd39a4db6ae5d4bff43c706e1f7f54b0d
│  │  │  └─ 9ed30afb5039a45fe0decb8d8cc6551c58721c
│  │  ├─ 6d
│  │  │  ├─ dca9ad8abe062bae7f5f3bb73e31811a9747c1
│  │  │  └─ e09bd5b6f5a664e5a03f4bbee94136a6f773ba
│  │  ├─ 74
│  │  │  ├─ 035f2d8b441dc9a8094e67da58141a3f38d865
│  │  │  └─ 35d26a8a88f94599b95e5b785ca2a5edd988c9
│  │  ├─ 76
│  │  │  └─ 47fbe9ef9cb3af891a314178f2e70d2834a3f0
│  │  ├─ 77
│  │  │  └─ 06c65afccb520b21b66ab14b320e17be47d824
│  │  ├─ 79
│  │  │  ├─ 12acdf322faaa3d56c2c741431e1cc882eb281
│  │  │  └─ 32869e19d4ee882142d1114f08161717af5ca0
│  │  ├─ 7a
│  │  │  └─ fd13d48cffc4d1c97887513816d493b6638ce7
│  │  ├─ 7e
│  │  │  ├─ b23ced0f3c8ad883a35f31b29a315af8723187
│  │  │  └─ f6c21d1609cee4f8070a55d132b7538999833a
│  │  ├─ 7f
│  │  │  ├─ 6c7e16ddc509e384dc3c70474d0814e536bfa4
│  │  │  └─ dd202b2510604ae62dcc2578c3c57fc4440dc8
│  │  ├─ 83
│  │  │  └─ c6482433092e419d748242ab06985ef9b628d4
│  │  ├─ 84
│  │  │  ├─ 609b55c90487d1268ec7596cbe3404ae3cf8ad
│  │  │  ├─ 620b65500746c7e5bdabfa0eb57ae3b6ca3319
│  │  │  └─ c4c9042fecd2219bfd0f53675c41f11e9e766b
│  │  ├─ 85
│  │  │  ├─ 4aa6ae7f0542e2139c43cea791372a752a2030
│  │  │  ├─ abe76a18014eb9b99748dfe64878cd389180bb
│  │  │  └─ c73c11d94063ea81642b699ef69f7273b03fb9
│  │  ├─ 8f
│  │  │  └─ cd4b713fe4edf7b334bad028a7473065ec22fc
│  │  ├─ 90
│  │  │  └─ 94908d80c31ef9077b31af39e31b1e6fa038c2
│  │  ├─ 92
│  │  │  └─ 642b58d69d0538d9736b271a0f42e257f3b181
│  │  ├─ 96
│  │  │  └─ 70990a05bb606cebd2ffc040906e8c0db57269
│  │  ├─ 9a
│  │  │  └─ 0b08a40bdb962a28a4c8438429b96050bd08ab
│  │  ├─ 9d
│  │  │  ├─ 2fa02697a6b3d0d6c3be98c842f1700a8d58d3
│  │  │  └─ 954ac418f42afec685fd1c68921252c1339123
│  │  ├─ 9f
│  │  │  └─ fc2e8bbdab20ddaee34772268abbe62000a489
│  │  ├─ a0
│  │  │  └─ 3261bda7ac0aec9b83ebef9612824bc0e8de8e
│  │  ├─ a3
│  │  │  └─ a6ca2a2a1987e89f7516f2cba82f48391f723e
│  │  ├─ a5
│  │  │  └─ 17d175e8b98f093936ab322b3b38b8e2be954c
│  │  ├─ a6
│  │  │  └─ f57bdabeeae7e57aa23ac027f90e507c90fc0b
│  │  ├─ a9
│  │  │  ├─ 5eeca78a8456e63f9f187124e5ca32e0c8a3b0
│  │  │  └─ f80c996f6ffb77f6c75be51d82fbfa6a7ac43f
│  │  ├─ aa
│  │  │  └─ 6f981efcdd8d0b6a8d381770c1b5d05977a184
│  │  ├─ ae
│  │  │  └─ 24b4b7988218320ae94cbade1867bbb31e4662
│  │  ├─ b0
│  │  │  └─ 793dbb9f9f5a5b3937f906d15b0d7773bbb81b
│  │  ├─ b1
│  │  │  └─ 9e6ac470c9e8f2bf1641a57ac2753218883670
│  │  ├─ b6
│  │  │  └─ 5aa39d24d3075e6200618989423b74d2b84e69
│  │  ├─ b8
│  │  │  └─ 69babb2a9e1824af9661ff7c9d3c3e7621e0ff
│  │  ├─ b9
│  │  │  └─ 2f10b57d0980993423083754f496a5751cb5c0
│  │  ├─ ba
│  │  │  └─ 20ce0a033b07d5de4c531cc9773098ff2a5268
│  │  ├─ bf
│  │  │  └─ 98161baa87047375df88fe0328fa8556163758
│  │  ├─ c0
│  │  │  └─ 20959a572fe0970c03b616c78d62589c6d8695
│  │  ├─ c2
│  │  │  └─ e05e08991df6a5b47c085ea82a5435753fa5ea
│  │  ├─ c3
│  │  │  ├─ 59ee284a59d03dc4937d059e7ec526a8aa4933
│  │  │  └─ 8782d682ec395c565026bf727972a1c4983747
│  │  ├─ c6
│  │  │  └─ 4dce86c2b81d59e36e942546f3db13b38011e7
│  │  ├─ c7
│  │  │  └─ ff596b44874b1262c74dfbd66e5d35b4f68629
│  │  ├─ c9
│  │  │  ├─ 146c2f06f974a743e4ca5c6ce95e8a42bb0e91
│  │  │  └─ 9e0ac6c56cb241980c305b0ebc96b6ebfb5aa4
│  │  ├─ ca
│  │  │  └─ 391880c7fa4da37a1725dffb1268166a17ae0e
│  │  ├─ cb
│  │  │  └─ f43005046cd53942dbe14d2f30c2170b861acb
│  │  ├─ d6
│  │  │  └─ 16d8dc6067a0b15d6297f3ed7db4ae6733ae51
│  │  ├─ d7
│  │  │  └─ f2e2e81e67f48e90d171e1d41db5727e47b78c
│  │  ├─ da
│  │  │  └─ cb7a3562859d74c9f19303eb37e9ae0ee22e3e
│  │  ├─ df
│  │  │  ├─ 0371e5d2ee9a48aa74c981e84fc655ee7a0b73
│  │  │  └─ 8f53f79d4a9b6d04fece32c5a05879e532cd36
│  │  ├─ e1
│  │  │  └─ cc54c8f208384ecf5648f9a7c0b72e9dda6acb
│  │  ├─ e2
│  │  │  ├─ 4622043cdd828d1c24b1b656fc8e45e40b699e
│  │  │  └─ 74a2710eb3a79855e660eff834eecb832c8a5e
│  │  ├─ e5
│  │  │  └─ 298e6a34a26030b3a8f2c28c1355a03655a52d
│  │  ├─ e6
│  │  │  └─ deb664dccddec046f7a1d3a3fd00bcda4b5d72
│  │  ├─ e7
│  │  │  └─ 99bc786ee354b8999ad6f53288a3e1af44faea
│  │  ├─ e8
│  │  │  └─ a4a90073028ee3f7eaf84335ddedf024c4aecd
│  │  ├─ e9
│  │  │  └─ 2cb30929a9c643355e9a21f67669d5b35d9112
│  │  ├─ ea
│  │  │  └─ ab7a39d39dd5e49b23e919b83bfacfc55ad52a
│  │  ├─ eb
│  │  │  └─ d41f02d0e86dfc1f40ec39592dc0670114dc5b
│  │  ├─ ed
│  │  │  └─ b73f8c96ea2e6b6a39785418e2de500f333a48
│  │  ├─ ee
│  │  │  └─ 415c93a74f8149aa60fdeb8089c1792475c5a9
│  │  ├─ f0
│  │  │  └─ 950c959acba9115f54ece4ff51e6efd973db36
│  │  ├─ f2
│  │  │  └─ f351a6b244463958f43d339354791de50c9852
│  │  ├─ f4
│  │  │  └─ 2a7ebb76d7e6e3d28463a028afef491c6912fd
│  │  ├─ f6
│  │  │  ├─ d7d8749dfe4762ee468f9eccb6e93a5787bc58
│  │  │  └─ f1bb340c08fbdb6730ca24f068b8d0d35ad3cc
│  │  ├─ f8
│  │  │  └─ 9343b89bce8deb6fe27ee9c0527d97ebd1a4aa
│  │  ├─ fb
│  │  │  └─ fa2bd5357c84baef845e70d495450f2b6521b7
│  │  ├─ fc
│  │  │  └─ 933ab80b2c37276914e8240654317024ba3e81
│  │  ├─ fe
│  │  │  ├─ 68fb5f74f649c3ff090cae0326854413de9b5a
│  │  │  └─ 6f3353dd322f95f07dcdf86d29bb4d0bc1aa3e
│  │  ├─ ff
│  │  │  └─ db50e70adb5df451edfb3836175799e0eac4d7
│  │  ├─ info
│  │  └─ pack
│  │     ├─ pack-1f441a57f5a6184927657157753a8cbc34b1b6c8.idx
│  │     └─ pack-1f441a57f5a6184927657157753a8cbc34b1b6c8.pack
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  ├─ Dev
│     │  ├─ Dev_Ref
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     ├─ Dev
│     │     ├─ Dev_Deploy_AWS
│     │     ├─ Dev_Ref
│     │     ├─ Dev_exterminator
│     │     ├─ Dev_user
│     │     ├─ HEAD
│     │     └─ main
│     ├─ stash
│     └─ tags
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
├─ core
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  └─ wsgi.py
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
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
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
   │  ├─ 0002_alter_customuser_options_alter_customuser_gender_and_more.py
   │  └─ __init__.py
   ├─ models.py
   ├─ permissions.py
   ├─ serializers.py
   ├─ service
   ├─ swagger_doc.py
   ├─ test
   │  ├─ nice.html
   │  └─ tests.py
   ├─ urls.py
   └─ views.py

```