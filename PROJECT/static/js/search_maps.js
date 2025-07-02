// 다중마커
window.initMap = function () {
    const map = new google.maps.Map(document.getElementById("map"), {
        // 전주시 중심 좌표
        center: { lat: 35.85, lng: 127.13 }, 
        // 지도 확대 크기 
        zoom: 13,
    });
    
    // 연습용 
    const accommodations = [
    { label: "C", name: "칼튼힐호텔", lat: 35.834734, lng: 127.134790 },
    { label: "H", name: "행복한추억", lat: 35.823974, lng: 127.146443 },
    { label: "B", name: "블랙스톤모텔", lat: 35.846754, lng: 127.155371 },
    { label: "Y", name: "와이케이호텔", lat: 35.844242, lng: 127.125354 },
    ];

    // (1.지도 경계를 조정)
    const bounds = new google.maps.LatLngBounds();
    // (ㄱ.클릭시 정보 제공)
    const infowindow = new google.maps.InfoWindow();
    // 주소 정보를 좌표 정보로 변환
    const geocoder = new google.maps.Geocoder();

    accommodations.forEach(({ label, name, lat, lng }) => {
        const marker = new google.maps.Marker({
            position: { lat, lng },
            label,
            map,
        });
        // (2.extend 메소드를 호출해서 위치정보 넘김)
        bounds.extend(marker.position);
        // (ㄴ.클릭이벤트시 정보창 제공)
        marker.addListener("click", () => {
            // 마커 클릭시 지도 중심 이동
            map.panTo(marker.position);
            infowindow.setContent(name);
            infowindow.open({
                anchor: marker,
                map,
            });
        });
    });
    // (3.객체의 fitbounds 메소드에 지도 경계 객체 넘김)
    map.fitBounds(bounds);
};

// 숙소상세정보(중복제거).csv
// 구글 드라이브에서 스프레드 시트로
// 확장 프로그램
// 부가기능 설치하기
// geocode 설치 후 실행
// 데이터량에 따라 요금발생