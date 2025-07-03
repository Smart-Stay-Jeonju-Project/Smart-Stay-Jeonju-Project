// search.html 에서 다중 마커 지도 표시

// 다중마커
function initMap () {
    // accommodations 객체에서 새로운 속성들을 받아오도록 구조 분해 할당을 수정합니다.
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

    accommodations.forEach(({ name, address, lat, lng, image_url, rating_score, rating_count }) => {
        // console.log("현재 숙소 정보 (평점 포함): ", { name, address, lat, lng, image_url, 
        // rating_score, rating_count });

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

            // 정보창 content에 평점과 리뷰 수를 추가합니다.
            const content = `
                <div style="max-width: 200px;">
                    <a href="/result?name=${encodeURIComponent(name)}" style="text-decoration: none; color: black;">
                        <img src="${image_url}" alt="${name}" style="width: 100%; height: auto; border-radius: 8px;">
                        <p><strong>${name}</strong>⭐${rating_score} (${rating_count})
                        <br>${address}</p>
                    </a>
                </div>
            `;
            infowindow.setContent(content);
            infowindow.open({
                anchor: marker,
                map,
            });
        });
    });
    // (3.객체의 fitbounds 메소드에 지도 경계 객체 넘김)
    map.fitBounds(bounds);
};