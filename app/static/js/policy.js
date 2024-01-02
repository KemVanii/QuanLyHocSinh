document.addEventListener("DOMContentLoaded", function() {
    fetch('static/policies.json')  // Đường dẫn đến file JSON
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const jsonData = data;

            // Gán dữ liệu từ jsonData vào các ô textbox tương ứng
            document.getElementById("classSizeNum").value = jsonData.max_class_size;
            document.getElementById("ageRange1").value = jsonData.age_min;
            document.getElementById("ageRangeNum1").value = jsonData.age_min;
            document.getElementById("ageRange2").value = jsonData.age_max;
            document.getElementById("ageRangeNum2").value = jsonData.age_max;
            // Gán dữ liệu cho các ô textbox khác nếu cần
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
});

function modifyPolicies() {
    let max_class_size = document.getElementById("classSizeNum").value
    let age_min = document.getElementById("ageRange1").value
    let age_max = document.getElementById("ageRange2").value

    fetch('/api/policy', {
        method: 'post',
        body: JSON.stringify({
            "max_class_size": max_class_size,
            "age_min": age_min,
            "age_max": age_max
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    });

    informApplied()
}

function informApplied() {
    // Create a new div element
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-info alert-dismissible fade show'; // Set Bootstrap alert classes
  alertDiv.setAttribute('role', 'alert');
  alertDiv.textContent = 'Đã chỉnh sửa thông tin thành công!! :>>'; // Set alert message

  // Create a close button for the alert
  const closeButton = document.createElement('button');
  closeButton.type = 'button';
  closeButton.className = 'btn-close';
  closeButton.setAttribute('data-bs-dismiss', 'alert');
  closeButton.setAttribute('aria-label', 'Close');
  alertDiv.appendChild(closeButton); // Append the close button to the alert

  // Display the alert in the document
  const alertContainer = document.getElementById('alertContainer');
  alertContainer.appendChild(alertDiv);
}

function updateRangeValue(obj) {
    const textbox = document.getElementById("ageRangeNum" + obj.id[obj.id.length - 1]);
    textbox.value = obj.value;
}

