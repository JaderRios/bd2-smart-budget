import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, ArrowRightLeft, Landmark, Target, Tags, Users, 
  FileText, Receipt, Edit2, Trash2, FolderOpen, Wallet, 
  TrendingUp, TrendingDown, Plus, Bell, RefreshCw 
} from 'lucide-react';
import './App.css';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  
  const [usuarios, setUsuarios] = useState([]);
  const [cuentas, setCuentas] = useState([]);
  const [facturas, setFacturas] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [transacciones, setTransacciones] = useState([]);
  const [metas, setMetas] = useState([]);
  const [estados, setEstados] = useState([]);
  const [notificaciones, setNotificaciones] = useState([]);
  const [sincronizaciones, setSincronizaciones] = useState([]);
  
  const [searchQuery, setSearchQuery] = useState('');

  // Modales Dinámicos
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState('CREATE'); // 'CREATE' o 'EDIT'
  const [formData, setFormData] = useState({});
  const [editId, setEditId] = useState(null);
  
  // Entity metadata para el titulo dinámico
  const entityMeta = {
    'usuarios': 'Usuarios',
    'cuentas': 'Cuentas Bancarias',
    'categorias': 'Categorías',
    'transacciones': 'Transacciones',
    'metas': 'Metas de Ahorro',
    'estados': 'Estados de Cuenta',
    'facturas': 'Facturas (Mongo)'
  };

  const loadData = async () => {
    try {
      if (activeTab !== 'dashboard') {
        const endpoints = {
          'usuarios': setUsuarios,
          'cuentas': setCuentas,
          'facturas': setFacturas,
          'categorias': setCategorias,
          'transacciones': setTransacciones,
          'metas': setMetas,
          'estados': setEstados
        };
        const res = await fetch(`${API_URL}/${activeTab}`);
        endpoints[activeTab](await res.json() || []);
      }

      // Precarga global de listas maestras secuencial
      const resU = await fetch(`${API_URL}/usuarios`);
      setUsuarios(await resU.json() || []);
      
      const resC = await fetch(`${API_URL}/cuentas`);
      setCuentas(await resC.json() || []);
      
      const resCat = await fetch(`${API_URL}/categorias`);
      setCategorias(await resCat.json() || []);
      
      const resT = await fetch(`${API_URL}/transacciones`);
      setTransacciones(await resT.json() || []);
      
      const resM = await fetch(`${API_URL}/metas`);
      setMetas(await resM.json() || []);

      const resN = await fetch(`${API_URL}/notificaciones`);
      setNotificaciones(await resN.json() || []);

      const resS = await fetch(`${API_URL}/sincronizaciones`);
      setSincronizaciones(await resS.json() || []);

    } catch (err) {
      console.error("Error al conectar con FastAPI:", err);
    }
  };

  useEffect(() => { loadData(); }, [activeTab]);

  // DELETE
  const handleDelete = async (entidad, id) => {
    if (!window.confirm(`¿Estás seguro de eliminar el registro #${id} de ${entidad}?`)) return;
    try {
      const res = await fetch(`${API_URL}/${entidad}/${id}`, { method: 'DELETE' });
      if (res.ok) { loadData(); } 
      else { alert("Error al eliminar el registro. Puede tener dependencias (Foreign Keys)."); }
    } catch (e) { alert("Error de red"); }
  };

  // ----------------------------------------------------
  // MANEJO DE FORMULARIOS DINÁMICOS
  // ----------------------------------------------------
  const getEmptyPayload = (entidad) => {
    switch(entidad) {
      case 'usuarios': return { nombre: '', apellido: '', correo: '' };
      case 'cuentas': return { id_usuario: '', banco: '', numero_cuenta: '', saldo_actual: '' };
      case 'categorias': return { nombre: '', tipo: 'INGRESO' };
      case 'transacciones': return { id_cuenta: '', id_categoria: '', monto: '', tipo: 'GASTO', descripcion: '' };
      case 'metas': return { id_usuario: '', nombre_meta: '', monto_objetivo: '', monto_actual: '', fecha_limite: '', estado: 'ACTIVO' };
      case 'estados': return { id_cuenta: '', fecha_inicio: '', fecha_fin: '', saldo_inicial: '', saldo_final: '' };
      case 'facturas': return { usuario_id: '', empresa: '', monto: '', categoria: '', detalles: [{ clave: '', valor: '' }] };
      default: return {};
    }
  };

  const extractEditPayload = (entidad, data) => {
    switch(entidad) {
      case 'transacciones': return { id_cuenta: data.id_cuenta, id_categoria: data.id_categoria, monto: data.monto, tipo: data.tipo, descripcion: data.descripcion };
      case 'metas': return { id_usuario: data.id_usuario, nombre_meta: data.nombre_meta, monto_objetivo: data.monto_objetivo, monto_actual: data.monto_actual, fecha_limite: data.fecha_limite, estado: data.estado };
      case 'estados': return { id_cuenta: data.id_cuenta, fecha_inicio: data.fecha_inicio, fecha_fin: data.fecha_fin, saldo_inicial: data.saldo_inicial, saldo_final: data.saldo_final };
      case 'cuentas': return { id_usuario: 1, banco: data.banco, numero_cuenta: data.nro_cuenta, saldo_actual: data.saldo_actual };
      case 'usuarios': return { nombre: data.nombre, apellido: data.apellido, correo: data.correo };
      case 'categorias': return { nombre: data.nombre, tipo: data.tipo };
      case 'facturas': return { 
        usuario_id: data.usuario_id, 
        empresa: data.empresa, 
        monto: data.monto, 
        categoria: data.categoria, 
        detalles: Object.keys(data.detalles || {}).length > 0 
          ? Object.entries(data.detalles).map(([k, v]) => ({ clave: k, valor: String(v) })) 
          : [{ clave: '', valor: '' }] 
      };
      default: return {};
    }
  };

  const openCreateModal = () => {
    setModalMode('CREATE');
    setFormData(getEmptyPayload(activeTab));
    setIsModalOpen(true);
  };

  const openEditModal = (entidad, id, data) => {
    setModalMode('EDIT');
    setEditId(id);
    setFormData(extractEditPayload(entidad, data));
    setIsModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let payload = { ...formData };
    
    ['id_usuario', 'usuario_id', 'id_cuenta', 'id_categoria'].forEach(key => {
      if (key in payload) payload[key] = parseInt(payload[key]);
    });
    ['monto', 'saldo_actual', 'saldo_inicial', 'saldo_final', 'monto_objetivo', 'monto_actual'].forEach(key => {
      if (key in payload) payload[key] = parseFloat(payload[key]);
    });
    
    // Convertir el array de detalles clave-valor a un objeto para MongoDB
    if ('detalles' in payload && Array.isArray(payload.detalles)) {
      const obj = {};
      payload.detalles.forEach(item => {
        if (item.clave.trim() !== '') {
          obj[item.clave.trim()] = item.valor;
        }
      });
      payload.detalles = obj;
    }

    try {
      const url = modalMode === 'CREATE' ? `${API_URL}/${activeTab}` : `${API_URL}/${activeTab}/${editId}`;
      const method = modalMode === 'CREATE' ? 'POST' : 'PUT';
      const res = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      
      if (res.ok) {
        setIsModalOpen(false);
        loadData();
      } else {
        const errorData = await res.json();
        alert(`Error al guardar: ${errorData.detail || 'Revise los campos.'}`);
      }
    } catch (err) { alert("Error de red."); }
  };

  const renderInput = (key, value) => {
    const handleObjChange = (e) => setFormData({ ...formData, [key]: e.target.value });
    
    if (key === 'id_cuenta') return (
      <select required className="search-input" style={{width: '100%'}} value={value} onChange={handleObjChange}>
        <option value="">Seleccione Cuenta</option>
        {cuentas.map(c => <option key={c.id_cuenta} value={c.id_cuenta}>{c.propietario} - {c.banco} ({c.nro_cuenta})</option>)}
      </select>
    );
    if (key === 'id_categoria') return (
      <select required className="search-input" style={{width: '100%'}} value={value} onChange={handleObjChange}>
        <option value="">Seleccione Categoría</option>
        {categorias.map(c => <option key={c.id_categoria} value={c.id_categoria}>{c.nombre} - {c.tipo}</option>)}
      </select>
    );
    if (key === 'id_usuario' || key === 'usuario_id') return (
      <select required className="search-input" style={{width: '100%'}} value={value} onChange={handleObjChange}>
        <option value="">Seleccione Usuario</option>
        {usuarios.map(u => <option key={u.id_usuario} value={u.id_usuario}>{u.nombre} {u.apellido}</option>)}
      </select>
    );
    if (key === 'tipo') return (
      <select required className="search-input" style={{width: '100%'}} value={value} onChange={handleObjChange}>
        <option value="GASTO">GASTO</option>
        <option value="INGRESO">INGRESO</option>
      </select>
    );
    if (key === 'estado' && activeTab === 'metas') return (
      <select required className="search-input" style={{width: '100%'}} value={value} onChange={handleObjChange}>
        <option value="ACTIVO">ACTIVO</option>
        <option value="COMPLETADO">COMPLETADO</option>
        <option value="CANCELADO">CANCELADO</option>
        <option value="EN_PROCESO">EN_PROCESO</option>
      </select>
    );
    if (key === 'detalles') {
      const detailsArray = value || [];
      const handleRowChange = (index, field, val) => {
        const newArray = [...detailsArray];
        newArray[index][field] = val;
        setFormData({ ...formData, detalles: newArray });
      };
      
      const addRow = () => {
        setFormData({ ...formData, detalles: [...detailsArray, { clave: '', valor: '' }] });
      };
      
      const removeRow = (index) => {
        const newArray = detailsArray.filter((_, i) => i !== index);
        setFormData({ ...formData, detalles: newArray.length > 0 ? newArray : [{ clave: '', valor: '' }] });
      };

      return (
        <div style={{display:'flex', flexDirection:'column', gap:'12px'}}>
          {detailsArray.map((item, index) => (
            <div key={index} style={{display:'flex', gap:'10px', alignItems:'center'}}>
              <input 
                required
                type="text" 
                placeholder="Ej: Número Boleta" 
                value={item.clave} 
                onChange={(e) => handleRowChange(index, 'clave', e.target.value)}
                style={{flex: 1, padding: '10px 14px', borderRadius: '8px', fontSize: '13px'}}
              />
              <input 
                required
                type="text" 
                placeholder="Ej: B-0453" 
                value={item.valor} 
                onChange={(e) => handleRowChange(index, 'valor', e.target.value)}
                style={{flex: 1.5, padding: '10px 14px', borderRadius: '8px', fontSize: '13px'}}
              />
              <button 
                type="button" 
                onClick={() => removeRow(index)} 
                className="action-btn delete-btn" 
                style={{padding:'8px', margin:0, background: 'transparent'}}
              >
                ✕
              </button>
            </div>
          ))}
          <button 
            type="button" 
            onClick={addRow} 
            className="btn btn-secondary" 
            style={{padding:'8px 16px', fontSize:'12px', alignSelf:'flex-start', borderRadius: '20px'}}
          >
            + Agregar Atributo
          </button>
        </div>
      );
    }
    
    let type = "text";
    if (key.includes('fecha')) type = "date";
    if (key.includes('monto') || key.includes('saldo')) type = "number";
    if (key === 'correo') type = "email";
    
    return (
      <input required type={type} step={type === 'number' ? "0.01" : undefined} value={value} onChange={handleObjChange} placeholder={`Ingrese ${key.replace('_', ' ')}`} />
    );
  };

  const safeLower = (val) => (val || '').toString().toLowerCase();

  // ----------------------------------------------------
  // DASHBOARD CALCULATIONS
  // ----------------------------------------------------
  const totalBalance = cuentas.reduce((acc, c) => acc + parseFloat(c.saldo_actual || 0), 0);
  const totalExpenses = transacciones.filter(t => t.tipo === 'GASTO').reduce((acc, t) => acc + parseFloat(t.monto || 0), 0);
  const totalIncome = transacciones.filter(t => t.tipo === 'INGRESO').reduce((acc, t) => acc + parseFloat(t.monto || 0), 0);
  const activeGoals = metas.filter(m => m.estado !== 'CUMPLIDA' && m.estado !== 'CANCELADO').length;

  const renderDashboard = () => (
    <>
      <div className="dashboard-kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon blue"><Wallet size={24} /></div>
          <div className="kpi-info">
            <h3>Balance Total</h3>
            <h2>S/ {totalBalance.toLocaleString('es-PE', { minimumFractionDigits: 2 })}</h2>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon green"><TrendingUp size={24} /></div>
          <div className="kpi-info">
            <h3>Ingresos Totales</h3>
            <h2>S/ {totalIncome.toLocaleString('es-PE', { minimumFractionDigits: 2 })}</h2>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon red"><TrendingDown size={24} /></div>
          <div className="kpi-info">
            <h3>Gastos Totales</h3>
            <h2>S/ {totalExpenses.toLocaleString('es-PE', { minimumFractionDigits: 2 })}</h2>
          </div>
        </div>
        <div className="kpi-card">
          <div className="kpi-icon yellow"><Target size={24} /></div>
          <div className="kpi-info">
            <h3>Metas Activas</h3>
            <h2>{activeGoals} Objetivos</h2>
          </div>
        </div>
      </div>

      <div className="dashboard-layout">
        <div className="table-card">
          <div style={{padding: '24px', borderBottom: '1px solid var(--border-color)'}}>
            <h3 style={{fontSize: '18px', fontWeight: '700', color: 'var(--text-main)'}}>Transacciones Recientes</h3>
          </div>
          <table className="data-table">
            <thead><tr><th>Categoría</th><th>Monto</th><th>Tipo</th><th>Descripción</th></tr></thead>
            <tbody>
              {transacciones.slice(0, 5).map(t => (
                <tr key={t.id_transaccion}>
                  <td><span className="text-bold">{t.categoria}</span></td>
                  <td><span className={t.tipo === 'INGRESO' ? 'badge-ingreso pill-badge' : 'badge-gasto pill-badge'} style={{background:'transparent'}}>
                    {t.tipo === 'INGRESO' ? '+' : '-'} S/ {parseFloat(t.monto).toFixed(2)}
                  </span></td>
                  <td><span className={t.tipo === 'INGRESO' ? 'badge-ingreso pill-badge' : 'badge-gasto pill-badge'}>{t.tipo}</span></td>
                  <td>{t.descripcion}</td>
                </tr>
              ))}
              {transacciones.length === 0 && <tr><td colSpan="4" className="empty-state">No hay transacciones registradas.</td></tr>}
            </tbody>
          </table>
        </div>

        {/* Columna Derecha: Resumen de Cuentas, Notificaciones y Sincronizaciones */}
        <div style={{display:'flex', flexDirection:'column', gap:'24px'}}>
          
          <div className="table-card" style={{background: 'linear-gradient(135deg, var(--primary-color) 0%, #7B52FF 100%)', color: 'white', padding: '24px'}}>
            <h3 style={{fontSize: '18px', fontWeight: '700', marginBottom: '20px', color: 'white'}}>Resumen Cuentas</h3>
            <div style={{display:'flex', flexDirection:'column', gap:'12px'}}>
              {cuentas.slice(0, 3).map(c => (
                <div key={c.id_cuenta} style={{display:'flex', justifyContent:'space-between', alignItems:'center', background:'rgba(255,255,255,0.1)', padding:'12px', borderRadius:'10px'}}>
                  <div>
                    <div style={{fontWeight:'700', fontSize:'14px'}}>{c.banco}</div>
                    <div style={{fontSize:'11px', opacity:0.8}}>{c.nro_cuenta}</div>
                  </div>
                  <div style={{fontWeight:'800', fontSize:'15px'}}>S/ {parseFloat(c.saldo_actual).toFixed(2)}</div>
                </div>
              ))}
              {cuentas.length === 0 && <div style={{opacity:0.8, fontSize:'13px'}}>Aún no tienes cuentas registradas.</div>}
            </div>
          </div>

          <div className="table-card" style={{padding: '24px'}}>
            <h3 style={{fontSize: '16px', fontWeight: '700', marginBottom: '16px', display:'flex', alignItems:'center', gap:'8px'}}>
              <Bell size={18} className="saldo-green" style={{color:'var(--primary-color)'}} /> Alertas Recientes
            </h3>
            <div style={{display:'flex', flexDirection:'column', gap:'12px'}}>
              {notificaciones.slice(0, 2).map((n, idx) => (
                <div key={idx} style={{padding:'12px', background:'#FAFCFE', borderRadius:'10px', borderLeft:'4px solid var(--primary-color)'}}>
                  <div style={{fontSize:'13px', fontWeight:'600', color:'var(--text-main)'}}>{n.mensaje}</div>
                  <div style={{fontSize:'11px', color:'var(--text-muted)', marginTop:'4px'}}>{n.fecha}</div>
                </div>
              ))}
              {notificaciones.length === 0 && <div style={{color:'var(--text-muted)', fontSize:'13px'}}>No hay alertas pendientes.</div>}
            </div>
          </div>

          <div className="table-card" style={{padding: '24px'}}>
            <h3 style={{fontSize: '16px', fontWeight: '700', marginBottom: '16px', display:'flex', alignItems:'center', gap:'8px'}}>
              <RefreshCw size={18} style={{color:'var(--success-color)'}} /> Sincronizaciones Bancarias
            </h3>
            <div style={{display:'flex', flexDirection:'column', gap:'12px'}}>
              {sincronizaciones.slice(0, 2).map((s, idx) => (
                <div key={idx} style={{display:'flex', justifyContent:'space-between', alignItems:'center', padding:'12px', background:'#FAFCFE', borderRadius:'10px'}}>
                  <div>
                    <div style={{fontSize:'13px', fontWeight:'700', color:'var(--text-main)'}}>{s.banco}</div>
                    <div style={{fontSize:'11px', color:'var(--text-muted)'}}>{s.fecha_sync}</div>
                  </div>
                  <span className="pill-badge badge-ingreso" style={{fontSize:'10px', padding:'4px 8px'}}>{s.estado}</span>
                </div>
              ))}
              {sincronizaciones.length === 0 && <div style={{color:'var(--text-muted)', fontSize:'13px'}}>No hay conexiones recientes.</div>}
            </div>
          </div>

        </div>
      </div>
    </>
  );

  const renderEmptyState = (entidad) => (
    <div className="empty-state">
      <div style={{marginBottom:'16px', color:'var(--primary-color)'}}>
        <FolderOpen size={48} strokeWidth={1.5} />
      </div>
      <h3>No hay datos en {entityMeta[entidad]}</h3>
      <p>Comienza creando tu primer registro utilizando el botón de la parte superior.</p>
    </div>
  );

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <h2>SmartBudget</h2>
        </div>
        
        <div className="nav-section-title">Principal</div>
        <nav className="nav-menu">
          <button className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => { setActiveTab('dashboard'); setSearchQuery(''); }}>
            <span className="nav-icon"><LayoutDashboard size={18} /></span> Dashboard
          </button>
          <button className={`nav-item ${activeTab === 'transacciones' ? 'active' : ''}`} onClick={() => { setActiveTab('transacciones'); setSearchQuery(''); }}>
            <span className="nav-icon"><ArrowRightLeft size={18} /></span> Transacciones
          </button>
          
          <div className="nav-section-title">Administración</div>
          <button className={`nav-item ${activeTab === 'cuentas' ? 'active' : ''}`} onClick={() => { setActiveTab('cuentas'); setSearchQuery(''); }}>
            <span className="nav-icon"><Landmark size={18} /></span> Cuentas
          </button>
          <button className={`nav-item ${activeTab === 'metas' ? 'active' : ''}`} onClick={() => { setActiveTab('metas'); setSearchQuery(''); }}>
            <span className="nav-icon"><Target size={18} /></span> Metas de Ahorro
          </button>
          
          <div className="nav-section-title">Configuración</div>
          <button className={`nav-item ${activeTab === 'categorias' ? 'active' : ''}`} onClick={() => { setActiveTab('categorias'); setSearchQuery(''); }}>
            <span className="nav-icon"><Tags size={18} /></span> Categorías
          </button>
          <button className={`nav-item ${activeTab === 'usuarios' ? 'active' : ''}`} onClick={() => { setActiveTab('usuarios'); setSearchQuery(''); }}>
            <span className="nav-icon"><Users size={18} /></span> Usuarios
          </button>
          <button className={`nav-item ${activeTab === 'estados' ? 'active' : ''}`} onClick={() => { setActiveTab('estados'); setSearchQuery(''); }}>
            <span className="nav-icon"><FileText size={18} /></span> Estados Cuenta
          </button>
          <button className={`nav-item ${activeTab === 'facturas' ? 'active' : ''}`} onClick={() => { setActiveTab('facturas'); setSearchQuery(''); }}>
            <span className="nav-icon"><Receipt size={18} /></span> Facturas (Mongo)
          </button>
        </nav>
      </aside>

      {/* Main Panel */}
      <main className="main-content">
        <header className="content-header">
          <div className="title-section">
            <h1>{activeTab === 'dashboard' ? 'Visión General' : entityMeta[activeTab]}</h1>
            <p className="subtitle">
              {activeTab === 'dashboard' ? 'Bienvenido a tu resumen financiero.' : `Gestión completa de ${entityMeta[activeTab].toLowerCase()}`}
            </p>
          </div>
          
          {activeTab !== 'dashboard' && (
            <div className="actions-section">
              <input type="text" placeholder="Buscar..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="search-input" />
              <button className="btn btn-primary" onClick={openCreateModal}>
                <Plus size={18} strokeWidth={3} /> Nuevo Registro
              </button>
            </div>
          )}
        </header>

        {activeTab === 'dashboard' ? renderDashboard() : (
          <section className="grid-container">
            <div className="table-card">
              
              {activeTab === 'usuarios' && (
                usuarios.length > 0 ? (
                  <table className="data-table">
                    <thead><tr><th>ID</th><th>Nombre</th><th>Apellidos</th><th>Correo</th><th>Acciones</th></tr></thead>
                    <tbody>
                      {usuarios.filter(u => safeLower(u.nombre).includes(safeLower(searchQuery))).map(u => (
                        <tr key={u.id_usuario}><td><span className="text-bold">#{u.id_usuario}</span></td><td>{u.nombre}</td><td>{u.apellido}</td><td>{u.correo}</td>
                        <td>
                          <button className="action-btn edit-btn" onClick={() => openEditModal('usuarios', u.id_usuario, u)}><Edit2 size={16} /></button>
                          <button className="action-btn delete-btn" onClick={() => handleDelete('usuarios', u.id_usuario)}><Trash2 size={16} /></button>
                        </td></tr>
                      ))}
                    </tbody>
                  </table>
                ) : renderEmptyState('usuarios')
              )}

              {activeTab === 'cuentas' && (
                cuentas.length > 0 ? (
                  <table className="data-table">
                    <thead><tr><th>ID</th><th>Propietario</th><th>Banco</th><th>Nro. Cuenta</th><th>Saldo</th><th>Acciones</th></tr></thead>
                    <tbody>
                      {cuentas.filter(c => safeLower(c.banco).includes(safeLower(searchQuery))).map(c => (
                        <tr key={c.id_cuenta}><td><span className="text-bold">#{c.id_cuenta}</span></td><td>{c.propietario}</td><td><span className="text-bold">{c.banco}</span></td><td>{c.nro_cuenta}</td><td>S/ {parseFloat(c.saldo_actual).toFixed(2)}</td>
                        <td>
                          <button className="action-btn edit-btn" onClick={() => openEditModal('cuentas', c.id_cuenta, c)}><Edit2 size={16} /></button>
                          <button className="action-btn delete-btn" onClick={() => handleDelete('cuentas', c.id_cuenta)}><Trash2 size={16} /></button>
                        </td></tr>
                      ))}
                    </tbody>
                  </table>
                ) : renderEmptyState('cuentas')
              )}

              {activeTab === 'categorias' && (
                categorias.length > 0 ? (
                  <table className="data-table">
                    <thead><tr><th>ID</th><th>Nombre</th><th>Tipo</th><th>Acciones</th></tr></thead>
                    <tbody>
                      {categorias.filter(c => safeLower(c.nombre).includes(safeLower(searchQuery))).map(c => (
                        <tr key={c.id_categoria}><td><span className="text-bold">#{c.id_categoria}</span></td><td><span className="text-bold">{c.nombre}</span></td>
                        <td><span className={c.tipo === 'INGRESO' ? 'badge-ingreso pill-badge' : 'badge-gasto pill-badge'}>{c.tipo}</span></td>
                        <td>
                          <button className="action-btn edit-btn" onClick={() => openEditModal('categorias', c.id_categoria, c)}><Edit2 size={16} /></button>
                          <button className="action-btn delete-btn" onClick={() => handleDelete('categorias', c.id_categoria)}><Trash2 size={16} /></button>
                        </td></tr>
                      ))}
                    </tbody>
                  </table>
                ) : renderEmptyState('categorias')
              )}

              {activeTab === 'transacciones' && (
                transacciones.length > 0 ? (
                  <table className="data-table">
                    <thead><tr><th>ID</th><th>Monto</th><th>Tipo</th><th>Categoría</th><th>Descripción</th><th>Acciones</th></tr></thead>
                    <tbody>
                      {transacciones.filter(t => safeLower(t.descripcion).includes(safeLower(searchQuery))).map(t => (
                        <tr key={t.id_transaccion}><td><span className="text-bold">#{t.id_transaccion}</span></td>
                        <td><span className={t.tipo === 'INGRESO' ? 'badge-ingreso pill-badge' : 'badge-gasto pill-badge'} style={{background:'transparent'}}>
                          {t.tipo === 'INGRESO' ? '+' : '-'} S/ {parseFloat(t.monto).toFixed(2)}
                        </span></td>
                        <td><span className={t.tipo === 'INGRESO' ? 'badge-ingreso pill-badge' : 'badge-gasto pill-badge'}>{t.tipo}</span></td>
                        <td><span className="text-bold">{t.categoria}</span></td><td>{t.descripcion}</td>
                        <td>
                          <button className="action-btn edit-btn" onClick={() => openEditModal('transacciones', t.id_transaccion, t)}><Edit2 size={16} /></button>
                          <button className="action-btn delete-btn" onClick={() => handleDelete('transacciones', t.id_transaccion)}><Trash2 size={16} /></button>
                        </td></tr>
                      ))}
                    </tbody>
                  </table>
                ) : renderEmptyState('transacciones')
              )}

              {activeTab === 'metas' && (
                metas.length > 0 ? (
                  <table className="data-table">
                    <thead><tr><th>ID</th><th>Meta</th><th>Objetivo</th><th>Actual</th><th>Estado</th><th>Acciones</th></tr></thead>
                    <tbody>
                      {metas.filter(m => safeLower(m.nombre_meta).includes(safeLower(searchQuery))).map(m => (
                        <tr key={m.id_meta}><td><span className="text-bold">#{m.id_meta}</span></td><td><span className="text-bold">{m.nombre_meta}</span></td><td>S/ {m.monto_objetivo}</td><td>S/ {m.monto_actual}</td>
                        <td><span className={`pill-badge ${m.estado === 'ACTIVO' || m.estado === 'EN_PROCESO' ? 'badge-activo' : m.estado === 'CUMPLIDA' ? 'badge-ingreso' : 'badge-gasto'}`}>{m.estado}</span></td>
                        <td>
                          <button className="action-btn edit-btn" onClick={() => openEditModal('metas', m.id_meta, m)}><Edit2 size={16} /></button>
                          <button className="action-btn delete-btn" onClick={() => handleDelete('metas', m.id_meta)}><Trash2 size={16} /></button>
                        </td></tr>
                      ))}
                    </tbody>
                  </table>
                ) : renderEmptyState('metas')
              )}

              {activeTab === 'estados' && (
                estados.length > 0 ? (
                  <table className="data-table">
                    <thead><tr><th>ID</th><th>Nro. Cuenta</th><th>Inicio</th><th>Fin</th><th>Saldo Inicial</th><th>Saldo Final</th><th>Acciones</th></tr></thead>
                    <tbody>
                      {estados.filter(e => safeLower(e.numero_cuenta).includes(safeLower(searchQuery))).map(e => (
                        <tr key={e.id_estado}><td><span className="text-bold">#{e.id_estado}</span></td><td><span className="text-bold">{e.numero_cuenta}</span></td><td>{e.fecha_inicio}</td><td>{e.fecha_fin}</td><td>S/ {e.saldo_inicial}</td><td>S/ {e.saldo_final}</td>
                        <td>
                          <button className="action-btn edit-btn" onClick={() => openEditModal('estados', e.id_estado, e)}><Edit2 size={16} /></button>
                          <button className="action-btn delete-btn" onClick={() => handleDelete('estados', e.id_estado)}><Trash2 size={16} /></button>
                        </td></tr>
                      ))}
                    </tbody>
                  </table>
                ) : renderEmptyState('estados')
              )}

              {activeTab === 'facturas' && (
                facturas.length > 0 ? (
                  <table className="data-table">
                    <thead><tr><th>ID</th><th>Empresa</th><th>Monto</th><th>Categoría</th><th>Detalles Dinámicos (Mongo)</th><th>Acciones</th></tr></thead>
                    <tbody>
                      {facturas.filter(f => safeLower(f.empresa).includes(safeLower(searchQuery))).map((f, i) => (
                        <tr key={i}><td><span className="text-bold">#{f.usuario_id}</span></td><td><span className="text-bold">{f.empresa}</span></td><td>S/ {f.monto}</td>
                        <td><span className="pill-badge badge-activo">{f.categoria.toUpperCase()}</span></td>
                        <td>
                          <div style={{display:'flex', flexWrap:'wrap', gap:'6px'}}>
                            {Object.entries(f.detalles || {}).map(([clave, valor]) => (
                              <span key={clave} className="pill-badge" style={{background:'rgba(67, 24, 255, 0.05)', color:'var(--primary-color)', fontSize:'11px', border:'1px solid rgba(67, 24, 255, 0.1)'}}>
                                <strong style={{color:'var(--text-main)'}}>{clave}:</strong> {String(valor)}
                              </span>
                            ))}
                            {Object.keys(f.detalles || {}).length === 0 && <span style={{color:'var(--text-muted)', fontSize:'12px'}}>Sin detalles</span>}
                          </div>
                        </td>
                        <td>
                          <button className="action-btn edit-btn" onClick={() => openEditModal('facturas', f.usuario_id, f)}><Edit2 size={16} /></button>
                          <button className="action-btn delete-btn" onClick={() => handleDelete('facturas', f.usuario_id)}><Trash2 size={16} /></button>
                        </td></tr>
                      ))}
                    </tbody>
                  </table>
                ) : renderEmptyState('facturas')
              )}
              
            </div>
          </section>
        )}
      </main>

      {/* MODAL UNIVERSAL DINÁMICO */}
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-card" style={{maxHeight:'90vh', overflowY:'auto'}}>
            <div className="modal-header">
              <h2>{modalMode === 'CREATE' ? 'NUEVO REGISTRO EN' : 'EDITANDO EN'} {entityMeta[activeTab].toUpperCase()}</h2>
              <button className="close-btn" onClick={() => setIsModalOpen(false)}>&times;</button>
            </div>
            
            <form onSubmit={handleSubmit} className="modal-form">
              {Object.entries(formData).map(([key, value]) => (
                <div className="form-group" key={key}>
                  <label>{key.toUpperCase().replace('_', ' ')}</label>
                  {renderInput(key, value)}
                </div>
              ))}
              
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>Cancelar</button>
                <button type="submit" className="btn btn-primary">
                  {modalMode === 'CREATE' ? 'Guardar Nuevo' : 'Actualizar Cambios'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}

export default App;
