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
 from accommodations a where a.name = '전주 비지니스 호텔 궁';



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
WHERE a.name = '전주 비지니스 호텔 궁'
ORDER BY r.write_date DESC;

