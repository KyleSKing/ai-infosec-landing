// 東情局 / DONG INTEL BUREAU — UI + Supabase interactions
// Sections: 1) lang/cat/lws  2) supabase client  3) analytics (view)  4) likes  5) popular + sparkline

(function () {
  'use strict';

  // ---------- 1. Existing UI: lang / cat / lsw ----------
  document.addEventListener('DOMContentLoaded', () => {
    const htmlEl = document.documentElement;

    document.querySelectorAll('.lang-opt').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.lang-opt').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        htmlEl.setAttribute('data-lang', btn.dataset.lang);
        try { localStorage.setItem('lang', btn.dataset.lang); } catch (_) {}
      });
    });

    try {
      const saved = localStorage.getItem('lang');
      if (saved) {
        htmlEl.setAttribute('data-lang', saved);
        document.querySelectorAll('.lang-opt').forEach(b => {
          b.classList.toggle('active', b.dataset.lang === saved);
        });
      }
    } catch (_) {}

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

    // ---------- 2. Supabase client shim (no SDK; just fetch) ----------
    const cfg = window.SUPABASE_CONFIG || {};
    const SUPABASE_URL = cfg.url;
    const SUPABASE_ANON_KEY = cfg.anonKey;
    const isSupabaseConfigured =
      SUPABASE_URL &&
      SUPABASE_ANON_KEY &&
      !SUPABASE_URL.includes('placeholder') &&
      SUPABASE_ANON_KEY !== 'SUPABASE_ANON_KEY_PLACEHOLDER';

    async function supabaseFetch(path, init = {}) {
      if (!isSupabaseConfigured) return null;
      try {
        const resp = await fetch(SUPABASE_URL + path, {
          ...init,
          headers: {
            'content-type': 'application/json',
            apikey: SUPABASE_ANON_KEY,
            Authorization: 'Bearer ' + SUPABASE_ANON_KEY,
            ...(init.headers || {}),
          },
        });
        if (!resp.ok) return null;
        if (resp.status === 204) return null;
        return await resp.json();
      } catch (_) {
        return null;
      }
    }

    // ---------- 3. Analytics: page views ----------
    function currentSlug() {
      // post page: data-slug is on .post-engage; otherwise the page id is _index
      const engage = document.querySelector('.post-engage');
      if (engage) return engage.dataset.slug;
      return '_index';
    }

    function trackView(slug, lang) {
      if (!isSupabaseConfigured) return;
      try {
        const cacheKey = 'dib:lastView:' + slug;
        const last = parseInt(localStorage.getItem(cacheKey) || '0', 10);
        if (Date.now() - last < 30 * 60 * 1000) return; // 30min dedupe
        localStorage.setItem(cacheKey, String(Date.now()));
      } catch (_) { /* localStorage may be disabled */ }
      supabaseFetch('/functions/v1/view', {
        method: 'POST',
        body: JSON.stringify({ slug, lang: lang || 'bi' }),
      });
    }

    // Post page: only count after 30s OR 50% scroll
    const slug = currentSlug();
    if (slug) {
      let counted = false;
      const tryCount = () => {
        if (counted) return;
        counted = true;
        const lang = document.documentElement.getAttribute('data-lang') || 'bi';
        trackView(slug, lang);
      };
      const t = setTimeout(tryCount, 30 * 1000);
      const onScroll = () => {
        const h = document.documentElement;
        const scrolled = (h.scrollTop || document.body.scrollTop || 0);
        const total = h.scrollHeight - h.clientHeight;
        if (total > 0 && scrolled / total > 0.5) {
          clearTimeout(t);
          window.removeEventListener('scroll', onScroll);
          tryCount();
        }
      };
      window.addEventListener('scroll', onScroll, { passive: true });
    }

    // ---------- 4. Likes ----------
    function setupLikes() {
      const engage = document.querySelector('.post-engage');
      const btn = document.querySelector('.like-btn');
      if (!engage || !btn) return;
      const postSlug = engage.dataset.slug;
      const numEl = engage.querySelector('[data-stat="likes"]');

      const storageKey = 'dib:liked:' + postSlug;

      function setLikedUI(liked) {
        btn.classList.toggle('is-liked', liked);
        btn.setAttribute('aria-pressed', liked ? 'true' : 'false');
        const lbl = btn.querySelector('.like-label');
        if (lbl) {
          lbl.innerHTML = liked
            ? '<span class="zh">已赞</span><span class="en">Liked</span>'
            : '<span class="zh">点赞</span><span class="en">Like</span>';
        }
      }

      // localStorage is a *hint* (the source of truth is the edge function
      // and the likes table). We use it to render the correct initial
      // "已赞" state for users who voted from this browser, but we do NOT
      // disable the button — they must be able to toggle their vote off.

      // Hydrate UI from localStorage so returning voters see the right state
      // before the Supabase query resolves.
      try {
        if (localStorage.getItem(storageKey) === '1') {
          setLikedUI(true);
        }
      } catch (_) {}

      // Initial count from Supabase (anon SELECT on likes). Also reconciles
      // the local "liked" state in case the user logged in elsewhere or
      // cleared their browser data.
      if (isSupabaseConfigured) {
        supabaseFetch(
          '/rest/v1/likes?slug=eq.' + encodeURIComponent(postSlug) + '&select=count',
        ).then(rows => {
          if (rows && rows[0] && typeof rows[0].count === 'number' && numEl) {
            numEl.textContent = rows[0].count;
          }
        });
        // Optionally fetch the "did *I* like this?" hint. We do not have a
        // per-IP query endpoint, so we trust the localStorage hint until the
        // user actually clicks. If their like_voters row was deleted server-
        // side (e.g. via a manual reset), the next click will reconcile.

        // We can also detect "was my previous like removed server-side?" by
        // checking the count delta — if local says liked=true but a fresh
        // user clicks, the server will return liked=false and we sync.
      }

      btn.addEventListener('click', async () => {
        if (!isSupabaseConfigured) {
          flash('Supabase 未配置', 'error');
          return;
        }
        const wasLiked = btn.classList.contains('is-liked');
        const action = wasLiked ? 'remove' : 'add';
        // optimistic
        const cur = parseInt((numEl && numEl.textContent) || '0', 10) || 0;
        const next = Math.max(0, cur + (action === 'add' ? 1 : -1));
        if (numEl) numEl.textContent = next;
        setLikedUI(action === 'add');
        btn.disabled = true;
        try {
          const res = await supabaseFetch('/functions/v1/like', {
            method: 'POST',
            body: JSON.stringify({ slug: postSlug, action }),
          });
          if (!res) {
            // rollback
            if (numEl) numEl.textContent = cur;
            setLikedUI(wasLiked);
            flash('网络异常，请稍后再试', 'error');
            return;
          }
          if (numEl && typeof res.count === 'number') numEl.textContent = res.count;
          // Reconcile UI with server's authoritative state.
          setLikedUI(!!res.liked);
          try {
            if (res.liked) localStorage.setItem(storageKey, '1');
            else localStorage.removeItem(storageKey);
          } catch (_) {}
        } finally {
          btn.disabled = false;
        }
      });
    }

    function flash(msg, kind) {
      const el = document.createElement('div');
      el.className = 'toast ' + (kind || 'info');
      el.textContent = msg;
      document.body.appendChild(el);
      requestAnimationFrame(() => el.classList.add('show'));
      setTimeout(() => {
        el.classList.remove('show');
        setTimeout(() => el.remove(), 300);
      }, 2200);
    }

    setupLikes();

    // ---------- 5. Popular + sparkline (homepage) ----------
    async function loadSiteTotals() {
      if (!isSupabaseConfigured) return;
      const data = await supabaseFetch('/functions/v1/stats?type=site');
      try { console.log('[stats] loadSiteTotals response:', data); } catch (_) {}
      if (!data || !data.totals) return;
      const t = data.totals;
      const setIfPresent = (key, val) => {
        const el = document.querySelector('[data-stat="' + key + '"]');
        if (el && typeof val === 'number') el.textContent = val;
      };
      setIfPresent('total-pv', t.total_pv);
      setIfPresent('total-uv', t.total_uv);
      setIfPresent('total-likes', t.total_likes);
    }

    async function loadPopular() {
      if (!isSupabaseConfigured) return;
      const list = document.getElementById('popular-list');
      if (!list) return;

      const data = await supabaseFetch('/functions/v1/stats?type=top&days=7&limit=5');
      if (!data || !data.items || !data.items.length) return;

      // Build slug -> post url map
      const slugMap = {};
      document.querySelectorAll('.article[data-cat]').forEach(a => {
        try {
          const u = new URL(a.href, location.href);
          const m = u.pathname.match(/\/(\d{4}-\d{2}-\d{2}(?:-\d+)?-[a-z0-9-]+)\/?$/);
          if (m) slugMap[m[1]] = a.getAttribute('href');
        } catch (_) {}
      });

      list.innerHTML = '';
      data.items.forEach((item, i) => {
        const li = document.createElement('li');
        li.className = 'popular-item';
        const a = document.createElement('a');
        a.className = 'popular-link';
        a.href = slugMap[item.slug] || ('./' + item.slug + '/');
        a.innerHTML =
          '<span class="popular-rank">' + (i + 1) + '</span>' +
          '<span class="popular-title">' + escapeHtml(item.slug.replace(/^\d{4}-\d{2}-\d{2}(?:-\d+)?-/, '')) + '</span>' +
          '<span class="popular-meta"><b>' + item.views + '</b> · <b>' + item.likes + '</b> ♥</span>';
        li.appendChild(a);
        list.appendChild(li);
      });
    }

    function escapeHtml(s) {
      return String(s).replace(/[&<>"']/g, c => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
      }[c]));
    }

    async function loadSparkline() {
      if (!isSupabaseConfigured) return;
      const svg = document.getElementById('daily-spark');
      const totalEl = document.getElementById('spark-pv-total');
      if (!svg) return;
      const data = await supabaseFetch('/functions/v1/stats?type=daily&days=30');
      if (!data || !data.items || !data.items.length) return;
      const max = data.items.reduce((m, d) => Math.max(m, d.pv), 0);
      if (max <= 0) return;
      const W = 200, H = 36;
      const pts = data.items
        .map((d, i) => {
          const x = (i / Math.max(1, data.items.length - 1)) * W;
          const y = H - 2 - (d.pv / max) * (H - 4);
          return x.toFixed(1) + ',' + y.toFixed(1);
        })
        .join(' ');
      svg.innerHTML =
        '<polyline class="spark-poly" fill="none" stroke="currentColor" stroke-width="1.5" points="' + pts + '"/>' +
        '<polygon class="spark-area" fill="currentColor" opacity="0.15" points="0,' + H + ' ' + pts + ' ' + W + ',' + H + '"/>';
      if (totalEl) {
        const total = data.items.reduce((s, d) => s + d.pv, 0);
        totalEl.textContent = total;
      }
    }

    loadSiteTotals();
    loadPopular();
    loadSparkline();
  });
})();
