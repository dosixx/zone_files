import os
import subprocess
import time

from info import DOWNLOAD_DIR, GIT_REPO_PATH

def commit_zone_file(zone_name):
    file_path = os.path.join(DOWNLOAD_DIR, f"{zone_name}.txt.gz")

    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        print(f"[ERROR] Git 커밋 실패: {file_path} 파일이 존재하지 않습니다.")
        return

    try:
        # Git 저장소로 이동
        os.chdir(GIT_REPO_PATH)

        # git add 실행
        add_result = subprocess.run(["git", "add", file_path], capture_output=True, text=True, check=True)
        print(add_result.stdout)  # git add 출력 확인

        # git commit 실행
        commit_result = subprocess.run(["git", "commit", "-m", f"Add {zone_name} zone file"], capture_output=True, text=True, check=True)
        print(commit_result.stdout)  # git commit 출력 확인

        # git push 실행
        push_result = subprocess.run(["git", "push"], capture_output=True, text=True, check=True)
        print(push_result.stdout)  # git push 출력 확인

        print(f"[SUCCESS] {zone_name} 파일을 Git에 커밋하고 푸시했습니다.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git 명령 실행 중 오류 발생: {e}")
        print(e.stderr)  # Git 명령 오류 메시지 출력
