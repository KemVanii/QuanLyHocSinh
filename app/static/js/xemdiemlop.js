const btnSendMail = document.querySelector('#btnSendMail');

btnSendMail.addEventListener('click', async function () {
  const userConfirmed = confirm('Xác nhận gửi?');
  if (userConfirmed) {
    const idLop = document.querySelector('#inputIdLop').value;
    const hk = document.querySelector('#inputIdHocKy').value;
    const formData = new FormData();
    formData.append('idLop', idLop);
    formData.append('hk', hk);
    try {
      const response = await fetch('/api/sendMail', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log(data);

      alert('Gửi email thành công!');
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      alert('Error submitting the form. Please try again.');
    }
  }
})