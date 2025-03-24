import time
from czds_token import get_auth_token
from download_zone import download_zone_file, get_zone_files


def download_all_zone_files():
    token = get_auth_token()
    if not token:
        print("[ERROR] CZDS API 인증 실패. 스크립트를 종료합니다.")
        return

    zone_files = get_zone_files(token)
    if not zone_files:
        print("[INFO] 다운로드할 zone 파일이 없습니다.")
        return

    print(f"[INFO] 총 {len(zone_files)}개의 zone 파일을 다운로드합니다...")

    for i, download_url in enumerate(zone_files, start=1):
        # zone name 추출
        zone_name = download_url.split('/')[-1].replace('.zone', '')

        if zone_name and download_url:
            print(f"[{i}/{len(zone_files)}] {zone_name} 다운로드 중...")
            download_zone_file(zone_name, download_url, token)
            time.sleep(5)  # 5초 대기 (서버 부하 방지)

    print("[INFO] 모든 zone 파일 다운로드 완료.")

# 실행
if __name__ == "__main__":
    print("[INFO] CZDS Zone File 다운로드 스크립트 실행 중...")
    download_all_zone_files()