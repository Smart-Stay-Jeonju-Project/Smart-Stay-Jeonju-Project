INSERT INTO accommodations (name, category, address, rating, image, feature, latitude, longitude)
SELECT
    -- 상호명: n 우선, 없으면 y
    COALESCE(MAX(CASE WHEN source = 'n' THEN source_name END),
             MAX(CASE WHEN source = 'y' THEN source_name END)) AS name,

    -- 카테고리: n 우선, 없으면 y
    COALESCE(MAX(CASE WHEN source = 'n' THEN source_category END),
             MAX(CASE WHEN source = 'y' THEN source_category END)) AS category,

    -- 주소 (묶는 기준)
    s.source_addr AS address,

    -- 평점: 평균값 사용 (n, y 둘 다 있을 경우)
    AVG(s.source_rating) AS rating,

    -- 이미지: n 우선, 없으면 y
    COALESCE(MAX(CASE WHEN source = 'n' THEN source_image END),
             MAX(CASE WHEN source = 'y' THEN source_image END)) AS image,

    -- 특징: n 우선, 없으면 y
    COALESCE(MAX(CASE WHEN source = 'n' THEN source_feature END),
             MAX(CASE WHEN source = 'y' THEN source_feature END)) AS feature,

    -- 위도: n 우선, 없으면 y
    COALESCE(MAX(CASE WHEN source = 'n' THEN latitude END),
             MAX(CASE WHEN source = 'y' THEN latitude END)) AS latitude,

    -- 경도: n 우선, 없으면 y
    COALESCE(MAX(CASE WHEN source = 'n' THEN longitude END),
             MAX(CASE WHEN source = 'y' THEN longitude END)) AS longtitude

FROM accom_source s
GROUP BY s.source_addr;



-- accom_source 테이블에 accommodations 테이블 주소 매칭하여 id 주가

UPDATE accom_source s
JOIN accommodations a
  ON s.source_addr = a.address
SET s.accommodation_id = a.accommodation_id;
