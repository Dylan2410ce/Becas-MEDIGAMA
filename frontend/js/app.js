const API_URL = "http://127.0.0.1:8000";

const state = {
  user: JSON.parse(localStorage.getItem("bm_user") || "null"),
  view: localStorage.getItem("bm_view") || "perfil",
  applicants: [],
  selectedApplicant: null
};

const loginView = document.getElementById("loginView");
const appView = document.getElementById("appView");
const content = document.getElementById("content");
const navMenu = document.getElementById("navMenu");
const viewTitle = document.getElementById("viewTitle");
const roleBadge = document.getElementById("roleBadge");
const sessionInfo = document.getElementById("sessionInfo");
const sessionLine = document.getElementById("sessionLine");

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!response.ok) {
    let detail = "No se pudo completar la accion.";
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch (error) {
      detail = response.statusText || detail;
    }
    throw new Error(detail);
  }
  return response.status === 204 ? null : response.json();
}

function money(value) {
  return Number(value || 0).toLocaleString("es-CR", { style: "currency", currency: "CRC" });
}

function setMessage(id, text, ok = false) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = text || "";
  el.style.color = ok ? "#0f9f6e" : "#dc2626";
}

function table(headers, rows) {
  return `
    <div class="table-wrap">
      <table>
        <thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead>
        <tbody>${rows.length ? rows.join("") : `<tr><td colspan="${headers.length}">Sin registros</td></tr>`}</tbody>
      </table>
    </div>
  `;
}

function saveSession(user) {
  state.user = user;
  localStorage.setItem("bm_user", JSON.stringify(user));
}

function updateStoredUser(user) {
  state.user = user;
  localStorage.setItem("bm_user", JSON.stringify(user));
}

function clearSession() {
  state.user = null;
  state.view = "perfil";
  state.selectedApplicant = null;
  localStorage.removeItem("bm_user");
  localStorage.removeItem("bm_view");
}

function navItems() {
  if (state.user.rol === "admin") {
    return [
      ["adminSolicitantes", "Solicitantes"],
      ["adminBecas", "Asignacion"],
      ["reportes", "Reportes"],
      ["admins", "Admins"]
    ];
  }
  return [
    ["perfil", "Mis datos"],
    ["solicitud", "Solicitud"],
    ["resultado", "Resultado"]
  ];
}

function render() {
  if (!state.user) {
    loginView.classList.remove("hidden");
    appView.classList.add("hidden");
    return;
  }

  loginView.classList.add("hidden");
  appView.classList.remove("hidden");

  const roleLabel = state.user.rol === "admin" ? "Administrador" : "Solicitante";
  sessionInfo.textContent = `${state.user.nombre} - ${roleLabel}`;
  sessionLine.textContent = `Sesion iniciada como: ${state.user.nombre}`;
  roleBadge.textContent = roleLabel;

  const allowed = navItems().map(([id]) => id);
  if (!allowed.includes(state.view)) state.view = state.user.rol === "admin" ? "adminSolicitantes" : "perfil";

  renderNav();
  openView(state.view);
}

function renderNav() {
  navMenu.innerHTML = navItems().map(([id, label]) => (
    `<button class="nav-btn ${state.view === id ? "active" : ""}" data-view="${id}">${label}</button>`
  )).join("");

  navMenu.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => openView(button.dataset.view));
  });
}

function openView(view) {
  state.view = view;
  localStorage.setItem("bm_view", view);
  renderNav();

  const titles = {
    perfil: "Mis datos",
    solicitud: "Solicitud de beca",
    resultado: "Consultar resultado",
    adminSolicitantes: "Solicitantes",
    adminBecas: "Asignacion de becas",
    reportes: "Reportes",
    admins: "Credenciales admin"
  };
  viewTitle.textContent = titles[view] || "Panel";

  if (view === "perfil") renderPerfil();
  if (view === "solicitud") renderSolicitud();
  if (view === "resultado") renderResultado();
  if (view === "adminSolicitantes") renderAdminSolicitantes();
  if (view === "adminBecas") renderAdminBecas();
  if (view === "reportes") renderReportes();
  if (view === "admins") renderAdmins();
}

