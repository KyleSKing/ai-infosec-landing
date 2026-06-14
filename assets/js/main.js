// AI Infosec Landing — Main JS

// Language toggle
document.addEventListener('DOMContentLoaded', () => {
  // Lang toggle buttons
  const langBtns = document.querySelectorAll('.lang-btn');
  const postContent = document.querySelector('.post-content');

  if (langBtns.length && postContent) {
    langBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        langBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const lang = btn.dataset.lang;
        postContent.classList.remove('show-en', 'show-both');
        if (lang === 'en') postContent.classList.add('show-en');
        if (lang === 'both') postContent.classList.add('show-both');
      });
    });
  }

  // Post filter
  const filterBtns = document.querySelectorAll('.filter-btn');
  const postCards = document.querySelectorAll('.post-card');

  if (filterBtns.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        postCards.forEach(card => {
          if (filter === 'all' || card.dataset.category === filter) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // Footer time
  const timeEl = document.getElementById('footer-time');
  if (timeEl) {
    const now = new Date();
    timeEl.textContent = `Last updated: ${now.toLocaleString('zh-CN', {timeZone: 'Asia/Shanghai'})} CST`;
  }
});
