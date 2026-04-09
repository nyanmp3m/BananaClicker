document.getElementById('bananaImg').addEventListener('click', () => {
  fetch('/click', { method: 'GET' })
    .then(response => response.text())
    .then(data => {
      document.getElementById('score').innerText = 'Бананчики: ' + data;

      const bananaImagePath = document.body.dataset.bananaImage;

      const miniBanana = document.createElement('img');
      miniBanana.src = bananaImagePath;
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

      requestAnimationFrame(() => {
        miniBanana.style.transform = 'translateY(600px)';
        miniBanana.style.opacity = '0';

        const intervalId = setInterval(() => {
          const rectDuringFall = miniBanana.getBoundingClientRect();
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
setInterval(function() {
    const bananaImagePath = document.body.dataset.superCatImage;

    const miniBanana = document.createElement('img');
    miniBanana.src = bananaImagePath;
    miniBanana.className = 'mini-banana-super';

    miniBanana.style.cursor = 'pointer';

    miniBanana.addEventListener('click', () => {
        fetch('/super_banana_click')
            .then(response => response.json())
            .then(data => {
                document.getElementById('score').innerText = "Бананчики: " + data.score;
                miniBanana.remove();
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
    });

    const windowWidth = window.innerWidth;
    const min = 140;
    const max = windowWidth - 220;

    const randomX = Math.floor(Math.random() * (max - min + 1)) + min;

    const rect = document.getElementById('bananaImg').getBoundingClientRect();
    miniBanana.style.left = randomX + "px";
    miniBanana.style.top = "0px";

    document.body.appendChild(miniBanana);

    const startRect = miniBanana.getBoundingClientRect();

    requestAnimationFrame(() => {
        miniBanana.style.transform = 'translateY(600px)';
        miniBanana.style.opacity = '0';

        const intervalId = setInterval(() => {
            const rectDuringFall = miniBanana.getBoundingClientRect();
        }, 200);

        miniBanana.addEventListener('transitionend', () => {
            clearInterval(intervalId);
            miniBanana.remove();
        });
    });
}, 30000)

document.getElementById('first-item').addEventListener('click', () => {
    fetch('/buy_first_item', { method: 'GET' })
        .then (response => response.json())
        .then (data => {
            document.getElementById('first-item-priceNum').innerText = data.newPrice;
            if (data.score >= 0) {
                document.getElementById('first-item-label').innerText = data.firstItem_count;
                document.getElementById('score').innerText = 'Бананчики: ' + data.score;
            } else {
                document.getElementById('score').innerText = "Ты нищита";
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
});
document.getElementById('second-item').addEventListener('click', () => {
    fetch('/buy_second_item', { method: 'GET' })
        .then (response => response.json())
        .then (data => {
            document.getElementById('second-item-priceNum').innerText = data.newPrice;
            if (data.score >= 0) {
                document.getElementById('second-item-label').innerText = data.secondItem_count;
                document.getElementById('score').innerText = 'Бананчики: ' + data.score;
            } else {
                document.getElementById('score').innerText = "Ты нищита";
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
});
document.getElementById('third-item').addEventListener('click', () => {
    fetch('/buy_third_item', { method: 'GET' })
        .then (response => response.json())
        .then (data => {
            document.getElementById('third-item-priceNum').innerText = data.newPrice;
            if (data.score >= 0) {
                document.getElementById('third-item-label').innerText = data.thirdItem_count;
                document.getElementById('score').innerText = 'Бананчики: ' + data.score;
            } else {
                document.getElementById('score').innerText = "Ты нищита";
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
});

document.getElementById('fourth-item').addEventListener('click', () => {
    fetch('/buy_fourth_item', { method: 'GET' })
        .then (response => response.json())
        .then (data => {
            document.getElementById('fourth-item-priceNum').innerText = data.newPrice;
            if (data.score >= 0) {
                document.getElementById('fourth-item-label').innerText = data.fourthItem_count;
                document.getElementById('score').innerText = 'Бананчики: ' + data.score;
            } else {
                document.getElementById('score').innerText = "Ты нищита";
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
});


setInterval(function() {
    fetch('/auto_click')
        .then(response => response.json())
        .then(data => {
            if (data.score >= 0) {
                document.getElementById('score').innerText = "Бананчики: " + data.score;
            }
        });
}, 850);