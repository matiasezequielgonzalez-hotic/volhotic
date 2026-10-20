/**
 * Bot de stock Volhotic: servidor.
 *
 * Buscador (sin IA) sobre la hoja General de vol_ml_listings(No_tocar).
 * Funciones públicas que llama la pantalla (BotUI.html) con google.script.run:
 *   botBuscar(texto, linea)            -> { fichas, total, modo, nota, sugerencias }
 *   botDetalle(id)                     -> ficha
 *   botNoLoEncontre(id)                -> { ok, mensaje }
 *   botCorregirUbicacion(id, pisoVisto, zonaVista, pisoNuevo, zonaNueva) -> { ok, mensaje, ficha }
 *   botOpcionesUbicacion()             -> { pisos, zonas }
 *   botInicio()                        -> { nombre, avatar, lineas, puedeUbicar, verPrecios }
 *
 * Integración con tu app:
 *   1. Reemplazá botEmailActual_() por como tu app sabe quién está logueado.
 *   2. En tu doGet:  if (e.parameter.v === 'bot') return botPagina();
 *      o incluí BotUI.html dentro de tu propia página con botInclude('BotUI').
 */

const BOT = {
  // Si el proyecto está vinculado a la planilla, se puede usar SpreadsheetApp.getActive().
  PLANILLA_ID: '1Ui77_spb9OF4fuuTpxN-eatZdpZI5Yw277KcZRuOiTw', // vol_ml_listings(No_tocar)
  HOJAS: {
    stock: 'General',
    publicaciones: 'Publicaciones',
    precios: 'Precios',
    recuentos: 'Recuentos',
    decisiones: 'Decisiones',
    sinonimos: 'Sinonimos',
    equipo: 'Equipo',
    permisos: 'Permisos',
    config: 'Config',
  },
  SECCION_CONSULTAS: 'consultas',
  SECCION_PRECIOS: 'precios',
  SECCION_UBICAR: 'ubicar',
  MAX_FICHAS: 5,
  CACHE_SEGUNDOS: 600,
  DIAS_PRECIO_VIEJO: 30,
  ZONA_HORARIA: 'America/Argentina/Buenos_Aires',
  ESTADO_RECUENTO_PENDIENTE: 'Pendiente',
  // Estados de ML en los que no se muestra el link.
  ESTADOS_ML_INACTIVOS: ['paus', 'final', 'closed', 'inactiv', 'under_review'],
};

// Cómo se reconoce cada línea. La primera regla que coincide gana; el resto es Autopartes.
const BOT_LINEAS = [
  { linea: 'SEX', soloSexAdmin: true, coincide: (f) => f.marca === 'sexhotic' },
  { linea: 'Pet', coincide: (f) => f.skuNorm.startsWith('bio') },
  { linea: 'Tecnología', coincide: (f) => f.skuNorm.startsWith('tec') },
];
const BOT_LINEA_DEFECTO = 'Autopartes';

const BOT_STOPWORDS = new Set([
  'de', 'del', 'la', 'el', 'los', 'las', 'para', 'con', 'por', 'y', 'a', 'en', 'un', 'una',
  'unos', 'unas', 'al', 'x', 'tenes', 'tienen', 'hay', 'tengo', 'busco', 'necesito',
]);

// Columnas de la hoja General que usa el bot (por nombre de encabezado, no por posición).
const BOT_COLS = {
  id: 'ID', descripcion: 'Descripcion', sku: 'SKU', stock: 'Stock', marca: 'Marca', oem: 'EAN',
  condicion: 'Condicion', deposito: 'Deposito', ubicacion: 'Ubicacion', piso: 'Piso', zona: 'Zona',
  estado: 'Estado', estadoMl: 'Estado_ML', observacion: 'Observación', carpetaFotos: 'Carpeta_Fotos',
};

// ---------------------------------------------------------------------------
// Usuario y permisos
// ---------------------------------------------------------------------------

/** Reemplazá esto por como tu app identifica al usuario (sesión, token, etc.). */
function botEmailActual_() {
  return Session.getActiveUser().getEmail();
}

