// 다중마커
window.initMap = function () {
    const map = new google.maps.Map(document.getElementById("map"), {
        // 전주시 중심 좌표
        center: { lat: 35.85, lng: 127.13 }, 
        // 지도 확대 크기 
        zoom: 13,
    });
    // 마커로 위치 표시할 구역 지정
    const acommodation = [
    { label: "C", name: "칼튼힐호텔", lat: 35.834734, lng: 127.134790,  },
    { label: "H", name: "행복한추억", lat: 35.823974, lng: 127.146443 },
    { label: "B", name: "블랙스톤모텔", lat: 35.846754, lng: 127.155371 },
    { label: "Y", name: "와이케이호텔", lat: 35.844242, lng: 127.125354 },
    ];

    // (1.지도 경계를 조정)
    const bounds = new google.maps.LatLngBounds();
    // (ㄱ.클릭시 정보 제공)
    const infowindow = new google.maps.InfoWindow();

    acommodation.forEach(({ label, name, lat, lng }) => {
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

// // 단일 마커 (손 더 봐야함)
// function initMap() {
//     // 좌표 설정
//     const myLatLng = {
//         lat: 35.85, 
//         lng: 127.13
//     };
//     // // 숙소 정보 DB에서 가져오기
//     // const acommodation =

//     // 지정한 좌표에 중심 설정
//     const map = new google.maps.Map(document.getElementById("map"), {
//         zoom : 13,
//         center : myLatLng
//     });

//     // 원하는 위치에 마커 설정
//     new google.maps.Marker({
//         position : myLatLng,
//         map,
//     });
// }
