# Publicaciones en Mercado Libre Argentina, foco en autopartes (reglas y buenas prácticas vigentes, octubre 2026)

> **Cómo se armaron estas notas (leer primero).** La sesión de investigación (21/10/2026) **no pudo abrir directamente** ningún dominio de Mercado Libre (mercadolibre.com.ar, vendedores.mercadolibre.com.ar, developers.mercadolibre.com.ar, api.mercadolibre.com): el proxy de salida rechazó todas las conexiones. Todo lo "oficial" de abajo viene de **extractos del buscador sobre páginas oficiales de ML Argentina**, con la URL oficial citada. Es buena señal, pero no equivale a haber leído la página entera ni a ver su fecha de actualización. Etiquetas:
> - **[OFICIAL-AR]**: extracto de una página oficial de ML Argentina.
> - **[OFICIAL-OTRO PAÍS]**: oficial, pero de otro sitio de ML (MX, CL, CO).
> - **[NO OFICIAL]**: blog, integrador o calculadora de terceros. Sirve solo para cruzar datos.
> - **[CONFIRMAR EN TU PANEL]**: montos y umbrales que cambian seguido.

---

## 1. Títulos: largo máximo, estructura, qué no poner, títulos en catálogo

### Takeaway
La estructura oficial es **Producto + Marca + Modelo + especificaciones clave**, sin signos de puntuación, sin símbolos, sin "oferta" ni datos de envío, cuotas o devoluciones, y sin poner color ni condición en el título. El largo máximo **lo fija cada categoría** (campo `max_title_length` en la API). La referencia típica es de **60 caracteres**, pero no encontré una página oficial de ML Argentina que diga "60" para autopartes.

