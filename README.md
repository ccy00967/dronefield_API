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
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ ORIG_HEAD
│  ├─ branches
│  ├─ config
│  ├─ description
│  ├─ filter-repo
│  │  ├─ already_ran
│  │  ├─ commit-map
│  │  ├─ ref-map
│  │  └─ suboptimal-issues
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
│  │  ├─ exclude
│  │  └─ refs
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  ├─ Dev
│  │     │  ├─ Dev_Deploy_AWS
│  │     │  ├─ Dev_Deploy_EB
│  │     │  ├─ Dev_Ref
│  │     │  ├─ Dev_exterminator
│  │     │  ├─ Dev_user
│  │     │  ├─ dev_user_accout
│  │     │  ├─ main
│  │     │  └─ main_Dev
│  │     └─ remotes
│  │        └─ origin
│  │           ├─ Dev
│  │           ├─ Dev_Deploy_AWS
│  │           ├─ Dev_Deploy_EB
│  │           ├─ Dev_Ref
│  │           ├─ Dev_Trade_ccy
│  │           ├─ Dev_auth_ccy
│  │           ├─ Dev_exterminator
│  │           ├─ Dev_user
│  │           ├─ REFACTOR_Trade_ccy
│  │           ├─ dev_user_accout
│  │           ├─ main
│  │           └─ main_Dev
│  ├─ objects
│  │  ├─ 01
│  │  │  └─ 645fd3711474bd264f347bab8a5451476b842e
│  │  ├─ 02
│  │  │  ├─ 6ad25e0da12bbab9e57e3c25f05501113fb255
│  │  │  └─ aeafdd9624173b283768ab69dd9843cda857b9
│  │  ├─ 03
│  │  │  ├─ 02d322ecdc775dcfa55783c88d460dd21d3c0d
│  │  │  ├─ 3bb1c5ea24ad5f6930a12a587e4c035f9c19d0
│  │  │  ├─ 3c3edbf66f55682e9b92867f86d56e16398251
│  │  │  └─ c340e80ab7c7e54e8fa2bc1044b33004c3e484
│  │  ├─ 04
│  │  │  ├─ 454d25ac9b08ba3ea4e601711f5ba8100090b9
│  │  │  └─ f55a77ce3b4e78c665d0eb3d9ea52b508bf2b2
│  │  ├─ 05
│  │  │  ├─ 2444c6968b9006c10ea008068a91618b647449
│  │  │  └─ 9a2c35a36493822650eb84e0abc119f0f5fee0
│  │  ├─ 06
│  │  │  ├─ 196d6dc30a148ee9cdbcdb8d94ff8afd132ee4
│  │  │  ├─ 213f7e4943725f9e82571f7ca96f46b008d4dc
│  │  │  └─ 541a7619dfb77f4b9a3d63c75f485bb6f8d968
│  │  ├─ 08
│  │  │  ├─ 0cf1f6d33d27da3d0224b56f1ad5e8e03a6448
│  │  │  └─ 86bc50ab25341330e2d0fd2f1f12cd27bf78cd
│  │  ├─ 09
│  │  │  ├─ 4a94ca5e1fb2edbee8f922f9ebdb3e63aafcff
│  │  │  └─ ccdfbea5b9feacb88232a0dd99e47117de3240
│  │  ├─ 0a
│  │  │  ├─ 14da6bf6b1cff68842ef04393f252c435cea5c
│  │  │  ├─ 564be605328a4614b6c0ee3aa38ea41ca4b017
│  │  │  └─ db1fcb686b91a0ed74e7151010acf600150ee9
│  │  ├─ 0b
│  │  │  └─ 3840ff4ae822cdc9872b5ebccc45807ee0001c
│  │  ├─ 0c
│  │  │  ├─ 202e99beed8f776ab1cca302d9f3f3b3becb0f
│  │  │  ├─ 56e4e8c599822168e62a2a2c6bffdb659f8489
│  │  │  └─ a5f19e9e526b2eaa231a88662ac219f9f23d79
│  │  ├─ 10
│  │  │  └─ 3e80dea16dbc40932cbd98184b865e0874599c
│  │  ├─ 11
│  │  │  ├─ 8714ea9d39cfd8d560b7b1eb0d40b2ad189b82
│  │  │  └─ f2e6a720debfc25f9df4818bd1f7d9fcc47682
│  │  ├─ 12
│  │  │  └─ 8f64411bf1b3f7a342014f90d83c6fdf96bcd9
│  │  ├─ 13
│  │  │  ├─ 1240d65949376c4d4ab57ea2c8adf7568c174f
│  │  │  ├─ 660ff548986e980e7e0f0c972ea30efde4a00c
│  │  │  ├─ 74c065a2222edd313c7f275193a51216acd124
│  │  │  └─ facfa7c11cb4fe6840f5a3a48382a5153ea464
│  │  ├─ 14
│  │  │  └─ 25e969de40cd5d89f4deb7c44cee5a0aff8ccc
│  │  ├─ 15
│  │  │  └─ 1ba855188496a0f0510011f8537ce4c1881cf0
│  │  ├─ 17
│  │  │  ├─ 793f98d689946fb120ebd45b91af703262a546
│  │  │  └─ f194d2f1608cf7f67c2347212eff9222d84a12
│  │  ├─ 18
│  │  │  ├─ 749073749665f461cb6af37070ff4d0e674d6b
│  │  │  ├─ 85013cd7b2405b74e0b4c4e5be907168e0a738
│  │  │  └─ ed38f249472d5ad3f7ea6c76333bdb77ef8f36
│  │  ├─ 19
│  │  │  ├─ 0ce905ba3dd9556a7470e35fca0eba7e64504a
│  │  │  ├─ 318d8ff1ffde5343084bba378de980203d5116
│  │  │  ├─ 908303f032671f77e2a19b939f14d69096cd55
│  │  │  └─ f63b7374a65e58a8e5e3bc8f27e67d5834271a
│  │  ├─ 1a
│  │  │  ├─ 89b5db2b581cf32dac5218d620ec412d3aa647
│  │  │  └─ baf7b624af2e2f259bd31bdaf98219bc8f7daf
│  │  ├─ 1b
│  │  │  ├─ 54f9846f1d6f2a4468f5c74e1959c9b4044c08
│  │  │  ├─ e7ab4f50cfe79755630c96e8ab25d30e351e27
│  │  │  └─ f68c8bd5f32e27f9f5bbab39a4f30b78d726a2
│  │  ├─ 1e
│  │  │  └─ 4207abf5e0f9293b2cf98b34149573b9298bbe
│  │  ├─ 20
│  │  │  └─ c41dab430aa6fd7191a667e4859b893d13bc62
│  │  ├─ 21
│  │  │  ├─ 2de9557d94e8a73a9c901c3a8c229e674e8932
│  │  │  └─ d5b48ef7ea2dc62e88664f0c7d490960f4cb30
│  │  ├─ 26
│  │  │  ├─ 1d4f49c1d3c1db2f6f1455039043b29af2d4db
│  │  │  └─ d090173afd631f079ac3933e635f0067a13de9
│  │  ├─ 27
│  │  │  ├─ 0bea4a3bb9a64611f52358c1703ddea7556b6e
│  │  │  ├─ 317be799babb20373af666058b57c3f0d14d79
│  │  │  └─ d3eeb8049c0e332e21b4261445aacac55dd86f
│  │  ├─ 28
│  │  │  └─ ca4fc8a73ac70df1f72353e5c940a2f1b3316c
│  │  ├─ 29
│  │  │  ├─ 0fc8f915280474f308032b17766a9e90e4cfef
│  │  │  └─ 96a3600f89cfe457a880a9a228368dde557385
│  │  ├─ 2a
│  │  │  └─ 25460deb3e185d56c978f6f5bdc27aad6f96cf
│  │  ├─ 2b
│  │  │  ├─ 0d47be340a063c849e85cc37b246fa797daca0
│  │  │  ├─ 23c47a4366ff428347d479387e0250a3d4afd7
│  │  │  ├─ 926fffe44e160e2607900065c78886aa5e642d
│  │  │  └─ e874eef518fbfa7a2810055e672236ecdd52c2
│  │  ├─ 2c
│  │  │  ├─ 2c3fcad5eae1bfb261f85a7c1ac85d71c083c9
│  │  │  └─ 2e77f0af306d4f13684baa6b7aaf9a10dd4b6f
│  │  ├─ 2d
│  │  │  ├─ 321f74ba2f9e1715523782d556d3a0223e8084
│  │  │  ├─ 7089bbeffde720bd032d474e5d828596e60fa4
│  │  │  ├─ b7a69476d058a361bb73727f6f95bc54ed5afb
│  │  │  └─ c450dd0eac7cb8470d571741f1d930f52b1864
│  │  ├─ 2e
│  │  │  ├─ a0bd4d225d16f308c3c126a5f9eff58a46f780
│  │  │  ├─ d222f6f055f65a8cf46a01586e7c13e2f3f555
│  │  │  ├─ d655763608d1546cf8725e83da6b4567f24027
│  │  │  └─ f3818a2a658c2e32b80740e4bdd494eb762f67
│  │  ├─ 30
│  │  │  ├─ 5c912d7ff99ec78193600f664a00cc62fd6833
│  │  │  ├─ b0691bf44b3ad7d5096d9497df78a966e582ff
│  │  │  └─ ff4a5d4c99d8ea7a1be1bfacb07ec7c84e9555
│  │  ├─ 31
│  │  │  ├─ 0028430499361c7e9250000346f3b929cdf138
│  │  │  └─ b5db8596c7ccc50a9929201c6c5cf274dbacb4
│  │  ├─ 33
│  │  │  ├─ b9a0cacb992b1610a9bd0be00c0016217c93b1
│  │  │  └─ c5628fe69b964bbb8ea32390b6f5979f415816
│  │  ├─ 34
│  │  │  └─ 21ebaca60be429aa2389c552a8d2814bc0f2f3
│  │  ├─ 35
│  │  │  └─ a40ee562bbd767f76db646b55f6c44d8ddbd8d
│  │  ├─ 37
│  │  │  └─ f89a9c80b8e9936323a63d385fcb89265e6a17
│  │  ├─ 38
│  │  │  └─ 45acfaeaa5c3bf0a78a5e79a814b39680ac5bf
│  │  ├─ 39
│  │  │  ├─ 60f081d5d8ea7efbc1fd8ee84406c225ce8876
│  │  │  └─ ee4697c05d47a58cc6904a974e268b9113e1f0
│  │  ├─ 3a
│  │  │  └─ 2517f08da24c3e07543ae1837d934df173675b
│  │  ├─ 3d
│  │  │  ├─ 19aa35bc3e4fbfa05c073f5500d7935cb5bb67
│  │  │  └─ a8741c86bd2d00d904c2f2308d696071955089
│  │  ├─ 3e
│  │  │  └─ 1544e9f556b03bd588fe997a315e494f913015
│  │  ├─ 3f
│  │  │  └─ 37fcaed21469356a4c6ed92b96b8fe81672bf0
│  │  ├─ 40
│  │  │  ├─ 6f11d4779f63b0a3b8ae450d22fb8005b01005
│  │  │  └─ f1d232c92bb5816761a0c603de78e99602630a
│  │  ├─ 41
│  │  │  ├─ 82b1312fb7d967cad50b044e7363e5d3251648
│  │  │  └─ c44f3b9a883a212b86785e26c6a2a11b068852
│  │  ├─ 42
│  │  │  ├─ 58b5e03145d9a9fcbbdbe34620b4db2faba0b2
│  │  │  ├─ 728598f996e503d667f905e41aeaad16256908
│  │  │  └─ d47c1148f5453ae7a62e1036408b42b54e064e
│  │  ├─ 43
│  │  │  ├─ 0b637499941dc81bbc997e51dae9d75e573109
│  │  │  ├─ 79aa8b30e909b5ad0fcbe41ee0b2b692a1a84e
│  │  │  └─ d0bc7a98b2a7df91bf3770a8d273e291bee22a
│  │  ├─ 46
│  │  │  └─ 3e20779eec5aa6a0f23c6ae557f7633059cdd1
│  │  ├─ 47
│  │  │  ├─ 8a5854a80720e29ce5073dcebbc022059f9bfd
│  │  │  └─ d99f75938fc7b3aa4af3bc10365068430c37e6
│  │  ├─ 48
│  │  │  ├─ 0ddbc4dfbf3852e30de6380e87407c42c2a351
│  │  │  ├─ 12cc4a4430f1410d84c7518b566c096027816f
│  │  │  ├─ 3e208c1f50f6b837b54312935d687050fb4578
│  │  │  └─ 5284d5335dddbd15e6201ebf281c67cc2158f9
│  │  ├─ 4a
│  │  │  ├─ c830d140122ed8f39c280ba1e7b13ee11f442d
│  │  │  └─ f723e856f25dbba0deef2d17cefd9f0de93888
│  │  ├─ 4b
│  │  │  ├─ 4ce3faa791b706ddf3fb2d691c659d6133e904
│  │  │  └─ 98f31dd952df2ad8a71c21a911b24640ab0011
│  │  ├─ 4c
│  │  │  └─ ba3d32c692a8171a050705e66fba7c36b49c49
│  │  ├─ 4e
│  │  │  ├─ 259365bc345400fa758da566bf7dd6b9cff8c2
│  │  │  ├─ 4b1338d61158cf77b9df0f5dbf27c186090bb4
│  │  │  ├─ 5aeb5ffff4fc44e4d140bbb4851760b5b68c22
│  │  │  └─ ab0fa7ae5c5f797d0cea5a856fe2c699a52b12
│  │  ├─ 51
│  │  │  └─ 565f00e167264b5534b73425d2bf5397bc809e
│  │  ├─ 52
│  │  │  └─ 995068a03892006159770c568fd1f0c36f3831
│  │  ├─ 53
│  │  │  └─ da2c48816fdff71190e7cfa92bc0c5f2086705
│  │  ├─ 54
│  │  │  ├─ 44174a25cd2f152352d6527caecfc162315d59
│  │  │  ├─ 9efc66f1322aaa38791c24089159476b6a700d
│  │  │  └─ bde00dec498900005f719bbe5d566bb07f7a25
│  │  ├─ 55
│  │  │  └─ aa782a696ca490052b20e0f47a917d92a0e986
│  │  ├─ 56
│  │  │  └─ ac8b430e32ca1c3183a1975c20a526e6566b76
│  │  ├─ 58
│  │  │  ├─ 62318de2ee496e7ab0c77eb96fbe035014ff10
│  │  │  └─ 6ef77085046752ad6f7b8137e67559ab48caa3
│  │  ├─ 59
│  │  │  ├─ 73250225b3a00c2b57312a6b1e3f4281f72d8e
│  │  │  └─ 839356e43d0abb7ef0c12f97a6dffdce9f2bf5
│  │  ├─ 5b
│  │  │  └─ 2ca1682a39615dc6c9fe9ff247b80a08dd9ed2
│  │  ├─ 5d
│  │  │  └─ 5194cdee674151c55e26e97ccfab262b8c88e0
│  │  ├─ 5e
│  │  │  └─ 60fe258fd9540cc33ce8c80761696cf32318ee
│  │  ├─ 5f
│  │  │  ├─ 09d206912995da0566babce89b728321ddaf59
│  │  │  ├─ e1b2b5da0c845b1174ba901ae5f366daa4fdee
│  │  │  └─ ecfb8064f53ee98c3be731c93e728b9b133466
│  │  ├─ 60
│  │  │  └─ 67fa04fbc5d511793331637a82dfe493da18c4
│  │  ├─ 61
│  │  │  ├─ 8526a8ae7c187d49f1e738752ba17d7c5f0eb5
│  │  │  ├─ 972a4ff2b6a06f1fb164f2361f47434e642be1
│  │  │  └─ a6edce707541b4e72b13d94cf1bf176d4b9b1a
│  │  ├─ 62
│  │  │  ├─ 9a26ef03ac64af5396b61c06e5a6865203b266
│  │  │  └─ eaecbfbf2a7b1fb37cecbd22d73f473fc025fe
│  │  ├─ 63
│  │  │  ├─ 30215fdff0292762ce52140cc1417bcc0a9471
│  │  │  └─ 82bd5f3ac98052fe482606cc43c7ec963822a7
│  │  ├─ 65
│  │  │  ├─ 094c347943453621ddbf5d65e01e7ab9b68c90
│  │  │  └─ 5a9eccf6f41e597c0cf7f757b7dfba42d4230d
│  │  ├─ 67
│  │  │  └─ cb5c01154d8c97cd75e8e90e2003dddb13b9b5
│  │  ├─ 68
│  │  │  ├─ 0ec56332f6eda01dbd1d53b932da566d0397b9
│  │  │  └─ c8ed407c737fe13415c663be54525e264ab465
│  │  ├─ 69
│  │  │  ├─ 1386483fa4a14c7bedfbfcf9d545272921b17e
│  │  │  └─ 8d43a56ed31c6bcddd1f5661a1ea77dc94d99e
│  │  ├─ 6a
│  │  │  └─ 9ea1f71fb9dca223c1de7b745c3f397fc90f6f
│  │  ├─ 6b
│  │  │  └─ 8c8cdc36a1a52c4f017fb8717abb9813c0fd2c
│  │  ├─ 6c
│  │  │  ├─ 27413fe457158097bf9f086ca4de6c1f5a6715
│  │  │  └─ d69e999807786b2b6f75f52b15b6b6544469b1
│  │  ├─ 6d
│  │  │  ├─ 78fa0606c0c6bdf962cdf6dccc1ac5cae20636
│  │  │  ├─ a20abe71f060012047499efb7292309df3c60f
│  │  │  └─ afbd8e6ec2d65ee87aaa8073840fc4441a1b3e
│  │  ├─ 6f
│  │  │  ├─ 18e56c4795601ffce7c9beab7090229d468845
│  │  │  ├─ 7854a0296dec23567b20f4cf979053f2ca3c65
│  │  │  ├─ b0925a248c4ec2221521dba92aae5c1eef1315
│  │  │  └─ c0852716652fff10c40d98d8eb146bb15a5104
│  │  ├─ 70
│  │  │  ├─ 7df9a5609bcd597d07dd027eae8571e9e7be5b
│  │  │  └─ ca916a6099ec923cd4f06461ba68753b4d7101
│  │  ├─ 71
│  │  │  ├─ 3f1642fab1a9b440e03cbabe37655bc0fbee2c
│  │  │  └─ 473a2a88c995b9e1e6c4d353eb7ffd75463de4
│  │  ├─ 73
│  │  │  ├─ 07ac54464e76281db626057ea0e5c386f9b134
│  │  │  └─ b3e8ad8c04f29891309229d0b8165ba3c7d1ae
│  │  ├─ 74
│  │  │  ├─ 75fc748a5b640a2278b4320328bdcbf1484f10
│  │  │  └─ ec6ce8ebecd91d662ce73636eebdbb65374eba
│  │  ├─ 75
│  │  │  ├─ 865784ccd250f93c90939e5d22d3d481556272
│  │  │  └─ dc931caff9771b2ba4922f128e842508d82977
│  │  ├─ 76
│  │  │  └─ bb98d704d6165cc020e085e77720fb64556da4
│  │  ├─ 77
│  │  │  ├─ 3da59aec3c21f323b7a144a3853921a3058c19
│  │  │  └─ c978c83e5d98b09a942ad0ef5e020f4675dba3
│  │  ├─ 79
│  │  │  ├─ 7502169421c9f04be3d2988ecdf5b2943b35eb
│  │  │  └─ 825b0f92572c5eccdaa3f4eaad68ef717aa476
│  │  ├─ 80
│  │  │  ├─ 12b3b8434c60927d796fa5c7be14cd99fc37c4
│  │  │  └─ 380fec73499c82b11d9d791dc7fd37a366556f
│  │  ├─ 81
│  │  │  └─ c5222cb61d70fc7596cf79568246e5cd372345
│  │  ├─ 83
│  │  │  ├─ 4125ec2c1f522890bacad76d2eca9c298a5d07
│  │  │  ├─ 58b9569a65200d0f220d79da91ecbc2f34fcad
│  │  │  └─ e2bb460d78dd63d765097e315478d581da1f91
│  │  ├─ 84
│  │  │  ├─ 4d9730ae166bb0eeaaa892df580d6ac4a50af9
│  │  │  ├─ 83b8bd0063f6f348c90bb3297b28cfa37e4592
│  │  │  └─ c4c9042fecd2219bfd0f53675c41f11e9e766b
│  │  ├─ 85
│  │  │  └─ c73c11d94063ea81642b699ef69f7273b03fb9
│  │  ├─ 87
│  │  │  └─ b8dba04b097671e36f1a773efafd818971da80
│  │  ├─ 88
│  │  │  └─ 8fcd45940e93f1cc2cad9bed3abca0249b24b6
│  │  ├─ 89
│  │  │  └─ b7141833d434bef6ed71e2fa822bf43d9db204
│  │  ├─ 8a
│  │  │  └─ a6020d88242093c6586547181998d623312ce5
│  │  ├─ 8b
│  │  │  ├─ 6beac9c7e4df44cbe369f2a5b7a7b48ee8becc
│  │  │  └─ a342dde27c74096df0d1c4d17705ab59112608
│  │  ├─ 8d
│  │  │  └─ 6288daced9c44a1b1d46ccf38a83ace8ac4bb7
│  │  ├─ 8f
│  │  │  ├─ 29e46099fc25c8121fd3875f0f7059ab956c31
│  │  │  ├─ cd4b713fe4edf7b334bad028a7473065ec22fc
│  │  │  └─ e2dd786d0aa38c17b73be0cfd7556eb5c969f9
│  │  ├─ 90
│  │  │  └─ db3b2037d22c7ac7c421df8adb0cf877b420e7
│  │  ├─ 91
│  │  │  └─ 5b36bbb0b544de4e44a33fd5972dcd740bdf3d
│  │  ├─ 93
│  │  │  └─ ad3a1e817c626f5fbee4ef55ed97e5df7c5544
│  │  ├─ 95
│  │  │  ├─ 233a086080f524bf8c296453187259eddc7c66
│  │  │  └─ d924c029f8cdb06c0f2dcb47dcb5ed6d1c4a2e
│  │  ├─ 98
│  │  │  └─ 4c5ca2e3776c7cddf7faf497c8f0119a94f737
│  │  ├─ 99
│  │  │  └─ 27b55022038fe61372043daf763c71c8c4f959
│  │  ├─ 9a
│  │  │  └─ b26be5d40c32d81a79fe978e1bc9a43f71b0b9
│  │  ├─ 9b
│  │  │  ├─ 1aed9ee9b98914be12a800575527a3c04e5ec7
│  │  │  └─ e0f6ab35747c162dfd7921cd912bae17b2c742
│  │  ├─ 9d
│  │  │  ├─ 33a9de3695b8284e845502d85334b4648cc94d
│  │  │  └─ 616795c64b282dadcdbd3a2104615b02076889
│  │  ├─ 9e
│  │  │  └─ 5476864fe96d358609fd7071a03e5c0b2d8414
│  │  ├─ a0
│  │  │  ├─ b9892e54e85bf4551de19ce81672d75beaa74d
│  │  │  └─ d751d36790863812c7e8a8068bebb37845292d
│  │  ├─ a1
│  │  │  ├─ 74dff1207c08b1628d042ca09797abe370f4fe
│  │  │  └─ e16094b51532d69d67bc32089f27e9704596e1
│  │  ├─ a3
│  │  │  ├─ 0c1fec0d769645fc8a602369e22242bdab68bb
│  │  │  ├─ 102c476b8affba0b1daafda6b4db231494c6a8
│  │  │  ├─ a6ca2a2a1987e89f7516f2cba82f48391f723e
│  │  │  └─ b80449045aa169f046b49cee2ac10d91ccd746
│  │  ├─ a4
│  │  │  ├─ 090028b8f56d3f6d40eef218304ff1f06ebfdc
│  │  │  └─ fcbfda56a3a426e56f32b88acdcfe8a5db0d3e
│  │  ├─ a8
│  │  │  └─ 9aa76fdbe71b66c38065d0f4515faa33a68f7e
│  │  ├─ a9
│  │  │  ├─ 2a5a34c51e761248d2a3d0f06e1acaf01aefc2
│  │  │  ├─ 912f433f1438ea3b5a40823bfb5a157162621a
│  │  │  ├─ a6b2b6541e36937460bcd3196b45c0100f4be2
│  │  │  └─ e1311882364c915a35c8fa31bfd74de1ee8e8b
│  │  ├─ ab
│  │  │  ├─ 3318c47643ebe69fb71392e09168ed011aaaa8
│  │  │  ├─ 89a23fca5dede115a363501b0f2aa4a82652ac
│  │  │  └─ 96567da4875dbca21540bc6b47f00789842912
│  │  ├─ ae
│  │  │  ├─ 71ef13193cece11056a4498f41dea455f6a702
│  │  │  ├─ 759b7bbfc2c2fa961e5d04d25c229f97c99f79
│  │  │  └─ 78f00910c4dc414b9db4671638b57cb0964732
│  │  ├─ b0
│  │  │  ├─ 338bab9d5160dd23a1e007cedda49b529dce91
│  │  │  ├─ 793dbb9f9f5a5b3937f906d15b0d7773bbb81b
│  │  │  └─ 942e373cf3d6cb5306435e3024d35a3382504d
│  │  ├─ b2
│  │  │  └─ d0c12d282a85f45bd9f00b8d085486af0f0965
│  │  ├─ b3
│  │  │  └─ d4fee12811c505cb91600cb8719d7360c43a7b
│  │  ├─ b6
│  │  │  ├─ 4a9c30427d927a0667f3e6c47b699bf9308a4b
│  │  │  └─ 7bb825932fcf0d91bde783080967d001d7490b
│  │  ├─ b7
│  │  │  ├─ 30fce4975ade3aeed9ce7edee9d9d8716735d7
│  │  │  ├─ 56c8c0534cb9a591c2784fc1527f9a305d0839
│  │  │  └─ 8d6b36e5d1fb8a89bdef47f370e41b9bae672d
│  │  ├─ b9
│  │  │  └─ 5ab881937b5f1a068e636f04243fed30ed670b
│  │  ├─ ba
│  │  │  └─ fff12006992688c313b633c54feb36129fa465
│  │  ├─ bb
│  │  │  ├─ 01af58cccc733f82148dddcde3af6e44e9d852
│  │  │  ├─ 46f2f13c83b5e668ae902858c6e291f58f4540
│  │  │  ├─ 58c4b22ec3fdef9f4a1e79316331b28d5780c9
│  │  │  └─ 5b0f13ff0d7d8ac44e5433601971a37588142a
│  │  ├─ bc
│  │  │  └─ b4067ac5366b2f990cab64cbc60e871c386cfb
│  │  ├─ bd
│  │  │  ├─ 1e8d6f5f0b55868dd0e25a16f8262e5384bc40
│  │  │  ├─ 84286ec9b1171459af5a62362f49bf924c2283
│  │  │  └─ 89fe2ad072c50a31751891b7d830640feaad4a
│  │  ├─ be
│  │  │  └─ 407d653343ee50ae468a306c28608aa057d101
│  │  ├─ bf
│  │  │  ├─ 05bf1f44a87d69873aeb7a309d29a0742a8ae4
│  │  │  └─ a2c914aa0cbb94170b1edb1ac0420ba4171269
│  │  ├─ c0
│  │  │  └─ 3e275f6bacfb2e6f642d97ee3668be0848b406
│  │  ├─ c2
│  │  │  ├─ 58129573fff4df444796628ae5ebb79210e1b5
│  │  │  └─ c1bf063bfc8e23a0aa3026d781f245c152e6d5
│  │  ├─ c3
│  │  │  └─ 5bf57ca02403df866c16d84419dafa089f837b
│  │  ├─ c4
│  │  │  └─ 9caf2add1f24f47c85f105697d8f4b21b69bc8
│  │  ├─ c5
│  │  │  └─ 6857c27d4923fbdc3258342184ca129391f176
│  │  ├─ c6
│  │  │  └─ abea354447274b2d57083c498d8ec77a5eada0
│  │  ├─ c7
│  │  │  └─ 29dc1d7e577aa58ac4a4ac4bd801d650d79cf3
│  │  ├─ c8
│  │  │  ├─ 251920d1ff91eaccf79dc4828ea6009ca772ab
│  │  │  ├─ 5f987bbd56dcaddea8d59198f628d8e96fff49
│  │  │  └─ 84ca9fd56270aebd2e04c05e613ae70eb191b1
│  │  ├─ ca
│  │  │  └─ 5364e3f0882f3101bbc90ac019a87c106af1cb
│  │  ├─ cc
│  │  │  └─ 413e615358e5e7740c36e596170eaf1fd3f912
│  │  ├─ d0
│  │  │  ├─ 1e7597a06a5d6933f25adf0f4779534456ca38
│  │  │  └─ 47ac3241e53ef38d0a03c86b995eed86852c6f
│  │  ├─ d1
│  │  │  └─ 5ff4b564f78ccaccc3296584aa5edfbcac0703
│  │  ├─ d2
│  │  │  ├─ 1a7131333a538376a12984fbedbf975cb7c8ff
│  │  │  ├─ 1fc468a81e7c11ed3cf4c60bc135dd29d9b3d2
│  │  │  └─ 22ef871bd957de9d96d9b1da09d119e1a13a53
│  │  ├─ d4
│  │  │  └─ e1b3f14250f518bc9a1ec5c8fa99a6a5434f1a
│  │  ├─ d5
│  │  │  ├─ 65ced53c5533c98a83dfd9d2a1200bf7d425d6
│  │  │  └─ 86ea1e60cc083dcc5e1f89ede731a0e8aab619
│  │  ├─ d6
│  │  │  └─ a5a4297d1a12c80c03623a7fba781314490194
│  │  ├─ d7
│  │  │  ├─ 411cd8e147e65a2d71e81104a034599364c0cf
│  │  │  └─ 9464a1b3fca7c87793213c3957064da12b2a06
│  │  ├─ d9
│  │  │  └─ b2e010cb0219dd3ea73c89fc428196811ed0a6
│  │  ├─ da
│  │  │  └─ 6705fc1a694175def611af437231be64b6b0ab
│  │  ├─ db
│  │  │  └─ fa407b23d16b6066b0060121336c6e66c490e9
│  │  ├─ dc
│  │  │  └─ 5573ef09b654c268f3aae72d6095143c7d7158
│  │  ├─ dd
│  │  │  ├─ 1d01dc8f1e7d6ce43a8652b2f357b216a8e96b
│  │  │  └─ b859056d7680a953c78e04bad3a2f9ec09a384
│  │  ├─ df
│  │  │  ├─ 30d646ac716878fd39c7d682421a5e09beb927
│  │  │  ├─ 451f79d3438b024b92250ab63d304d8a1a6c7a
│  │  │  ├─ 4615040c0a54fabcbe69b62e23bc921a50bc9c
│  │  │  └─ ac9e3253cff318a05577bac55664e31ad9da1a
│  │  ├─ e0
│  │  │  ├─ 4b64f2c480771e15563a41aad554b12a9e2f99
│  │  │  └─ c2583d0f921296360b6df4de0fda954b013a2e
│  │  ├─ e1
│  │  │  └─ e40a2b8746a9b6bbdab0c0df0ea61b88a12407
│  │  ├─ e2
│  │  │  └─ fe454f616543ae6ef06b9ab687907799571541
│  │  ├─ e3
│  │  │  ├─ b34249c2d4f7bd66182cdf9131820e50491b93
│  │  │  └─ b4c9220766f9d0f10e39daf98fedb795964f55
│  │  ├─ e5
│  │  │  ├─ 5a8d19980e5a273c808f10e5989dd9546ec839
│  │  │  └─ d24fcfc85b5a9cfe170f8a275745124369d8b4
│  │  ├─ e7
│  │  │  ├─ 4c29f19ec8be67da8b572c346884c97899ff06
│  │  │  └─ 817a246e2798a5024d3ab0643c82453e6ce2f8
│  │  ├─ ea
│  │  │  └─ fe4f9fc05d96e03a31ce039d4491d5050b33eb
│  │  ├─ eb
│  │  │  ├─ 22c7e998380f56db4f657059460c2735382d37
│  │  │  ├─ 40f198c0f4dbca263fc6bb3f810e4b825488a7
│  │  │  ├─ 55c82baf0af9826487de4c7f86ea68f405cdcb
│  │  │  ├─ d41f02d0e86dfc1f40ec39592dc0670114dc5b
│  │  │  └─ f827953a8690d661a0c3046a84f407721bdbf7
│  │  ├─ ec
│  │  │  └─ 7191781ccc6b8a2d492c67cc09c524150d3518
│  │  ├─ ef
│  │  │  └─ f9e8ee844c6ad55db748be35b837f56bf22911
│  │  ├─ f1
│  │  │  └─ c85ca7efb48732919b620a19e20599ce1d7b05
│  │  ├─ f2
│  │  │  ├─ 32b706dbcac3a23452fc8d75dddd20da027030
│  │  │  ├─ 6480f0900e93d8b6d2d2e2a0d3baeac6ec7fc4
│  │  │  └─ b9b2b6f2f42f258824b386fb675737664879cb
│  │  ├─ f3
│  │  │  └─ a787392ec09242a83c039050d1cd9f5d91a882
│  │  ├─ f4
│  │  │  ├─ 145a6e83c057930d079231986de8d6109617a3
│  │  │  └─ 2a7ebb76d7e6e3d28463a028afef491c6912fd
│  │  ├─ f5
│  │  │  ├─ 85042dee7babcd8dbebfe31d1ee8703dc6be75
│  │  │  ├─ a5d26b3f242fe8c96132ffbb7f7d343f4a1dee
│  │  │  └─ f8e48e373f5d4698a59db4b1131a4203ffbb76
│  │  ├─ f6
│  │  │  ├─ 1ce528ee4e940f67dc4e0fac54c110e0311ed1
│  │  │  └─ d7d8749dfe4762ee468f9eccb6e93a5787bc58
│  │  ├─ f8
│  │  │  ├─ 39632cd7c1bd8584440ed6e130686d8a312926
│  │  │  └─ 5a69448b96324106f10c98d5b9c1a2c65b6da3
│  │  ├─ f9
│  │  │  └─ 52dbc3c15389298fbd17c95d9b5616c555cc08
│  │  ├─ fa
│  │  │  └─ fb5db7e30fcb374612cb3a1c3bf441a7502f94
│  │  ├─ fb
│  │  │  ├─ 1ea527bcc39cafa6ec96bcc35152e17ed6a0a4
│  │  │  └─ afbc2734c17bb5984d3f62773b2a1df43287fc
│  │  ├─ fc
│  │  │  └─ f3a7d34640b7a8c887e94466f6edc88031452d
│  │  ├─ fd
│  │  │  └─ 63aa084ea65366159f6921f20743b620a25341
│  │  ├─ fe
│  │  │  ├─ 68fb5f74f649c3ff090cae0326854413de9b5a
│  │  │  └─ aaa560551a321c0cf0f921366d208c76950db5
│  │  ├─ ff
│  │  │  └─ db50e70adb5df451edfb3836175799e0eac4d7
│  │  ├─ info
│  │  │  └─ packs
│  │  └─ pack
│  │     ├─ pack-c512f7846d45f2f9f356cefad519f9ee9ef0500c.idx
│  │     ├─ pack-c512f7846d45f2f9f356cefad519f9ee9ef0500c.pack
│  │     └─ pack-c512f7846d45f2f9f356cefad519f9ee9ef0500c.rev
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  ├─ dev_user_accout
│     │  ├─ main
│     │  └─ main_Dev
│     ├─ remotes
│     │  └─ origin
│     │     ├─ Dev
│     │     ├─ Dev_Deploy_AWS
│     │     ├─ Dev_Deploy_EB
│     │     ├─ Dev_Ref
│     │     ├─ Dev_Trade_ccy
│     │     ├─ Dev_auth_ccy
│     │     ├─ Dev_exterminator
│     │     ├─ Dev_user
│     │     ├─ REFACTOR_Trade_ccy
│     │     ├─ dev_user_accout
│     │     ├─ main
│     │     └─ main_Dev
│     ├─ replace
│     └─ tags
├─ .gitignore
├─ .platform
│  ├─ hooks
│  └─ packages.yml
├─ Dockerfile
├─ Dockerfile.copy
├─ Dockerrun.aws.json
├─ Procfile
├─ README.md
├─ application.py
├─ buildspec.yml
├─ common
│  ├─ Nice
│  │  └─ utils.py
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ management
│  │  └─ func.py
│  ├─ migrations
│  ├─ models.py
│  ├─ response.py
│  ├─ serializers.py
│  ├─ tests.py
│  └─ views.py
├─ core
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  └─ wsgi.py
├─ entrypoint.dev.sh
├─ entypoint.sh
├─ exterminator
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_initial.py
│  │  └─ __init__.py
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
│  │  ├─ 0002_farminfo_owner.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ permissions.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ main
│  ├─ urls.py
│  └─ views.py
├─ manage.py
├─ payments
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
├─ requirements.txt
├─ trade
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_initial.py
│  │  └─ __init__.py
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
   ├─ jwt
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

```# Dronefield_API_server
