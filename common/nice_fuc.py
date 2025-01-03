# 나이스 인증에 필요한 함수 따로 빼서 정리

import base64, requests, time, random, json, hashlib, hmac
from datetime import datetime
from Crypto.Cipher import AES

clientID = "0545ff92-f535-444d-928c-d572d8679445"
secretKey = "bd6911abee518341ff25a65aa1813e0c"
APIUrl = "https://svc.niceapi.co.kr:22001"
productID = "2101979031"
access_token = "ec1dcd1c-02d8-48da-8018-5c0ff193f030"  # 기관토큰(access_token)은 반영구적으로 사용가능하며 한번 발급 후 50년 유효합니다.


def encrypt_data(plain_text, key, iv):
    from Crypto.Cipher import AES

    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    pad = 16 - len(plain_text) % 16
    plain_text += chr(pad) * pad
    encrypted = cipher.encrypt(plain_text.encode())
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt_data(enc_text, key, iv):
    from Crypto.Cipher import AES

    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    enc_text = base64.b64decode(enc_text)
    decrypted = cipher.decrypt(enc_text).decode('utf-8')
    pad = ord(decrypted[-1])
    return decrypted[:-pad]
