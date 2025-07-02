// 검색타입을 주소로 눌렀을 때

document.addEventListener("DOMContentLoaded", function () {
    const searchTypeSelect = document.getElementById("search_type");
    const searchTermInput = document.getElementById("search_term");
    const addressHint = document.getElementById("addressHint");

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
        // 주소 검색 시 안내 문구 보이기
        if (addressHint) {
            if (selectedType === "address") {
                addressHint.style.display = "block";
            } else {
                addressHint.style.display = "none";
            }
        }
    }
    
    if (searchTypeSelect) {
        searchTypeSelect.addEventListener("change", toggleSearchOptions);
        toggleSearchOptions();  // 초기 상태 설정
    } else {
        console.warn("search_type 요소를 찾을 수 없습니다.");
    }
});
