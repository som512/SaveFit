from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from datetime import datetime, timedelta

# 鍵の作成
def create_key():
    key = get_random_bytes(AES.block_size)

    return b64encode(key).decode('utf-8')


# 暗号化する
def encrypt(key, data):
    key = b64decode(key)
    data = bytes(data, 'utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return ct, iv


# 復号化する
def decrypt(key, iv, ct):
    key = b64decode(key)
    iv = b64decode(iv)
    ct = b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

def encrypt_do(password):
    key = create_key()
    ct, iv = encrypt(key, password)
    pt = decrypt(key, iv, ct)
    return iv
password = str(datetime.now() + timedelta(minutes=30))
print(password)
# 新しい鍵の作成
key = create_key()
# 新しい鍵のprint
print(key)
# 暗号化する
ct, iv = encrypt(key, password)
# 暗号化したパスワードのprint
print(ct)
# padding部のprint
print(iv)
# 復号化する
pt = decrypt(key, iv, ct)
# 結果確認のため、復号したものをprint
decrypt_password = datetime.strptime(pt, "%Y-%m-%d %H:%M:%S.%f")
if datetime.now() > decrypt_password:
    print(datetime.now())
    print(decrypt_password)

