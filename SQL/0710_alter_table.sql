alter table review add COLUMN nickname varchar(50) not null;
alter table review modify COLUMN write_date VARCHAR(10) not null;
alter TABLE Accom_Source modify COLUMN source_rating float default 0;
alter table keywords modify COLUMN keyword_score int not null;
alter TABLE accommodations modify COLUMN feature varchar(50);
alter TABLE accommodations modify COLUMN name varchar(50) NOT NULL UNIQUE;

alter table Report add COLUMN positive_img varchar(100) not null;

-- 유니크 확인 필요
alter TABLE accommodations modify COLUMN name varchar(50) NOT NULL;


alter TABLE accom_source modify COLUMN accommodation_id int;
alter table accom_source add COLUMN latitude float;
alter table accom_source add COLUMN longtitude float;

-- 컬럼명 변경
ALTER TABLE accom_source CHANGE COLUMN longtitude longitude float;
ALTER TABLE accommodations CHANGE COLUMN longtitude longitude float;

-- primary 자동 id 초기화
ALTER TABLE accom_source AUTO_INCREMENT = 1;

SHOW CREATE TABLE accommodations;

-- 외래키 삭제
alter table accom_source DROP CONSTRAINT `accom_source_ibfk_1`;
ALTER TABLE accom_source DROP accommodation_id;

-- 외래키 추가
alter table accom_source add COLUMN accommodation_id int not null;
alter table accom_source add foreign key(accommodation_id) references accommodations(accommodation_id);