function botUsuario_() {
  const email = String(botEmailActual_() || '').trim().toLowerCase();
  if (!email) throw new Error('No pudimos identificarte. Entrá con tu Gmail.');

  const equipo = botTabla_(BOT.HOJAS.equipo);
  const fila = equipo.filas.find((f) => String(equipo.get(f, 'Email')).trim().toLowerCase() === email);
  if (!fila || String(equipo.get(fila, 'Activo')).trim().toUpperCase() === 'NO') {
    throw new Error('Tu Gmail no está en el equipo. Pedile acceso a un admin.');
  }
  const nombre = String(equipo.get(fila, 'Nombre')).trim();
  const foto = String(equipo.get(fila, 'Foto')).trim();
  const icono = String(equipo.get(fila, 'Icono')).trim();
  const esAdmin = String(equipo.get(fila, 'Rol')).trim().toLowerCase() === 'admin';

  const permisos = botTabla_(BOT.HOJAS.permisos);
  const filaPermisos = permisos.filas.find((f) => String(permisos.get(f, 'Nombre')).trim() === nombre);
  const secciones = new Set(
    String(filaPermisos ? permisos.get(filaPermisos, 'Secciones') : '')
      .split(',').map((s) => s.trim().toLowerCase()).filter(Boolean)
  );

  const sexAdmins = String(botConfig_('SEX_ADMIN') || '').split(',').map((s) => s.trim().toLowerCase());
  const puede = (seccion) => esAdmin || secciones.has(seccion);
  return {
    email, nombre, esAdmin, foto, icono,
    consultas: puede(BOT.SECCION_CONSULTAS),
    verPrecios: puede(BOT.SECCION_PRECIOS),
    puedeUbicar: puede(BOT.SECCION_UBICAR),
    sexAdmin: sexAdmins.includes(email),
  };
}

function botExigir_(permiso) {
  const u = botUsuario_();
  if (!u.consultas) throw new Error('No tenés habilitada la sección Consultas.');
  if (permiso && !u[permiso]) throw new Error('No tenés permiso para esta acción.');
  return u;
}

// ---------------------------------------------------------------------------
// Lectura de la planilla
// ---------------------------------------------------------------------------

let botPlanillaMemo_ = null;
function botPlanilla_() {
  if (!botPlanillaMemo_) botPlanillaMemo_ = SpreadsheetApp.openById(BOT.PLANILLA_ID);
  return botPlanillaMemo_;
}

/** Lee una hoja como texto (getDisplayValues mantiene los ceros: "09600"). */
function botTabla_(nombreHoja) {
  const hoja = botPlanilla_().getSheetByName(nombreHoja);
  if (!hoja) return { hoja: null, enc: {}, filas: [], get: () => '' };
  const valores = hoja.getDataRange().getDisplayValues();
  const enc = {};
  (valores[0] || []).forEach((h, i) => { enc[String(h).trim()] = i; });
  return {
    hoja, enc, filas: valores.slice(1),
    get: (fila, columna) => (columna in enc ? fila[enc[columna]] : ''),
  };
}

function botConfig_(clave) {
  const t = botTabla_(BOT.HOJAS.config);
  const fila = t.filas.find((f) => String(t.get(f, 'Clave')).trim() === clave);
  return fila ? t.get(fila, 'Valor') : '';
}

// ---------------------------------------------------------------------------
// Normalización y sinónimos
// ---------------------------------------------------------------------------

function botNormalizar_(texto) {
  return String(texto || '').normalize('NFD').replace(/[̀-ͯ]/g, '')
    .toLowerCase().replace(/\s+/g, ' ').trim();
}

/** "1J0 411-336/H" -> "1j0411336h" */
function botNormalizarCodigo_(texto) {
  return botNormalizar_(texto).replace(/[^a-z0-9]/g, '');
}

