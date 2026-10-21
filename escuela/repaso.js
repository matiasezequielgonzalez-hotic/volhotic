// Repaso espaciado (cajas de Leitner) para las preguntas de la Escuela.
// Lo que se erra vuelve a los 10 minutos; lo que se sabe, a los 1, 3, 7 y 16 días.
// Sin dependencias: funciona en el navegador (localStorage) o con cualquier almacenamiento
// que tenga getItem/setItem (por ejemplo, uno que guarde en tu backend).

export const DIAS_CAJA = [0, 1, 3, 7, 16];
const DIEZ_MINUTOS = 10 * 60 * 1000;
const UN_DIA = 24 * 60 * 60 * 1000;

/** Todas las preguntas del programa, con el curso y la lección de donde salen. */
export function bancoDePreguntas(programa, { incluirSex = false } = {}) {
  const banco = [];
  programa.cursos.forEach((curso) => {
    if (curso.para === 'sex' && !incluirSex) return;
    curso.lecciones.forEach((leccion) => {
      leccion.preguntas.forEach((q) => banco.push({ ...q, curso: curso.id, leccion: leccion.id }));
    });
  });
  return banco;
}

export function crearRepaso(usuario, almacen = globalThis.localStorage) {
  const clave = 'escuela-repaso-' + String(usuario || 'anonimo').toLowerCase().replace(/\s+/g, '_');
  const leer = () => {
    try { return JSON.parse(almacen.getItem(clave) || '{}'); } catch (e) { return {}; }
  };
  const guardar = (datos) => {
    try { almacen.setItem(clave, JSON.stringify(datos)); } catch (e) { /* sin almacenamiento: no se guarda */ }
  };

  return {
    /** La próxima pregunta que toca: primero las vencidas (de la caja más baja), después las nuevas. */
    proxima(banco, ahora = Date.now()) {
      const datos = leer();
      const vencidas = banco.filter((q) => datos[q.id] && datos[q.id].proxima <= ahora)
        .sort((a, b) => datos[a.id].caja - datos[b.id].caja);
      if (vencidas.length) return vencidas[0];
      const nuevas = banco.filter((q) => !datos[q.id]);
      return nuevas.length ? nuevas[Math.floor(Math.random() * nuevas.length)] : null;
    },
    /** Guarda la respuesta y devuelve en qué caja quedó y cuántas están dominadas (caja 3 o más). */
    responder(id, acierto, ahora = Date.now()) {
      const datos = leer();
      const d = datos[id] || { caja: 0 };
      d.caja = acierto ? Math.min(d.caja + 1, DIAS_CAJA.length - 1) : 0;
      d.proxima = ahora + (acierto ? DIAS_CAJA[d.caja] * UN_DIA : DIEZ_MINUTOS);
      datos[id] = d;
      guardar(datos);
      const dominadas = Object.values(datos).filter((x) => x.caja >= 3).length;
      return { caja: d.caja, dominadas };
    },
    /** Cuántas preguntas tocan hoy. */
    pendientes(banco, ahora = Date.now()) {
      const datos = leer();
      return banco.filter((q) => !datos[q.id] || datos[q.id].proxima <= ahora).length;
    },
  };
}
