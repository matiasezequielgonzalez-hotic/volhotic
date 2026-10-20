/**
 * hottie, la bot de stock de Volhotic: servidor.
 *
 * Buscador (sin IA) sobre la hoja General de vol_ml_listings(No_tocar).
 * Funciones públicas que llama la pantalla (BotUI.html) con google.script.run:
 *   botBuscar(texto, linea)            -> { fichas, total, modo, nota, sugerencias }
 *   botDetalle(id)                     -> ficha
 *   botNoLoEncontre(id)                -> { ok, mensaje }
 *   botCorregirUbicacion(id, pisoVisto, zonaVista, pisoNuevo, zonaNueva) -> { ok, mensaje, ficha }
 *   botOpcionesUbicacion()             -> { pisos, zonas }
 *   botInicio()                        -> { nombre, avatar, lineas, puedeUbicar, verPrecios }
 *   botSalaInicio()                    -> datos del Modo Sala: jugador, XP, nivel, zonas, ranking
 *   botSumarXP(accion, ref)            -> { ganado, total, nivel } (solo 'encontrado' y 'despachado')
 *   botSalaLatido(estado)              -> sala compartida: { jugadores, eventos, desafio } (cada ~2 s)
 *   botSalaResponder(desafioId, zona)  -> { ok, correcta, mensaje, xp }
 *   botSalaNuevoPedido(zonas)          -> pedido de práctica: productos reales, etiquetas parecidas, envío
 *   botSalaCompletarPedido(id, errores)-> { xp } (+25 sin errores, +10 con errores)
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
    xp: 'BotXP', // Fecha | Nombre | Accion | Ref | XP  (la crea el bot si no existe)
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
// Si la hoja tiene columna Linea, manda esa (Sexhotic siempre pasa a SEX, solo para SEX_ADMIN).
const BOT_LINEAS = [
  { linea: 'SEX', soloSexAdmin: true, coincide: (f) => f.marca === 'sexhotic' || f.linea.includes('sex') || f.cuenta.includes('sexhotic') },
  { linea: 'Pet', coincide: (f) => !f.linea && f.skuNorm.startsWith('bio') },
  { linea: 'Tecnología', coincide: (f) => !f.linea && f.skuNorm.startsWith('tec') },
];
const BOT_LINEA_DEFECTO = 'Autopartes';

const BOT_STOPWORDS = new Set([
  'de', 'del', 'la', 'el', 'los', 'las', 'para', 'con', 'por', 'y', 'a', 'en', 'un', 'una',
  'unos', 'unas', 'al', 'x', 'tenes', 'tienen', 'hay', 'tengo', 'busco', 'necesito',
  // Charla que se cuela en las búsquedas: "hola hottie, ¿dónde está el disco de gol?"
  'hola', 'hottie', 'buenas', 'che', 'donde', 'esta', 'estan', 'queda', 'quedan', 'me', 'pasas', 'pasame',
  'porfa', 'favor', 'tenemos', 'algun', 'alguno', 'alguna', 'quiero', 'dame', 'sabes',
]);

// Columnas de la hoja General que usa el bot (por nombre de encabezado, no por posición).
// Si una columna tiene varios nombres posibles, se usa el primero que exista en la hoja
// (sirve para la hoja General vieja y para el inventario nuevo con "Producto", "EAN / OEM" y "Linea").
const BOT_COLS = {
  id: 'ID', descripcion: ['Descripcion', 'Producto'], sku: 'SKU', stock: 'Stock', marca: 'Marca', oem: ['EAN', 'EAN / OEM', 'OEM'],
  condicion: 'Condicion', deposito: 'Deposito', ubicacion: 'Ubicacion', piso: 'Piso', zona: 'Zona',
  estado: 'Estado', estadoMl: ['Estado_ML', 'En ML'], observacion: 'Observación', carpetaFotos: 'Carpeta_Fotos',
  lineaHoja: ['Linea', 'Línea'], cuenta: 'Cuenta',
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
  // La sala pregunta cada 2 segundos: el usuario se guarda 5 minutos en caché.
  const cache = CacheService.getScriptCache();
  const guardado = cache.get('bot_u_' + email);
  if (guardado) return JSON.parse(guardado);
  const u = botLeerUsuario_(email);
  cache.put('bot_u_' + email, JSON.stringify(u), 300);
  return u;
}

function botLeerUsuario_(email) {
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
  if (!hoja) return { hoja: null, enc: {}, filas: [], col: () => -1, get: () => '' };
  const valores = hoja.getDataRange().getDisplayValues();
  const enc = {};
  (valores[0] || []).forEach((h, i) => { enc[String(h).trim()] = i; });
  // columna: un nombre o una lista de nombres posibles (gana el primero que exista).
  const col = (columna) => {
    const n = [].concat(columna).find((c) => c in enc);
    return n === undefined ? -1 : enc[n];
  };
  return {
    hoja, enc, col, filas: valores.slice(1),
    get: (fila, columna) => { const i = col(columna); return i < 0 ? '' : fila[i]; },
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
    if (!f.descripcion || f.descripcion === 'Descripcion' || f.descripcion === 'Producto') return; // vacías y encabezados repetidos
    const m = f.stock.match(/-?\d+/);
    f.stock = m ? Number(m[0]) : 0; // "1 caja" -> 1
    const skuNorm = botNormalizarCodigo_(f.sku);
    const regla = BOT_LINEAS.find((r) => r.coincide({
      marca: botNormalizar_(f.marca), skuNorm, linea: botNormalizar_(f.lineaHoja), cuenta: botNormalizar_(f.cuenta) }));
    f.linea = regla ? regla.linea : (f.lineaHoja || BOT_LINEA_DEFECTO);
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
  // Las palabras vacías se sacan antes y después del singular ("tenes" -> "ten", "buenas" -> "buena").
  const palabras = botCanonizar_(texto, sinonimos).split(' ')
    .map((w) => w.replace(/[^a-z0-9./-]/g, ''))
    .filter((w) => w && !BOT_STOPWORDS.has(w))
    .map(botRaiz_)
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
  const xp = botDarXp_(u, 'reporte', id);
  return { ok: true, mensaje: 'Listo, pedí un recuento de ' + f.descripcion + '.', xp };
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
    const colId = t.col(BOT_COLS.id);
    // Se busca por ID y no por número de fila: si alguien ordenó la hoja, la fila cambia.
    const celda = t.hoja.getRange(2, colId + 1, Math.max(t.hoja.getLastRow() - 1, 1), 1)
      .createTextFinder(id).matchEntireCell(true).findNext();
    if (!celda) throw new Error('No encontré el producto ' + id + ' en General.');
    const fila = celda.getRow();
    const rPiso = t.hoja.getRange(fila, t.col(BOT_COLS.piso) + 1);
    const rZona = t.hoja.getRange(fila, t.col(BOT_COLS.zona) + 1);
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
  const xp = botDarXp_(u, 'ubicado', id);
  return { ok: true, mensaje: 'Ubicación actualizada.', ficha: botDetalle(id), xp };
}

// ---------------------------------------------------------------------------
// XP del Modo Sala
// ---------------------------------------------------------------------------

const BOT_XP = {
  encontrado: 10, despachado: 5, reporte: 3, ubicado: 15, desafio: 20, limpieza: 2,
  pedido: 25,       // venta despachada sin errores y antes del corte
  pedido_err: 10,   // despachada a tiempo, con errores que se corrigieron en el camino
  pedido_tarde: 5,  // despachada después del horario de corte (en ML sería una venta demorada)
  criterio: 15,     // frenó una venta que necesitaba al encargado (no se despacha algo distinto a lo vendido)
  pregunta: 3,      // pregunta rápida de hottie bien respondida (repaso espaciado)
};
// Lo que la pantalla puede pedir directamente. Reporte y ubicado los suma el servidor
// al hacer la acción real, así nadie se los puede dar sin hacerla.
const BOT_XP_DESDE_CLIENTE = ['encontrado', 'despachado', 'limpieza', 'pregunta'];
// Topes diarios por acción (además del tope general).
const BOT_XP_TOPE_ACCION = { limpieza: 20, pregunta: 30 };
const BOT_XP_TOPE_DIARIO = 300;

function botHojaXp_() {
  const planilla = botPlanilla_();
  let hoja = planilla.getSheetByName(BOT.HOJAS.xp);
  if (!hoja) {
    hoja = planilla.insertSheet(BOT.HOJAS.xp);
    hoja.appendRow(['Fecha', 'Nombre', 'Accion', 'Ref', 'XP']);
  }
  return hoja;
}

function botNivel_(xp) {
  // Nivel n necesita 50·(n-1)² XP: 0, 50, 200, 450, 800…
  const nivel = Math.floor(Math.sqrt(xp / 50)) + 1;
  return { nivel, desde: 50 * (nivel - 1) ** 2, hasta: 50 * nivel ** 2 };
}

/** Totales de XP: { total: {nombre: xp}, semana: {nombre: xp}, hoy: {nombre: {xp, claves:Set}} } */
function botTotalesXp_() {
  botHojaXp_();
  const t = botTabla_(BOT.HOJAS.xp);
  const hoy = Utilities.formatDate(new Date(), BOT.ZONA_HORARIA, 'dd/MM/yyyy');
  const ahora = new Date();
  const lunes = new Date(ahora.getFullYear(), ahora.getMonth(), ahora.getDate() - ((ahora.getDay() + 6) % 7));
  const total = {}, semana = {}, delDia = {};
  t.filas.forEach((f) => {
    const nombre = String(t.get(f, 'Nombre')).trim();
    const xp = Number(t.get(f, 'XP')) || 0;
    const fechaTxt = String(t.get(f, 'Fecha'));
    total[nombre] = (total[nombre] || 0) + xp;
    const fecha = botParsearFecha_(fechaTxt);
    if (fecha && fecha >= lunes) semana[nombre] = (semana[nombre] || 0) + xp;
    if (fechaTxt.startsWith(hoy)) {
      const d = delDia[nombre] || (delDia[nombre] = { xp: 0, claves: new Set(), porAccion: {} });
      const accion = String(t.get(f, 'Accion'));
      d.xp += xp;
      d.porAccion[accion] = (d.porAccion[accion] || 0) + xp;
      d.claves.add(accion + '|' + t.get(f, 'Ref'));
    }
  });
  return { total, semana, delDia };
}

