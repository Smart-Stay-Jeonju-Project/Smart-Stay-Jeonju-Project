// 검색타입을 키워드로 눌렀을 때

// 이벤트 리스너
document.addEventListener("DOMContentLoaded", function () {
    // 키워드 목록 표시 ox
    const searchTypeSelect = document.getElementById("search_type");
    const keywordListDiv = document.getElementById("keywordList");
    // 검색타입 키워드와 키워드 리스트 존재 시
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

    // 키워드 초기화 기능
    const resetBtn = document.getElementById("resetKeyword");
    const keywordUl = document.getElementById("keywordUl");
    const selectedKeyword = window.searchTerm; 

    // 선택된 키워드가 있으면 그것만 먼저 출력
    if (keywordUl && selectedKeyword) {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${selectedKeyword}</strong>`;
        keywordUl.appendChild(li);  // 새 자식 요소 추가
    }

    // 초기화 버튼 클릭 시 전체 키워드 다시 렌더링 (중복 없이)
    if (resetBtn && window.allKeywords && keywordUl) {
        resetBtn.addEventListener("click", function (e) {
            e.preventDefault(); // 기본 동작(페이지 새로고침) 방지

            keywordUl.innerHTML = ""; // 기존 키워드 목록 초기화

            // 모든 키워드를 목록에 추가
            window.allKeywords.forEach(keyword => {
                if (keyword === selectedKeyword) {
                    return;
                }
                const li = document.createElement("li");
                const a = document.createElement("a");
                a.href = `/search?search_type=keyword&search_term=${keyword}`;
                a.textContent = keyword;
                li.appendChild(a);
                keywordUl.appendChild(li);
            });
        });
    }
});