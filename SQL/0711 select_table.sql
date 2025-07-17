SELECT * FROM ateam_project1.keywords;

-- 전체 숙소의 키워드 빈도수 top1
SELECT keyword_text, SUM(keyword_score) AS total_score
FROM keywords
GROUP BY keyword_text
ORDER BY total_score DESC
LIMIT 10;


-- 숙소별 키워드 조회
SELECT k.keyword_text, SUM(k.keyword_score) AS total_score
FROM keywords k
JOIN review r ON k.review_id = r.review_id
JOIN accommodations a ON r.accommodation_id = a.accommodation_id
WHERE a.name = '전주 비지니스 호텔 궁'
GROUP BY k.keyword_text
ORDER BY total_score DESC
LIMIT 5;


-- 키워드로 숙소 리스트 조회
-- distinct : 동일한 키워드를 가진 숙소 중복제거
SELECT DISTINCT a.*
FROM accommodations a
-- 숙소와 리뷰 테이블 연결
JOIN review r ON a.accommodation_id = r.accommodation_id
-- 리뷰테이블과 키워드 테이블 연결
JOIN keywords k ON r.review_id = k.review_id
-- 키워드가 OO일때
WHERE k.keyword_text = '담배냄새'
-- 숙소리스트를 평점순으로 내림차순
ORDER BY a.rating DESC;


-- 숙소별 리포트 테이블의 내용, 이미지 조회
select * , (select positive_img from report r where r.accommodation_id = a.accommodation_id) as p_img,
 (select negative_img from report r where r.accommodation_id = a.accommodation_id) as n_img,
 (select report_text from report r where r.accommodation_id = a.accommodation_id) as report_text
 from accommodations a where a.name = '전주 중앙동 라온 호텔';

-- 여러 리포트
SELECT 
    a.*, 
    r.positive_img AS p_img,
    r.negative_img AS n_img,
    r.report_text
FROM accommodations a
JOIN report r ON r.accommodation_id = a.accommodation_id
WHERE a.name = '전주 중화산동 호텔 인트로(HOTEL INTRO)';

-- 리포트 내용을 하나의 문자열
-- 리포트 조회 수정수정수정!!
SELECT a.*,
    (SELECT r.positive_img FROM report r WHERE r.source_id IN 
    (SELECT source_id FROM accom_source WHERE accommodation_id = a.accommodation_id) limit 1) as p_img,
    
    (SELECT r.negative_img FROM report r WHERE r.source_id IN 
    (SELECT source_id FROM accom_source WHERE accommodation_id = a.accommodation_id) limit 1) as n_img,
    GROUP_CONCAT(DISTINCT r.report_text order by s.source desc SEPARATOR '\n\n') AS report_text
FROM accommodations a
JOIN accom_source s ON a.accommodation_id = s.accommodation_id
JOIN report r ON s.source_id = r.source_id
WHERE a.name = '전주 산정동 호텔 감스테이'
GROUP BY a.accommodation_id;


-- 수정 버전
SELECT a.*,
    (SELECT r.positive_img FROM report r WHERE r.source_id IN 
    (SELECT source_id FROM accom_source WHERE accommodation_id = a.accommodation_id) limit 1) as p_img,
    
    (SELECT r.negative_img FROM report r WHERE r.source_id IN 
    (SELECT source_id FROM accom_source WHERE accommodation_id = a.accommodation_id) limit 1) as n_img,
    GROUP_CONCAT(DISTINCT CONCAT('출처: ', s.source, '\n', r.report_text) SEPARATOR '\n\n'
    ) AS report_text
FROM accommodations a
JOIN accom_source s ON a.accommodation_id = s.accommodation_id
JOIN report r ON s.source_id = r.source_id
WHERE a.name = '전주 신시가지 호텔 팝'
GROUP BY a.accommodation_id;


-- 워드클라우드 제외
SELECT a.*,
    GROUP_CONCAT(DISTINCT CONCAT('출처: ', s.source, '\n', r.report_text) SEPARATOR '\n\n') AS report_text
FROM accommodations a
JOIN accom_source s ON a.accommodation_id = s.accommodation_id
JOIN report r ON s.source_id = r.source_id
WHERE a.name = '전주 신시가지 호텔 팝'
GROUP BY a.accommodation_id;



-- 숙소별 리뷰 조회하는 쿼리
-- 날짜 최신순
SELECT 
    a.name,
    r.content,
    r.write_date,
    r.review_rating,
    r.review_source,
    r.review_type,
    r.nickname
FROM accommodations a
JOIN review r ON a.accommodation_id = r.accommodation_id
WHERE a.name = '전주 궁호텔'
ORDER BY r.write_date DESC;



SELECT 
a.name,
	r.content,
	r.write_date,
	r.review_rating,
	r.review_source,
	r.review_type,
	r.nickname
FROM accommodations a
join accom_source s on a.accommodation_id = s.accommodation_id
JOIN review r ON s.source_id = r.source_id
WHERE a.name = '전주 중앙동 라온 호텔'
ORDER BY r.write_date DESC;