/** Plural simple: "amortiguadores" -> "amortiguador". */
function botRaiz_(palabra) {
  if (palabra.length > 4 && palabra.endsWith('es')) return palabra.slice(0, -2);
  if (palabra.length > 3 && palabra.endsWith('s')) return palabra.slice(0, -1);
  return palabra;
}

/** Hoja Sinonimos: Palabra | Equivale_a. Palabras sueltas (sin espacios). */
function botSinonimos_() {
  const t = botTabla_(BOT.HOJAS.sinonimos);
  const mapa = {};
  t.filas.forEach((f) => {
    const palabra = botNormalizar_(t.get(f, 'Palabra'));
    const equivale = botNormalizar_(t.get(f, 'Equivale_a'));
    if (palabra && equivale && !palabra.includes(' ')) mapa[botRaiz_(palabra)] = equivale;
  });
  return mapa;
}

function botCanonizar_(texto, sinonimos) {
  return botNormalizar_(texto).split(' ')
    .map((w) => sinonimos[botRaiz_(w)] || w).join(' ');
}

// ---------------------------------------------------------------------------
// Índice (se guarda en caché para no leer la planilla en cada búsqueda)
// ---------------------------------------------------------------------------

const BOT_CAMPOS = ['id', 'descripcion', 'sku', 'stock', 'marca', 'oem', 'condicion', 'deposito',
  'ubicacion', 'piso', 'zona', 'estado', 'estadoMl', 'observacion', 'carpetaFotos', 'linkMl',
  'linea', 'texto', 'codigos'];
const BOT_BLOQUE = 400; // filas por clave de caché (CacheService admite 100 KB por clave)

let botIndiceMemo_ = null;

function botIndice_() {
  if (botIndiceMemo_) return botIndiceMemo_;
  const cache = CacheService.getScriptCache();
  const meta = cache.get('bot_indice_meta');
  if (meta) {
    const bloques = Number(meta);
    const claves = Array.from({ length: bloques }, (_, i) => 'bot_indice_' + i);
    const partes = cache.getAll(claves);
    if (claves.every((k) => partes[k])) {
      botIndiceMemo_ = claves.flatMap((k) => JSON.parse(partes[k])).map(botDesempacar_);
      return botIndiceMemo_;
    }
  }
  const items = botConstruirIndice_();
  const empacados = items.map(botEmpacar_);
  const aGuardar = {};
  for (let i = 0; i * BOT_BLOQUE < empacados.length; i++) {
    aGuardar['bot_indice_' + i] = JSON.stringify(empacados.slice(i * BOT_BLOQUE, (i + 1) * BOT_BLOQUE));
  }
  try {
    cache.putAll(aGuardar, BOT.CACHE_SEGUNDOS);
    cache.put('bot_indice_meta', String(Object.keys(aGuardar).length), BOT.CACHE_SEGUNDOS);
  } catch (e) {
    console.warn('No se pudo guardar el índice en caché: ' + e); // sigue funcionando sin caché
  }
  botIndiceMemo_ = items;
  return items;
}

function botInvalidarIndice_() {
  botIndiceMemo_ = null;
  CacheService.getScriptCache().remove('bot_indice_meta');
}

function botEmpacar_(item) { return BOT_CAMPOS.map((c) => item[c]); }
function botDesempacar_(arr) {
  const item = {};
  BOT_CAMPOS.forEach((c, i) => { item[c] = arr[i]; });
  return item;
}

function botConstruirIndice_() {
  const sinonimos = botSinonimos_();
  const links = botLinksMl_();
  const t = botTabla_(BOT.HOJAS.stock);
  const items = [];
  t.filas.forEach((fila) => {
    const f = {};
    Object.keys(BOT_COLS).forEach((campo) => { f[campo] = String(t.get(fila, BOT_COLS[campo]) || '').trim(); });
    if (!f.descripcion || f.descripcion === 'Descripcion') return; // vacías y encabezados repetidos
    const m = f.stock.match(/-?\d+/);
    f.stock = m ? Number(m[0]) : 0; // "1 caja" -> 1
    const skuNorm = botNormalizarCodigo_(f.sku);
    const regla = BOT_LINEAS.find((r) => r.coincide({ marca: botNormalizar_(f.marca), skuNorm }));
    f.linea = regla ? regla.linea : BOT_LINEA_DEFECTO;
    f.linkMl = links[skuNorm] || '';
    f.texto = botCanonizar_([f.descripcion, f.marca, f.sku, f.oem].join(' '), sinonimos);
    f.codigos = '|' + [f.id, f.sku, f.oem].map(botNormalizarCodigo_).join('|') + '|';
    items.push(f);
  });
  return items;
}