### Cited Findings
- [OFICIAL-AR] Fórmula recomendada: "Producto + Marca + Modelo" (ej. "Zapatillas Adidas Superstar") y, si hace falta, especificaciones — [Cómo hacer un buen título para tu publicación (Centro de Vendedores AR)](https://vendedores.mercadolibre.com.ar/nota/como-hacer-un-buen-titulo-para-tu-publicacion); [Cómo hacer un buen título (Ayuda AR)](https://www.mercadolibre.com.ar/ayuda/Como-hacer-una-buena-publicacion_677)
- [OFICIAL-AR] Ejemplo de la API: "Microondas Grill BGH Quick Chef B223D plata 23L 220V" (Producto + Marca + modelo + algunas especificaciones que ayudan a identificarlo) — [Publicar productos (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/sobre-nuestra-api/publica-productos)
- [OFICIAL-AR] Compatibilidad con otra marca: aclararla con "para" o "compatible con". **No** usar "tipo", "símil", "igual a", "idéntico a". Si el producto no tiene marca, indicar "genérico" — [Cómo hacer un buen título (Ayuda AR)](https://www.mercadolibre.com.ar/ayuda/Como-hacer-una-buena-publicacion_677); [Centro de Vendedores AR](https://vendedores.mercadolibre.com.ar/nota/como-hacer-un-buen-titulo-para-tu-publicacion); ver también [Cómo evitar denuncias por infringir propiedad intelectual](https://vendedores.mercadolibre.com.ar/nota/como-publicar-sin-infringir-propiedad-intelectual)
- [OFICIAL-AR] No incluir en el título información sobre devoluciones, envío gratis ni pagos en cuotas (ML lo muestra solo). Tampoco "oferta" o "promoción": los descuentos llevan sus propias etiquetas — [Cómo hacer un buen título (Ayuda AR)](https://www.mercadolibre.com.ar/ayuda/Como-hacer-una-buena-publicacion_677)
- [OFICIAL-AR] El color no va en el título: se crean variantes. El estado (nuevo/usado) se carga en las características — [Cómo hacer un buen título (Ayuda AR)](https://www.mercadolibre.com.ar/ayuda/Como-hacer-una-buena-publicacion_677)
- [OFICIAL-AR] Forma: sin signos de puntuación ni símbolos, siempre un espacio entre palabras, sin errores de ortografía. Evitar abreviaturas poco claras y mayúsculas innecesarias — [Cómo hacer un buen título (Ayuda AR)](https://www.mercadolibre.com.ar/ayuda/Como-hacer-una-buena-publicacion_677); [Cómo gestionar tus publicaciones de forma efectiva](https://vendedores.mercadolibre.com.ar/nota/como-gestionar-tus-publicaciones-de-forma-efectiva)
- [OFICIAL-AR] Datos de contacto (teléfono, mail, links) prohibidos en título, descripción, fotos, preguntas y respuestas. Van solo en los campos específicos del formulario — [Políticas de Publicación AR](https://www.mercadolibre.com.ar/seguro_publicacion.html); [Cómo gestionar tus publicaciones de forma efectiva](https://vendedores.mercadolibre.com.ar/nota/como-gestionar-tus-publicaciones-de-forma-efectiva)
- [OFICIAL-AR] Hay una herramienta de IA, "Sugerir un título", que genera títulos automáticamente (según el extracto del buscador sobre las páginas de títulos de ML AR) — [Centro de Vendedores AR](https://vendedores.mercadolibre.com.ar/nota/como-hacer-un-buen-titulo-para-tu-publicacion)
- [OFICIAL-AR, API] El largo máximo del título se define **por categoría** en `settings.max_title_length` (ej. 60 en celulares y "Otros"; 200 en algunas categorías de alquiler de inmuebles). El valor vigente sale de `/categories/{id}` — [Categories and Attributes (Developers AR)](https://developers.mercadolibre.com.ar/en_us/categories-and-attributes); [List products (Developers AR)](https://developers.mercadolibre.com.ar/en_us/list-products)
- [OFICIAL-AR, API] En User Products, el nombre de la familia también tiene que respetar el `max_title_length` del dominio — [User Products (Developers AR)](https://developers.mercadolibre.com.ar/en_us/user-products)
- [OFICIAL-OTRO PAÍS: Chile] "El título tiene un límite máximo de 60 caracteres" — [La clave está en el título (ML Chile)](https://www.mercadolibre.cl/consejo_1)
- [NO OFICIAL] Integradores repiten 60 caracteres como máximo y la estructura producto + marca + modelo + especificaciones — [anymarket](https://suporteanymarket.freshdesk.com/es-LA/support/solutions/articles/19000105011-exigencias-y-particularidades-mercado-libre); [Ventiapp](https://ayuda.ventiapp.mx/es/article/publicador-masivo-mercadolibre-1zda7u/). Una guía SEO 2026 dice que algunas categorías aceptarían hasta 90 caracteres y que en mobile solo se ven ~60 sin cortar: **no verificado** — [comercioelectronico.lat](https://comercioelectronico.lat/guias/titulos-descripciones-producto-mercadolibre-shopify-seo/)
- [OFICIAL-AR] Catálogo: la ficha de catálogo trae fotos, título, descripción y características principales precargadas. El vendedor busca el producto (en autopartes, por "Número de pieza"), revisa los datos y define precio y condiciones de venta — [Publicá rápido autopartes con el catálogo de Mercado Libre](https://vendedores.mercadolibre.com.ar/nota/publica-rapido-con-el-catalogo-de-mercado-libre)
- [OFICIAL-AR] Compatibilidades: no indicarlas en el título ni en la ficha técnica, se cargan en la herramienta de compatibilidades (fuente original de integrador. El dato coincide con la doc de ML pero no lo leí textual en una página oficial) — [Real Trends (NO OFICIAL)](http://ayuda.real-trends.com/es/articles/6399228-como-agrego-la-compatibilidad-a-mis-publicaciones-de-autopartes)

### Inferences
- Plantilla para autopartes: **[Pieza] [Marca de la pieza] [Nº de pieza/modelo] [especificación clave] para [Marca vehículo] [Modelo]**, ej. "Amortiguador Delantero Corven 12345 para Volkswagen Gol Trend". La palabra "para" es la vía oficial para nombrar la marca del vehículo sin infringir propiedad intelectual. El listado completo de vehículos va en Compatibilidades, no en el título.
- En catálogo, el título lo pone la ficha del producto de ML y el vendedor no compite por el título. Esto se deduce de que la ficha "incluye título".
- Conviene que el equipo lea `max_title_length` de cada categoría de autopartes (vía API o mirando el contador del formulario) en vez de asumir 60.

### Gaps
- No encontré un texto oficial de ML Argentina que diga explícitamente el máximo en caracteres para categorías de Accesorios para Vehículos/Autopartes (MLA1747). Hay que confirmarlo en el formulario o en la API.
- No pude leer completa la página de Ayuda AR "Cómo hacer un buen título" (bloqueada), así que su fecha de actualización no está verificada.
- No encontré una regla oficial explícita contra "todo en MAYÚSCULAS" en el título. Solo "evitar mayúsculas innecesarias".

---

## 2. Fotos: tamaño, fondo, prohibiciones, cantidad, foto principal, consecuencias

### Takeaway
Subí fotos de **1200 x 1200 px** (mínimo aceptado 500 x 500, máximo 1920 x 1920, hasta 10 MB, JPG/PNG). La portada va con **fondo blanco digital** (en algunas categorías también gris claro o crema), un solo artículo, sin logos, textos, marcas de agua, bordes, QR ni datos de contacto. Una foto que no cumple genera moderación: pérdida de exposición (tag `poor_quality_thumbnail`) o pausa.

### Cited Findings
- [OFICIAL, Developers] Subir imágenes de 1200 x 1200 px. Máximo aceptado 1920 x 1920 px y mínimo 500 x 500 px (las más chicas no se agrandan). Hasta 10 MB. Formatos JPG, JPEG y PNG — [Working with pictures (Developers AR)](https://developers.mercadolibre.com.ar/en_us/working-with-pictures); [Imágenes (Developers, sitio CO, es_ar)](https://developers.mercadolibre.com.co/es_ar/trabajar-con-imagenes). La guía tenía ~2,7 años de antigüedad según el buscador.
- [OFICIAL-AR, API] La cantidad máxima de fotos depende de la categoría (`max_pictures_per_item`, `max_pictures_per_item_var`). Ejemplos: 12 en celulares, 30 en alquileres — [Categories and Attributes (Developers AR)](https://developers.mercadolibre.com.ar/en_us/categories-and-attributes)
- [OFICIAL-AR] Foto principal: un solo artículo, alta resolución, fondo blanco, sin logos del vendedor, sin texto ni similares — [Políticas de Publicación AR](https://www.mercadolibre.com.ar/seguro_publicacion.html)
- [OFICIAL-AR] Portada con fondo digitalizado blanco, crema o gris claro, sin degradé ni texturas. El producto debe diferenciarse del fondo. "No agregues tu logo, marcas de agua, bordes, códigos QR o textos" — [Requisitos de fotos para Accesorios](https://vendedores.mercadolibre.com.ar/nota/requisitos-de-fotos-para-vender-accesorios); [Requisitos de fotos para Packs](https://vendedores.mercadolibre.com.ar/nota/requisitos-de-fotos-para-vender-packs); [Las fotos son la cara de tu negocio](https://vendedores.mercadolibre.com.ar/nota/las-fotos-son-la-cara-de-tu-negocio-lucite-en-ellas)
- [OFICIAL-AR] Prohibido insertar información personal o cualquier forma de contacto en las fotos — [Políticas de Publicación AR](https://www.mercadolibre.com.ar/seguro_publicacion.html)
- [OFICIAL-AR, categoría Hogar/Muebles] Portada cuadrada, nítida, de al menos 1200 x 1200 px. Secundarias con fondo blanco — [Requisitos de fotos para sillones](https://vendedores.mercadolibre.com.ar/nota/requisitos-de-fotos-para-sillones) (no es autopartes, sirve como referencia del estándar).
- [OFICIAL-AR] Moderación de imágenes: puede dejar la publicación activa o pausada, con el tag `poor_quality_thumbnail`. Para recuperar exposición hay que cambiar las fotos o completar la ficha técnica — [Moderaciones de imágenes (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/moderaciones-de-imagenes)
- [OFICIAL-AR] Existe una API de **diagnóstico de imágenes** que valida fotos antes de publicarlas y detecta fondo no blanco, tamaño insuficiente, textos/logos y marcas de agua. ML también ofrece un editor (botón del lápiz sobre la foto) para corregirlas — [Diagnóstico de imágenes (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/diagnostico-imagenes); [Moderaciones de imágenes](https://developers.mercadolibre.com.ar/es_ar/moderaciones-de-imagenes)
- [OFICIAL-AR] Fotos que no cargan bien, no cumplen los requisitos mínimos o son de mala calidad son motivo de pausa — [Moderaciones con pausado (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/moderaciones-con-pausado); [Cómo gestionar tus publicaciones](https://vendedores.mercadolibre.com.ar/nota/como-gestionar-tus-publicaciones-de-forma-efectiva)
- [NO OFICIAL] El zoom se activa con imágenes de más de 800 px de ancho. Conviene que el producto ocupe ~95% del encuadre. ML recomendaría no fotografiar contra una pared o sábana blanca (sombras) y crear el fondo blanco digitalmente — [Jaguar Sheet](https://jaguarsheet.com/es/blog/calidad-imagenes-mercado-libre); [Multivende](https://help.multivende.com/hc/es-419/articles/30498468592141-Gu%C3%ADa-de-Im%C3%A1genes-para-Mercado-Libre); [Algoritmo Digital](https://algoritmodigital.com.ar/fotos-que-venden-en-mercado-libre/)
- [OFICIAL-AR, según el extracto del buscador] En algunas categorías (moda) sugieren formato vertical de 1200 x 1540 px, en RGB — [Requisitos de fotos para Prendas inferiores](https://vendedores.mercadolibre.com.ar/nota/requisitos-de-fotos-para-bottoms). No aplica a autopartes.

### Inferences
- Estándar práctico para autopartes: 1200 x 1200 px cuadrada, fondo blanco digital puro, pieza sola centrada ocupando casi todo el cuadro. En las secundarias: detalles, número de pieza o etiqueta del fabricante, conectores y una foto de medidas, siempre sin texto agregado ni logo propio.
- Lo más grave en autopartes usadas es fotografiar la pieza sobre el banco del taller con el logo del desarmadero o un teléfono. Eso dispara moderación por contacto o logo.

### Gaps
- No encontré la página oficial "Requisitos de fotos" específica para **Accesorios para Vehículos/Autopartes** en AR. La nota de "Accesorios" encontrada podría ser de moda (accesorios de vestir).
- No pude confirmar con fuente oficial AR la cantidad máxima de fotos en autopartes ni si el fondo blanco es obligatorio (vs. recomendado) para piezas usadas.

---

## 3. Ficha técnica / atributos, GTIN/EAN/MPN/OEM, indicadores de calidad

### Takeaway
La ficha técnica (atributos) define exposición y calidad. Cada categoría marca atributos `required`, `new_required` y `conditional_required`. En autopartes el **Número de pieza** (atributo `PART_NUMBER`, MPN) es el identificador clave: con él ML encuentra el producto de catálogo y define compatibilidades. El GTIN (EAN) se valida al publicar y, si es incorrecto o se repite entre productos distintos, ML lo borra y la publicación pierde visibilidad.

### Cited Findings
- [OFICIAL-AR] Los atributos obligatorios dependen de la categoría y figuran como "required" en el detalle de la categoría. La API también usa `new_required` y `conditional_required` — [Categorías y Atributos (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/categorias-y-atributos); [What is an attribute? (Developers AR)](https://developers.mercadolibre.com.ar/en_us/attributes)
- [OFICIAL-AR] "La ficha técnica del producto es el conjunto de atributos que describen al producto". Hoy el GTIN es el identificador en el que se agrupan todos los demás. Los identificadores más comunes son GTIN, MPN (número de pieza del fabricante) y marca. Algunas categorías exigen GTIN y la exigencia puede volverse obligatoria según cuántos GTIN tenga ya publicados la marca — [Identificadores de productos (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/identificadores-de-productos)
- [OFICIAL-AR] Los GTIN pueden tener 8, 10, 12, 13 o 14 dígitos y se validan: si no son válidos, no se permite el POST — [Identificadores de productos (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/identificadores-de-productos)
- [OFICIAL-AR] El número de pieza sirve para localizar un repuesto de manera única y definir sus compatibilidades — [Identificadores de productos (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/identificadores-de-productos)
- [OFICIAL-AR] Ejemplo de producto de suspensión con atributo `PART_NUMBER` (Número de pieza) junto a la marca — [Buscador de productos (Developers AR)](https://developers.mercadolibre.com.ar/buscador-de-productos); dominios y atributos de autopartes en [Referencias de dominios, productos y atributos para Autopartes](https://developers.mercadolibre.com.ar/es_ar/referencias-de-dominios-productos-y-atributos-para-autopartes)
- [OFICIAL-AR] "Completar el código universal de tus productos es clave para que tus publicaciones tengan más exposición, mejor calidad y más compradores te encuentren". Si el código es incorrecto o se usa el mismo para productos distintos, hay que corregirlo. ML puede borrarlo y la publicación pierde visibilidad. Si el producto no tiene código de fábrica, **no hace falta comprar uno** — [Código universal de producto: todo lo que tenés que saber](https://vendedores.mercadolibre.com.ar/nota/codigo-universal-de-producto-todo-lo-que-tenes-que-saber)
- [OFICIAL-AR] API de calidad: `quality_level` = 0 cuando no cumple los requisitos de completitud y calidad y **está perdiendo exposición**, y 1 cuando cumple todo. Devuelve los atributos faltantes (ej. GTIN). ML está cambiando la medición: el recurso `/health` se reemplaza por `/performance` — [Calidad de publicaciones (Developers AR)](https://developers.mercadolibre.com.ar/calidad-de-publicaciones); [Carga de atributos (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/conoce-como-estan-los-vendedores-frente-la-carga-de-atributos)
- [OFICIAL-AR] Guía general de calidad de publicaciones para vendedores — [¿Cómo garantizar la calidad de tus publicaciones?](https://vendedores.mercadolibre.com.ar/aprender/nota/como-crear-publicaciones-de-calidad)
- [OFICIAL-AR] Una moderación por foto se resuelve cambiando fotos **o completando la ficha técnica** — [Moderaciones de imágenes](https://developers.mercadolibre.com.ar/es_ar/moderaciones-de-imagenes)

### Inferences
- Orden de carga para autopartes: 1) Marca de la pieza, 2) Número de pieza/MPN tal como figura en la caja o la pieza, 3) GTIN solo si existe en el empaque (no inventarlo ni repetirlo), 4) resto de atributos obligatorios y opcionales de la categoría (posición, lado, material, etc.).
- Los indicadores "calidad de la publicación" / "experiencia de compra" del panel se nutren de la completitud de la ficha y de las fotos. Que el recurso `/health` pase a `/performance` indica que el panel puede mostrar otros nombres o niveles.

### Gaps
- No encontré con fuente oficial AR si existe un atributo específico de "Código OEM" separado del "Número de pieza" en las categorías MLA de autopartes. Confirmarlo en el formulario de cada categoría.
- No pude leer la página de "Experiencia de compra" (indicador de reclamos/devoluciones) para describir sus umbrales.

---

## 4. Autopartes en Argentina: compatibilidades, número de pieza, condición, ítems restringidos

### Takeaway
Las publicaciones de autopartes tienen que cargar **vehículos compatibles** (por catálogo/número de pieza, por atributos Marca-Modelo-Año-Motor o como universal) y, en algunas categorías, la **posición** de la pieza. Si publicás de forma masiva y no lo completás en **7 días**, ML pausa la publicación. **No se permite vender autopartes usadas sin las certificaciones legales** emitidas por la autoridad de aplicación. No encontré una prohibición específica y explícita de airbags usados en ML AR.

### Cited Findings
- [OFICIAL-AR] Compatibilidades: asociar el ítem con vehículos (Marca, Modelo, Año, Motor; ej. "Amortiguador Corven Plus") — [Compatibilidades entre ítems y productos de Autopartes (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/compatibilidades-entre-items-y-productos)
- [OFICIAL-AR] Hay distintas formas de informar compatibilidades — [Las diferentes formas de informar compatibilidades](https://vendedores.mercadolibre.com.ar/nota/las-diferentes-formas-de-informar-compatibilidades); [El poder de la herramienta de compatibilidades](https://vendedores.mercadolibre.com.ar/nota/el-poder-de-la-herramienta-de-compatibilidades). [NO OFICIAL] Los tipos serían universal, por catálogo y por atributos — [Bling MX](https://ayuda.bling.mx/hc/es-mx/articles/15803807113997-Compatibilidad-de-autopartes-en-los-anuncios-de-Mercado-Libre); [Multivende](https://help.multivende.com/hc/es-419/articles/30504115907085-Compatibilidad-de-autopartes-para-Mercado-Libre)
- [OFICIAL-AR] Si publicás muchos productos a la vez (integrador o ML), tenés **7 días** para agregar la compatibilidad. Si no, las publicaciones se pausan. Los ítems con compatibilidades incompletas se marcan con etiqueta (API: `incomplete_compatibilities`, `pending_compatibilities`). En "Publicaciones" hay un filtro para encontrar las que no tienen vehículos compatibles — [Compatibilidades entre ítems y productos (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/compatibilidades-entre-items-y-productos); [Las diferentes formas de informar compatibilidades](https://vendedores.mercadolibre.com.ar/nota/las-diferentes-formas-de-informar-compatibilidades)
- [OFICIAL-AR] **Posiciones**: en algunas categorías hay que indicar la posición de la pieza (ej. delantera/trasera, izquierda/derecha). Publicadas de forma masiva sin posiciones, se pausan a los 7 días de creadas — [Agregá posiciones y evitá que pausemos tus publicaciones](https://vendedores.mercadolibre.com.ar/aprender/nota/como-agregar-posiciones-en-la-autoparte-y-evitar-que-se-paus)
- [OFICIAL-AR] Informar vehículos no compatibles genera reclamos, afecta la reputación y produce costos de devolución. Hay que revisar las compatibilidades sugeridas antes de copiarlas — [Cómo evitar reclamos por incompatibilidad](https://vendedores.mercadolibre.com.ar/nota/como-evitar-reclamos-por-incompatibilidadd)
- [OFICIAL-AR, API] Desde el **15/07/2026** dejó de estar disponible `POST /catalog_compatibilities/products_search/chunks`. Las integraciones que lo usaban tienen que migrar — [Compatibilidades entre ítems y productos (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/compatibilidades-entre-items-y-productos)
- [OFICIAL-AR] Publicar con catálogo: ingresar el "Número de pieza" en el buscador, revisar los datos precargados y definir precio y condiciones — [Publicá rápido autopartes con el catálogo](https://vendedores.mercadolibre.com.ar/nota/publica-rapido-con-el-catalogo-de-mercado-libre)
- [OFICIAL-AR] Accesorios de vehículos tienen su propio esquema de compatibilidad — [Compatibility between items and vehicle accessories (Developers AR)](https://developers.mercadolibre.com.ar/en_us/compatibility-between-items-and-vehicle-accessories?nocache=true)
- [OFICIAL-AR] **Artículos prohibidos**: "No se permite la oferta y/o venta de autopartes y repuestos usados para autos, motos, camiones, camionetas, tráilers y acoplados que no cuenten con las certificaciones legales correspondientes" emitidas por la autoridad de aplicación. Tampoco se permiten artículos de contrabando, falsificados o adulterados — [Artículos Prohibidos (ML AR)](https://www.mercadolibre.com.ar/seguro_prohibidos.html)
- [OFICIAL-AR, observación de listados] Los listados de autopartes tienen filtro de condición **Nuevo / Usado / Reacondicionado** — [Reacondicionado Autos Accesorios](https://vehiculos.mercadolibre.com.ar/reacondicionado-autos-accesorios); [Autopartes Usadas](https://listado.mercadolibre.com.ar/autopartes-usadas)
- [NO OFICIAL, otro país] eBay prohibió la venta de airbags e infladores en todo el mundo por el riesgo de piezas falsificadas (contexto España). **No es una política de ML** — [Motor16](https://www.motor16.com/las-ultimas-noticias/ebay-prohibicion-venta-airbags)
- [NO OFICIAL] Un integrador afirma que con un integrador se aceptan todas las compatibilidades sugeridas o ninguna — [Real Trends](http://ayuda.real-trends.com/es/articles/6399228-como-agrego-la-compatibilidad-a-mis-publicaciones-de-autopartes)

### Inferences
- La "certificación legal" para autopartes usadas en Argentina corresponde, presumiblemente, al régimen de desarmaderos (Ley 25.761 y su sistema de identificación de autopartes, que gestiona la DNRPA). **No verificado en esta investigación.** Confirmarlo con asesoría legal o en la página de prohibidos antes de publicar usados.
- Las piezas de seguridad usadas (airbags, pretensores, frenos) caen como mínimo bajo la regla general de usados sin certificación. Recomendación conservadora: no publicarlas usadas sin certificado.
- Flujo sugerido: buscar por número de pieza en catálogo, aceptar o revisar las compatibilidades, cargar posiciones y verificar en 7 días el filtro "sin compatibilidades".

### Gaps
- No encontré una regla oficial ML AR que mencione explícitamente airbags usados.
- No encontré la definición oficial ML AR de "reacondicionado" para autopartes (en catálogo existen grados excelente/bueno/aceptable, pero documentados para celulares).
- No confirmé qué categorías MLA exigen compatibilidades obligatorias ni cuáles exigen posición.

---

## 5. Tipos de publicación (Clásica vs Premium), comisiones, cargo fijo, envío gratis

### Takeaway
En el frontend ML AR ya no muestra "Clásica"/"Premium": distingue las publicaciones por cuotas. En la API siguen como **`gold_special` (Clásica: solo cuotas con interés del banco)** y **`gold_pro` (Premium: cuotas sin interés al mismo precio, con costo adicional)**. La comisión es un % por categoría (terceros: ~11,8–15% Clásica y ~14,8–17,14% Premium, + IVA). Hay un **cargo fijo por unidad solo bajo $33.000**, cuyos montos cambian seguido. El umbral de envío gratis en productos nuevos que cita la ayuda AR es **$33.000**. **Todo esto: [CONFIRMAR EN TU PANEL] / simulador de costos.**

### Cited Findings
- [OFICIAL-AR] ML dejó de usar "Clásica"/"Premium" en el frontend y ahora diferencia las publicaciones por las cuotas que ofrecen. En backend siguen `gold_special` (Clásica: solo cuotas con interés bancario) y `gold_pro` (Premium: cuotas propias con costo adicional). En ambas se paga el cargo por vender y, si corresponde, el costo fijo — [Tipos de publicación (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/tipos-de-publicacion-y-actualizaciones-de-articulos)
- [OFICIAL-AR] En campañas de cuotas, las Premium ofrecen 3, 6 o 9 cuotas al mismo precio publicado, según la campaña. Las Clásicas pueden entrar en campañas de 3 a 12 cuotas con interés bajo. El programa Cuota Simple fue discontinuado — [Campañas con cuotas para Marketplace (Developers AR)](https://developers.mercadolibre.com.ar/campana-con-cuotas-para-marketplace)
- [OFICIAL-AR, API] En los ejemplos de la API, ambos tipos figuran con `listing_exposure: "highest"`. No encontré una diferencia oficial de exposición entre Clásica y Premium — [Tipos de publicación (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/tipos-de-publicacion-y-actualizaciones-de-articulos)
- [OFICIAL-AR, histórico] Nota de septiembre de 2019: "hasta 18 cuotas sin interés en publicaciones Premium" (desactualizada) — [Centro de Vendedores AR, 02/09/2019](https://vendedores.mercadolibre.com.ar/2019/09/02/ahora-podes-ofrecer-hasta-18-cuotas-sin-interes-en-tu-publicaciones-premium/)
- [OFICIAL-AR, API] `sale_fee_details.fixed_fee` = costo fijo por unidad vendida. Ya no depende solo del precio, también del **tipo de logística**. Hay un ejemplo de comisión 13% Clásica vs 36% Premium (incluye `financing_add_on_fee`): es un **ejemplo antiguo**, no la tarifa vigente — [Costos por vender (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/comision-por-vender)
- [OFICIAL-AR] El costo fijo se aplica solo a publicaciones de menos de **$33.000**, con montos escalonados por tramo. Un kit de menos de $33.000 paga un solo costo fijo. En Supermercado/Full Súper no hay costo fijo, pero el cargo por vender sube 3 p.p. — [Costos por vender un producto y opciones de cuotas (Ayuda AR)](https://www.mercadolibre.com.ar/ayuda/Costos-para-vender-productos_870). **Fecha de la página no visible.** El buscador mostró montos de $1.115 a $2.810 en esa página (posiblemente ya reemplazados).
- [OFICIAL-AR] Costo por unidad vendida para Full, correo, colecta y puntos de despacho: depende de precio, medidas y peso (el mayor entre físico y volumétrico) — [Ayuda AR 42400](https://www.mercadolibre.com.ar/ayuda/cambios-costos-venta_42400)
- [OFICIAL-AR] Con Full o Colecta no se paga costo fijo en ventas mayores a $33.000 — [Cuánto cuesta operar en Full](https://vendedores.mercadolibre.com.ar/nota/cuanto-cuesta-operar-en-full) (sin fecha clara).
- [OFICIAL-AR] Guía general y simulador de costos — [¿Cómo funcionan los costos de Mercado Libre?](https://vendedores.mercadolibre.com.ar/aprender/nota/como-funcionan-los-costos-de-mercado-libre?guideKeyId=GE53); [Cómo usar el simulador de costos](https://vendedores.mercadolibre.com.ar/aprender/nota/como-usar-el-simulador-de-costos-de-mercado-libre)
- [NO OFICIAL, cronología de montos del cargo fijo — CONFIRMAR EN TU PANEL]:
  - Guías de **enero 2026**: ~$1.115 (hasta $15.000), ~$2.300 ($15.000–$25.000), ~$2.810 ($25.000–$33.000) — [Algoritmo Digital](https://algoritmodigital.com.ar/cuanto-es-la-comision-de-mercado-libre-por-vender/); [Snowprofit](https://snowprofit.com/blog/costos-vender-mercadolibre-argentina)
  - Fuente que afirma vigencia **desde el 01/09/2026**: $1.330 (hasta $14.999), $2.740 ($15.000–$23.999), $3.320 ($24.000–$32.999), al menos con Flex, acuerdo con el comprador o retiro — [Calculadora 2026 Algoritmo Digital](https://algoritmodigital.com.ar/calculadora-comision-mercado-libre-2026/); [Spom Solutions](https://app.spomsolutions.com/herramientas/calculadora-comisiones-mercadolibre). **Fuente única, no confirmada con un comunicado oficial.**
  - Otra fuente con escalones $900 / $1.800 (+IVA) hasta $12.000 / $33.000: **parece desactualizada** — [Jaguar Sheet](https://jaguarsheet.com/es/blog/comisiones-mercado-libre)
- [NO OFICIAL] Comisión % 2026 en AR: Clásica 11,8%–15%, Premium 14,8%–17,14% según categoría. Otra fuente dice 11,62%–17,75% según categoría **y provincia**. Se suma IVA 21% sobre comisión y cargo fijo — [Snowball Partners](https://snowballpartners.co/blogs/comisiones-mercado-libre-2026); [Gestodo](https://gestodo.net/blog/comisiones-mercado-libre-argentina-2026-guia-completa-para-vendedores); [Pyme Inteligente](https://www.pymeinteligente.com.ar/blog/cuanto-cobra-mercado-libre-de-comision); [Digital Sellers](https://digitalsellers.com.ar/blog/comisiones-mercado-libre/). Ninguna dio el % específico de Accesorios para Vehículos con fuente oficial.
- [OFICIAL-AR] Envío gratis: en productos nuevos **desde $33.000** el vendedor ofrece envío gratis con descuentos importantes en el costo, cuando distancia y dimensiones lo permiten. Bajo $33.000, el envío gratis corre por cuenta del vendedor si lo ofrece — [Funcionamiento de los envíos gratis (Ayuda AR 16467)](https://www.mercadolibre.com.ar/ayuda/16467); [Primeros pasos en Envíos Flex](https://vendedores.mercadolibre.com.ar/nota/envios-flex-tarifas)
- [OFICIAL-AR, histórico] Notas anteriores citaban un umbral de $23.000 (desactualizado). Una novedad antigua citaba un precio mínimo de $33 y un costo fijo de $22 — [Cómo funcionan los envíos](https://vendedores.mercadolibre.com.ar/nota/como-funcionan-los-envios-de-mercado-libre); [Novedades en los costos y envíos gratis](https://vendedores.mercadolibre.com.ar/novedad/novedades-en-los-costos-de-tus-publicaciones-y-envios-gratis/)
- [OFICIAL-AR, promoción comprador] La home anunció "envíos gratis en productos desde $15.000/$16.000" (según la versión cacheada). MELI+ ofrece envío gratis desde $15.000 en productos seleccionados, con tope de $5.500. Son beneficios para el **comprador** y no cambian la obligación del vendedor — [Home ML AR](https://www.mercadolibre.com.ar/); [Envíos gratis con meli+](https://www.mercadolibre.com.ar/ofertas/envios-gratis)
- [OFICIAL-AR] Precio mínimo para publicar: $1.000 según un anuncio antiguo de la página de costos — [Ayuda AR 870](https://www.mercadolibre.com.ar/ayuda/Costos-para-vender-productos_870) (confirmar vigencia).

### Inferences
- $33.000 es hoy el corte clave en AR: por debajo pagás cargo fijo y el envío gratis es opcional y a tu costo. Por encima no hay cargo fijo (al menos con Full/Colecta) y el envío gratis corre con subsidio de ML.
- Para autopartes de ticket bajo (filtros, lámparas, fichas), el cargo fijo puede comerse buena parte del margen. Conviene evaluar kits (un solo cargo fijo por kit).

### Gaps
- No obtuve el % oficial vigente de comisión para Accesorios para Vehículos ni la fecha exacta de la última actualización de la tabla oficial (página bloqueada).
- No pude confirmar con fuente oficial el cambio de cargo fijo del 01/09/2026.

---

## 6. Catálogo: publicar en catálogo y competir para ganar

### Takeaway
En catálogo, varios vendedores compiten en una misma página de producto. Gana quien ofrece las **mejores condiciones de venta en conjunto** (precio, cuotas sin interés, envío gratis o en el día), con reputación **verde, verde claro o amarilla**. Las publicaciones con reputación naranja o roja compiten pero no pueden ganar.

### Cited Findings
- [OFICIAL-AR] Lo más importante son las condiciones de venta en conjunto. Se puede ganar con un precio más alto si se ofrecen cuotas sin interés, envío gratis o envío en el día — [¿Qué tengo que hacer para ganar? (Ayuda AR 4648)](https://www.mercadolibre.com.ar/ayuda/-Qu--tengo-que-hacer-para-gana_4648); [Cómo funciona la competencia en catálogo](https://vendedores.mercadolibre.com.ar/nota/como-funciona-la-competencia-en-catalogo)
- [OFICIAL-AR] Reputación necesaria para ganar: verde, verde claro o amarilla. Con naranja o roja se participa pero no se gana — [Ayuda AR 4648](https://www.mercadolibre.com.ar/ayuda/-Qu--tengo-que-hacer-para-gana_4648)
- [OFICIAL-AR] En el detalle de la publicación hay una tabla que te compara con el ganador (o con tu mejor competidor si comparten el primer lugar). Hay **ajuste automático de precios** dentro de los límites que definas — [Ayuda AR 4648](https://www.mercadolibre.com.ar/ayuda/-Qu--tengo-que-hacer-para-gana_4648)
- [OFICIAL-AR] Elegibilidad: el producto tiene que cumplir requisitos, como ser nuevo (en celulares, nuevo o reacondicionado y liberado). Los reacondicionados compiten solo con los de su mismo estado (excelente, bueno, aceptable) — [Qué significa que tu publicación sea elegible para competir](https://vendedores.mercadolibre.com.ar/nota/que-significa-que-tu-publicacion-sea-elegible-para-catalogo)
- [OFICIAL-AR] El ganador aparece como vendedor destacado en la página de producto, que se muestra arriba en los resultados de búsqueda — [Para qué sirven las publicaciones con competencia](https://vendedores.mercadolibre.com.ar/nota/con-catalogo-el-primer-lugar-del-listado-puede-ser-tuyo)
- [OFICIAL-AR] Qué es un producto de catálogo y uso de la información del catálogo — [Qué significa que un producto sea de catálogo](https://vendedores.mercadolibre.com.ar/nota/que-significa-que-un-producto-sea-de-catalogo); [Ayuda AR 5104](https://www.mercadolibre.com.ar/ayuda/Cuales-son-las-categorias-y-productos-que-estan-en-catalogo_5104); [Qué es catálogo (Developers AR)](https://developers.mercadolibre.com.ar/que-es-catalogo)
- [OFICIAL-AR, API] Existen "publicaciones requeridas en catálogo": productos donde ML exige que la publicación esté asociada a catálogo — [Publicaciones requeridas (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/sobre-nuestra-api/publicaciones-requeridas-en-catalogo); [Publicar en catálogo](https://developers.mercadolibre.com.ar/publicacion-en-catalogo)

### Inferences
- En autopartes nuevas con número de pieza en catálogo, la palanca para ganar no es el título ni las fotos (los pone ML), sino precio, cuotas, envío (Full/en el día) y reputación.

### Gaps
- No encontré qué categorías de autopartes MLA son de catálogo obligatorio ni si los usados pueden competir (la regla general menciona "ser nuevo").

---

## 7. Moderaciones e infracciones: motivos comunes de pausa en Argentina

### Takeaway
Según la gravedad, una publicación queda **pausada** (se reactiva corrigiéndola), **anulada** (no se reactiva) o se inhabilita la cuenta. Motivos frecuentes: fotos de mala calidad o fuera de requisitos, datos de contacto, falta de compatibilidades o posiciones en autopartes (7 días), cambios inusuales de precio, falta de ventas por mucho tiempo, artículos prohibidos (usados sin certificación, falsificados) y denuncias de propiedad intelectual (BPP, 4 días corridos para responder).

### Cited Findings
- [OFICIAL-AR] La gravedad de la falta define si la publicación queda pausada, anulada o si la cuenta se inhabilita. Una anulada no puede reactivarse, una pausada sí — [Cómo gestionar tus publicaciones de forma efectiva](https://vendedores.mercadolibre.com.ar/nota/como-gestionar-tus-publicaciones-de-forma-efectiva)
- [OFICIAL-AR, API] La moderación "Inactiva para revisar" = pausada, se reactiva con cambios. Cada moderación trae REASON (motivo) y REMEDY (acción sugerida) — [Gestionar moderaciones (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/gestionar-moderaciones)
- [OFICIAL-AR, API] Motivos de pausa: cambio inusual de precio (se verifica y se reactiva), fotos que no cargan o no cumplen requisitos, falta de ventas durante mucho tiempo — [Moderaciones con pausado (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/moderaciones-con-pausado)
- [OFICIAL-AR] Datos personales o de contacto en título, descripción, fotos o preguntas — [Cómo gestionar tus publicaciones](https://vendedores.mercadolibre.com.ar/nota/como-gestionar-tus-publicaciones-de-forma-efectiva); [Políticas de Publicación](https://www.mercadolibre.com.ar/seguro_publicacion.html)
- [OFICIAL-AR] Autopartes sin compatibilidades o sin posiciones: pausa a los 7 días cuando se publicó de forma masiva — [Agregá posiciones y evitá que pausemos tus publicaciones](https://vendedores.mercadolibre.com.ar/aprender/nota/como-agregar-posiciones-en-la-autoparte-y-evitar-que-se-paus); [Compatibilidades (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/compatibilidades-entre-items-y-productos)
- [OFICIAL-AR] Brand Protection Program: ante una denuncia, la publicación se pausa y el vendedor tiene **una única oportunidad** de responder, en **4 días corridos**. Si no responde, la publicación se da de baja — [Brand Protection Program: qué es y cómo usarlo](https://vendedores.mercadolibre.com.ar/nota/brand-protection-program-que-es-y-como-usarlo/); [Ayuda AR 994](https://www.mercadolibre.com.ar/ayuda/programa-de-proteccion-de-prop_994); [Ayuda AR 1083](https://www.mercadolibre.com.ar/ayuda/1083)
- [OFICIAL-AR, API] Para responder denuncias: si es por falsificación suelen pedirse facturas de compra y fotos de etiquetas y empaques. Si es por uso de marca, la autorización del titular — [Publicaciones denunciadas (Developers AR)](https://developers.mercadolibre.com.ar/es_ar/publicaciones-denunciadas)
- [OFICIAL-AR] Usar "tipo", "símil", "igual a" con marcas ajenas es motivo de denuncia por propiedad intelectual. Usar "para" o "compatible con" — [Cómo evitar denuncias por infringir propiedad intelectual](https://vendedores.mercadolibre.com.ar/nota/como-publicar-sin-infringir-propiedad-intelectual)
- [OFICIAL-AR] Artículos prohibidos: autopartes usadas sin certificación legal, contrabando, falsificados o adulterados — [Artículos Prohibidos](https://www.mercadolibre.com.ar/seguro_prohibidos.html)
- [OFICIAL-AR] Fotos de baja calidad: pérdida de exposición con tag `poor_quality_thumbnail`, pudiendo quedar activa o pausada — [Moderaciones de imágenes](https://developers.mercadolibre.com.ar/es_ar/moderaciones-de-imagenes)

### Inferences
- Checklist anti-pausa para autopartes: sin contacto ni logo en fotos o texto, "para [vehículo]" en vez de "tipo [marca]", compatibilidades y posiciones cargadas antes de los 7 días, usados solo con certificación, revisar el precio antes de cambios grandes y responder cualquier denuncia BPP dentro de los 4 días.

### Gaps
- No obtuve una lista oficial ML AR con todos los motivos de moderación, ni la política de sanciones progresivas para la cuenta.
- Ninguna página oficial pudo leerse completa ni con su fecha de actualización por el bloqueo de red. Antes de usar estas notas como material de capacitación definitivo, conviene que alguien con acceso abra cada URL citada y revise los montos en el simulador de costos del panel.