function renderPerfil() {
  content.innerHTML = `
    <section class="panel narrow">
      <div class="section-title">
        <div>
          <h2>Datos personales</h2>
          <p>Actualiza solo los datos de contacto. El ID es autogenerado.</p>
        </div>
      </div>
      <form id="profileForm" class="form-grid two">
        <label>ID <input value="${state.user.id}" readonly></label>
        <label>Rol <input value="${state.user.rol}" readonly></label>
        <label>Nombre <input name="nombre" value="${state.user.nombre}"></label>
        <label>Correo <input name="correo" type="text" value="${state.user.correo}"></label>
        <label class="wide">Telefono <input name="telefono" value="${state.user.telefono}"></label>
        <div class="actions wide"><button type="submit" class="primary">Guardar cambios</button></div>
      </form>
      <p id="profileMsg" class="message"></p>
    </section>
  `;
  document.getElementById("profileForm").addEventListener("submit", saveProfile);
}

async function saveProfile(event) {
  event.preventDefault();
  try {
    const user = await api(`/usuarios/me?usuario_id=${state.user.id}`, {
      method: "PUT",
      body: JSON.stringify(Object.fromEntries(new FormData(event.target).entries()))
    });
    updateStoredUser(user);
    setMessage("profileMsg", "Datos actualizados correctamente.", true);
    render();
  } catch (error) {
    setMessage("profileMsg", error.message);
  }
}

async function renderSolicitud() {
  content.innerHTML = `
    <section class="panel">
      <div class="section-title">
        <div>
          <h2>Formulario socioeconomico</h2>
          <p>Completa la informacion para calcular una categoria sugerida.</p>
        </div>
        <span class="badge">Revision admin</span>
      </div>
      <form id="requestForm" class="form-stack large-form">
        <div class="form-block">
          <h3>Datos academicos y ubicacion</h3>
          <div class="form-grid calm">
            <label>Edad <input name="edad" type="number"></label>
            <label>Provincia <input name="provincia"></label>
            <label>Canton <input name="canton"></label>
            <label>Universidad <input name="universidad"></label>
            <label>Carrera <input name="carrera"></label>
            <label>Nivel
              <select name="nivel">
                <option>Diplomado</option>
                <option>Bachillerato</option>
                <option>Licenciatura</option>
              </select>
            </label>
          </div>
        </div>
        <div class="form-block">
          <h3>Situacion economica</h3>
          <div class="form-grid calm">
            <label>Ingreso mensual familiar <input name="ingresos" type="number" step="0.01"></label>
            <label>Gastos mensuales <input name="gastos" type="number" step="0.01"></label>
            <label>Dependientes economicos <input name="dependientes" type="number"></label>
            <label>Miembros del hogar <input name="miembros_hogar" type="number"></label>
            <label>Promedio academico <input name="promedio" type="number" step="0.01"></label>
            <label>Vivienda
              <select name="vivienda">
                <option>Propia</option>
                <option>Alquilada</option>
                <option>Prestada</option>
              </select>
            </label>
            <label>Trabaja
              <select name="trabaja">
                <option>No</option>
                <option>Si</option>
              </select>
            </label>
            <label>Transporte
              <select name="transporte">
                <option>Bus</option>
                <option>Propio</option>
                <option>Beca transporte</option>
              </select>
            </label>
            <label>Condicion especial
              <select name="condicion_especial">
                <option>Ninguna</option>
                <option>Discapacidad</option>
                <option>Enfermedad</option>
                <option>Cuido familiar</option>
                <option>Desempleo familiar</option>
              </select>
            </label>
            <label class="wide">Comentario opcional <input name="situacion_especial" placeholder="Explique algo importante si aplica"></label>
          </div>
        </div>
        <div class="actions wide"><button type="submit" class="primary">Enviar solicitud</button></div>
      </form>
      <p id="requestMsg" class="message"></p>
    </section>
    <section class="panel" id="myRequestPanel"></section>
  `;

  document.getElementById("requestForm").addEventListener("submit", saveRequest);
  await loadMyRequest();
}