/** Publicaciones activas: SKU normalizado -> link de Mercado Libre. */
function botLinksMl_() {
  const t = botTabla_(BOT.HOJAS.publicaciones);
  const links = {};
  t.filas.forEach((f) => {
    const sku = botNormalizarCodigo_(t.get(f, 'SKU'));
    const mla = String(t.get(f, 'MLA')).toUpperCase().replace(/-/g, '');
    const estado = String(t.get(f, 'Estado_ML')).toLowerCase();
    if (!sku || !/^MLA\d+$/.test(mla) || BOT.ESTADOS_ML_INACTIVOS.some((e) => estado.includes(e))) return;
    if (!links[sku]) links[sku] = 'https://articulo.mercadolibre.com.ar/MLA-' + mla.slice(3);
  });
  return links;
}

/** Hoja Precios: ID | SKU | Precio | Moneda | Actualizado | Quien */
function botPrecios_() {
  const t = botTabla_(BOT.HOJAS.precios);
  const porId = {};
  const porSku = {};
  t.filas.forEach((f) => {
    const precio = String(t.get(f, 'Precio')).trim();
    if (!precio) return;
    const dato = { precio, moneda: t.get(f, 'Moneda') || 'ARS', actualizado: t.get(f, 'Actualizado') };
    const id = botNormalizarCodigo_(t.get(f, 'ID'));
    const sku = botNormalizarCodigo_(t.get(f, 'SKU'));
    if (id) porId[id] = dato;
    if (sku) porSku[sku] = dato;
  });
  return { porId, porSku };
}

// ---------------------------------------------------------------------------
// Búsqueda
// ---------------------------------------------------------------------------

/** "1J0411336H", "415 0491 09", "1j0-411 336/h": todas las partes tienen algún número. */
function botPareceCodigo_(texto) {
  const partes = String(texto).trim().split(/\s+/);
  return partes.every((p) => /\d/.test(p)) && botNormalizarCodigo_(texto).length >= 5;
}

function botVisibles_(u, linea) {
  return botIndice_().filter((f) =>
    (f.linea !== 'SEX' || u.sexAdmin) && (!linea || linea === 'Todo' || f.linea === linea));
}

function botBuscarPorCodigo_(items, texto) {
  const codigo = botNormalizarCodigo_(texto);
  if (codigo.length < 3) return [];
  const exacto = '|' + codigo + '|';
  return items.filter((f) => f.codigos.includes(codigo))
    .sort((a, b) => (b.codigos.includes(exacto) - a.codigos.includes(exacto)) || (b.stock - a.stock));
}

function botBuscarPorPalabras_(items, texto) {
  const sinonimos = botSinonimos_();
  const palabras = botCanonizar_(texto, sinonimos).split(' ')
    .map((w) => botRaiz_(w.replace(/[^a-z0-9./-]/g, '')))
    .filter((w) => w && !BOT_STOPWORDS.has(w));
  if (!palabras.length) return { resultados: [], palabras };
  const resultados = items.filter((f) => palabras.every((p) => f.texto.includes(p)));
  const exacta = (p) => new RegExp('(?<![a-z0-9])' + p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?:e?s)?(?![a-z0-9])');
  const puntaje = (f) => [
    palabras.filter((p) => exacta(p).test(f.texto)).length, // "gol" antes que "golf"
    f.stock > 0 ? 1 : 0,
    f.texto.startsWith(palabras[0]) ? 1 : 0,
    -f.texto.length,
  ];
  resultados.sort((a, b) => {
    const pa = puntaje(a), pb = puntaje(b);
    for (let i = 0; i < pa.length; i++) if (pa[i] !== pb[i]) return pb[i] - pa[i];
    return 0;
  });
  return { resultados, palabras };
}

