// 검색타입을 주소로 눌렀을 때

// 이벤트 리스너
document.addEventListener("DOMContentLoaded", function () {
    const searchTypeSelect = document.getElementById("search_type"); // 검색타입 주소
    const searchTermInput = document.getElementById("search_term");  // 검색어
    const addressHint = document.getElementById("addressHint");      // 힌트 : 덕진구/완산구

    // 검색 선택했을때 보이고 그 외는 안보이는
    function toggleSearchOptions() {
        const selectedType = searchTypeSelect.value;

        // 문장 검색 시 검색창 숨김
        if (searchTermInput) {
            if (selectedType === "sentence") {
                searchTermInput.style.display = "none";
            } else {
                searchTermInput.style.display = "block";
            }
        }
        // 주소 검색 시 보임
        if (addressHint) {
            if (selectedType === "address") {
                addressHint.style.display = "block";
            } else {
                addressHint.style.display = "none";
            }
        }
    }
    // search_type이 있을때 toggle 함수 불러옴
    if (searchTypeSelect) {
        searchTypeSelect.addEventListener("change", toggleSearchOptions);
        toggleSearchOptions();  // 초기 상태 설정
    } else {
        console.warn("search_type 요소를 찾을 수 없습니다.");
    }
});