/** Suma XP si no la ganó ya hoy por lo mismo y no pasó el tope diario. */
function botDarXp_(u, accion, ref) {
  const puntos = BOT_XP[accion];
  if (!puntos) throw new Error('Acción de XP desconocida: ' + accion);
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const { total, delDia } = botTotalesXp_();
    const hoy = delDia[u.nombre] || { xp: 0, claves: new Set(), porAccion: {} };
    const topeAccion = BOT_XP_TOPE_ACCION[accion];
    const dentroTopeAccion = !topeAccion || (hoy.porAccion[accion] || 0) + puntos <= topeAccion;
    let ganado = 0;
    if (!hoy.claves.has(accion + '|' + ref) && hoy.xp + puntos <= BOT_XP_TOPE_DIARIO && dentroTopeAccion) {
      botAgregarFila_(BOT.HOJAS.xp, { Fecha: botAhora_(), Nombre: u.nombre, Accion: accion, Ref: ref, XP: puntos });
      ganado = puntos;
    }
    const nuevoTotal = (total[u.nombre] || 0) + ganado;
    return Object.assign({ ganado, total: nuevoTotal }, botNivel_(nuevoTotal));
  } finally {
    lock.releaseLock();
  }
}

function botSumarXP(accion, ref) {
  const u = botExigir_();
  if (!BOT_XP_DESDE_CLIENTE.includes(accion)) throw new Error('Esa XP se gana haciendo la acción.');
  ref = String(ref || '').trim().slice(0, 40);
  if (accion === 'pregunta') ref = ref.replace(/[^a-z0-9_-]/gi, '').slice(0, 20); // id de la pregunta: una vez por día cada una
  else if (accion !== 'limpieza' && !botVisibles_(u).some((f) => f.id === ref)) throw new Error('No encontré el producto ' + ref + '.');
  return botDarXp_(u, accion, ref);
}

