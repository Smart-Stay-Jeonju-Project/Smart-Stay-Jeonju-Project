
CREATE TABLE Accommodations (
    accommodation_id int PRIMARY KEY auto_increment,
    name varchar(50) NOT NULL UNIQUE,
    category varchar(50) not null,
    address varchar(200) not null,
    rating float default 0,
    image varchar(100),
    feature varchar(50),
    latitude float,
    longtitude float
);

-- source_rating default 0 수정
-- accommodation_id int not null 삭제

CREATE TABLE Accom_Source (
    source_id  int PRIMARY KEY auto_increment,
    accommodation_id int NOT NULL,
    source enum('y','n') not null,
    source_name varchar(50) not null,
    source_category varchar(50) not null,
    source_addr varchar(200) not null,
    source_image varchar(100),
    source_rating float default 0,
    source_feature varchar(20),
    FOREIGN KEY (accommodation_id) REFERENCES Accommodations(accommodation_id)
);

-- 작성날짜 VARCHAR(10)로 수정
-- 닉네임 추가
CREATE TABLE Review (
    review_id int PRIMARY KEY auto_increment,
    accommodation_id int NOT NULL,
    content longtext NOT NULL,
    write_date date NOT NULL,
    review_rating float,
    review_source enum('y','n') not null,
    review_type varchar(50),
    nickname varchar(50),
    FOREIGN KEY (accommodation_id) REFERENCES Accommodations(accommodation_id)
);

CREATE TABLE Keywords (
    keyword_id int PRIMARY KEY auto_increment,
    review_id int not null,
    keyword_text varchar(50) not null,
    keyword_score float not null, 
    keyword_type varchar(50) not null,
	FOREIGN KEY (review_id) REFERENCES Review(review_id)
);
-- 긍정, 부정 워드클라우드 이미지 컬럼 추가
CREATE TABLE Report (
    report_id int PRIMARY KEY auto_increment,
	accommodation_id int NOT NULL,
	report_text longtext not null,
    positive_keywords longtext,
    negative_keywords longtext,
    report_score float,
    report_writedate datetime not null,
	Positive_img varchar(100),
    negative_img varchar(100),
    FOREIGN KEY (accommodation_id) REFERENCES Accommodations(accommodation_id) 
);
