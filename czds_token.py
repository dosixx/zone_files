import os
import requests
from info import CZDS_PASSWORD, CZDS_USERNAME, DOWNLOAD_DIR
import  tempCodeRunnerFile


# 폴더 생성 (존재하지 않을 경우)
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# CZDS 로그인 후 인증 토큰 받기
def get_auth_token():
    login_url = "https://account-api.icann.org/api/authenticate"
    response = requests.post(login_url, json={"username": CZDS_USERNAME, "password": CZDS_PASSWORD})
    
    if response.status_code == 200:
        token = response.json().get("accessToken")
        print("[SUCCESS] CZDS API 인증 토큰을 가져왔습니다.")
        return token
    else:
        print(f"[ERROR] 로그인 실패: {response.status_code}, 응답: {response.text}")
        return None