async function saveRequest(event) {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.target).entries());
  ["edad", "ingresos", "gastos", "dependientes", "miembros_hogar", "promedio"].forEach((key) => {
    data[key] = Number(data[key]);
  });

  try {
    const solicitud = await api(`/solicitantes/mi-solicitud?usuario_id=${state.user.id}`, { method: "POST", body: JSON.stringify(data) });
    setMessage("requestMsg", "Solicitud enviada correctamente.", true);
    fillRequestForm(solicitud);
    renderMyRequest(solicitud);
  } catch (error) {
    setMessage("requestMsg", error.message);
  }
}

async function loadMyRequest() {
  const panel = document.getElementById("myRequestPanel");
  try {
    const solicitud = await api(`/solicitantes/mi-solicitud?usuario_id=${state.user.id}`);
    if (!solicitud) {
      panel.innerHTML = `<h2>Solicitud actual</h2><p class="muted">Todavia no has enviado una solicitud.</p>`;
      return;
    }
    fillRequestForm(solicitud);
    renderMyRequest(solicitud);
  } catch (error) {
    panel.innerHTML = `<h2>Solicitud actual</h2><p class="message">${error.message}</p>`;
  }
}

function fillRequestForm(s) {
  const form = document.getElementById("requestForm");
  if (!form) return;
  Object.keys(s).forEach((key) => {
    if (form[key] !== undefined) form[key].value = s[key] ?? "";
  });
}

function renderMyRequest(s) {
  document.getElementById("myRequestPanel").innerHTML = `
    <div class="section-title">
      <div>
        <h2>Solicitud actual</h2>
        <p>SOL-${String(s.id).padStart(5, "0")} - ${s.estado_solicitud}</p>
      </div>
    </div>
    <div class="summary-grid">
      <article><span>Indice</span><strong>${s.indice_vulnerabilidad}</strong></article>
      <article><span>Categoria sugerida</span><strong>${s.categoria_sugerida}</strong></article>
      <article><span>Ingreso</span><strong>${money(s.ingresos)}</strong></article>
      <article><span>Gastos</span><strong>${money(s.gastos)}</strong></article>
    </div>
    ${table(
      ["Universidad", "Carrera", "Promedio", "Dependientes", "Vivienda", "Condicion"],
      [`<tr><td>${s.universidad}</td><td>${s.carrera}</td><td>${s.promedio}</td><td>${s.dependientes}</td><td>${s.vivienda}</td><td>${s.condicion_especial}</td></tr>`]
    )}
  `;
}

function renderResultado() {
  content.innerHTML = `
    <section class="panel narrow">
      <h2>Consultar resultado aprobado</h2>
      <p class="muted">Solo se muestran becas ya aprobadas.</p>
      <form id="resultForm" class="form-grid">
        <label>Correo del solicitante <input name="correo" type="text" value="${state.user.correo || ""}"></label>
        <div class="actions"><button type="submit" class="primary">Consultar</button></div>
      </form>
      <p id="resultMsg" class="message"></p>
    </section>
    <section class="panel hidden" id="resultPanel"></section>
  `;
  document.getElementById("resultForm").addEventListener("submit", searchResult);
}

