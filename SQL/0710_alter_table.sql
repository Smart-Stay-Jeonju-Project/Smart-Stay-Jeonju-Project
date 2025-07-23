alter table review add COLUMN nickname varchar(50) not null;
alter table review modify COLUMN write_date VARCHAR(10) not null;
alter TABLE Accom_Source modify COLUMN source_rating float default 0;
alter table keywords modify COLUMN keyword_score int not null;
alter TABLE accommodations modify COLUMN feature varchar(50);
alter TABLE accommodations modify COLUMN name varchar(50) NOT NULL UNIQUE;

alter table Report add COLUMN positive_img varchar(100) not null;
alter table review modify COLUMN clean_reviews longtext;
alter table review modify COLUMN content longtext;

 alter table report modify COLUMN report_writedate datetime not null DEFAULT CURRENT_TIMESTAMP;


alter table keywords modify COLUMN keyword_type varchar(50);
    
    

-- 리뷰테이블에 원본숙소 테이블에 연결하는 외래키 추가
alter table review add COLUMN source_id int;
alter table review add foreign key(source_id) references accom_source(source_id);

-- 리포트 테이블 키워드 컬럼 삭제
ALTER TABLE report DROP COLUMN negative_keywords;
ALTER TABLE report DROP COLUMN positive_keywords;

-- 중복 데이터 불가
ALTER TABLE review
ADD UNIQUE (
    accommodation_id, 
    content, 
    write_date, 
    review_rating, 
    review_source, 
    review_type, 
    nickname, 
    clean_reviews
);

-- 유니크 확인 필요
alter TABLE accommodations modify COLUMN name varchar(50) NOT NULL;


alter TABLE accom_source modify COLUMN accommodation_id int;
alter table accom_source add COLUMN latitude float;
alter table accom_source add COLUMN longtitude float;

-- 컬럼명 변경
ALTER TABLE accom_source CHANGE COLUMN longtitude longitude float;
ALTER TABLE accommodations CHANGE COLUMN longtitude longitude float;



-- primary 자동 id 초기화
ALTER TABLE report AUTO_INCREMENT = 1;

ALTER TABLE accom_source AUTO_INCREMENT = 1;
ALTER TABLE review AUTO_INCREMENT = 5;

ALTER TABLE keywords AUTO_INCREMENT = 1;

SHOW CREATE TABLE accommodations;

-- 외래키 삭제
alter table review DROP CONSTRAINT `review_ibfk_1`;
ALTER TABLE review DROP accommodation_id;

-- 외래키 삭제
alter table accom_source DROP CONSTRAINT `accom_source_ibfk_1`;
ALTER TABLE accom_source DROP accommodation_id;

-- 외래키 추가
alter table accom_source add COLUMN accommodation_id int not null;
alter table accom_source add foreign key(accommodation_id) references accommodations(accommodation_id);


-- 리포트 외래키 삭제
alter table report DROP CONSTRAINT `report_ibfk_1`;
ALTER TABLE report DROP accommodation_id;

-- 외래키 추가
alter table report add COLUMN source_id int not null;
alter table report add foreign key(source_id) references accom_source(source_id);




-- **** 안전모드 끄기
SET SQL_SAFE_UPDATES = 0;

-- accom_source 테이블에 accommodations 테이블 주소 매칭하여 id 주가
UPDATE accom_source s
JOIN accommodations a
  ON s.source_addr = a.address
SET s.accommodation_id = a.accommodation_id;


 alter table report modify Positive_img varchar(100);
 alter table report modify negative_img varchar(100);

-- 컬럼 데이터만 삭제, 컬럼은 유지
UPDATE report SET positive_img = NULL;
UPDATE report SET negative_img = NULL;

-- 여기어때 평점/2한 값과 야놀자 평점의 평균으로 통합숙소 테이블 평점 업데이트
UPDATE accommodations a
JOIN (
    SELECT 
        source_addr,
        AVG(CASE 
                WHEN source = 'y' THEN source_rating / 2
                WHEN source = 'n' THEN source_rating
                ELSE NULL
            END) AS avg_rating
    FROM accom_source
    GROUP BY source_addr
) s ON a.address = s.source_addr
SET a.rating = s.avg_rating;


-- **** 안전모드 켜기
SET SQL_SAFE_UPDATES = 1;


