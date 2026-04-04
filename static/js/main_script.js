document.getElementById('clickBtn').addEventListener('click', function() {
  fetch('/click', {
    method: 'GET'
  })
  .then(response => response.text())
  .then(data => {
    document.getElementById('score').innerText = 'Счёт: ' + data;
  })
  .catch(error => {
    console.error('Ошибка при отправке запроса:', error);
  });
});