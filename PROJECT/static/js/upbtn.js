// 맨 위로 이동 버튼
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 맨 위로 버튼 객체
const scrollBtn = document.getElementById("scrollTopBtn");

if (scrollBtn) {
    // 스크롤 시 버튼 보이기
    window.addEventListener("scroll", function () {
        if (window.scrollY > 300) {
            scrollBtn.style.display = "block";
        } else {
            scrollBtn.style.display = "none";
        }
    });

    // 클릭 시 맨 위로 이동
    scrollBtn.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}