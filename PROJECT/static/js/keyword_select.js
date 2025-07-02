// 검색 타입을 키워드로 눌렀을 때

document.addEventListener("DOMContentLoaded", function () {
    const searchTypeSelect = document.getElementById("search_type");
    const keywordListDiv = document.getElementById("keywordList");

    if (searchTypeSelect && keywordListDiv) {
        function toggleKeywordList() {
            if (searchTypeSelect.value === "keyword") {
                keywordListDiv.style.display = "block";
            } else {
                keywordListDiv.style.display = "none";
            }
        }
        searchTypeSelect.addEventListener("change", toggleKeywordList);
        toggleKeywordList();  
    }
});