async function searchResult(event) {
  event.preventDefault();
  const correo = new FormData(event.target).get("correo");
  try {
    const r = await api(`/becas/resultado/${encodeURIComponent(correo)}`);
    const panel = document.getElementById("resultPanel");
    panel.classList.remove("hidden");
    panel.innerHTML = `
      <h2>Detalle de beca</h2>
      <div class="summary-grid">
        <article><span>Solicitud</span><strong>${r.id_solicitud}</strong></article>
        <article><span>Categoria</span><strong>${r.categoria}</strong></article>
        <article><span>Monto</span><strong>${money(r.monto)}</strong></article>
        <article><span>Estado</span><strong>${r.estado}</strong></article>
      </div>
      <p class="decision-note">${r.descripcion}</p>
    `;
    setMessage("resultMsg", "", true);
  } catch (error) {
    document.getElementById("resultPanel").classList.add("hidden");
    setMessage("resultMsg", error.message);
  }
}

async function renderAdminSolicitantes() {
  content.innerHTML = `
    <section class="panel">
      <div class="section-title">
        <div>
          <h2>Solicitantes registrados</h2>
          <p>Resumen de solicitudes recibidas. Cada tarjeta muestra los datos clave para la revision.</p>
        </div>
      </div>
      <div id="adminApplicantsList"></div>
    </section>
  `;
  await loadApplicants("adminApplicantsList", true);
}

async function loadApplicants(targetId, includeAction = false) {
  state.applicants = await api(`/solicitantes/?admin_id=${state.user.id}`);
  const cards = state.applicants.map((s) => `
    <article class="applicant-card">
      <div class="applicant-head">
        <div>
          <h3>${s.nombre}</h3>
          <p>${s.correo}</p>
        </div>
        <span class="status-pill">${s.estado_solicitud}</span>
      </div>
      <div class="applicant-meta">
        <span><strong>ID</strong>${s.id}</span>
        <span><strong>Carrera</strong>${s.carrera}</span>
        <span><strong>Promedio</strong>${s.promedio}</span>
        <span><strong>Indice</strong>${s.indice_vulnerabilidad}</span>
        <span><strong>Sugerida</strong>${s.categoria_sugerida}</span>
        <span><strong>Liquidez</strong>${money(s.ingresos - s.gastos)}</span>
        <span><strong>Hogar</strong>${s.miembros_hogar} personas</span>
        <span><strong>Condicion</strong>${s.condicion_especial}</span>
      </div>
      <div class="applicant-footer">
        <p>${s.universidad} - ${s.provincia}, ${s.canton}</p>
        ${includeAction ? `<button class="small-btn" data-select-applicant="${s.id}">Revisar solicitud</button>` : ""}
      </div>
    </article>
  `);

  document.getElementById(targetId).innerHTML = cards.length
    ? `<div class="applicant-grid">${cards.join("")}</div>`
    : `<div class="empty-state">No hay solicitudes registradas.</div>`;

  document.querySelectorAll("[data-select-applicant]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedApplicant = Number(button.dataset.selectApplicant);
      openView("adminBecas");
    });
  });
}

async function renderAdminBecas() {
  if (!state.applicants.length) {
    try {
      state.applicants = await api(`/solicitantes/?admin_id=${state.user.id}`);
    } catch (error) {
      state.applicants = [];
    }
  }

  const selected = state.applicants.find((s) => s.id === state.selectedApplicant) || null;
  content.innerHTML = `
    <section class="review-layout">
      <div class="panel">
        <div class="section-title">
          <div>
            <h2>Solicitudes</h2>
            <p>Seleccione un caso. La categoria sugerida se carga automaticamente en la decision.</p>
          </div>
        </div>
        <div id="grantApplicantsList"></div>
      </div>
      <div class="panel sticky-panel" id="decisionPanel">
        ${renderDecisionForm(selected)}
      </div>
    </section>
    <section class="panel">
      <h2>Becas decididas</h2>
      <div id="grantsTable"></div>
    </section>
  `;

  await loadApplicants("grantApplicantsList", true);
  renderSelectedSummary(selected);
  document.getElementById("grantForm")?.addEventListener("submit", saveGrant);
  await loadGrants();
}

