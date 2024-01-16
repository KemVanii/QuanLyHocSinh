const btnSendMail = document.querySelector('#btnSendMail');
const btnLoadSendMail = document.querySelector('#btnLoadSendMail');
btnSendMail.addEventListener('click', async function () {
  const userConfirmed = confirm('Xác nhận gửi?');
  if (userConfirmed) {
    btnSendMail.classList.toggle('d-none');
    btnLoadSendMail.classList.toggle('d-none');
    const idLop = document.querySelector('#inputIdLop').value;
    const hk = document.querySelector('#inputIdHocKy').value;
    const formData = new FormData();
    formData.append('idLop', idLop);
    formData.append('hk', hk);
    try {
      await fetch('/api/sendMail', {
        method: 'POST',
        body: formData,
      });

      btnSendMail.classList.toggle('d-none');
      btnLoadSendMail.classList.toggle('d-none');
      alert('Gửi email thành công!');
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      alert('Error submitting the form. Please try again.');
    }
  }
})