@echo off

if not exist .env (
    copy /-Y .env.example .env;
    echo .env 파일이 생성되었습니다. API 키를 설정하세요.
) else (
    echo .env 파일이 이미 존재합니다.
)
