document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('searchForm');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const params = new URLSearchParams(new FormData(form));

      // Add filters from the filter bar
      const fields = ['min_price','max_price','min_bed','max_bed','min_bath','max_bath','type'];
      for (const f of fields) {
        const el = document.getElementById(f);
        if (el && el.value) params.set(f, el.value);
      }

      await fetchAndRender(params);
      history.replaceState(null, '', `/?${params.toString()}`);
    });
  }

  const applyBtn = document.getElementById('applyFilters');
  if (applyBtn) {
    applyBtn.addEventListener('click', async () => {
      const params = new URLSearchParams(new FormData(document.getElementById('searchForm')));
      const fields = ['min_price','max_price','min_bed','max_bed','min_bath','max_bath','type','sort'];
      for (const f of fields) {
        const el = document.getElementById(f);
        if (el && el.value) params.set(f, el.value);
      }
      await fetchAndRender(params);
      history.replaceState(null, '', `/?${params.toString()}`);
    });
  }
});

async function fetchAndRender(params) {
  const container = document.getElementById('results');
  if (!container) return;
  const url = `/api/properties?${params.toString()}`;
  const res = await fetch(url);
  if (!res.ok) {
    container.innerHTML = `<p>Failed to load listings.</p>`;
    return;
  }
  const data = await res.json();
  container.innerHTML = data.items.map(renderCard).join('');
}

function renderCard(p) {
  const image = p.cover_image_url || `https://picsum.photos/640/420?grayscale`;
  const price = new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(p.price);
  return `
  <a class="card" href="/properties/${p.id}">
    <div class="card-image" style="background-image:url('${image}')"></div>
    <div class="card-body">
      <div class="price">${price}</div>
      <div class="meta">${p.bedrooms} bd • ${p.bathrooms} ba • ${p.square_feet ?? '?'} sqft</div>
      <div class="address">${p.address_line}, ${p.city}, ${p.state} ${p.zipcode}</div>
    </div>
  </a>`;
}
