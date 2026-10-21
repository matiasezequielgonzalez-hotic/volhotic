// Forma de escuela/programa.json (Escuela de Mercado Libre Argentina).
// Para usarlo en TypeScript: import programa from './programa.json'; const p = programa as Programa;

/** De dónde sale cada dato. */
export type Estado =
  | 'oficial'     // Ayuda o Centro de vendedores de ML Argentina, ARCA o el Estado
  | 'dev'         // Documentación técnica de ML (developers.mercadolibre.com.ar)
  | 'confirmar'   // Cambia seguido o depende de la cuenta: mirarlo en el panel
  | 'no_oficial'; // Fuente de terceros, solo de referencia

export type Para = 'todos' | 'deposito' | 'publicadores' | 'administracion' | 'sex';

export interface Punto {
  texto: string;
  estado: Estado;
  /** URL de la fuente ('' si no hay fuente oficial). */
  fuente: string;
}

export interface Pregunta {
  /** Único en todo el programa: sirve de clave para el repaso espaciado. */
  id: string;
  q: string;
  /** Opciones en orden original; mezclarlas al mostrar. */
  o: string[];
  /** Índice de la opción correcta dentro de `o`. */
  c: number;
  /** Explicación que se muestra después de responder. */
  p: string;
}

export interface Leccion {
  id: string;
  titulo: string;
  minutos: number;
  objetivo: string;
  puntos: Punto[];
  error_comun: string;
  /** Qué practicar en la sala 3D ('' si no aplica). */
  en_la_sala: string;
  confirmar_en_panel: string[];
  preguntas: Pregunta[];
}

export interface Curso {
  id: string;
  titulo: string;
  /** Para quién es. 'sex' solo se muestra a quien tiene acceso a Sexhotic. */
  para: Para;
  descripcion: string;
  practica: { modo: string; texto: string };
  lecciones: Leccion[];
}

export interface Programa {
  version: string;
  titulo: string;
  aviso: string;
  /** Orden recomendado de los cursos (ids). */
  orden: string[];
  cursos: Curso[];
  verificacion: {
    fecha: string;
    metodo: string;
    confirmado: string[];
    pendiente_de_fuente_oficial: string[];
    revisar_cada: string;
  };
}
