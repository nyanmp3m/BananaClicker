let count = 0;
const btn = document.getElementById('clickBtn');
const scoreDiv = document.getElementById('score');

btn.addEventListener('click', () => {
    count++;
scoreDiv.textContent = 'Счёт: ' + count;
});