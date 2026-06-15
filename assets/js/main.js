// 东情局 / DONG INTEL BUREAU — UI interactions

document.addEventListener('DOMContentLoaded', () => {
  const htmlEl = document.documentElement;

  document.querySelectorAll('.lang-opt').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.lang-opt').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      htmlEl.setAttribute('data-lang', btn.dataset.lang);
      localStorage.setItem('lang', btn.dataset.lang);
    });
  });

  const saved = localStorage.getItem('lang');
  if (saved) {
    htmlEl.setAttribute('data-lang', saved);
    document.querySelectorAll('.lang-opt').forEach(b => {
      b.classList.toggle('active', b.dataset.lang === saved);
    });
  }

  document.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.cat;
      document.querySelectorAll('.article[data-cat]').forEach(a => {
        a.style.display = (cat === 'all' || a.dataset.cat === cat) ? '' : 'none';
      });
    });
  });

  document.querySelectorAll('.lsw-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.lsw-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const target = btn.dataset.target;
      const pc = document.querySelector('.post-content');
      if (!pc) return;
      pc.classList.remove('show-en', 'show-both');
      if (target === 'en') pc.classList.add('show-en');
      if (target === 'both') pc.classList.add('show-both');
    });
  });
});