function botRanking_() {
  const { semana } = botTotalesXp_();
  return Object.keys(semana).map((nombre) => ({ nombre, xp: semana[nombre] }))
    .sort((a, b) => b.xp - a.xp).slice(0, 8);
}

function botSalaInicio() {
  const u = botExigir_();
  const { total } = botTotalesXp_();
  const xp = total[u.nombre] || 0;
  // Las zonas con más productos (las estanterías de la sala).
  const cuenta = {};
  botVisibles_(u).forEach((f) => { if (f.zona) cuenta[f.zona] = (cuenta[f.zona] || 0) + 1; });
  const zonas = Object.keys(cuenta).sort((a, b) => cuenta[b] - cuenta[a]).slice(0, 8)
    .sort((a, b) => a.localeCompare(b, 'es', { numeric: true }));
  const equipo = botTabla_(BOT.HOJAS.equipo);
  const companeros = equipo.filas
    .filter((f) => String(equipo.get(f, 'Activo')).trim().toUpperCase() !== 'NO')
    .map((f) => String(equipo.get(f, 'Nombre')).trim())
    .filter((n) => n && n !== u.nombre);
  return {
    jugador: Object.assign({ nombre: u.nombre, avatar: botAvatarPersona_(u), xp }, botNivel_(xp)),
    zonas, companeros, ranking: botRanking_(),
    lineas: botInicio().lineas, puedeUbicar: u.puedeUbicar, verPrecios: u.verPrecios,
    xpPorAccion: BOT_XP,
  };
}

// ---------------------------------------------------------------------------
// Sala compartida: posiciones, chat, feed y desafíos
// ---------------------------------------------------------------------------
// Todo vive en CacheService (memoria compartida del script, sin tocar la planilla).

const BOT_SALA = {
  VIGENCIA_JUGADOR: 12,     // segundos sin latido para dejar de mostrar a alguien
  MAX_EVENTOS: 25,
  PAUSA_ENTRE_DESAFIOS: 15, // segundos entre que alguien gana y sale el próximo
  PISTA_SEGUNDOS: 30,
  REVELAR_SEGUNDOS: 60,
  ESPERA_ERROR: 10,         // segundos de castigo por responder mal
  MAX_TEXTO: 140,
};

function botSalaClave_(nombre) { return 'sala_j_' + botNormalizarCodigo_(nombre); }

function botSalaLeer_(clave, porDefecto) {
  const v = CacheService.getScriptCache().get(clave);
  return v ? JSON.parse(v) : porDefecto;
}
function botSalaGuardar_(clave, valor, segundos) {
  CacheService.getScriptCache().put(clave, JSON.stringify(valor), segundos || 21600);
}

