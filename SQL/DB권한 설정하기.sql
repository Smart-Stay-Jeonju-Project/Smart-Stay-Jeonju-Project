use mysql;
select user, host from user;

# 계정 생성
# create user '계정'@'도메인' identified by '사용할비번'
create user 'ateam'@'%' identified by '1234';

# DB와 테이블에의 권한 설정
# grant all privileges on 데이터베이스이름.테이블이름 to 계정@주소
# 주소 부분에 %를 사용하면, 모든 주소에서 접속 가능합니다

# 모든 DB와 모든 테이블에 대한 권한 획득
grant all privileges on *.* to 'ateam'@'%';

# 지정된 DB의 모든 테이블에 대한 권한 획득
grant all privileges on ezen.* to 'ateam'@'%';

flush privileges;