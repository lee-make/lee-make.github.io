---
title: 搜尋
description: 站內搜索

date: 2026-09-09T12:00:00+08:00
lastmod: 2026-09-09T12:00:00+08:00
comments: false
---

<div class="local-search">
  <input id="local-search-input" type="search" placeholder="輸入關鍵詞，回車搜尋…" autocomplete="off" />
  <p id="local-search-tip"></p>
  <ul id="local-search-result"></ul>
</div>

<style>
.local-search input {
  width: 100%;
  padding: 10px 14px;
  font-size: 15px;
  color: var(--color-text, #333);
  background: var(--color-background, #fff);
  border: 1px solid var(--color-red-4, #d1e8f8);
  border-radius: 8px;
  outline: none;
  box-sizing: border-box;
}
.local-search input:focus {
  border-color: var(--color-link, #0a72b8);
}
#local-search-tip {
  font-size: 13px;
  opacity: 0.6;
  margin: 10px 0 0;
}
#local-search-result {
  list-style: none;
  padding: 0;
  margin: 16px 0 0;
}
#local-search-result li {
  padding: 12px 0;
  border-bottom: 1px dashed rgba(128, 128, 128, 0.25);
}
#local-search-result a {
  font-size: 17px;
  color: var(--color-link, #0a72b8);
  text-decoration: none;
}
#local-search-result a:hover {
  text-decoration: underline;
}
#local-search-result .meta {
  display: block;
  font-size: 12px;
  opacity: 0.6;
  margin-top: 4px;
}
#local-search-result .excerpt {
  font-size: 14px;
  line-height: 1.7;
  margin-top: 6px;
  opacity: 0.85;
  word-break: break-all;
}
#local-search-result mark {
  background: var(--color-red-5, #f1f8fd);
  color: inherit;
  padding: 0 2px;
}
</style>

<script>
(function () {
  var input = document.getElementById('local-search-input');
  var tip = document.getElementById('local-search-tip');
  var list = document.getElementById('local-search-result');
  if (!input) return;

  var m = location.pathname.match(/^\/(zh-tw|en)\//);
  var base = m ? '/' + m[1] + '/' : '/';
  var posts = [];
  var timer = null;

  fetch(base + 'index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      posts = data || [];
      tip.textContent = '已索引 ' + posts.length + ' 篇文章';
    })
    .catch(function () {
      tip.textContent = '索引載入失敗';
    });

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function highlight(text, kw) {
    var safe = escapeHtml(text);
    if (!kw) return safe;
    var re = new RegExp(kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    return safe.replace(re, function (m) { return '<mark>' + m + '</mark>'; });
  }

  function excerpt(content, kw) {
    var idx = content ? content.toLowerCase().indexOf(kw.toLowerCase()) : -1;
    if (idx < 0) return content ? content.slice(0, 120) : '';
    var start = Math.max(0, idx - 40);
    return (start > 0 ? '…' : '') + content.slice(start, start + 200);
  }

  function render(kw) {
    var k = kw.trim();
    list.innerHTML = '';
    if (!k) { tip.textContent = '已索引 ' + posts.length + ' 篇文章'; return; }

    var hits = posts.filter(function (p) {
      return (p.title + (p.desc || '') + (p.content || '')).toLowerCase().indexOf(k.toLowerCase()) > -1;
    });

    tip.textContent = '找到 ' + hits.length + ' 條結果';
    hits.forEach(function (p) {
      var li = document.createElement('li');
      li.innerHTML =
        '<a href="' + p.url + '">' + highlight(p.title, k) + '</a>' +
        '<span class="meta">' + (p.date || '') + '</span>' +
        '<div class="excerpt">' + highlight(excerpt(p.content, k), k) + '</div>';
      list.appendChild(li);
    });
  }

  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () { render(input.value); }, 200);
  });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); render(input.value); }
  });
})();
</script>