/** Agrega un evento al feed de la sala (con lock: lo escriben varios a la vez). */
function botSalaEvento_(tipo, texto, quien) {
  const lock = LockService.getScriptLock();
  lock.waitLock(5000);
  try {
    const eventos = botSalaLeer_('sala_eventos', []);
    const ultimo = eventos.length ? eventos[eventos.length - 1].id : 0;
    eventos.push({ id: ultimo + 1, ts: Date.now(), tipo, texto: String(texto).slice(0, 200), quien: quien || '' });
    botSalaGuardar_('sala_eventos', eventos.slice(-BOT_SALA.MAX_EVENTOS));
  } finally {
    lock.releaseLock();
  }
}

/** Producto al azar con zona entre las de la sala, para el desafío. */
function botSalaNuevoDesafio_(u, zonas) {
  const candidatos = botVisibles_(u).filter((f) => f.zona && zonas.includes(f.zona) && f.stock > 0 && f.linea === 'Autopartes');
  if (!candidatos.length) return null;
  const f = candidatos[Math.floor(Math.random() * candidatos.length)];
  return {
    id: 'D' + Date.now().toString(36), inicio: Date.now(), ganador: '', fin: 0,
    producto: { id: f.id, descripcion: f.descripcion, marca: f.marca, piso: f.piso, oem: f.oem },
    zona: f.zona, intentos: {},
  };
}

/** Lo que ve cada jugador del desafío: la zona solo aparece como pista o al final. */
function botSalaDesafioVisible_(d) {
  if (!d) return null;
  const seg = (Date.now() - d.inicio) / 1000;
  const vista = { id: d.id, producto: { descripcion: d.producto.descripcion, marca: d.producto.marca }, segundos: Math.floor(seg), ganador: d.ganador };
  if (d.ganador || seg >= BOT_SALA.REVELAR_SEGUNDOS) vista.zona = d.zona;
  else if (seg >= BOT_SALA.PISTA_SEGUNDOS) {
    vista.pista = d.producto.piso ? 'Está en el piso ' + d.producto.piso + ' de su estantería.' : 'Su código OEM empieza con ' + String(d.producto.oem || d.producto.descripcion).slice(0, 3) + '.';
  }
  return vista;
}

function botSalaLatido(estado) {
  const u = botExigir_();
  estado = estado || {};
  const ahora = Date.now();
  const yo = {
    nombre: u.nombre,
    x: Number(estado.x) || 0, z: Number(estado.z) || 0, mira: estado.mira < 0 ? -1 : 1,
    carga: !!estado.carga, ts: ahora,
  };
  const anterior = botSalaLeer_(botSalaClave_(u.nombre), {});
  if (estado.dice && String(estado.dice).trim()) {
    yo.dice = String(estado.dice).trim().slice(0, BOT_SALA.MAX_TEXTO);
    yo.diceId = (anterior.diceId || 0) + 1;
    yo.diceTs = ahora;
    if (estado.diceAlEquipo) botSalaEvento_('chat', yo.dice, u.nombre);
  } else if (anterior.dice && ahora - anterior.diceTs < 5000) {
    Object.assign(yo, { dice: anterior.dice, diceId: anterior.diceId, diceTs: anterior.diceTs });
  }
  botSalaGuardar_(botSalaClave_(u.nombre), yo, 60);

  // Lista de nombres que alguna vez entraron (para leer a todos de una).
  let lista = botSalaLeer_('sala_lista', []);
  if (!lista.includes(u.nombre)) {
    const lock = LockService.getScriptLock();
    lock.waitLock(5000);
    try {
      lista = botSalaLeer_('sala_lista', []);
      if (!lista.includes(u.nombre)) { lista.push(u.nombre); botSalaGuardar_('sala_lista', lista); }
    } finally {
      lock.releaseLock();
    }
    botSalaEvento_('entra', u.nombre + ' entró a la sala', u.nombre);
  }
  const todos = CacheService.getScriptCache().getAll(lista.map(botSalaClave_));
  const jugadores = Object.values(todos).map((v) => JSON.parse(v))
    .filter((j) => j.nombre !== u.nombre && ahora - j.ts < BOT_SALA.VIGENCIA_JUGADOR * 1000);

  // Desafío: si no hay uno en curso (o el último terminó hace rato), sale otro.
  let d = botSalaLeer_('sala_desafio', null);
  const zonas = Array.isArray(estado.zonas) ? estado.zonas.map(String) : [];
  if ((!d || (d.fin && ahora - d.fin > BOT_SALA.PAUSA_ENTRE_DESAFIOS * 1000)) && zonas.length) {
    const lock = LockService.getScriptLock();
    lock.waitLock(5000);
    try {
      d = botSalaLeer_('sala_desafio', null);
      if (!d || (d.fin && ahora - d.fin > BOT_SALA.PAUSA_ENTRE_DESAFIOS * 1000)) {
        d = botSalaNuevoDesafio_(u, zonas);
        if (d) {
          botSalaGuardar_('sala_desafio', d);
          botSalaEvento_('desafio', '⚡ Nuevo desafío: ¿dónde está ' + d.producto.descripcion + (d.producto.marca ? ' (' + d.producto.marca + ')' : '') + '?', 'hottie');
        }
      }
    } finally {
      lock.releaseLock();
    }
  }
  // Nadie lo encontró en 2 minutos: se cierra y sale otro.
  if (d && !d.fin && ahora - d.inicio > 120000) {
    d.fin = ahora; botSalaGuardar_('sala_desafio', d);
    botSalaEvento_('desafio', 'Nadie llegó 😅 ' + d.producto.descripcion + ' estaba en la zona ' + d.zona + '.', 'hottie');
  }

  const desde = Number(estado.ultimoEvento) || 0;
  const eventos = botSalaLeer_('sala_eventos', []).filter((e) => e.id > desde);
  return { jugadores, eventos, desafio: botSalaDesafioVisible_(d), ahora, reputacion: botSalaLeer_('sala_reputacion', null) };
}

