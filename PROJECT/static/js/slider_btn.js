document.addEventListener("DOMContentLoaded", function () {
    let currentSlide = 0;
    const slidesToShow = 4;

    const sliderTrack = document.getElementById("slider_track");
    const sliderCards = document.querySelectorAll(".slider_card");
    const slideWidth = sliderCards[0].offsetWidth;
    const totalSlides = sliderCards.length;

    const nextBtn = document.getElementById("next_btn");
    const prevBtn = document.getElementById("prev_btn");

    function updateButtons() {
        prevBtn.disabled = currentSlide <= 0;
        nextBtn.disabled = (currentSlide + slidesToShow) >= totalSlides;
    }

    nextBtn.addEventListener("click", () => {
        if ((currentSlide + slidesToShow) < totalSlides) {
            currentSlide++;
            sliderTrack.style.transform = `translateX(-${slideWidth * currentSlide}px)`;
            updateButtons();
        }
    });

    prevBtn.addEventListener("click", () => {
        if (currentSlide > 0) {
            currentSlide--;
            sliderTrack.style.transform = `translateX(-${slideWidth * currentSlide}px)`;
            updateButtons();
        }
    });

    // ✅ 초기 버튼 상태 설정
    updateButtons();
});
