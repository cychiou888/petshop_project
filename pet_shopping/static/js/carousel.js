document.addEventListener("DOMContentLoaded", () => {
  let currentIndex = 0;
  const slides = document.querySelectorAll(".carousel-container .slide");
  const container = document.querySelector(".carousel-container");
  const totalSlides = slides.length;

  function showSlide(index) {
   
      if (index < 0) {
          currentIndex = totalSlides - 1;
      } else if (index >= totalSlides) {
          currentIndex = 0;
      } else {
          currentIndex = index;
      }


      const width = container.parentElement.offsetWidth;
      container.style.transform = `translateX(-${currentIndex * width}px)`;

 
      slides.forEach((slide, i) => {
          slide.classList.toggle("active", i === currentIndex);
      });
  }

  function nextSlide() {
      showSlide(currentIndex + 1);
  }

  function prevSlide() {
      showSlide(currentIndex - 1);
  }


  setInterval(() => {
      nextSlide();
  }, 8000);

  document.querySelector(".carousel-controls .next").addEventListener("click", nextSlide);
  document.querySelector(".carousel-controls .prev").addEventListener("click", prevSlide);


  showSlide(0);
});
