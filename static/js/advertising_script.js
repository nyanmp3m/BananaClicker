class AdPopup {
        constructor(options = {}) {
        const options = [
            '🎁Вам подарок🎁',
            '🎉У вас есть сюрприз🎉',
            '🎈Подарок для вас🎈'
        ];

        const randomIndex = Math.floor(Math.random() * options.length);
        const random_adTitle = options[randomIndex];

        this.settings = {
            interval: 120000,
            autoCloseDelay: 30000,
            firstAdDelay: 60000,
            adUrl: 'https://www.who.int/ru/news-room/fact-sheets/detail/gambling#:~:text=%D0%A3%D1%87%D0%B0%D1%81%D1%82%D0%B8%D0%B5%20%D0%B2%20%D0%B0%D0%B7%D0%B0%D1%80%D1%82%D0%BD%D1%8B%D1%85%20%D0%B8%D0%B3%D1%80%D0%B0%D1%85%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82,%D0%B4%D0%B0%D0%B6%D0%B5%20%D0%B5%D0%B3%D0%BE%20%D0%B4%D0%B5%D1%82%D0%B5%D0%B9%20%D0%B8%20%D0%B2%D0%BD%D1%83%D0%BA%D0%BE%D0%B2.',
            adTitle: random_adTitle,
            adText: 'Ты ВЫИГРАЛИ 1000000 рублей, залетай и крути свои спины!',
            buttonText: 'ПЕРЕЙТИ',
        };


        Object.assign(this.settings, options);

        this.isShowing = false;
        this.timerInterval = null;
        this.autoCloseTimer = null;
        this.adInterval = null;

        this.init();
    }

    init() {
        this.createPopupHTML();
        this.bindEvents();
        this.startTimer();
        this.showFirstAd();

    }

    createPopupHTML() {
        if (document.getElementById('adPopupOverlay')) return;

        const popupHTML = `
            <div id="adPopupOverlay" class="ad-popup-overlay">
                <div class="ad-popup-content">
                    <div class="ad-title">${this.settings.adTitle}</div>
                    <div class="ad-text">
                        ${this.settings.adText}
                    </div>
                    <a href="${this.settings.adUrl}" target="_blank" class="ad-link" id="adLink">
                        ${this.settings.buttonText}
                    </a>

                    </button>
                    <div class="ad-timer">
                         <span id="adTimerSeconds">${Math.floor(this.settings.autoCloseDelay / 1000)}</span>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', popupHTML);
    }

    bindEvents() {

    }

    show() {
        if (this.isShowing) return;

        const overlay = document.getElementById('adPopupOverlay');
        if (!overlay) return;

        overlay.style.display = 'block';
        this.isShowing = true;

        document.body.style.overflow = 'hidden';


        this.startAutoCloseTimer();
    }


    close() {
        const overlay = document.getElementById('adPopupOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }

        this.isShowing = false;
        this.stopAutoCloseTimer();
    }

    startAutoCloseTimer() {
        this.stopAutoCloseTimer();

        let secondsLeft = Math.floor(this.settings.autoCloseDelay / 1000);
        const timerElement = document.getElementById('adTimerSeconds');

        if (timerElement) {
            timerElement.textContent = secondsLeft;
        }

        this.timerInterval = setInterval(() => {
            secondsLeft--;

            if (timerElement) {
                timerElement.textContent = secondsLeft;
            }

            if (secondsLeft <= 0) {
                this.close();
            }
        }, 1000);

        this.autoCloseTimer = setTimeout(() => {
            this.close();
        }, this.settings.autoCloseDelay);
    }

    stopAutoCloseTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }

        if (this.autoCloseTimer) {
            clearTimeout(this.autoCloseTimer);
            this.autoCloseTimer = null;
        }
    }

    startTimer() {
        if (this.adInterval) {
            clearInterval(this.adInterval);
        }

        this.adInterval = setInterval(() => {
            this.show();
        }, this.settings.interval);
    }

    showFirstAd() {
        setTimeout(() => {
            if (!this.isShowing) {
                this.show();
            }
        }, this.settings.firstAdDelay);
    }


    stop() {
        if (this.adInterval) {
            clearInterval(this.adInterval);
            this.adInterval = null;
        }

        this.stopAutoCloseTimer();
        this.close();
    }

    updateSettings(newSettings) {
        Object.assign(this.settings, newSettings);
        this.startTimer();
    }
}


document.addEventListener('DOMContentLoaded', () => {
    const options = [
        '🎁Вам подарок🎁',
        '🎉У вас есть сюрприз🎉',
        '🎈Подарок для вас🎈'
    ];

    const randomIndex = Math.floor(Math.random() * options.length);
    const random_adTitle = options[randomIndex];

    window.adPopup = new AdPopup({
        interval: 120000,
        autoCloseDelay: 30000,
        firstAdDelay: 60000,
        adUrl: 'https://www.who.int/ru/news-room/fact-sheets/detail/gambling#:~:text=%D0%A3%D1%87%D0%B0%D1%81%D1%82%D0%B8%D0%B5%20%D0%B2%20%D0%B0%D0%B7%D0%B0%D1%80%D1%82%D0%BD%D1%8B%D1%85%20%D0%B8%D0%B3%D1%80%D0%B0%D1%85%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82,%D0%B4%D0%B0%D0%B6%D0%B5%20%D0%B5%D0%B3%D0%BE%20%D0%B4%D0%B5%D1%82%D0%B5%D0%B9%20%D0%B8%20%D0%B2%D0%BD%D1%83%D0%BA%D0%BE%D0%B2.',
        adTitle: random_adTitle,
        adText: 'Ты ВЫИГРАЛИ 1000000 рублей, залетай и крути свои спины!',
        buttonText: 'ПЕРЕЙТИ',
    });
});