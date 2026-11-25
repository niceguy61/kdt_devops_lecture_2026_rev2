# 1) 베이스 이미지: 파이썬이 이미 설치된 가벼운 Linux
FROM python:3.14-slim

# 2) 컨테이너 안에서 작업할 폴더
WORKDIR /app

# 3) 관리자(root)가 아닌 실행용 사용자를 만든다 (거의 바뀌지 않으므로 앞쪽에)
RUN useradd --create-home --uid 10001 appuser

# 4) 의존성 목록을 먼저 복사하고 설치한다 (캐시를 잘 쓰기 위한 순서)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) 앱 코드를 복사한다 (가장 자주 바뀌므로 마지막에)
COPY app.py .

# 6) 실행할 사용자, 기본 설정, 문서용 포트 표시
USER appuser
ENV APP_VERSION=1.0.0
EXPOSE 8000

# 7) 컨테이너가 시작될 때 실행할 명령
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]
