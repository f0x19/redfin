async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

function formatPrice(cents) {
  const n = Number(cents);
  return isFinite(n) ? n.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }) : '$—';
}

function h(el, attrs = {}, children = []) {
  const node = document.createElement(el);
  Object.entries(attrs).forEach(([k,v]) => {
    if (k.startsWith('on') && typeof v === 'function') {
      node.addEventListener(k.slice(2).toLowerCase(), v);
    } else if (v != null) {
      node.setAttribute(k, v);
    }
  });
  (Array.isArray(children) ? children : [children]).forEach(c => {
    if (c == null) return;
    if (typeof c === 'string') node.appendChild(document.createTextNode(c));
    else node.appendChild(c);
  });
  return node;
}

// Listings page logic
async function initListings() {
  const results = document.getElementById('results');
  if (!results) return;

  const params = new URLSearchParams(window.location.search);
  let page = Number(params.get('page') || '1');

  async function load() {
    const url = `/api/properties?${params.toString()}`;
    const data = await fetchJSON(url);

    results.innerHTML = '';
    data.items.forEach(p => {
      const card = h('div', { class: 'card' }, [
        h('img', { src: p.image_url || 'https://images.unsplash.com/photo-1560185127-6a8c0b4e0f4b?q=80&w=1200&auto=format&fit=crop', alt: p.title }),
        h('div', { class: 'content' }, [
          h('div', { class: 'price' }, formatPrice(p.price)),
          h('div', { class: 'title' }, p.title),
          h('div', { class: 'meta' }, `${p.beds} bd • ${p.baths} ba • ${p.sqft || '—'} sqft`),
          h('div', { class: 'meta' }, `${p.address}, ${p.city}, ${p.state} ${p.zip_code}`),
          h('a', { href: `/property/${p.id}` }, 'View details')
        ])
      ]);
      results.appendChild(card);
    });

    document.getElementById('pageInfo').textContent = `Page ${data.page} of ${data.pages}`;
    document.getElementById('prevPage').disabled = data.page <= 1;
    document.getElementById('nextPage').disabled = data.page >= data.pages;
  }

  document.getElementById('prevPage').addEventListener('click', () => {
    const current = Number(params.get('page') || '1');
    params.set('page', String(Math.max(1, current - 1)));
    history.replaceState(null, '', `?${params.toString()}`);
    load();
  });
  document.getElementById('nextPage').addEventListener('click', () => {
    const current = Number(params.get('page') || '1');
    params.set('page', String(current + 1));
    history.replaceState(null, '', `?${params.toString()}`);
    load();
  });

  document.getElementById('filtersForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const newParams = new URLSearchParams();
    for (const [k, v] of fd.entries()) if (v) newParams.set(k, v);
    history.replaceState(null, '', `?${newParams.toString()}`);
    params.set('page', '1');
    for (const [k, v] of newParams.entries()) params.set(k, v);
    load();
  });

  await load();
}

// Property detail page logic
async function initPropertyDetail() {
  const container = document.getElementById('property');
  if (!container) return;
  const id = window.__PROPERTY_ID__;
  const data = await fetchJSON(`/api/properties/${id}`);

  const view = h('div', { class: 'detail' }, [
    h('img', { src: data.image_url || 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=1200&auto=format&fit=crop', alt: data.title, style: 'width:100%;max-height:360px;object-fit:cover;border-radius:12px' }),
    h('h1', {}, data.title),
    h('div', { class: 'price', style: 'font-size:28px;margin:8px 0' }, formatPrice(data.price)),
    h('div', { class: 'meta' }, `${data.beds} bd • ${data.baths} ba • ${data.sqft || '—'} sqft`),
    h('div', { class: 'meta' }, `${data.address}, ${data.city}, ${data.state} ${data.zip_code}`),
    h('p', {}, data.description || 'No description provided.'),
  ]);
  container.appendChild(view);
}

window.addEventListener('DOMContentLoaded', () => {
  initListings();
  initPropertyDetail();
});
