// search.html 에서 다중 마커 지도 표시

// 다중마커
function initMap () {
    const accommodations = window.accommodations || [];
    const map = new google.maps.Map(document.getElementById("map"), {
        // 전주시 중심 좌표
        center: { lat: 35.85, lng: 127.13 }, 
        // 지도 확대 크기 
        zoom: 13,
    });

    // (1.지도 경계를 조정)
    const bounds = new google.maps.LatLngBounds();
    // (ㄱ.클릭시 정보 제공)
    const infowindow = new google.maps.InfoWindow();

    accommodations.forEach(({ name, address, lat, lng }) => {
        const marker = new google.maps.Marker({
            position : { lat, lng },
            map,
        });
        // (2.extend 메소드를 호출해서 위치정보 넘김)
        bounds.extend(marker.position);
        // (ㄴ.클릭이벤트시 정보창 제공)
        marker.addListener("click", () => {
            // 마커 클릭시 지도 중심 이동
            map.panTo(marker.position);
            // JavaScript에서 템플릿 문자열을 만드는 문법
            infowindow.setContent(`<strong>${name}</strong><br><strong>${address}</strong>`);
            infowindow.open({
                anchor: marker,
                map,
            });
        });
    });
    // (3.객체의 fitbounds 메소드에 지도 경계 객체 넘김)
    map.fitBounds(bounds);
};