function botSalaResponder(desafioId, zona) {
  const u = botExigir_();
  zona = String(zona || '').trim();
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  let resultado;
  try {
    const d = botSalaLeer_('sala_desafio', null);
    if (!d || d.id !== desafioId) return { ok: false, mensaje: 'Ese desafío ya terminó.' };
    if (d.ganador) return { ok: false, mensaje: d.ganador + ' llegó primero 😅 Era la zona ' + d.zona + '.' };
    const ultimoError = d.intentos[u.nombre] || 0;
    const espera = BOT_SALA.ESPERA_ERROR * 1000 - (Date.now() - ultimoError);
    if (espera > 0) return { ok: false, mensaje: 'Esperá ' + Math.ceil(espera / 1000) + ' s para volver a intentar.' };
    if (botNormalizarCodigo_(zona) === botNormalizarCodigo_(d.zona)) {
      d.ganador = u.nombre; d.fin = Date.now();
      botSalaGuardar_('sala_desafio', d);
      resultado = { ok: true, correcta: true, mensaje: '¡Bien! Era la zona ' + d.zona + ' 🏆' };
    } else {
      d.intentos[u.nombre] = Date.now();
      botSalaGuardar_('sala_desafio', d);
      resultado = { ok: true, correcta: false, mensaje: 'No, no está en la zona ' + zona + ' ❌ Probá en otra en 10 s.' };
    }
  } finally {
    lock.releaseLock();
  }
  if (resultado.correcta) {
    resultado.xp = botDarXp_(u, 'desafio', desafioId);
    botSalaEvento_('gana', '🏆 ' + u.nombre + ' encontró ' + botSalaLeer_('sala_desafio', {}).producto.descripcion + ' en la zona ' + zona + ' (+' + BOT_XP.desafio + ' XP)', u.nombre);
  } else {
    botSalaEvento_('error', u.nombre + ' probó en la zona ' + zona + ' ❌', u.nombre);
  }
  return resultado;
}

// ---------- Pedidos de práctica: ver en la PC, buscar, comparar SKU, embalar, canasto ----------

const BOT_ENVIOS = ['Flex', 'Colecta', 'Retiro'];

// Dificultad según el nivel del jugador: el juego acompaña al que arranca y exige al que ya sabe.
//  minutosCorte: tiempo real para despachar antes del "horario de corte".
//  ocultar: datos que el checklist deja de mostrar (hay que recordarlos o volver a mirar la venta en la PC).
//  casiIguales: etiquetas trampa que difieren en un solo carácter (entrena la atención al detalle).
const BOT_DIFICULTAD = [
  { nombre: 'Aprendiz', desdeNivel: 1, minutosCorte: 8, ocultar: [], casiIguales: 0, mensaje: 0.3, pack: 0.15 },
  { nombre: 'Pro', desdeNivel: 3, minutosCorte: 6, ocultar: ['etiqueta', 'cantidad'], casiIguales: 1, mensaje: 0.45, pack: 0.3 },
  { nombre: 'Experto', desdeNivel: 6, minutosCorte: 4.5, ocultar: ['etiqueta', 'cantidad', 'envio'], casiIguales: 2, mensaje: 0.55, pack: 0.45 },
];

