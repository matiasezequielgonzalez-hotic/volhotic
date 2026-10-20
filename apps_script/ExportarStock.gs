/**
 * Web app de solo lectura que le pasa el stock al bot de Volhotic.
 *
 * Devuelve en JSON solo las columnas que el bot necesita de las hojas "General" y
 * "Publicaciones" de vol_ml_listings(No_tocar). No expone Costos, Ventas, Equipo ni
 * ninguna otra hoja, y no escribe nada en la planilla.
 *
 * Instalación (proyecto aparte, no toca la app que ya usan):
 *  1. script.google.com -> Nuevo proyecto -> pegar este archivo.
 *  2. Configuración del proyecto -> Propiedades del script -> agregar TOKEN con una
 *     clave larga al azar (es la contraseña del bot).
 *  3. Implementar -> Nueva implementación -> Aplicación web.
 *     Ejecutar como: Yo. Quién tiene acceso: Cualquier persona.
 *  4. Copiar la URL /exec y en el bot poner:
 *     VOLHOTIC_FUENTE=https://script.google.com/macros/s/.../exec?token=LA_CLAVE
 */

const PLANILLA_ID = '1Ui77_spb9OF4fuuTpxN-eatZdpZI5Yw277KcZRuOiTw'; // vol_ml_listings(No_tocar)

const HOJAS = {
  general: {
    nombre: 'General',
    columnas: ['ID', 'Descripcion', 'SKU', 'Stock', 'Marca', 'EAN', 'Condicion', 'Deposito',
               'Ubicacion', 'Piso', 'Zona', 'Estado', 'Estado_ML', 'Observación'],
  },
  publicaciones: {
    nombre: 'Publicaciones',
    columnas: ['MLA', 'SKU', 'Estado_ML'],
  },
};

function doGet(e) {
  const token = PropertiesService.getScriptProperties().getProperty('TOKEN');
  if (!token || !e || !e.parameter || e.parameter.token !== token) {
    return json_({ error: 'no autorizado' });
  }
  const planilla = SpreadsheetApp.openById(PLANILLA_ID);
  const salida = { actualizado: new Date().toISOString() };
  Object.keys(HOJAS).forEach(function (clave) {
    salida[clave] = leerColumnas_(planilla, HOJAS[clave].nombre, HOJAS[clave].columnas);
  });
  return json_(salida);
}

/** Devuelve [[encabezados], [fila], ...] con solo las columnas pedidas, como texto. */
function leerColumnas_(planilla, nombreHoja, columnas) {
  const hoja = planilla.getSheetByName(nombreHoja);
  if (!hoja) return [];
  // getDisplayValues mantiene los ceros a la izquierda de los códigos (ej: 09600).
  const valores = hoja.getDataRange().getDisplayValues();
  const encabezados = valores[0].map(function (h) { return String(h).trim(); });
  const indices = columnas.map(function (c) { return encabezados.indexOf(c); });
  const presentes = columnas.filter(function (_, i) { return indices[i] >= 0; });
  const filas = valores.slice(1).map(function (fila) {
    return indices.filter(function (i) { return i >= 0; }).map(function (i) { return fila[i]; });
  });
  return [presentes].concat(filas);
}

function json_(objeto) {
  return ContentService.createTextOutput(JSON.stringify(objeto))
    .setMimeType(ContentService.MimeType.JSON);
}