/** Las 3 descripciones que comparten más palabras, para cuando no hay resultados. */
function botSugerencias_(items, palabras) {
  const vistas = new Set();
  return items
    .map((f) => ({ f, n: palabras.filter((p) => f.texto.includes(p)).length }))
    .filter((x) => x.n > 0)
    .sort((a, b) => b.n - a.n || b.f.stock - a.f.stock)
    .map((x) => x.f.descripcion)
    .filter((d) => !vistas.has(d) && vistas.add(d))
    .slice(0, 3);
}

function botBuscar(texto, linea) {
  const u = botExigir_();
  texto = String(texto || '').trim();
  if (!texto) return { fichas: [], total: 0, modo: 'palabras', sugerencias: [] };
  const items = botVisibles_(u, linea);

  let modo = 'palabras';
  let resultados = [];
  let palabras = [];
  if (botPareceCodigo_(texto)) {
    resultados = botBuscarPorCodigo_(items, texto);
    if (resultados.length) modo = 'codigo';
  }
  if (!resultados.length) ({ resultados, palabras } = botBuscarPorPalabras_(items, texto));

  const precios = u.verPrecios ? botPrecios_() : null;
  const respuesta = {
    fichas: resultados.slice(0, BOT.MAX_FICHAS).map((f) => botFicha_(f, u, precios)),
    total: resultados.length,
    modo,
    sugerencias: resultados.length ? [] : botSugerencias_(items, palabras),
    nota: '',
  };
  if (/bilstein/i.test(texto)) {
    respuesta.nota = 'Si es Bilstein, está en planta baja y no figura acá, es de Fabián (Bilstein Performance): no se toca.';
  }
  return respuesta;
}

function botDetalle(id) {
  const u = botExigir_();
  const f = botVisibles_(u).find((x) => x.id === id);
  if (!f) throw new Error('No encontré el producto ' + id + '.');
  return botFicha_(f, u, u.verPrecios ? botPrecios_() : null);
}

function botFicha_(f, u, precios) {
  const avisos = [];
  if (/sin stock/i.test(f.ubicacion) && f.stock > 0) avisos.push('Dice SIN STOCK pero figura con ' + f.stock);
  if (!f.piso && !f.zona) avisos.push('Sin ubicación');
  if (/no encontrado/i.test(f.estado)) avisos.push('No encontrado en el relevamiento');

  const ficha = {
    id: f.id, descripcion: f.descripcion, marca: f.marca, condicion: f.condicion, stock: f.stock,
    linea: f.linea, sku: f.sku, oem: f.oem, deposito: f.deposito, piso: f.piso, zona: f.zona,
    estado: f.estado, estadoMl: f.estadoMl, linkMl: f.linkMl, observacion: f.observacion,
    carpetaFotos: f.carpetaFotos, avisos, puedeUbicar: u.puedeUbicar,
  };
  if (precios) {
    const p = precios.porId[botNormalizarCodigo_(f.id)] || precios.porSku[botNormalizarCodigo_(f.sku)];
    if (p) {
      ficha.precio = p.precio;
      ficha.moneda = p.moneda;
      ficha.precioActualizado = p.actualizado;
      const fecha = botParsearFecha_(p.actualizado);
      if (fecha && (Date.now() - fecha.getTime()) / 864e5 > BOT.DIAS_PRECIO_VIEJO) avisos.push('Precio viejo');
    } else {
      ficha.precio = null; // la pantalla muestra "sin precio cargado"
    }
  }
  return ficha;
}

/** "15/10/2026" o "15/10/2026 9:45:53" -> Date */
function botParsearFecha_(texto) {
  const m = String(texto || '').match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})/);
  return m ? new Date(Number(m[3]), Number(m[2]) - 1, Number(m[1])) : null;
}