// Mensajes del comprador. Regla de fondo: se despacha exactamente lo que dice la venta;
// lo que cambia la venta, la factura o los datos de contacto lo maneja el encargado, siempre dentro de Mercado Libre.
const BOT_MENSAJES_COMPRADOR = [
  { texto: '¡Hola! Es para regalo, ¿lo pueden embalar bien? 🎁', correcta: 0, frena: false,
    opciones: ['Lo embalo bien protegido, como siempre', 'Le pongo papel de regalo por mi cuenta', 'Freno el pedido hasta que alguien le conteste'],
    leccion: 'Todo pedido se embala bien protegido. No hace falta frenar nada ni inventar extras.' },
  { texto: 'Me equivoqué, necesito otra medida. ¿Me mandan la otra?', correcta: 1, frena: true,
    opciones: ['Le mando la otra medida', 'No lo despacho y aviso al encargado', 'Despacho lo que dice la venta igual'],
    leccion: 'Nunca se despacha algo distinto a lo vendido, y tampoco conviene mandar algo que ya sabemos que no le sirve. Se frena y lo resuelve el encargado (cancelación o nueva venta).' },
  { texto: '¿Me pasás tu WhatsApp así coordinamos?', correcta: 2, frena: false,
    opciones: ['Le paso mi número', 'Le paso el de la empresa', 'No: todo se habla por la mensajería de Mercado Libre'],
    leccion: 'La charla con el comprador queda dentro de Mercado Libre: protege la venta y la reputación. Vos seguís armando.' },
  { texto: '¿Me pueden hacer factura A?', correcta: 0, frena: false,
    opciones: ['Aviso al encargado y sigo armando', 'Freno el pedido hasta que esté la factura', 'Le escribo los datos en la caja'],
    leccion: 'La factura la gestiona administración. El pedido sigue su curso para no llegar tarde al corte.' },
  { texto: 'Lo necesito urgente, ¿sale hoy?', correcta: 1, frena: false,
    opciones: ['Le prometo que llega hoy', 'Lo armo ya para que salga antes del corte', 'Lo dejo para después de los otros'],
    leccion: 'No prometas fechas: la promesa la da Mercado Libre. Lo que sí depende de vos es despacharlo antes del horario de corte.' },
  { texto: 'Compré 2 pero solo necesito 1, ¿me mandan 1?', correcta: 1, frena: true,
    opciones: ['Mando 1 y listo', 'No lo despacho y aviso al encargado', 'Mando 2 igual, es lo que dice la venta'],
    leccion: 'Si el comprador pide cambiar la venta, no se despacha hasta que el encargado la modifique o la cancele.' },
];

// Lado y posición: si la descripción lo dice, se practica no confundirlo.
const BOT_VARIANTES = [['izquierdo', 'derecho'], ['izquierda', 'derecha'], ['delantero', 'trasero'], ['delantera', 'trasera'], ['superior', 'inferior']];
const BOT_COMPRADORES = ['JUANCHO_22', 'MARIANELA.R', 'TALLER_ELGRINGO', 'LUCAS1987', 'REPUESTOSOESTE', 'CAROSANZ', 'EL_TANO_MECANICO', 'PATRI.G', 'NICOVW', 'MECANICA_LOS_HERMANOS'];

function botDificultad_(nivel) {
  return BOT_DIFICULTAD.filter((d) => nivel >= d.desdeNivel).pop();
}

/** Una etiqueta que difiere en un solo carácter (dos dígitos cambiados de lugar o un dígito distinto). */
function botCasiIgual_(etiqueta) {
  const c = String(etiqueta).split('');
  const pos = c.map((x, i) => i).filter((i) => /[0-9A-Za-z]/.test(c[i]));
  if (pos.length < 3) return '';
  const i = pos[1 + Math.floor(Math.random() * (pos.length - 2))];
  if (Math.random() < 0.5 && /\d/.test(c[i]) && c[i + 1] && /\d/.test(c[i + 1]) && c[i] !== c[i + 1]) [c[i], c[i + 1]] = [c[i + 1], c[i]];
  else c[i] = /\d/.test(c[i]) ? String((Number(c[i]) + 1 + Math.floor(Math.random() * 8)) % 10) : (c[i].toUpperCase() === 'B' ? '8' : 'B');
  const r = c.join('');
  return r === etiqueta ? '' : r;
}

/** Título de la publicación en ML (hoja Publicaciones) o uno armado con la descripción. */
function botTitulosMl_() {
  const t = botTabla_(BOT.HOJAS.publicaciones);
  const titulos = {};
  t.filas.forEach((f) => {
    const sku = botNormalizarCodigo_(t.get(f, 'SKU'));
    const titulo = String(t.get(f, 'Titulo')).trim();
    if (sku && titulo && !titulos[sku]) titulos[sku] = titulo;
  });
  return titulos;
}

