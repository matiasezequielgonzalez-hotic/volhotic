# Escuela hotic. de Mercado Libre Argentina

Contenido y código para el área de aprendizaje del panel. Verificado al **21/10/2026**.

## Qué hay

| Archivo | Qué es |
|---|---|
| `programa.json` | El programa completo: 7 cursos, 25 lecciones y 53 preguntas. Cada dato tiene su fuente y su estado (oficial, técnico, a confirmar, no oficial). |
| `programa.d.ts` | La forma de `programa.json`, para TypeScript o como documentación. |
| `repaso.js` | Repaso espaciado (cajas de Leitner), sin dependencias: lo que se erra vuelve a los 10 minutos, lo que se sabe a los 1, 3, 7 y 16 días. |
| `escuela.html` | Página de referencia lista para usar: cursos → lecciones → preguntas, progreso y repaso. Sin dependencias. |
| `generar_bot_escuela.py` | Regenera `BotEscuela.html` (las preguntas que usa hottie en la sala) cuando cambia el programa. |

El informe con todas las fuentes está en `docs/Escuela Mercado Libre Argentina.md`.

## Usarlo en el panel

**Opción rápida:** subí `escuela.html`, `repaso.js` y `programa.json` a la misma carpeta del sitio
(por ejemplo `/escuela/`) y enlazala desde el menú **Escuela**. Parámetros de la URL:
- `?usuario=Facundo` guarda el progreso de esa persona (en el panel, pasale el usuario logueado).
- `&sex=1` muestra el curso de Sexhotic (solo para quien tiene acceso).

El progreso queda en el navegador de cada uno (localStorage). Si querés el progreso en la planilla,
`crearRepaso(usuario, almacen)` acepta cualquier objeto con `getItem`/`setItem`: pasale uno que lea y
escriba en tu backend.

**Opción integrada:** importá `programa.json` en tus componentes y usá `escuela.html` como guía:
- Lista de cursos en el orden de `programa.orden`, filtrando `para === 'sex'` según permisos.
- Lección: `puntos` con su etiqueta y el link a `fuente`, `error_comun`, `confirmar_en_panel`
  y `preguntas`. Mezclá las opciones al mostrarlas.
- Cada respuesta: `repaso.responder(pregunta.id, acierto)`. La pestaña de repaso usa
  `repaso.proxima(bancoDePreguntas(programa))`.

## Mantenerlo al día

- Los montos (cargo fijo, comisiones, MercadoLíder, envío gratis) cambian seguido. Están marcados
  como "confirmar" o "no oficial": revisalos en el panel de vendedor antes de cada clase, y como
  mínimo una vez por mes. La lista está en `programa.verificacion.pendiente_de_fuente_oficial`.
- Para cambiar un dato: editá `programa.json` (texto, estado y fuente), actualizá `version` y
  `verificacion.fecha`, y corré `python3 generar_bot_escuela.py` para que la sala use lo mismo.
- Si agregás una pregunta, su `id` tiene que ser único: es la clave del repaso de cada persona.