// ---------------------------------------------------------------------------
// Acciones
// ---------------------------------------------------------------------------

function botAhora_() {
  return Utilities.formatDate(new Date(), BOT.ZONA_HORARIA, 'dd/MM/yyyy H:mm:ss');
}

/** Agrega una fila a una hoja respetando el orden de sus encabezados. */
function botAgregarFila_(nombreHoja, datos) {
  const t = botTabla_(nombreHoja);
  if (!t.hoja) throw new Error('Falta la hoja ' + nombreHoja + '.');
  const fila = new Array(Object.keys(t.enc).length).fill('');
  Object.keys(datos).forEach((col) => { if (col in t.enc) fila[t.enc[col]] = datos[col]; });
  t.hoja.appendRow(fila);
}

function botNoLoEncontre(id) {
  const u = botExigir_();
  const f = botVisibles_(u).find((x) => x.id === id);
  if (!f) throw new Error('No encontré el producto ' + id + '.');

  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const t = botTabla_(BOT.HOJAS.recuentos);
    const yaPedido = t.filas.some((r) =>
      String(t.get(r, 'ID')).trim() === id &&
      String(t.get(r, 'Estado')).trim().toLowerCase() === BOT.ESTADO_RECUENTO_PENDIENTE.toLowerCase());
    if (yaPedido) return { ok: true, mensaje: 'Ya había un recuento pendiente para ' + id + '.' };
    botAgregarFila_(BOT.HOJAS.recuentos, {
      Fecha: botAhora_(), ID: id, Motivo: 'No lo encontré (bot)', Pedido_por: u.nombre,
      Estado: BOT.ESTADO_RECUENTO_PENDIENTE,
    });
  } finally {
    lock.releaseLock();
  }
  return { ok: true, mensaje: 'Listo, pedí un recuento de ' + f.descripcion + '.' };
}

function botOpcionesUbicacion() {
  botExigir_('puedeUbicar');
  const pisos = new Set();
  const zonas = new Set();
  botIndice_().forEach((f) => {
    if (f.piso) pisos.add(f.piso);
    if (f.zona) zonas.add(f.zona);
  });
  const orden = (a, b) => a.localeCompare(b, 'es', { numeric: true });
  return { pisos: [...pisos].sort(orden), zonas: [...zonas].sort(orden) };
}

function botCorregirUbicacion(id, pisoVisto, zonaVista, pisoNuevo, zonaNueva) {
  const u = botExigir_('puedeUbicar');
  pisoNuevo = String(pisoNuevo || '').trim();
  zonaNueva = String(zonaNueva || '').trim();
  const opciones = botOpcionesUbicacion();
  if (pisoNuevo && !opciones.pisos.includes(pisoNuevo)) throw new Error('El piso ' + pisoNuevo + ' no existe.');
  if (zonaNueva && !opciones.zonas.includes(zonaNueva)) throw new Error('La zona ' + zonaNueva + ' no existe.');

  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const t = botTabla_(BOT.HOJAS.stock);
    const colId = t.enc[BOT_COLS.id];
    // Se busca por ID y no por número de fila: si alguien ordenó la hoja, la fila cambia.
    const celda = t.hoja.getRange(2, colId + 1, Math.max(t.hoja.getLastRow() - 1, 1), 1)
      .createTextFinder(id).matchEntireCell(true).findNext();
    if (!celda) throw new Error('No encontré el producto ' + id + ' en General.');
    const fila = celda.getRow();
    const rPiso = t.hoja.getRange(fila, t.enc[BOT_COLS.piso] + 1);
    const rZona = t.hoja.getRange(fila, t.enc[BOT_COLS.zona] + 1);
    const pisoActual = rPiso.getDisplayValue().trim();
    const zonaActual = rZona.getDisplayValue().trim();
    if (pisoActual !== String(pisoVisto || '').trim() || zonaActual !== String(zonaVista || '').trim()) {
      return { ok: false, mensaje: 'Alguien la cambió recién: ahora está en piso ' + (pisoActual || '—') +
        ', zona ' + (zonaActual || '—') + '. Revisá y probá de nuevo.' };
    }
    rPiso.setValue(pisoNuevo);
    rZona.setValue(zonaNueva);
    botAgregarFila_(BOT.HOJAS.decisiones, {
      Fecha: botAhora_(), Tipo: 'UBICACION', Ref: id, Valor: pisoNuevo + '|' + zonaNueva,
      Detalle: 'antes ' + (pisoActual || '—') + '|' + (zonaActual || '—') + ' · desde el bot',
      Quien: u.nombre, Persona: u.email,
    });
  } finally {
    lock.releaseLock();
  }
  botInvalidarIndice_();
  return { ok: true, mensaje: 'Ubicación actualizada.', ficha: botDetalle(id) };
}

