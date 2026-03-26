const API = 'http://localhost:8031'

export const api = {
    // ── Customer ──
    register: (data) =>
        fetch(`${API}/api/customer/register/`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(r => r.json().then(d => ({ ok: r.ok, data: d }))),

    customerLogin: (data) =>
        fetch(`${API}/api/customer/login/`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(r => r.json().then(d => ({ ok: r.ok, data: d }))),

    searchProducts: (q = '') =>
        fetch(`${API}/api/customer/search/?q=${q}`).then(r => r.json()),

    // Carts
    getCarts: () =>
        fetch(`${API}/api/customer/carts/`).then(r => r.json()),

    addCartItem: (data) =>
        fetch(`${API}/api/customer/cart-items/`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(r => r.json()),

    deleteCartItem: (id) =>
        fetch(`${API}/api/customer/cart-items/${id}/`, { method: 'DELETE' }),

    // ── Products (direct) ──
    getLaptops: () =>
        fetch(`${API}/api/laptop/laptops/`).then(r => r.json()),

    getMobiles: () =>
        fetch(`${API}/api/clothes/clothes/`).then(r => r.json()),

    getClothes: () =>
        fetch(`${API}/api/clothes/clothes/`).then(r => r.json()),

    // ── Staff ──
    staffLogin: (data) =>
        fetch(`${API}/api/staff/login/`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(r => r.json().then(d => ({ ok: r.ok, data: d }))),

    staffListProducts: () =>
        fetch(`${API}/api/staff/products/`).then(r => r.json()),

    staffCreateProduct: (data) =>
        fetch(`${API}/api/staff/product/create/`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(r => r.json().then(d => ({ ok: r.ok, data: d }))),

    staffUpdateProduct: (type, id, data) =>
        fetch(`${API}/api/staff/product/${id}/update/`, {
            method: 'PUT', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...data, type }),
        }).then(r => r.json().then(d => ({ ok: r.ok, data: d }))),

    staffDeleteProduct: (type, id) =>
        fetch(`${API}/api/staff/product/${id}/delete/?type=${type}`, {
            method: 'DELETE',
        }),
}