function renderDecisionForm(s) {
  if (!s) {
    return `
      <h2>Decision administrativa</h2>
      <div class="empty-state">Seleccione una solicitud para ver el resumen y guardar la decision.</div>
    `;
  }

  return `
    <h2>Decision administrativa</h2>
    <div id="selectedSummary"></div>
    <form id="grantForm" class="form-grid decision-form">
      <label>ID solicitante <input name="id_solicitante" value="${s.id}" readonly></label>
      <label>Categoria
        <select name="categoria">
          ${["Beca 1", "Beca 2", "Beca 3", "Beca 4", "Beca 5"].map((c) => `<option ${c === s.categoria_sugerida ? "selected" : ""}>${c}</option>`).join("")}
        </select>
      </label>
      <label>Estado
        <select name="estado">
          <option>Aprobado</option>
          <option>Rechazado</option>
        </select>
      </label>
      <label class="wide">Descripcion de la decision <input name="descripcion" value="Indice ${s.indice_vulnerabilidad}, categoria sugerida ${s.categoria_sugerida}."></label>
      <div class="actions wide"><button type="submit" class="primary">Guardar decision</button></div>
    </form>
    <p id="grantMsg" class="message"></p>
  `;
}

function renderSelectedSummary(s) {
  const target = document.getElementById("selectedSummary");
  if (!target || !s) return;
  target.innerHTML = `
    <div class="summary-grid compact">
      <article><span>Indice</span><strong>${s.indice_vulnerabilidad}</strong></article>
      <article><span>Sugerida</span><strong>${s.categoria_sugerida}</strong></article>
      <article><span>Promedio</span><strong>${s.promedio}</strong></article>
      <article><span>Hogar</span><strong>${s.miembros_hogar}</strong></article>
    </div>
    <div class="case-detail">
      <p><strong>${s.nombre}</strong> estudia ${s.carrera} en ${s.universidad}.</p>
      <p>Ingresos: ${money(s.ingresos)} | Gastos: ${money(s.gastos)} | Dependientes: ${s.dependientes}</p>
      <p>Vivienda: ${s.vivienda} | Transporte: ${s.transporte} | Condicion: ${s.condicion_especial}</p>
      <p>Comentario: ${s.situacion_especial || "Sin comentario adicional."}</p>
    </div>
  `;
}

async function saveGrant(event) {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.target).entries());
  data.id_solicitante = Number(data.id_solicitante);
  try {
    await api(`/becas/asignar?admin_id=${state.user.id}`, { method: "PATCH", body: JSON.stringify(data) });
    setMessage("grantMsg", "Decision guardada correctamente.", true);
    state.applicants = [];
    await loadGrants();
  } catch (error) {
    setMessage("grantMsg", error.message);
  }
}

async function loadGrants() {
  const data = await api(`/becas/?usuario_id=${state.user.id}`);
  const rows = data.map((b) => `
    <tr>
      <td>${b.id}</td>
      <td>${b.id_solicitante}</td>
      <td>${b.categoria}</td>
      <td>${money(b.monto_total)}</td>
      <td>${b.estado}</td>
      <td>${b.descripcion}</td>
    </tr>
  `);
  document.getElementById("grantsTable").innerHTML = table(["ID", "Solicitante", "Categoria", "Monto", "Estado", "Descripcion"], rows);
}

async function renderReportes() {
  content.innerHTML = `
    <section class="summary-grid" id="metrics"></section>
    <section class="review-layout">
      <div class="panel"><h2>Por categoria</h2><div id="categoriaTable"></div></div>
      <div class="panel"><h2>Por estado</h2><div id="estadoTable"></div></div>
    </section>
  `;

  const gasto = await api(`/reportes/gasto-total?admin_id=${state.user.id}`);
  const categorias = await api(`/reportes/por-categoria?admin_id=${state.user.id}`);
  const estados = await api(`/reportes/por-estado?admin_id=${state.user.id}`);
  document.getElementById("metrics").innerHTML = `
    <article><span>Becas aprobadas</span><strong>${gasto.cantidad_aprobadas}</strong></article>
    <article><span>Monto aprobado</span><strong>${money(gasto.monto_total)}</strong></article>
    <article><span>Disponible</span><strong>${money(gasto.presupuesto_disponible)}</strong></article>
    <article><span>Solicitudes revisadas</span><strong>${Object.values(estados).reduce((a, b) => a + b, 0)}</strong></article>
  `;
  document.getElementById("categoriaTable").innerHTML = table(["Categoria", "Cantidad"], Object.entries(categorias).map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`));
  document.getElementById("estadoTable").innerHTML = table(["Estado", "Cantidad"], Object.entries(estados).map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`));
}