function botSalaNuevoPedido(zonas) {
  const u = botExigir_();
  zonas = (Array.isArray(zonas) ? zonas : []).map(String);
  const conEtiqueta = botVisibles_(u).filter((f) => f.linea === 'Autopartes' && f.stock > 0 && (f.sku || f.oem));
  const candidatos = conEtiqueta.filter((f) => zonas.includes(f.zona));
  if (!candidatos.length) throw new Error('No hay productos con zona en la sala para armar un pedido.');
  const azar = (lista) => lista[Math.floor(Math.random() * lista.length)];
  const { total } = botTotalesXp_();
  const nivel = botNivel_(total[u.nombre] || 0).nivel;
  const dif = botDificultad_(nivel);
  const titulos = botTitulosMl_();
  // Pack: varios productos de la misma venta, en una sola caja con una sola etiqueta.
  const cantidadItems = Math.random() < dif.pack ? (dif.nombre === 'Experto' && Math.random() < 0.4 ? 3 : 2) : 1;
  const items = [];
  for (let intentos = 0; items.length < cantidadItems && intentos < 50; intentos++) {
    const f = azar(candidatos);
    if (items.some((i) => i.id === f.id)) continue;
    const etiqueta = f.sku || f.oem;
    // Etiquetas "trampa": productos parecidos (misma primera palabra) y, con más nivel, códigos casi iguales.
    const primera = botNormalizar_(f.descripcion).split(' ')[0];
    let parecidas = conEtiqueta.filter((x) => x.id !== f.id && (x.sku || x.oem) !== etiqueta && botNormalizar_(x.descripcion).startsWith(primera));
    if (parecidas.length < 2) parecidas = conEtiqueta.filter((x) => x.id !== f.id && (x.sku || x.oem) !== etiqueta);
    const trampas = [];
    for (let k = 0; k < dif.casiIguales; k++) {
      const casi = botCasiIgual_(etiqueta);
      if (casi && !trampas.some((t) => t.etiqueta === casi)) trampas.push({ etiqueta: casi, descripcion: f.descripcion + ' (otra medida)', casi: true });
    }
    while (trampas.length < 2 && parecidas.length) {
      const x = parecidas.splice(Math.floor(Math.random() * parecidas.length), 1)[0];
      if (!trampas.some((t) => t.etiqueta === (x.sku || x.oem))) trampas.push({ etiqueta: x.sku || x.oem, descripcion: x.descripcion });
    }
    const palabras = botNormalizar_(f.descripcion).split(' ');
    const par = BOT_VARIANTES.find(([a, b]) => palabras.includes(a) || palabras.includes(b));
    const variante = par ? (palabras.includes(par[0]) ? { pide: par[0], otra: par[1] } : { pide: par[1], otra: par[0] }) : null;
    items.push({
      id: f.id, descripcion: f.descripcion, marca: f.marca, zona: f.zona, piso: f.piso, etiqueta,
      titulo: titulos[botNormalizarCodigo_(f.sku)] || [f.descripcion, f.marca].filter(Boolean).join(' '),
      cantidad: f.stock >= 2 && Math.random() < 0.3 ? 2 : 1,
      danado: Math.random() < 0.2, // a veces la primera unidad viene golpeada
      variante, trampas,
    });
  }
  const creado = Date.now();
  const mensaje = Math.random() < dif.mensaje ? azar(BOT_MENSAJES_COMPRADOR) : null;
  const pedido = {
    id: 'ML-' + creado.toString(36).slice(-5).toUpperCase(),
    venta: '2000' + String(creado).slice(-9) + String(Math.floor(Math.random() * 900) + 100),
    comprador: azar(BOT_COMPRADORES),
    items, envio: azar(BOT_ENVIOS), creado, corte: creado + dif.minutosCorte * 60000,
    dificultad: { nombre: dif.nombre, ocultar: dif.ocultar },
    mensaje: mensaje && { texto: mensaje.texto, opciones: mensaje.opciones, correcta: mensaje.correcta, frena: mensaje.frena, leccion: mensaje.leccion },
  };
  botSalaGuardar_('sala_pedido_' + botNormalizarCodigo_(u.nombre), pedido, 7200);
  return pedido;
}

/**
 * Cierra el pedido. resultado: { errores, pausado } (o un número de errores, como antes).
 * Despachado después del corte = venta demorada. Pausado = lo frenó bien para el encargado.
 */
function botSalaCompletarPedido(id, resultado) {
  const u = botExigir_();
  const clave = 'sala_pedido_' + botNormalizarCodigo_(u.nombre);
  const pedido = botSalaLeer_(clave, null);
  if (!pedido || pedido.id !== id) throw new Error('Ese pedido no es tuyo o ya se cerró.');
  const r = typeof resultado === 'object' && resultado ? resultado : { errores: resultado };
  const errores = Math.max(0, Number(r.errores) || 0);
  const pausado = !!r.pausado && !!(pedido.mensaje && pedido.mensaje.frena);
  if (!pausado && Date.now() - pedido.creado < 20000) throw new Error('Muy rápido 😅 Revisá bien el pedido antes de cerrarlo.');
  CacheService.getScriptCache().remove(clave);
  const tarde = !pausado && Date.now() > (pedido.corte || Infinity);
  const accion = pausado ? 'criterio' : tarde ? 'pedido_tarde' : errores === 0 ? 'pedido' : 'pedido_err';
  const xp = botDarXp_(u, accion, id);
  botSalaReputacion_(accion);
  const textos = {
    criterio: '🛑 ' + u.nombre + ' frenó la venta ' + id + ' para el encargado. ¡Buen criterio!',
    pedido_tarde: '⏰ ' + u.nombre + ' despachó ' + id + ' después del corte (venta demorada)',
    pedido: '✅ ' + u.nombre + ' despachó ' + id + ' perfecto y a tiempo (+' + BOT_XP.pedido + ' XP)',
    pedido_err: '📦 ' + u.nombre + ' despachó ' + id + ' con ' + errores + (errores === 1 ? ' error corregido' : ' errores corregidos'),
  };
  botSalaEvento_('logro', textos[accion], u.nombre);
  return { xp, errores, tarde, pausado, reputacion: botSalaReputacion_() };
}

