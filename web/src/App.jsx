import { useState, useEffect, useCallback } from 'react'
import './index.css'
import { api } from './api'

/* ─────────────────── CUSTOMER DASHBOARD ─────────────────── */
function CustomerDashboard({ user, onLogout }) {
  const [tab, setTab] = useState('laptops')
  const [laptops, setLaptops] = useState([])
  const [clothes, setClothes] = useState([])
  const [search, setSearch] = useState('')
  const [cart, setCart] = useState([]) // local cart
  const [view, setView] = useState('browse') // browse | cart
  const [loading, setLoading] = useState(false)

  const fetchProducts = useCallback(async () => {
    setLoading(true)
    try {
      if (search) {
        const data = await api.searchProducts(search)
        setLaptops(data.laptops || [])
        setClothes(data.clothes || [])
      } else {
        const [l, m] = await Promise.all([api.getLaptops(), api.getClothes()])
        setLaptops(Array.isArray(l) ? l : [])
        setClothes(Array.isArray(m) ? m : [])
      }
    } catch { setLaptops([]); setClothes([]) }
    setLoading(false)
  }, [search])

  useEffect(() => { fetchProducts() }, [fetchProducts])

  const addToCart = (product, type) => {
    setCart(prev => {
      const existing = prev.find(i => i.id === product.id && i.type === type)
      if (existing) return prev.map(i =>
        i.id === product.id && i.type === type ? { ...i, qty: i.qty + 1 } : i)
      return [...prev, { ...product, type, qty: 1 }]
    })
  }

  const removeFromCart = (id, type) => {
    setCart(prev => prev.filter(i => !(i.id === id && i.type === type)))
  }

  const updateQty = (id, type, delta) => {
    setCart(prev => prev.map(i => {
      if (i.id === id && i.type === type) {
        const newQty = i.qty + delta
        return newQty > 0 ? { ...i, qty: newQty } : i
      }
      return i
    }))
  }

  const products = tab === 'laptops' ? laptops : clothes
  const cartTotal = cart.reduce((sum, i) => sum + parseFloat(i.price) * i.qty, 0)

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="brand">KTPM <span>Store</span></div>
        <nav className="nav-menu">
          <button className={`nav-item ${view === 'browse' && tab === 'laptops' ? 'active' : ''}`}
            onClick={() => { setView('browse'); setTab('laptops') }}>💻 Laptops</button>
          <button className={`nav-item ${view === 'browse' && tab === 'clothes' ? 'active' : ''}`}
            onClick={() => { setView('browse'); setTab('clothes') }}>👕 Clothes</button>
          <button className={`nav-item ${view === 'cart' ? 'active' : ''}`}
            onClick={() => setView('cart')}>🛒 Giỏ hàng ({cart.length})</button>
          <div style={{ flex: 1 }} />
          <button className="nav-item danger" onClick={onLogout}>Đăng xuất</button>
        </nav>
        <div className="sidebar-footer">
          Xin chào, <strong>{user.username}</strong>
        </div>
      </aside>

      <main className="main-content">
        {view === 'cart' ? (
          <>
            <div className="page-header"><h1>🛒 Giỏ hàng</h1></div>
            {cart.length === 0 ? (
              <div className="empty-state">
                <div className="icon">🛒</div>
                <h3>Giỏ hàng trống</h3>
                <p>Hãy thêm sản phẩm vào giỏ hàng</p>
              </div>
            ) : (
              <>
                <div className="cart-list">
                  {cart.map((item) => (
                    <div className="cart-item" key={`${item.type}-${item.id}`}>
                      <div className="cart-item-info">
                        <h3>{item.name}</h3>
                        <span className="meta">{item.brand} · {item.type === 'laptop' ? 'Laptop' : 'Clothes'}</span>
                      </div>
                      <div className="cart-item-right">
                        <div className="qty-control">
                          <button onClick={() => updateQty(item.id, item.type, -1)}>−</button>
                          <span>{item.qty}</span>
                          <button onClick={() => updateQty(item.id, item.type, 1)}>+</button>
                        </div>
                        <span className="product-price">${(parseFloat(item.price) * item.qty).toLocaleString()}</span>
                        <button className="btn btn-danger btn-sm" onClick={() => removeFromCart(item.id, item.type)}>Xóa</button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="cart-summary">
                  <div className="total"><span>Tổng cộng</span><span>${cartTotal.toLocaleString()}</span></div>
                </div>
              </>
            )}
          </>
        ) : (
          <>
            <div className="page-header">
              <h1>Khám phá <span>{tab === 'laptops' ? 'Laptops' : 'Clothes'}</span></h1>
              <div className="header-actions">
                <form className="search-box" onSubmit={(e) => { e.preventDefault(); fetchProducts() }}>
                  <input placeholder="Tìm kiếm sản phẩm..." value={search} onChange={e => setSearch(e.target.value)} />
                </form>
              </div>
            </div>
            {loading ? (
              <div className="empty-state"><h3>Đang tải...</h3></div>
            ) : products.length === 0 ? (
              <div className="empty-state">
                <div className="icon">🔍</div>
                <h3>Không tìm thấy sản phẩm</h3>
                <p>Thử thay đổi từ khóa tìm kiếm</p>
              </div>
            ) : (
              <div className="product-grid">
                {products.map(p => (
                  <div key={p.id} className="product-card">
                    <div className="product-img">{p.brand?.charAt(0)}</div>
                    <span className="product-badge">{tab === 'laptops' ? 'laptop' : 'clothes'}</span>
                    <div className="product-brand">{p.brand}</div>
                    <h3>{p.name}</h3>
                    <div className="product-price">${parseFloat(p.price).toLocaleString()}</div>
                    <div className="product-specs">
                      {tab === 'laptops' ? (<>
                        <div className="spec-row"><span>CPU</span><span>{p.cpu || 'N/A'}</span></div>
                        <div className="spec-row"><span>RAM</span><span>{p.ram || 'N/A'}</span></div>
                        <div className="spec-row"><span>Storage</span><span>{p.storage || 'N/A'}</span></div>
                      </>) : (<>
                        <div className="spec-row"><span>Màn hình</span><span>{p.screen_size || 'N/A'}</span></div>
                        <div className="spec-row"><span>Pin</span><span>{p.battery || 'N/A'}</span></div>
                      </>)}
                    </div>
                    <div className="product-actions">
                      <button className="btn btn-primary btn-sm" onClick={() => addToCart(p, tab === 'laptops' ? 'laptop' : 'clothes')}>
                        Thêm vào giỏ
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

/* ─────────────────── STAFF DASHBOARD ─────────────────── */
function StaffDashboard({ user, onLogout }) {
  const [tab, setTab] = useState('laptop')
  const [data, setData] = useState({ laptops: [], clothes: [] })
  const [modal, setModal] = useState(null) // null | 'create' | 'edit'
  const [editItem, setEditItem] = useState(null)
  const [form, setForm] = useState({})
  const [loading, setLoading] = useState(false)

  const refresh = async () => {
    setLoading(true)
    const d = await api.staffListProducts()
    setData(d)
    setLoading(false)
  }

  useEffect(() => { refresh() }, [])

  const openCreate = () => {
    setForm({ name: '', brand: '', price: '', cpu: '', ram: '', storage: '', screen_size: '', battery: '', description: '' })
    setModal('create')
  }

  const openEdit = (item, type) => {
    setEditItem({ ...item, type })
    setForm({ ...item })
    setModal('edit')
  }

  const handleSave = async () => {
    if (modal === 'create') {
      await api.staffCreateProduct({ ...form, type: tab })
    } else if (modal === 'edit') {
      await api.staffUpdateProduct(editItem.type, editItem.id, form)
    }
    setModal(null)
    refresh()
  }

  const handleDelete = async (id, type) => {
    if (!confirm('Bạn có chắc chắn muốn xóa sản phẩm này?')) return
    await api.staffDeleteProduct(type, id)
    refresh()
  }

  const products = tab === 'laptop' ? data.laptops : data.clothes

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="brand">KTPM <span>Admin</span></div>
        <nav className="nav-menu">
          <button className={`nav-item ${tab === 'laptop' ? 'active' : ''}`}
            onClick={() => setTab('laptop')}>💻 Quản lý Laptop</button>
          <button className={`nav-item ${tab === 'clothes' ? 'active' : ''}`}
            onClick={() => setTab('clothes')}>👕 Quản lý Clothes</button>
          <div style={{ flex: 1 }} />
          <button className="nav-item danger" onClick={onLogout}>Đăng xuất</button>
        </nav>
        <div className="sidebar-footer">
          Staff: <strong>{user.username}</strong>
        </div>
      </aside>

      <main className="main-content">
        <div className="page-header">
          <h1>Quản lý <span>{tab === 'laptop' ? 'Laptop' : 'Clothes'}</span></h1>
          <button className="btn btn-primary" onClick={openCreate}>+ Thêm sản phẩm</button>
        </div>

        <div className="tabs">
          <button className={`tab ${tab === 'laptop' ? 'active' : ''}`} onClick={() => setTab('laptop')}>Laptop ({data.laptops?.length || 0})</button>
          <button className={`tab ${tab === 'clothes' ? 'active' : ''}`} onClick={() => setTab('clothes')}>Clothes ({data.clothes?.length || 0})</button>
        </div>

        {loading ? (
          <div className="empty-state"><h3>Đang tải...</h3></div>
        ) : products.length === 0 ? (
          <div className="empty-state">
            <div className="icon">📦</div>
            <h3>Chưa có sản phẩm nào</h3>
            <p>Nhấn "Thêm sản phẩm" để bắt đầu</p>
          </div>
        ) : (
          <table className="data-table">
            <thead><tr>
              <th>ID</th><th>Tên</th><th>Thương hiệu</th><th>Giá ($)</th>
              {tab === 'laptop' ? <><th>CPU</th><th>RAM</th><th>Storage</th></> : <><th>Màn hình</th><th>Pin</th></>}
              <th>Thao tác</th>
            </tr></thead>
            <tbody>
              {products.map(p => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td><strong>{p.name}</strong></td>
                  <td>{p.brand}</td>
                  <td>${parseFloat(p.price).toLocaleString()}</td>
                  {tab === 'laptop' ? <><td>{p.cpu || '—'}</td><td>{p.ram || '—'}</td><td>{p.storage || '—'}</td></> : <><td>{p.screen_size || '—'}</td><td>{p.battery || '—'}</td></>}
                  <td>
                    <div className="actions">
                      <button className="btn btn-secondary btn-sm" onClick={() => openEdit(p, tab)}>Sửa</button>
                      <button className="btn btn-danger btn-sm" onClick={() => handleDelete(p.id, tab)}>Xóa</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* Modal Create / Edit */}
        {modal && (
          <div className="modal-overlay" onClick={() => setModal(null)}>
            <div className="modal-card" onClick={e => e.stopPropagation()}>
              <h2>{modal === 'create' ? 'Thêm sản phẩm mới' : 'Cập nhật sản phẩm'}</h2>
              <div className="form-row">
                <div className="form-group">
                  <label>Tên sản phẩm</label>
                  <input value={form.name || ''} onChange={e => setForm({ ...form, name: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Thương hiệu</label>
                  <input value={form.brand || ''} onChange={e => setForm({ ...form, brand: e.target.value })} />
                </div>
              </div>
              <div className="form-group">
                <label>Giá ($)</label>
                <input type="number" value={form.price || ''} onChange={e => setForm({ ...form, price: e.target.value })} />
              </div>

              {tab === 'laptop' ? (
                <div className="form-row">
                  <div className="form-group"><label>CPU</label>
                    <input value={form.cpu || ''} onChange={e => setForm({ ...form, cpu: e.target.value })} /></div>
                  <div className="form-group"><label>RAM</label>
                    <input value={form.ram || ''} onChange={e => setForm({ ...form, ram: e.target.value })} /></div>
                  <div className="form-group"><label>Storage</label>
                    <input value={form.storage || ''} onChange={e => setForm({ ...form, storage: e.target.value })} /></div>
                </div>
              ) : (
                <div className="form-row">
                  <div className="form-group"><label>Màn hình</label>
                    <input value={form.screen_size || ''} onChange={e => setForm({ ...form, screen_size: e.target.value })} /></div>
                  <div className="form-group"><label>Pin</label>
                    <input value={form.battery || ''} onChange={e => setForm({ ...form, battery: e.target.value })} /></div>
                </div>
              )}

              <div className="form-group">
                <label>Mô tả</label>
                <textarea value={form.description || ''} onChange={e => setForm({ ...form, description: e.target.value })} />
              </div>
              <div className="modal-actions">
                <button className="btn btn-secondary" onClick={() => setModal(null)}>Hủy</button>
                <button className="btn btn-primary" onClick={handleSave}>
                  {modal === 'create' ? 'Tạo mới' : 'Lưu thay đổi'}
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

/* ─────────────────── AUTH PAGES ─────────────────── */
function LoginPage({ onLogin, onSwitchToRegister, onSwitchToStaff }) {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    const res = await api.customerLogin(form)
    if (res.ok) {
      onLogin({ ...res.data, role: 'customer' })
    } else {
      setError(res.data.error || 'Đăng nhập thất bại')
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="role-badge">Customer</div>
        <h1>Đăng nhập</h1>
        <p className="subtitle">Chào mừng quay lại KTPM Store</p>
        {error && <div className="error-msg">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group"><label>Tên đăng nhập</label>
            <input value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} required /></div>
          <div className="form-group"><label>Mật khẩu</label>
            <input type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required /></div>
          <button className="btn btn-primary btn-full" type="submit">Đăng nhập</button>
        </form>
        <div className="auth-footer">
          Chưa có tài khoản? <a href="#" onClick={onSwitchToRegister}>Đăng ký</a>
        </div>
        <div className="auth-footer">
          <a href="#" onClick={onSwitchToStaff}>Đăng nhập với tư cách Nhân viên →</a>
        </div>
      </div>
    </div>
  )
}

function RegisterPage({ onRegister, onSwitchToLogin }) {
  const [form, setForm] = useState({ username: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(''); setSuccess('')
    const res = await api.register(form)
    if (res.ok) {
      setSuccess('Đăng ký thành công! Vui lòng đăng nhập.')
      setTimeout(() => onRegister(), 1500)
    } else {
      const firstError = Object.values(res.data).flat()[0]
      setError(typeof firstError === 'string' ? firstError : 'Đăng ký thất bại')
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="role-badge">Customer</div>
        <h1>Đăng ký</h1>
        <p className="subtitle">Tạo tài khoản mua sắm tại KTPM Store</p>
        {error && <div className="error-msg">{error}</div>}
        {success && <div className="success-msg">{success}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group"><label>Tên đăng nhập</label>
            <input value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} required /></div>
          <div className="form-group"><label>Email</label>
            <input type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} /></div>
          <div className="form-group"><label>Mật khẩu</label>
            <input type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required /></div>
          <button className="btn btn-primary btn-full" type="submit">Tạo tài khoản</button>
        </form>
        <div className="auth-footer">
          Đã có tài khoản? <a href="#" onClick={onSwitchToLogin}>Đăng nhập</a>
        </div>
      </div>
    </div>
  )
}

function StaffLoginPage({ onLogin, onSwitchToCustomer }) {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    const res = await api.staffLogin(form)
    if (res.ok) {
      onLogin({ ...res.data, role: 'staff' })
    } else {
      setError(res.data.error || 'Đăng nhập thất bại')
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="role-badge">Staff</div>
        <h1>Đăng nhập Nhân viên</h1>
        <p className="subtitle">Truy cập bảng quản trị KTPM Store</p>
        {error && <div className="error-msg">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group"><label>Tên đăng nhập</label>
            <input value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} required /></div>
          <div className="form-group"><label>Mật khẩu</label>
            <input type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required /></div>
          <button className="btn btn-primary btn-full" type="submit">Đăng nhập</button>
        </form>
        <div className="auth-footer">
          <a href="#" onClick={onSwitchToCustomer}>← Về trang Khách hàng</a>
        </div>
      </div>
    </div>
  )
}

/* ─────────────────── APP ROOT ─────────────────── */
function App() {
  const [page, setPage] = useState('login') // login | register | staff-login
  const [user, setUser] = useState(null)

  const handleLogin = (userData) => {
    setUser(userData)
  }

  const handleLogout = () => {
    setUser(null)
    setPage('login')
  }

  if (user) {
    if (user.role === 'staff') {
      return <StaffDashboard user={user} onLogout={handleLogout} />
    }
    return <CustomerDashboard user={user} onLogout={handleLogout} />
  }

  if (page === 'register') {
    return <RegisterPage onRegister={() => setPage('login')} onSwitchToLogin={() => setPage('login')} />
  }
  if (page === 'staff-login') {
    return <StaffLoginPage onLogin={handleLogin} onSwitchToCustomer={() => setPage('login')} />
  }

  return <LoginPage onLogin={handleLogin} onSwitchToRegister={() => setPage('register')} onSwitchToStaff={() => setPage('staff-login')} />
}

export default App
