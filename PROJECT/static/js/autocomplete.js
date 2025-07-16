// 자동 완성 검색기능

document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('search_term');
    const typeSelect = document.getElementById('search_type');

    // 자동완성 결과를 보여줄 <ul> 요소를 생성하고, input의 부모 요소에 추가
    const wrapper = input.closest('.autocomplete_wrapper');
    const suggestionBox = document.createElement('ul');
    suggestionBox.classList.add('autocomplete_box');    // 스타일 위한 클래스 지정
    input.parentNode.appendChild(suggestionBox);    // input 아래에 자동완성 기능 붙이기

    // 사용자가 입력창을 입력할 때마다
    input.addEventListener('input', async () => {
        const query = input.value.trim();
        if (!query || typeSelect.value !== 'name') {  // 검색타입 상호명이 아니면
            suggestionBox.innerHTML = '';
            suggestionBox.style.display = 'none';  // 숨기기
            return;
        }

        // 서버에 자동완성 요청 보내기
        const response = await fetch(`/autocomplete?search_type=name&term=${encodeURIComponent(query)}`);
        const suggestions = await response.json();

        suggestionBox.innerHTML = ''; // 이전 추천어 초기화
        if (suggestions.length > 0) {
            // 추천어가 있을 경우 각각 <li>로 만들어서 박스에 추가
            suggestions.forEach(name => {
                const li = document.createElement('li');
                li.textContent = name;
                li.classList.add('autocomplete_item');
                // 추천어 클릭 시 해당 검색어로 검색 결과 페이지로 이동
                li.addEventListener('click', () => {
                    window.location.href = `/search?search_type=name&search_term=${encodeURIComponent(name)}`;
                });
                suggestionBox.appendChild(li);
            });
            suggestionBox.style.display = 'block'; // 검색 결과 있으면 보이기
        } else {
            suggestionBox.style.display = 'none'; // 결과 없으면 숨김
        }
    });

    // 페이지 아무 곳이나 클릭했을 때 자동완성 박스 외부 클릭이면 숨기기
    document.addEventListener('click', (e) => {
        if (!suggestionBox.contains(e.target) && e.target !== input) {
            suggestionBox.innerHTML = '';
            suggestionBox.style.display = 'none';  // 외부 클릭 시 숨기기
        }
    });
});
