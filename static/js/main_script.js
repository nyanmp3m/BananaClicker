document.getElementById('bananaImg').addEventListener('click', () => {
  fetch('/click', { method: 'GET' })
    .then(response => response.text())
    .then(data => {
      document.getElementById('score').innerText = 'Счёт: ' + data;

      const miniBanana = document.createElement('img');
      miniBanana.src = 'https://www.nicepng.com/png/full/769-7690159_-banana-8-8-8bit-picsart.png';
      miniBanana.className = 'mini-banana';

      const windowWidth = window.innerWidth;
      const min = 140;
      const max = windowWidth - 220;
      
      const randomX = Math.floor(Math.random() * (max - min + 1)) + min;

      const rect = document.getElementById('bananaImg').getBoundingClientRect();
      miniBanana.style.left = randomX + "px";
      miniBanana.style.top = "0px";

      document.body.appendChild(miniBanana);

      // Выводим начальные координаты
      const startRect = miniBanana.getBoundingClientRect();
      console.log('Начальные координаты мини-банана:', startRect.left, startRect.top);

      requestAnimationFrame(() => {
        miniBanana.style.transform = 'translateY(600px)';
        miniBanana.style.opacity = '0';

        // Можно вывести координаты во время падения, например, через setInterval
        const intervalId = setInterval(() => {
          const rectDuringFall = miniBanana.getBoundingClientRect();
          console.log('Координаты во время падения:', rectDuringFall.left, rectDuringFall.top);
        }, 200);

        miniBanana.addEventListener('transitionend', () => {
          clearInterval(intervalId);
          miniBanana.remove();
        });
      });
    })
    .catch(error => {
      console.error('Ошибка при отправке запроса:', error);
    });
});