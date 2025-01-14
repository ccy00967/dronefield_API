# 나이스 인증에 필요한 함수 따로 빼서 정리

import base64, requests, time, random, json, hashlib, hmac
from datetime import datetime
from Crypto.Cipher import AES

clientID = "0545ff92-f535-444d-928c-d572d8679445"
secretKey = "bd6911abee518341ff25a65aa1813e0c"
APIUrl = "https://svc.niceapi.co.kr:22001"
productID = "2101979031"
access_token = "ec1dcd1c-02d8-48da-8018-5c0ff193f030"  # 기관토큰(access_token)은 반영구적으로 사용가능하며 한번 발급 후 50년 유효합니다.

Email = "email"
ValidateKey = "validatekey"
isNicePassDone = "isNicePassDone"
isEmailValidate = "isEmailValidate"

def encrypt_data(plain_data, key, iv):
    block_size = 16
    pad = lambda s: s + (block_size - len(s) % block_size) * chr(
        block_size - len(s) % block_size
    )
    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    return base64.b64encode(cipher.encrypt(pad(plain_data).encode("utf-8"))).decode(
        "utf-8"
    )


def decrypt_data(enc_data, key, iv):
    encryptor = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    unpad = lambda s: s[0 : -ord(s[-1:])]
    return unpad(encryptor.decrypt(base64.b64decode(enc_data))).decode("euc-kr")

# def nice_toekn():
#     now = str(int(time.time()))
#     req_dtim = datetime.now().strftime("%Y%m%d%H%M%S")
#     req_no = "REQ" + req_dtim + str(random.randint(0, 10000)).zfill(4)
#     url = APIUrl + "/digital/niceid/api/v1.0/common/crypto/token"
#     auth = access_token + ":" + now + ":" + clientID
#     base64_auth = base64.b64encode(auth.encode("utf-8")).decode("utf-8")
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "bearer " + base64_auth,
#         "productID": productID,
#     }
#     datas = {
#         "dataHeader": {"CNTY_CD": "ko", "TRAN_ID": ""},
#         "dataBody": {"req_dtim": req_dtim, "req_no": req_no, "enc_mode": "1"},
#     }
#     return requests.post(url, data=json.dumps(datas), headers=headers)