// ---------------------------------------------------------------------------
// Avatar de cada persona (hoja Equipo: Foto, Icono)
// ---------------------------------------------------------------------------

const BOT_COLORES_AVATAR = ['#5ef2c4', '#7fb0ea', '#f2b84b', '#ff8a80', '#c39bf2', '#7fe08a'];
const BOT_MAX_FOTO_BYTES = 300 * 1024;

/**
 * Foto si hay (link o ID de Drive, o data:image...), si no el emoji de Icono,
 * si no las iniciales con un color fijo por persona.
 */
function botAvatarPersona_(u) {
  const src = botFotoEquipo_(u.foto);
  if (src) return { tipo: 'foto', src };
  const icono = u.icono && !/^(no|si|sí)$/i.test(u.icono) ? u.icono : '';
  const color = BOT_COLORES_AVATAR[[...u.nombre].reduce((a, c) => a + c.charCodeAt(0), 0) % BOT_COLORES_AVATAR.length];
  if (icono) return { tipo: 'icono', texto: icono, color };
  const iniciales = u.nombre.split(/\s+/).map((p) => p[0] || '').join('').slice(0, 2).toUpperCase();
  return { tipo: 'iniciales', texto: iniciales, color };
}

/** Convierte la celda Foto en una imagen que el navegador pueda mostrar sin pedir permisos de Drive. */
function botFotoEquipo_(valor) {
  valor = String(valor || '').trim();
  if (!valor) return '';
  if (/^data:image\//.test(valor)) return valor;
  const m = valor.match(/\/d\/([\w-]{20,})/) || valor.match(/[?&]id=([\w-]{20,})/) || valor.match(/^([\w-]{20,})$/);
  if (!m) return '';
  const cache = CacheService.getScriptCache();
  const clave = 'bot_foto_' + m[1];
  const guardada = cache.get(clave);
  if (guardada) return guardada;
  try {
    const blob = DriveApp.getFileById(m[1]).getBlob();
    if (blob.getBytes().length > BOT_MAX_FOTO_BYTES) {
      console.warn('La foto ' + m[1] + ' pesa más de 300 KB; subí una más chica (256 px alcanza).');
      return '';
    }
    const src = 'data:' + blob.getContentType() + ';base64,' + Utilities.base64Encode(blob.getBytes());
    if (src.length < 100000) cache.put(clave, src, 21600);
    return src;
  } catch (e) {
    console.warn('No se pudo leer la foto ' + m[1] + ': ' + e);
    return '';
  }
}

// ---------------------------------------------------------------------------
// Pantalla
// ---------------------------------------------------------------------------

function botInicio() {
  const u = botExigir_();
  const lineas = ['Todo', BOT_LINEA_DEFECTO].concat(
    BOT_LINEAS.filter((r) => !r.soloSexAdmin || u.sexAdmin).map((r) => r.linea));
  return {
    nombre: u.nombre, avatar: botAvatarPersona_(u), lineas,
    puedeUbicar: u.puedeUbicar, verPrecios: u.verPrecios,
  };
}

function botPagina() {
  return HtmlService.createTemplateFromFile('BotUI').evaluate()
    .setTitle('Consultas de stock')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function botInclude(nombre) {
  return HtmlService.createHtmlOutputFromFile(nombre).getContent();
}
