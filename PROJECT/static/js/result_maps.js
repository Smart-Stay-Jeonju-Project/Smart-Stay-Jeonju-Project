// 단일 마커 (손 더 봐야함)
function initMap() {
    // 좌표 설정
    const myLatLng = {
        lat: 35.85, 
        lng: 127.13
    };

    // 지정한 좌표에 중심 설정
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom : 13,
        center : myLatLng
    });

    // 원하는 위치에 마커 설정
    new google.maps.Marker({
        position : myLatLng,
        map,
    });
}
