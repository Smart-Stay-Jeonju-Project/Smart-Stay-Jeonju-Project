// result.html에 단일 마커

function initMap() {
    const accommodation = window.accommodation;
    // 숙소 정보 확인
    if (!accommodation) {
        console.error("accommodation 정보가 없습니다.");
        return;
    }

    // 페이지에는 accommodation.lat&accommodation.lat이 출력되는데 콘솔에는 오류가 발생하면 Number로 지정
    const lat = accommodation.lat;
    const lng = accommodation.lng;
    // const lat = Number(accommodation.lat);
    // const lng = Number(accommodation.lng);

    // lat 과 lng 확인
    if (isNaN(lat) || isNaN(lng)) {
        console.error("유효하지 않은 위도/경도 값입니다.", accommodation.lat, accommodation.lng);
        return;
    }

    // map_in_result 가 있는지 확인
    const mapDiv = document.getElementById("map_in_result");
    if (!mapDiv) {
        console.error("#map_in_result 요소를 찾을 수 없습니다.");
        return;
    }

    // 지도 생성과 중심 좌표
    const map = new google.maps.Map(mapDiv, {
        center : { lat : lat, lng : lng },
        zoom : 16.8,
    });

    // 지도에 마커 
    new google.maps.Marker({
        position : { lat : lat, lng : lng },
        map : map,
        title : accommodation.name || "숙소 위치"
    });
}

window.initMap = initMap;
