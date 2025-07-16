@REM 배치 파일

@echo off
cd /d "C:\Users\MYCOM\Documents\GitHub\Smart-Stay-Jeonju-Project\PROJECT\data\processed\reviews"
"C:\conda\python.exe" n_ai_cleaned_reviews.py

pause

@REM 작업 스케줄러

@REM 작업 만들기

@REM 일반 탭
@REM - 이름 정하기
@REM - 가장 높은 권한

@REM 트리거 탭
@REM - 실행 시간 정하기
@REM - 실행만 해놓을 거니 한 번만

@REM 동작 탭
@REM - 작업 : 프로그램 시작
@REM - 프로그램 스크립트 batch 파일 전체 경로 "C:\Users\MYCOM\Documents\GitHub\Smart-Stay-Jeonju-Project\PROJECT\data\processed\reviews\cleaning.bat"

@REM 실행 확인
@REM - .bat 파일 직접실행
@REM - 실행 시간 앞당겨서 실행 해보기
