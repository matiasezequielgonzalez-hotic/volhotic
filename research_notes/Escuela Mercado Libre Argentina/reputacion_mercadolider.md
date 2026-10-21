# Reputación de vendedor (termómetro) y MercadoLíder — Mercado Libre Argentina (estado a octubre 2026)

> **Aviso metodológico (leer antes de usar).** El proxy de esta sesión bloqueó el acceso directo (HTTP 403 al CONNECT) a `mercadolibre.com.ar`, `vendedores.mercadolibre.com.ar` y `developers.mercadolibre.com.ar`, así que **no pude abrir las páginas oficiales completas**. Todo lo que sigue sale de los **extractos que devolvió el buscador web, filtrado por dominios oficiales de ML Argentina**. Las URLs son las páginas oficiales de donde salen esos extractos, pero conviene que alguien abra cada link y revise la cifra antes de enseñarla. Lo marcado **[NO OFICIAL]** sale de blogs de terceros. Lo marcado **[NO VERIFICADO]** no lo pude confirmar en una fuente oficial.

## 1. Colores del termómetro y qué implica cada uno para el vendedor

### Takeaway
El termómetro va del rojo (peor) al verde (mejor), con 5 niveles (rojo, naranja, amarillo, verde claro y verde). Se recalcula todos los días. Con naranja o rojo se pierde mucho: menos exposición, en catálogo no se gana la compra y no se puede activar "Mi página". Además, la bonificación del envío gratis depende de la reputación.

