// 슬라이더

document.addEventListener("DOMContentLoaded", function () {
    let currentSlide = 0;   
    const slidesToShow = 4; // 보여줄 슬라이드 개수

    const sliderTrack = document.getElementById("slider_track");        // 전체 카드들
    const sliderCards = document.querySelectorAll(".slider_card");      // 각 개체의 카드들
    const slideWidth = sliderCards[0].offsetWidth;                      // 각 카드 너비
    const totalSlides = sliderCards.length;                             // 총 슬라이드 개수
    const cardGap = 20;
    const sliderStep = slideWidth + cardGap;

    // 다음 버튼이랑 이전버튼
    const nextBtn = document.getElementById("next_btn");
    const prevBtn = document.getElementById("prev_btn");

    // 버튼 활성/비활성 상태 갱신 함수
    function updateButtons() {
        prevBtn.disabled = currentSlide <= 0;                            // 첫 슬라이드 일때는 이전버튼 비활성화
        nextBtn.disabled = (currentSlide + slidesToShow) >= totalSlides; // 다음 슬라이드로 못넘길때 다음버튼 비활성화
    }

    // 다음버튼 클릭 시 이벤트리스너
    nextBtn.addEventListener("click", () => {
        // 현재 + 보여지는 것까지 < 마지막
        if ((currentSlide + slidesToShow) < totalSlides) {
            currentSlide++;
            // 슬라이더 트랙을 왼쪽으로 이동시켜 슬라이드 효과
            sliderTrack.style.transform = `translateX(-${sliderStep * currentSlide}px)`; 
            updateButtons();
        }
    });

    // 이전버튼 클릭 시 이벤트리스너
    prevBtn.addEventListener("click", () => {
        if (currentSlide > 0) {
            currentSlide--;
            sliderTrack.style.transform = `translateX(-${sliderStep * currentSlide}px)`;
            updateButtons();
        }
    });

    
    updateButtons();
});
