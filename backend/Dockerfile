FROM python:3.12.1

# 기본 UTF-8 환경 변수 설정 (locale을 설치하지 않고 설정)
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]