### Cited Findings
- La reputación mide la atención que el vendedor da a los compradores y se muestra con colores, del rojo (la peor) al verde. Mejor reputación suele significar más ventas — [Por qué es importante la reputación del vendedor (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/por-que-es-importante-la-reputacion-del-vendedor)
- El color sale de reclamos, cancelaciones y envíos demorados, en una escala de rojo a verde que es dinámica y se actualiza a diario — [Qué es y cómo funciona la reputación como vendedor (Ayuda ML AR)](https://www.mercadolibre.com.ar/ayuda/Como-funciona-la-reputacion-de-vendedor_4024)
- En la API, `seller_reputation.level_id` da el nivel como número + color (p. ej. `"5_green"`) y `power_seller_status` dice si el vendedor es MercadoLíder y con qué medalla (Silver, Gold o Platinum) — [Sellers reputation (Developers ML AR)](https://developers.mercadolibre.com.ar/en_us/sellers-reputation); [Reputación de vendedores (Developers ML AR)](https://developers.mercadolibre.com.ar/es_ar/reputacion-de-vendedores)
- Los 5 colores serían rojo, naranja, amarillo, verde claro y verde — **[NO OFICIAL]** [Nubimetrics](https://academia.nubimetrics.com/reputacion-baja-mercado-libre). Coincide con el esquema de `level_id` de 1 a 5 (1_red … 5_green). Los nombres intermedios (`2_orange`, `3_yellow`, `4_light_green`) **[NO VERIFICADO]** en un extracto oficial.
- **Catálogo:** con reputación naranja o roja la publicación puede competir pero no ganar la compra; solo aparece en "Opciones de compra" — [Cómo funciona la competencia en Mercado Libre (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/como-funciona-la-competencia-en-catalogo)
- **Exposición:** con reputación roja hay menos visibilidad en los resultados de búsqueda — [Cómo posicionar tus productos en los listados (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/como-posicionar-tus-productos-en-los-listados). Además, las publicaciones de vendedores en rojo solo las ven compradores con experiencia en el sitio — [Quiénes ven mis publicaciones (Ayuda ML AR)](https://www.mercadolibre.com.ar/ayuda/23427)
- **"Mi página" (tienda propia):** no se puede activar con reputación roja o naranja — [Diseñá tu tienda dentro de Mercado Libre (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/disena-tu-pagina-dentro-de-mercado-libre)
- **Envío gratis:** ML paga una parte del costo del envío gratis y ese descuento depende de la reputación del vendedor — [Cómo funcionan los envíos en Mercado Libre (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/como-funcionan-los-envios-de-mercado-libre). El porcentaje de descuento por color **[NO VERIFICADO]**. El monto mínimo de envío gratis aparece distinto según la página ($33.000 en una, $23.000 en otra), así que hay que revisarlo en el panel.
- **Beneficio de Reputación / Programa de Despegue:** vendedores en rojo, naranja o amarillo pueden "congelar" el nivel en verde por un tiempo a cambio de un depósito en garantía. Ese depósito se devuelve total o parcialmente según los problemas que generen. Los que ya están en verde no pueden entrar — [Programa de Despegue y Beneficio de Reputación (Developers ML AR)](https://developers.mercadolibre.com.ar/es_ar/recuperacion-reputacion); [Programa de Despegue (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/logra-ventas-en-menos-tiempo-con-el-programa-de-despegue)

### Inferences
- Para el equipo de depósito, lo más importante es que **naranja ya cuesta plata**: se deja de ganar en catálogo y se pierde la tienda. No hace falta llegar a rojo para que duela.
- En la ficha pública (termómetro) se ve el color, pero las penalizaciones reales (exposición, descuento de envío, catálogo) se aplican "por detrás".

### Gaps
- No encontré una tabla oficial de **cuánto descuento de envío corresponde a cada color** en Argentina.
- No encontré una cifra oficial de **cuánta exposición se pierde** por color (ML no la publica).
- La página antigua "Sistema de reputación" ([seguro_calif.html](https://www.mercadolibre.com.ar/seguro_calif.html)) tiene fecha de actualización 10/09/2010. **Está obsoleta y no hay que usarla.**

## 2. Métricas y umbrales vigentes por color (Argentina), con cambios recientes

### Takeaway
Hay tres métricas: **reclamos**, **cancelaciones hechas por el vendedor** y **envíos incorrectos / despachos con demora**. Desde el **16 de septiembre de 2026** hay doble tabla. Si al vendedor lo miden por **60 días**, los umbrales son los de siempre. Si lo miden por **365 días**, los de cancelaciones y envíos incorrectos son más amplios. Los reclamos tienen los mismos límites en los dos casos: 1,5% / 3% / 6%.

### Cited Findings
- **Cambio oficial:** ML cambió dos criterios, "los límites de ventas afectadas y cómo definimos tu tiempo de medición", y lo aplicó automáticamente el **16 de septiembre**. El vendedor no tiene que hacer nada. Si te miden por los últimos 60 días, los porcentajes no cambian — [Vamos a cambiar la forma en que calculamos tu reputación (ML AR)](https://vendedores.mercadolibre.com.ar/nota/vamos-a-cambiar-la-forma-en-que-calculamos-tu-reputacion). El extracto no muestra el año. Que sea 2026 lo confirma **[NO OFICIAL]** [UpSeller, 09/09/2026: "Cambios en la reputación de ML Argentina desde el 16/09/2026"](https://www.upseller.com/es/blog-article-1020).

**Tabla vigente (según la nota oficial del cambio, vía extractos):**

| Métrica | Medición | Verde | Amarillo | Naranja | Rojo |
|---|---|---|---|---|---|
| Reclamos | 60 o 365 días (igual) | ≤ 1,5% | 1,5%–3% | 3%–6% | > 6% |
| Canceladas por vos | 60 días | ≤ 1% | 1%–2,5% | 2,5%–3% | > 3% |
| Canceladas por vos | 365 días | ≤ 1,5% | 1,5%–4% | 4%–5% | > 5% |
| Envíos incorrectos (demoras) | 60 días | ≤ 10% | 10%–15% * | 15%–22% * | > 22% |
| Envíos incorrectos (demoras) | 365 días | ≤ 13% | 13%–19,5% | 19,5%–28,5% | > 28,5% |

Fuente de la tabla: [Vamos a cambiar la forma en que calculamos tu reputación (ML AR)](https://vendedores.mercadolibre.com.ar/nota/vamos-a-cambiar-la-forma-en-que-calculamos-tu-reputacion)
\* Los cortes de amarillo y naranja para envíos incorrectos a 60 días (10–15 y 15–22) no aparecieron en el extracto de la nota. Los saco de la tabla de la API para MLA, donde `delayed_handling_time` da Líderes 8%, Green 10%, Yellow 15%, Orange 22%, Red > 22% — [Reputación de vendedores (Developers ML AR)](https://developers.mercadolibre.com.ar/es_ar/reputacion-de-vendedores). Esa tabla tendría entre 14 y 21 meses según el buscador, o sea que es anterior al cambio.

- Para la API, el umbral de reclamos en MLA es verde 1,5%, amarillo 3%, naranja 6% y rojo > 6%. Coincide con la nota nueva — [Reputación de vendedores (Developers ML AR)](https://developers.mercadolibre.com.ar/es_ar/reputacion-de-vendedores?nocache=true)
- Para ser verde, los reclamos no tienen que pasar el 1,5% de las ventas (**1% si sos MercadoLíder**). Los despachos con demora no tienen que pasar el 10% (60 días) ni el 13% (365 días) — [Por qué es importante la reputación del vendedor (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/por-que-es-importante-la-reputacion-del-vendedor)
- Fórmulas de la API: `cancellations rate = cancelaciones del vendedor / ventas totales` y `delayed handling time rate = ventas despachadas con retraso / ventas despachadas con me2` — [Sellers reputation (Developers ML AR)](https://developers.mercadolibre.com.ar/en_us/sellers-reputation)
- Los valores de cada métrica no se suman entre sí: cada porcentaje se mira por separado — [Evitá problemas en tus ventas con las métricas de atención (ML AR)](https://vendedores.mercadolibre.com.ar/nota/analiza-tus-metricas-de-atencion-y-reduci-problemas-en-tus-ventas)
- **Cifras viejas que todavía andan dando vueltas:** una versión anterior de la nota de despacho hablaba de un **15%** de demoras para verde — [Tiempo de despacho (Centro de vendedores, versión vieja)](https://vendedores.mercadolibre.com.ar/blog/notas/tiempo-de-despacho-la-clave-de-una-buena-reputacion/). En 2020, Real Trends también hablaba de 15% — **[NO OFICIAL, 2020]** [Real Trends](https://blog.real-trends.com/2020/09/07/ajustes-en-la-reputacion-de-mercado-libre/). Algunos blogs de 2026 dan otros números (3,5% de reclamos, 20% de demoras, 2% de reclamos con mediación) — **[NO OFICIAL, contradictorio]** [Nubimetrics](https://academia.nubimetrics.com/reputacion-baja-mercado-libre), [Base](https://base.com/es-AR/blog/?p=18410). **Ninguno de esos números hay que usarlo.**

### Inferences
- La métrica de demoras ahora aparece en la nota oficial como **"Envíos incorrectos"**. Junta los despachos tardíos de envíos que entrega el correo con las entregas demoradas o fallidas de Flex (ver sección 4). En el depósito conviene enseñarla como "cada paquete que sale tarde o que no llega en la promesa".
- Para un vendedor de volumen medido a 60 días, el colchón es muy chico: con 1.000 ventas en 60 días, **11 cancelaciones propias ya lo sacan de verde (> 1%)** y **16 reclamos lo sacan de verde (> 1,5%)**.

### Gaps
- No pude confirmar de primera mano los cortes de amarillo y naranja de envíos incorrectos a 60 días en la nota nueva.
- No encontré una versión de la tabla de la API (developers) actualizada después del 16/09/2026.
- No encontré una métrica oficial y separada de "mediaciones" en la reputación actual. Sí aparece como requisito de MercadoLíder en la ayuda (ver sección 5).

## 3. Período de evaluación, mínimo de ventas y qué NO cuenta

### Takeaway
Desde el 16/09/2026: con **101 ventas o más en los últimos 60 días**, te miden por 60 días. Con menos, te miden por los **últimos 365 días**. Antes el corte era de 50 ventas. No cuentan las cancelaciones que hace el comprador cuando no hay culpa del vendedor, ni los reclamos que no son por calidad del producto (por ejemplo, paquete roto). Tampoco cuentan los reclamos por demora si despachás dentro de los 2 días hábiles, ni los casos que ML excluye.

### Cited Findings
- Te miden por los últimos 60 días si tenés 101 ventas o más en ese lapso, y por los últimos 365 días si tenés menos. Antes el corte era de 50 ventas — [Vamos a cambiar la forma en que calculamos tu reputación (ML AR)](https://vendedores.mercadolibre.com.ar/nota/vamos-a-cambiar-la-forma-en-que-calculamos-tu-reputacion). Algunas otras páginas de ayuda todavía mostraban el umbral viejo de 50: **están desactualizadas.**
- La API mide `delayed_handling_time` sobre los últimos 365 días si el vendedor vendió menos del mínimo en 60 días — [Reputación de vendedores (Developers ML AR)](https://developers.mercadolibre.com.ar/es_ar/reputacion-de-vendedores)
- **Cancelación del comprador:** si el comprador cancela directamente, no afecta la reputación, "siempre y cuando la cancelación no haya sido por alguna falta tuya como vendedor". Si hubo reclamo y después el comprador cancela, impacta una sola vez, como reclamo — [Cómo cuidar tu reputación en los reclamos con cancelación (ML AR)](https://vendedores.mercadolibre.com.ar/nota/cuida-tu-reputacion-en-los-reclamos-con-cancelacion)
- **Reclamos que no cuentan:** "solo afectarán a tu reputación los reclamos relacionados a la calidad de tus productos". El resto no impacta, por ejemplo los **paquetes rotos o dañados** — [Por qué es importante la reputación del vendedor (ML AR)](https://vendedores.mercadolibre.com.ar/nota/por-que-es-importante-la-reputacion-del-vendedor) (según extracto citado por el buscador)
- **Reclamo por paquete demorado:** si despachás dentro de los primeros 2 días hábiles desde que arrancó el reclamo, la reputación no se ve afectada. Si no usás Mercado Envíos, además tenés que avisar desde los mensajes de la venta — [Cuidá tu reputación si te reclaman por un paquete demorado (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/cuida-tu-reputacion-si-te-reclaman-por-un-paquete-demorado)
- **Reintegrar en vez de resolver:** devolver la plata cuando no es la solución que esperaba el comprador "podría afectar tu reputación" — [Consejos para evitar que tus compradores inicien un reclamo (ML AR)](https://vendedores.mercadolibre.com.ar/nota/consejos-para-evitar-que-tus-compradores-inicien-un-reclamo)
- **Exclusiones:** desde "Métricas" > "Atención a tus compradores" > "Revisar todos" > "Ventas con problemas" se puede pedir que ML analice un caso para que no afecte la reputación — [Conocé las reglas de exclusión (ML AR)](https://vendedores.mercadolibre.com.ar/nota/conoce-las-reglas-de-exclusion); [Métricas de atención (ML AR)](https://vendedores.mercadolibre.com.ar/nota/analiza-tus-metricas-de-atencion-y-reduci-problemas-en-tus-ventas)
- **Full:** ML se ocupa del almacenamiento, el empaque, el envío y la posventa, y "cumple la promesa de envío". En cambios de producto de ventas Full, ML gestiona el cambio de punta a punta — [Qué es Full y qué beneficios te ofrece (ML AR)](https://vendedores.mercadolibre.com.ar/nota/envios-full-seguridad-y-velocidad-en-tus-entregas); [Cómo gestionar cambios de producto (ML AR)](https://vendedores.mercadolibre.com.ar/nota/como-gestionar-cambios-de-producto-en-tus-ventas)
- En la API existen tipos de reclamo específicos para compras Full (`fulfillment`, reclamo entre comprador y ML) y para cancelaciones del comprador por envío demorado (`ml_case`) — [Gestionar reclamos (Developers ML AR)](https://developers.mercadolibre.com.ar/es_ar/que-es-un-reclamo)
- Cambio de variante: si el comprador recibe bien el producto y pide otra variante, no afecta la reputación siempre que mandes el producto nuevo dentro del plazo — [Cómo gestionar cambios de producto (ML AR)](https://vendedores.mercadolibre.com.ar/nota/como-gestionar-cambios-de-producto-en-tus-ventas)

### Inferences
- Que el reclamo sea `fulfillment` (entre comprador y ML) sugiere que los problemas logísticos de Full los absorbe ML y no van contra el vendedor. **No lo vi dicho de forma explícita** (ver Gaps).
- Con el nuevo mínimo de 101 ventas, muchas cuentas chicas o medianas pasan a medirse por 365 días: **un error tarda hasta un año en salir de la cuenta**, aunque los límites sean un poco más amplios.

### Gaps
- **[NO VERIFICADO]**: que un reclamo **resuelto a favor del vendedor** quede fuera de la reputación. No lo encontré dicho así en un extracto oficial.
- **[NO VERIFICADO]**: una regla oficial explícita de que las demoras atribuibles al correo o a Mercado Envíos, o las ventas Full, no penalizan la métrica de demoras. La fórmula de la API mide desde "listo para enviar" hasta la "colecta confirmada", lo que sugiere que solo cuenta el tramo del vendedor (ver sección 4).
- No encontré si las ventas que se cuentan son "concretadas" o "totales" para cada métrica de reputación. Para MercadoLíder sí se habla de ventas concretadas.

## 4. Cómo se determina un "despacho con demora" y cómo cuentan las demoras de Flex

### Takeaway
En envíos con Mercado Envíos (colecta o drop-off), la demora se mide desde que la venta está **lista para despachar** hasta que el **correo confirma la colecta o la recepción**. Si eso pasa después del plazo o el horario de corte, cuenta como demora. En **Flex**, la venta que entra antes del horario de corte tiene que entregarse ese mismo día. Si no se entrega antes de las 23 hs, pasa a "envío incorrecto".

### Cited Findings
- El Handling Time se mide desde que el paquete está listo para enviar hasta que el correo confirma la recolección. La excepción es Cross Docking. La tasa es ventas despachadas con retraso / ventas despachadas con me2 — [Sellers reputation (Developers ML AR)](https://developers.mercadolibre.com.ar/en_us/sellers-reputation); [Reputación de vendedores (Developers ML AR)](https://developers.mercadolibre.com.ar/es_ar/reputacion-de-vendedores)
- ML recomienda ajustar el horario de corte por zona, despachar antes a las zonas más lejanas y no acumular paquetes en la semana — [Despachar a tiempo: la clave para una buena reputación (ML AR)](https://vendedores.mercadolibre.com.ar/nota/despachar-tus-ventas-a-tiempo-la-clave-de-una-buena-reputacion)
- Plazo de 48 horas hábiles para despachar con Mercado Envíos desde que se confirma la venta — **[NO OFICIAL]** [klicko.com.ar](https://klicko.com.ar/blog/como-mejorar-reputacion-mercado-libre) (no lo confirmé en una fuente oficial; el plazo real lo marca la fecha límite de despacho de cada venta en el panel).
- **Flex:** las ventas que entran antes del horario de corte se entregan ese mismo día, y las posteriores al día siguiente. Un envío es incorrecto cuando la entrega se demora y afecta la experiencia del comprador. Si no se entregó antes de las 23 hs, se reprograma solo para el día siguiente y cuenta como incorrecto, aunque el comprador cancele después de ese horario — [Envíos Flex: entregas en el día / ¿Cómo mantengo mis publicaciones destacadas? (ML AR)](https://vendedores.mercadolibre.com.ar/nota/envios-flex-entregas-en-el-dia)
- Flex: si el pedido no se entrega antes de las 21 hs y el comprador reprograma o no está, también cuenta como envío incorrecto. Si la visita fallida por comprador ausente se informa, no afecta la métrica — [Consejos para hacer entregas con Envíos Flex (Ayuda ML AR)](https://www.mercadolibre.com.ar/ayuda/4459); [Por qué es importante la reputación (ML AR)](https://vendedores.mercadolibre.com.ar/nota/por-que-es-importante-la-reputacion-del-vendedor)
- Exposición en Flex: depende del **% semanal de envíos correctos**. Con menos del 97% la exposición pasa a "regular": se mantiene "Llega hoy" pero con horario de corte limitado en las zonas con más envíos incorrectos. Por debajo del 90% se pierde el destaque "Llega hoy". Una sola demora en la semana no quita la exposición, pero sí cuenta para la reputación — [Envíos Flex (ML AR)](https://vendedores.mercadolibre.com.ar/nota/envios-flex-entregas-en-el-dia); [Cómo consigo excelente exposición y "Llega hoy" (Ayuda ML AR)](https://www.mercadolibre.com.ar/ayuda/4600)
- Envíos por cuenta del vendedor (sin ME): lo que se mira es si el envío llega a tiempo según la promesa de entrega. Con una demora de más de 10 días en un envío despachado, el comprador recibe un reembolso automático. Las demoras de 1 a 10 días generan un reclamo que el vendedor tiene que responder — [Por qué es importante la reputación (ML AR)](https://vendedores.mercadolibre.com.ar/nota/por-que-es-importante-la-reputacion-del-vendedor) (según extracto del buscador)

### Inferences
- Para el depósito, la regla operativa es: **"listo para despachar" no es "despachado"**. La venta cuenta como a tiempo recién cuando el correo escanea el paquete (colecta o drop-off) antes del corte o la fecha límite. Un paquete armado que pierde la colecta cuenta como demora.
- En Flex hay dos castigos separados: (a) la exposición semanal (97% / 90%) y (b) la métrica de reputación "envíos incorrectos" (10% / 13%). Una demora suma a las dos.

### Gaps
- No pude confirmar el texto oficial exacto de "fecha límite de despacho" ni cómo se calcula a partir del horario de corte para colecta vs. drop-off en AR, por ejemplo si una venta después del corte tiene hasta el día hábil siguiente. **Hay que confirmarlo en el panel**, donde cada venta muestra "Despachá antes del…".
- No encontré si los feriados o días no hábiles cambian el plazo en AR.

## 5. MercadoLíder en Argentina: niveles, requisitos y beneficios

### Takeaway
Hay tres medallas: **MercadoLíder (Silver)**, **Gold** y **Platinum**. En común piden más de 4 meses de antigüedad, reputación **verde (oscuro)** y requisitos de calidad más duros (reclamos < 1%, demoras < 8%). La ayuda oficial que encontré pide 60 / 180 / 415 ventas concretadas y $380.000 / $1.300.000 / $3.820.000 facturados en los últimos 60 días. **Esos montos en pesos parecen viejos.** Fuentes no oficiales de 2026 dicen que desde el 16/09/2026 son $1.500.000 / $3.000.000 / $9.000.000. **Hay que confirmarlo en el panel.**

### Cited Findings
- Requisitos según la ayuda oficial: más de 4 meses de antigüedad, reputación verde oscuro y, **en los últimos 60 días**, ventas concretadas de **60+ (MercadoLíder), 180+ (Gold) y 415+ (Platinum)**, con facturación de **$380.000, $1.300.000 y $3.820.000**. Las ventas concretadas son las que el comprador ya recibió — [Todo sobre ser MercadoLíder (Ayuda ML AR)](https://www.mercadolibre.com.ar/ayuda/Ser-MercadoL%C3%ADder_4058). **No tiene fecha visible. Los montos en ARS probablemente estén desactualizados por la inflación.**
- Requisitos de calidad de MercadoLíder según esa misma ayuda: reclamos < 1%, mediaciones < 0,5%, canceladas por el vendedor < 0,5% y despachos con demora < 8% — [Todo sobre ser MercadoLíder (Ayuda ML AR)](https://www.mercadolibre.com.ar/ayuda/Ser-MercadoL%C3%ADder_4058). La API para MLA confirma el 8% de demoras para "Líderes" — [Reputación de vendedores (Developers ML AR)](https://developers.mercadolibre.com.ar/es_ar/reputacion-de-vendedores). La nota de reputación confirma el 1% de reclamos para MercadoLíder — [Por qué es importante la reputación (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/por-que-es-importante-la-reputacion-del-vendedor)
- Una nota más vieja del Centro de vendedores menciona "menos del 2% de ventas canceladas con devolución de dinero" como requisito básico. **Contradice** el 0,5% de la ayuda — [Qué necesitás para ser MercadoLíder (Centro de vendedores, versión blog)](https://vendedores.mercadolibre.com.ar/blog/notas/que-necesitas-para-ser-mercadolider/)
- Una nota oficial dice que desde el 16 de septiembre se actualizan dos criterios ("límites de ventas afectadas" y "tiempo de medición"). El extracto apareció asociado a MercadoLíder, pero **no indica cambios de facturación** — [Qué necesitás para ser MercadoLíder (ML AR)](https://vendedores.mercadolibre.com.ar/aprender/nota/que-necesitas-para-ser-mercadolider)
- **[NO OFICIAL]** Desde el **16/09/2026**, la facturación mínima sería **Platinum ≥ $9.000.000, Gold ≥ $3.000.000 y Silver ≥ $1.500.000** — [UpSeller (09/09/2026)](https://www.upseller.com/es/blog-article-1020); coincide con [Calculadora Klicko 2026](https://klicko.com.ar/calculadora-reputacion-mercado-libre) (60/180/415 ventas; $1,5M/$3M/$9M). Otros terceros dan cifras viejas o distintas ($1.300.000 para Gold según [Nubimetrics](https://academia.nubimetrics.com/mercado-lider-gold), y $1.820.000 en 3 meses para Platinum según [gobots](https://gobots.ai/ar/blog/reputacion-mercadolider-platinum/)). **Hay contradicción. No la pude resolver con una fuente oficial.**
- Beneficios: más exposición en los listados cuanto más alto el nivel, envío gratis en productos nuevos y atención personalizada por chat del equipo de ML — [Qué necesitás para ser MercadoLíder (ML AR)](https://vendedores.mercadolibre.com.ar/nota/que-necesitas-para-ser-mercadolider)
- La medalla aparece en la API como `power_seller_status` = silver / gold / platinum — [Sellers reputation (Developers ML AR)](https://developers.mercadolibre.com.ar/en_us/sellers-reputation)

### Inferences
- Para MercadoLíder el margen operativo es más chico que para "solo verde": **demoras < 8% (y no 10%)**, cancelaciones propias < 0,5% y reclamos < 1%. Al equipo de depósito y de publicaciones hay que enseñarles el objetivo de MercadoLíder, no el de verde.
- Los montos en pesos los actualiza ML cada tanto. Para enseñar, conviene decir "el panel muestra cuánto te falta" y no fijar una cifra.

### Gaps
- **[NO VERIFICADO]**: los montos de facturación en ARS vigentes a octubre 2026 en una fuente oficial.
- No encontré una lista oficial de **beneficios diferenciados** entre Gold y Platinum (por ejemplo, descuentos en costos o atención dedicada).
- No sé si el cambio de 101 ventas / 365 días afecta también el período de medición de MercadoLíder. La ayuda dice "últimos 60 días".

## 6. Cómo ve el vendedor estas métricas en su panel (qué confirmar en la cuenta propia)

### Takeaway
La cuenta propia es la fuente definitiva. En **Reputación** se ve el color, el período de medición (60 o 365 días), el % de cada métrica contra su límite, el estado de MercadoLíder y los productos más afectados. En **Métricas > Atención a tus compradores** está el detalle de cada venta con problemas y se piden las exclusiones.

### Cited Findings
- En "Métricas" > "Atención a tus compradores" hay un gráfico de reclamos, cancelaciones y devoluciones. Con "Revisar todos" se abre el listado de "Ventas con problemas", que muestra el tipo de problema, si afectó la reputación y el detalle de cada venta. Desde ahí se pide la exclusión — [Evitá problemas en tus ventas con las métricas de atención (ML AR)](https://vendedores.mercadolibre.com.ar/nota/analiza-tus-metricas-de-atencion-y-reduci-problemas-en-tus-ventas); [Conocé las reglas de exclusión (ML AR)](https://vendedores.mercadolibre.com.ar/nota/conoce-las-reglas-de-exclusion)
- En "Posventa" se ven los problemas de las ventas y el motivo de cada uno. Desde la sección **Reputación** se puede descargar el listado de todos los reclamos y ver un resumen de los productos más afectados — [Consejos para evitar que tus compradores inicien un reclamo (ML AR)](https://vendedores.mercadolibre.com.ar/nota/consejos-para-evitar-que-tus-compradores-inicien-un-reclamo?guideKeyId=GE21)
- Sección general de métricas del negocio — [Cómo aprovechar tus métricas (ML AR)](https://vendedores.mercadolibre.com.ar/nota/todo-lo-que-necesitas-saber-sobre-la-seccion-de-metricas)
- Hay que tomar como referencia la tabla de la nota del cambio y el panel de cada vendedor, porque varias páginas de ayuda todavía tienen cifras viejas — [Vamos a cambiar la forma en que calculamos tu reputación (ML AR)](https://vendedores.mercadolibre.com.ar/nota/vamos-a-cambiar-la-forma-en-que-calculamos-tu-reputacion)

### Inferences
Checklist para confirmar en el panel propio antes de dar la capacitación:
1. Si la cuenta se mide por **60 o por 365 días** (depende de si tuvo 101+ ventas en 60 días).
2. Los **límites exactos** que muestra el panel para cada métrica y color, comparados con la tabla de la sección 2.
3. El nombre de la métrica de demoras en el panel ("Envíos incorrectos" / "Despachos con demora") y su % actual.
4. El **horario de corte** configurado para colecta / drop-off / Flex, y la "fecha límite de despacho" que aparece en cada venta.
5. Los requisitos de MercadoLíder vigentes (ventas y **facturación en ARS**) y cuánto falta.
6. El descuento de envío gratis que le corresponde a la cuenta por su color.
7. Qué ventas aparecen como "afectó tu reputación" en "Ventas con problemas", y si hay exclusiones para pedir.

### Gaps
- No pude ver capturas ni la ruta exacta de menú vigente (por ejemplo "Mi cuenta > Reputación" o "Ventas > Reputación"). La interfaz puede variar. **Hay que confirmarlo navegando en la cuenta.**