async function renderAdmins() {
  content.innerHTML = `
    <section class="panel narrow">
      <h2>Nuevo administrador</h2>
      <form id="adminForm" class="form-grid two">
        <label>Nombre <input name="nombre"></label>
        <label>Correo <input name="correo" type="text"></label>
        <label>Telefono <input name="telefono"></label>
        <label>Contrasena <input name="contrasena" type="password"></label>
        <div class="actions wide"><button class="primary" type="submit">Guardar admin</button></div>
      </form>
      <p id="adminMsg" class="message"></p>
    </section>
    <section class="panel">
      <h2>Administradores</h2>
      <div id="adminsTable"></div>
    </section>
  `;
  document.getElementById("adminForm").addEventListener("submit", saveAdmin);
  await loadAdmins();
}

async function saveAdmin(event) {
  event.preventDefault();
  try {
    await api(`/usuarios/admins?admin_id=${state.user.id}`, { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.target).entries())) });
    setMessage("adminMsg", "Administrador registrado correctamente.", true);
    event.target.reset();
    await loadAdmins();
  } catch (error) {
    setMessage("adminMsg", error.message);
  }
}

async function loadAdmins() {
  const data = await api(`/usuarios/admins?admin_id=${state.user.id}`);
  const rows = data.map((u) => `<tr><td>${u.id}</td><td>${u.nombre}</td><td>${u.correo}</td><td>${u.telefono}</td></tr>`);
  document.getElementById("adminsTable").innerHTML = table(["ID", "Nombre", "Correo", "Telefono"], rows);
}

document.getElementById("loginForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const data = await api("/auth/login", {
      method: "POST",
      body: JSON.stringify({
        correo: document.getElementById("loginEmail").value.trim(),
        contrasena: document.getElementById("loginPass").value.trim()
      })
    });
    saveSession(data.usuario);
    state.view = data.usuario.rol === "admin" ? "adminSolicitantes" : "perfil";
    setMessage("loginMsg", "");
    render();
  } catch (error) {
    setMessage("loginMsg", error.message);
  }
});

document.getElementById("logoutBtn").addEventListener("click", () => {
  clearSession();
  render();
});

const studentDialog = document.getElementById("studentDialog");
document.getElementById("openStudentRegister").addEventListener("click", () => studentDialog.showModal());
document.getElementById("closeStudentDialog").addEventListener("click", () => studentDialog.close());

document.getElementById("studentRegisterForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await api("/usuarios/estudiantes", { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.target).entries())) });
    setMessage("studentRegisterMsg", "Cuenta creada. Ingresa con ese correo y contrasena.", true);
    event.target.reset();
  } catch (error) {
    setMessage("studentRegisterMsg", error.message);
  }
});

const recoverDialog = document.getElementById("recoverDialog");
document.getElementById("openRecoverDialog").addEventListener("click", () => recoverDialog.showModal());
document.getElementById("closeRecoverDialog").addEventListener("click", () => recoverDialog.close());

document.getElementById("recoverForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await api("/auth/recuperar-contrasena", { method: "PATCH", body: JSON.stringify(Object.fromEntries(new FormData(event.target).entries())) });
    setMessage("recoverMsg", "Contrasena actualizada correctamente.", true);
    event.target.reset();
  } catch (error) {
    setMessage("recoverMsg", error.message);
  }
});

render();

