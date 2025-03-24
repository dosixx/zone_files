import os
import time
import json
import requests
import subprocess
from git_commit import commit_zone_file
import info


# CZDS API를 사용하여 zone 파일 목록 가져오기
def get_zone_files(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "CZDS Client/1.0 (Dosix)"  # User-Agent 추가
    }
    api_url = "https://czds-api.icann.org/czds/downloads/links"  # 올바른 엔드포인트로 수정

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        try:
            zone_files = response.json()
            if isinstance(zone_files, list) and all(isinstance(zone, str) for zone in zone_files):
                return zone_files
            else:
                print("[ERROR] 응답 형식이 올바르지 않습니다.")
                return []
        except json.decoder.JSONDecodeError:
            print("[ERROR] 응답이 JSON 형식이 아닙니다.")
            return []
    else:
        print(f"[ERROR] Zone 파일 목록 가져오기 실패: {response.status_code}, 응답: {response.text}")
        return []

# 개별 zone 파일 다운로드
def download_zone_file(zone_name, url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        file_path = os.path.join(info.DOWNLOAD_DIR, f"{zone_name}.txt.gz")
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        # 파일 생성 여부 확인
        if os.path.exists(file_path):
            print(f"[SUCCESS] {zone_name} 다운로드 완료 → {file_path}")
            # Git에 파일 추가 및 커밋
            commit_zone_file(zone_name)
        else:
            print(f"[ERROR] {zone_name} 다운로드 실패: 파일이 생성되지 않았습니다.")
    elif response.status_code == 403:
        print(f"[INFO] {zone_name}에 대한 접근 권한이 없습니다. 토큰을 확인하거나 권한을 요청하세요.")
    else:
        print(f"[ERROR] {zone_name} 다운로드 실패: {response.status_code}, 응답: {response.text}")