/**
 * Termómetro del día del equipo (como la reputación de ML, pero de práctica): cuenta despachos
 * perfectos, con errores y demorados. Vive en caché para que el latido no lea la hoja cada 2 segundos.
 */
function botSalaReputacion_(sumar) {
  const hoy = Utilities.formatDate(new Date(), BOT.ZONA_HORARIA, 'dd/MM/yyyy');
  const clave = 'sala_reputacion';
  let rep = botSalaLeer_(clave, null);
  if (!rep || rep.dia !== hoy) {
    rep = { dia: hoy, perfectos: 0, conErrores: 0, demorados: 0, frenados: 0 };
    const t = botTabla_(BOT.HOJAS.xp);
    t.filas.forEach((f) => {
      if (!String(t.get(f, 'Fecha')).startsWith(hoy)) return;
      const a = String(t.get(f, 'Accion'));
      if (a === 'pedido') rep.perfectos++; else if (a === 'pedido_err') rep.conErrores++;
      else if (a === 'pedido_tarde') rep.demorados++; else if (a === 'criterio') rep.frenados++;
    });
  } else if (sumar) {
    const campo = { pedido: 'perfectos', pedido_err: 'conErrores', pedido_tarde: 'demorados', criterio: 'frenados' }[sumar];
    if (campo) rep[campo]++;
  }
  botSalaGuardar_(clave, rep, 21600);
  return rep;
}

/** Eventos que avisa la pantalla (encontró, despachó) para el feed de todos. */
function botSalaAvisar(texto) {
  const u = botExigir_();
  botSalaEvento_('logro', u.nombre + ' ' + String(texto || '').slice(0, 120), u.nombre);
  return true;
}

// ---------------------------------------------------------------------------
// Avatar de cada persona (hoja Equipo: Foto, Icono)
// ---------------------------------------------------------------------------

// Paleta del equipo: un color por persona, los mismos que usan la sala y los retratos.
const BOT_COLOR_PERSONA = { hottie: '#5ef2c4', facundo: '#4d8dff', gabriel: '#f2b84b', sebastian: '#a98bff', agustin: '#ff7a7a' };
// Para quien no esté en la paleta (gente nueva), uno fijo según el nombre.
const BOT_COLORES_AVATAR = ['#4d8dff', '#f2b84b', '#a98bff', '#ff7a7a', '#7fe08a', '#8fa2ff'];
const BOT_MAX_FOTO_BYTES = 300 * 1024;

/**
 * Foto si hay (link o ID de Drive, o data:image...), si no el emoji de Icono,
 * si no las iniciales con un color fijo por persona.
 */
function botAvatarPersona_(u) {
  const src = botFotoEquipo_(u.foto);
  if (src) return { tipo: 'foto', src };
  const icono = u.icono && !/^(no|si|sí)$/i.test(u.icono) ? u.icono : '';
  const color = BOT_COLOR_PERSONA[botNormalizar_(u.nombre).split(' ')[0]] ||
    BOT_COLORES_AVATAR[[...u.nombre].reduce((a, c) => a + c.charCodeAt(0), 0) % BOT_COLORES_AVATAR.length];
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
  // Las líneas que hay de verdad en la hoja (SEX solo si es SEX_ADMIN).
  const lineas = ['Todo', BOT_LINEA_DEFECTO].concat([...new Set(botVisibles_(u).map((f) => f.linea))]
    .filter((l) => l !== BOT_LINEA_DEFECTO).sort());
  return {
    nombre: u.nombre, avatar: botAvatarPersona_(u), lineas,
    puedeUbicar: u.puedeUbicar, verPrecios: u.verPrecios,
  };
}

function botPagina() {
  return HtmlService.createTemplateFromFile('BotUI').evaluate()
    .setTitle('hottie · Consultas de stock')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    // Para poder abrirse dentro de la ventana emergente (iframe) de tu app.
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/** Ventana emergente: en cualquier página de tu app, al final del <body>:  <?!= botWidget() ?> */
function botWidget() {
  return HtmlService.createTemplateFromFile('BotWidget').evaluate().getContent();
}

/** URL de esta web app con ?v=... (para el chat y el Modo Sala). */
function botUrl(vista) {
  return ScriptApp.getService().getUrl() + '?v=' + encodeURIComponent(vista);
}

/** Modo Sala (3D). En tu doGet: if (e.parameter.v === 'sala') return botPaginaSala(); */
function botPaginaSala() {
  return HtmlService.createTemplateFromFile('BotSala').evaluate()
    .setTitle('Sala Volhotic')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1, maximum-scale=1');
}

function botInclude(nombre) {
  return HtmlService.createHtmlOutputFromFile(nombre).getContent();
}
