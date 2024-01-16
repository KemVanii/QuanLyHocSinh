let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

window.onload = function() {
      const ctx = document.getElementById('myChart');

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: '# Số lượng điểm',
            data: data,
            borderWidth: 1,
            backgroundColor: ['lightBlue', 'lightGreen', 'blue', 'gold', 'brown', 'lightPink']
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            title: {
                display: true,
                text: 'Biểu đồ biểu thị số lượng con điểm'
            }
          }
        }
      });

      const ctx2 = document.getElementById('myChart2');

      new Chart(ctx2, {
        type: 'pie',
        data: {
          labels: tLabels,
          datasets: [{
            label: '# Xếp loại điểm',
            data: tData,
            borderWidth: 1,
            backgroundColor: ['lightBlue', 'lightGreen', 'blue', 'gold', 'brown', 'lightPink']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          aspectRatio: 1,

          scales: {
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            title: {
                display: true,
                text: 'Biểu đồ biểu thị tỉ lệ xếp loại'
            }
          }
        }
      });
    }

function filterTable() {
        var selectedOption = document.getElementById('filterType').value;
        var secondDropdownContainer = document.getElementById('classroomPie');
        var thirdDropdownContainer = document.getElementById('gradePie');

        secondDropdownContainer.style.display = 'none';
        thirdDropdownContainer.style.display = 'none';

        // Hiển thị hoặc ẩn dropdown thứ hai dựa trên giá trị được chọn
        if (selectedOption === 'lop') {
            secondDropdownContainer.style.display = 'block';
        } else if (selectedOption === 'khoi') {
            thirdDropdownContainer.style.display = 'block';
        }

        // Thực hiện các thay đổi khác tương ứng với việc chọn giá trị
        // Ví dụ: Có thể thực hiện logic khác tùy thuộc vào giá trị được chọn
    }