class SimpleAdPopup {
    constructor(options = {}) {
        this.settings = {
            adUrl: 'https://www.who.int/ru/news-room/fact-sheets/detail/gambling#:~:text=%D0%A3%D1%87%D0%B0%D1%81%D1%82%D0%B8%D0%B5%20%D0%B2%20%D0%B0%D0%B7%D0%B0%D1%80%D1%82%D0%BD%D1%8B%D1%85%20%D0%B8%D0%B3%D1%80%D0%B0%D1%85%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82,%D0%B4%D0%B0%D0%B6%D0%B5%20%D0%B5%D0%B3%D0%BE%20%D0%B4%D0%B5%D1%82%D0%B5%D0%B9%20%D0%B8%20%D0%B2%D0%BD%D1%83%D0%BA%D0%BE%D0%B2.',
            adTitle: "Статистика:",
            adText: '<p>&nbsp;&nbsp;&nbsp;&nbsp;PerClick: 10,<br>&nbsp;&nbsp;&nbsp;&nbsp;AutoClick: 15</p>',
        };

        // Можно добавить опции пользователя
        Object.assign(this.settings, options);

        if (options.adText) {
            this.settings.adText = options.adText;
        }

        this.isShowing = false;
        this.createPopupHTML();
        this.bindCloseEvent();
    }

    createPopupHTML() {
        if (document.getElementById('simpleAdPopupOverlay')) return;
        const html = `
            <div id="simpleStatsPopupOverlay" class="stats-popup-overlay">
                <div class="stats-popup-content">
                    <form action="{{ url_for('stats_check') }}" method="post" class="stats-check-form">
                        <div class="stats-title">${this.settings.adTitle}</div>
                        <div class="stats-text">${this.settings.adText}</div>
                    </form>
                    <button id="closeStatsBtn" style="margin-top:10px;">Закрыть</button>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', html);
    }

    bindCloseEvent() {
        const btn = document.getElementById('closeStatsBtn');
        if (btn) {
            btn.addEventListener('click', () => {
                console.log("ЗАКРЫТО");
                this.close();
            });
        }
    }

    show() {
        const overlay = document.getElementById('simpleStatsPopupOverlay');
        if (overlay && !this.isShowing) {
            overlay.style.display = 'flex';
            this.isShowing = true;
            document.body.style.overflow = 'hidden'; // чтобы фон не прокручивался
        }
    }

    updateContent() {
        const overlay = document.getElementById('simpleStatsPopupOverlay');
        if (overlay) {
            const titleDiv = overlay.querySelector('.stats-title');
            const textDiv = overlay.querySelector('.stats-text');
            if (titleDiv) {
                titleDiv.innerHTML = this.settings.adTitle;
            }
            if (textDiv) {
                textDiv.innerHTML = this.settings.adText;
            }
        }
    }

    close() {
        const overlay = document.getElementById('simpleStatsPopupOverlay');
        if (overlay) {
            overlay.style.display = 'none';
            this.isShowing = false;
            document.body.style.overflow = '';
        }
    }
}

let stats = new SimpleAdPopup({
    adText: ""
});
document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('check-stats-button');
    if (button) {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            fetch('/check_stats', { method: 'GET' })
                .then(response => response.json())
                .then(data => {
                    stats.settings.adText = data.statsText;
                    stats.updateContent();
                    stats.show();
                })
        });
    } else {
        console.warn('Кнопка "check-stats-button" не найдена');
    }
});