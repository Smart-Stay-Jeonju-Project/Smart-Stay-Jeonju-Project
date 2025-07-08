// search.html 에서 다중 마커 지도 표시

function initMap () {
    // (1. 전체 숙소 데이터 받아오기)
    const accommodations = window.accommodations || [];

    // (2. 구글 맵 생성 및 중심 좌표 설정)
    const map = new google.maps.Map(document.getElementById("map_in_search"), {
        center: { lat: 35.85, lng: 127.13 }, // 전주시 중심
        zoom: 13,                            // 초기 확대 정도
    });

    // (3. 지도 경계 객체 생성 → 모든 마커 범위 맞춤용)
    const bounds = new google.maps.LatLngBounds();

    // (4. InfoWindow 객체 생성 → 마커 클릭 시 정보창)
    const infowindow = new google.maps.InfoWindow();

    // (5. 숙소 리스트 컨테이너 초기화)
    const listContainer = document.getElementById("accommodation-list");
    listContainer.innerHTML = "";

    // (6. InfoWindow에 들어갈 HTML content 생성 함수)
    function generateInfoContent({ name, address, image_url, rating_score, rating_count }) {
        return `
            <div style="max-width: 250px;">
                <a href="/result?name=${encodeURIComponent(name)}" 
                style="text-decoration: none; color: black; outline: none; border: none; ">
                    <img src="${image_url}" alt="${name}" style="width: 100%; border-radius: 6px;">
                    <h4 style="margin: 8px 0 4px 0;">${name}</h4>
                    <p>⭐ ${rating_score} (${rating_count})<br>${address}</p>
                </a>
            </div>
        `;
    }

    // (7. 숙소 리스트 순회하며 마커 및 리스트 항목 생성)
    accommodations.forEach(({ name, address, lat, lng, image_url, rating_score, rating_count }) => {
        // (7-1. 지도에 마커 추가)
        const marker = new google.maps.Marker({
            position: { lat, lng },
            map,
        });

        // (7-2. 지도 범위에 현재 마커 포함시키기)
        bounds.extend(marker.position);

        // (7-3. 마커 클릭 시 InfoWindow 열기)
        marker.addListener("click", () => {
            const content = generateInfoContent({ name, address, image_url, rating_score, rating_count });
            infowindow.setContent(content);
            infowindow.open(map, marker);
        });

        // (7-4. 좌측 리스트 항목 구성)
        const card = document.createElement("div");
        card.className = "accommodation-card";
        card.innerHTML = `
            <img src="${image_url}" alt="${name}">
            <div class="text-content">
                <h4>${name}</h4>
                <p>⭐ ${rating_score} (${rating_count})</p>
                <p>${address}</p>
            </div>
        `;

        // (7-5. 리스트 클릭 시 해당 마커로 이동 + InfoWindow 열기)
        card.addEventListener("click", () => {
            map.panTo({ lat, lng });
            map.setZoom(15);
            const content = generateInfoContent({ name, address, image_url, rating_score, rating_count });
            infowindow.setContent(content);
            infowindow.open(map, marker);
        });

        // (7-6. 리스트에 카드 추가)
        listContainer.appendChild(card);
    });

    // (8. 전체 마커가 화면에 보이도록 자동 확대/이동)
    map.fitBounds(bounds);
}
