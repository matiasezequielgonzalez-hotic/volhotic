# Mercado Libre Argentina: facturación esencial y políticas para productos de adultos / sex shop (vigencia a octubre 2026)

> **Nota de método (leer primero):** desde este entorno, los dominios mercadolibre.com.ar, vendedores.mercadolibre.com.ar y developers.mercadolibre.com.ar **no se pudieron abrir directo** (WebFetch dio error de DNS y curl un 403 del proxy). Por eso todo lo que sigue sale de **extractos que devolvió el buscador de esas mismas URLs oficiales**, sin lectura completa de cada página. Antes de publicar el material del curso conviene abrir cada link y confirmar el texto y la fecha. Etiquetas que uso: **[OFICIAL-ML]** = página de Mercado Libre Argentina; **[OFICIAL-ARCA]** / **[OFICIAL-GOB]** = Estado argentino; **[NO OFICIAL]** = terceros, solo para contrastar; **[NO VERIFICADO]** = no lo confirmé en una fuente oficial.

---

## A1. Obligación de facturar y tipos de comprobante de ARCA (A, B, C)

### Takeaway
Según el régimen de ARCA, la clase del comprobante depende de **quién vende y a quién le vende**. El Responsable Inscripto (RI) emite **A** a otro RI o a un monotributista, y **B** a consumidor final, exento o no categorizado. El monotributista emite **C** a cualquier receptor, salvo en exportación, que va con **E**. La obligación de emitir la factura es del vendedor, no de Mercado Libre.

### Cited Findings
- **[OFICIAL-ARCA]** La clase de comprobante "dependerá del sujeto con el que se opere". La tabla del régimen general indica: RI → RI o monotributista = clase **A**; RI → consumidor final o exento = clase **B**; monotributista o exento → cualquier receptor = clase **C**; exportación = clase **E**. — [ARCA, Régimen general – Comprobantes](https://www.afip.gob.ar/facturacion/regimen-general/comprobantes.asp)
- **[OFICIAL-ARCA]** La clase **B** la emiten los RI "por operaciones realizadas con consumidores finales, sujetos exentos en dicho impuesto, sujetos no alcanzados, sujetos no categorizados y con turistas del extranjero". — [ARCA, Régimen general – Comprobantes](https://www.afip.gob.ar/facturacion/regimen-general/comprobantes.asp)
- **[OFICIAL-ARCA]** La clase **A** puede tener variantes según la autorización del emisor, por ejemplo la leyenda "pago en CBU informada" o "operación sujeta a retención". — [ARCA, Régimen general – Comprobantes](https://www.afip.gob.ar/facturacion/regimen-general/comprobantes.asp)
- **[OFICIAL-ARCA]** "Los monotributistas de todas las categorías deben emitir comprobantes electrónicos tipo 'C' para las operaciones con consumidores finales, excepto que se trate de una operación de exportación, en cuyo caso corresponde emitir comprobantes tipo 'E'". — [ARCA, Monotributo – Ayuda: Facturación](https://www.afip.gob.ar/monotributo/ayuda/facturacion.asp)
- **[OFICIAL-ARCA]** El "Facturador" de ARCA (la app propia de ARCA, que no es el de Mercado Libre) permite a los monotributistas emitir tiques y notas de crédito C a consumidores finales desde el celular o la computadora. — [ARCA, Facturador – ¿Qué es?](https://www.arca.gob.ar/facturador/caracteristicas-y-funciones/que-es.asp) y [ARCA, Facturador](https://www.afip.gob.ar/facturador/)
- **[OFICIAL-GOB / Boletín Oficial]** La **RG ARCA 5700/2025** (BO 27/05/2025, vigente desde el 29/05/2025) llevó a **$10.000.000** el monto a partir del cual hay que identificar al consumidor final en el comprobante con CUIT, CUIL, CDI o DNI. Antes los topes eran $250.000 en efectivo y $400.000 con otros medios. — [Boletín Oficial, aviso 326743](https://www.boletinoficial.gob.ar/detalleAviso/primera/326743/1); también [CPCE Córdoba](https://web.cpcecba.org.ar/?p=56255) **[NO OFICIAL, colegio profesional]**
- **[NO OFICIAL]** Según resúmenes profesionales, la misma RG 5700/2025 subió el tope de uso del "Facturador" de ARCA a $500.000 por operación para monotributistas y a $250.000 para monotributistas sociales. No lo verifiqué en el texto del BO. — [Blog del Contador](https://blogdelcontador.com.ar/news-45898-arca-eleva-a-10-millones-el-limite-para-identificar-al-consumidor-final-en-comprobantes)
- **[OFICIAL-ML]** Mercado Libre trata como **"sujetos no categorizados"**, desde el **1/7/2025**, a quienes venden sin una condición válida en ARCA. Si el vendedor regulariza su situación, ML la actualiza en forma automática, aunque puede tardar hasta 4 días hábiles. — [ML Vendedores, Si sos sujeto no categorizado y vendés en Mercado Libre](https://vendedores.mercadolibre.com.ar/nota/si-sos-sujeto-no-categorizado-y-vendes-en-mercado-libre)
- **[NO OFICIAL]** "Mercado Libre actúa como agente de retención y percepción de impuestos, pero la obligación de emitir el comprobante recae en el vendedor con CUIT". — [Base.com blog](https://base.com/es-AR/blog/?p=18427)

### Inferences
- Para el curso: un vendedor **monotributista** de sex shop emite siempre **Factura C**, compre quien compre, incluso si el comprador es RI y pide "factura A". Un **RI** emite **A** si el comprador informa un CUIT de RI o de monotributista, y **B** en el resto de los casos. Esto sale de la tabla de ARCA y no es asesoramiento fiscal.
- Como el umbral es de $10.000.000, en la mayoría de las ventas minoristas la factura B o C a consumidor final no necesita identificar al comprador. Igual, el dato fiscal suele venir en la venta (ver A2).

### Gaps
- No consulté la norma de fondo que obliga a emitir comprobante en cada venta (RG AFIP 1415 y la RG 4291 de factura electrónica), así que no puedo citar el texto exacto de la obligación general. ARCA la presupone en las páginas citadas.
- No confirmé si hubo cambios posteriores a la RG 5700/2025 en el umbral o en los tipos de comprobante hasta octubre de 2026.
- No encontré en ARCA un texto específico sobre comercio electrónico o marketplaces que cambie estas reglas.

---

## A2. Cómo le llega la factura al comprador en Mercado Libre Argentina (cargar PDF, Facturador de ML, plazos, factura A)

### Takeaway
Hay dos caminos oficiales. El primero es el **Facturador de Mercado Libre**, gratuito y conectado con ARCA por webservice, en modo automático o manual. El segundo es **emitir por fuera** (ARCA o un sistema de terceros) y **adjuntar el PDF o XML a la venta**. Los datos fiscales del comprador (CUIT o DNI, condición frente al IVA) aparecen en la venta. **No encontré un plazo oficial para adjuntar la factura.**

### Cited Findings
- **[OFICIAL-ML]** El Facturador de Mercado Libre "es una herramienta gratuita que te permite emitir las facturas de las ventas en Mercado Libre". Lo pueden usar vendedores monotributistas, responsables inscriptos o exentos de IVA. — [ML Vendedores, Qué es el Facturador de Mercado Libre](https://vendedores.mercadolibre.com.ar/aprender/nota/que-es-el-facturador-de-mercado-libre)
- **[OFICIAL-ML]** Modos de emisión: en el **automático**, cada vez que se concreta una venta, ML emite la factura por el vendedor y se la envía al comprador. En el **manual**, se puede facturar venta por venta desde el detalle o en forma masiva desde el listado de ventas. **Solo se pueden facturar las ventas hechas a partir del día en que se configuró la herramienta.** — [ML Vendedores, Cómo emitir las facturas en Mercado Libre](https://vendedores.mercadolibre.com.ar/nota/como-emitir-las-facturas-en-mercado-libre); [Qué es el Facturador](https://vendedores.mercadolibre.com.ar/aprender/nota/que-es-el-facturador-de-mercado-libre)
- **[OFICIAL-ML]** ML le manda la factura por e-mail al comprador, que también puede descargarla desde el detalle de la compra. Este dato sale de un extracto del buscador y conviene confirmarlo en la página. — [ML Vendedores, Cómo emitir las facturas en Mercado Libre](https://vendedores.mercadolibre.com.ar/nota/como-emitir-las-facturas-en-mercado-libre)
- **[OFICIAL-ML]** Requisitos del Facturador:
  - CUIT registrado en ARCA. ML puede tardar hasta 72 h en validarlo.
  - Fecha de inicio de actividades y categoría de monotributo (figura en la Constancia de Opción).
  - Clave fiscal **nivel 3** para crear un **punto de venta exclusivo**. El servicio es "Factura electrónica – Monotributo – Webservices" para monotributistas y "Factura electrónica – RECE – Webservices" para RI.
  - **Certificado digital**: se descarga el CSR desde el Facturador, se sube en ARCA en "Administración de Certificados Digitales" y se carga en ML el .crt que devuelve ARCA.
  
  Fuentes: [Cómo crear un punto de venta en ARCA](https://vendedores.mercadolibre.com.ar/nota/paso-a-paso-como-cargar-tu-informacion-de-la-afip); [Cómo crear un certificado digital en ARCA](https://vendedores.mercadolibre.com.ar/nota/como-crear-un-certificado-digital-en-arca); [Conocé cómo configurar el Facturador](https://vendedores.mercadolibre.com.ar/nota/conoce-como-configurar-del-facturador-de-mercado-libre)
- **[OFICIAL-ML Developers]** Para la facturación automática en Argentina, el vendedor tiene que cargar antes los **datos fiscales de cada producto** (NCM, alícuota de IVA, origen, etc.). La documentación aclara que esta función está disponible **solo en Argentina**. — [Developers ML, Envío de datos fiscales (MLA)](https://developers.mercadolibre.com.ar/es_ar/envio-de-datos-fiscales-mla)
- **[OFICIAL-ML Developers]** **Cargar una factura propia:** los vendedores pueden "compartir las facturas de sus compradores dentro de la venta" en lugar de mandarlas por mensajería posventa. Se hace con un POST form-data con el archivo `fiscal_document` al pack (`pack_id`, que se obtiene de /orders) y acepta **PDF y XML**. Según el buscador, la página se actualizó el **16/03/2026**. — [Developers ML, Cargar factura](https://developers.mercadolibre.com.ar/cargar-factura)
- **[OFICIAL-ML Developers]** **Datos fiscales del comprador:** se obtienen del recurso *billing info* de la orden. La documentación distingue persona física (DNI o CUIL) de persona jurídica (CUIT). Incluye la situación fiscal y, a veces, el número de IIBB, que solo aparece si el comprador tiene CUIT y lo informó en el checkout. — [Developers ML, Datos de facturación](https://developers.mercadolibre.com.ar/es_ar/facturacion)
- **[OFICIAL-ML Developers]** En las facturas emitidas por ML que se descargan por API, el campo `document_type` vale `factura_a` o `factura_b` "según el perfil fiscal del comprador". — [Developers ML, Descargar facturas (MLA)](https://developers.mercadolibre.com.ar/descargar-facturas-mla)
- **[NO OFICIAL]** Si a la venta le faltan datos fiscales obligatorios, el vendedor puede pedirlos por el chat de la venta. Una vez adjuntada la factura, su número se ve en el detalle de la venta. — [Jaguar Sheet](https://jaguarsheet.com/es/blog/datos-facturacion-mercado-libre)
- **[NO OFICIAL]** Hay facturadores de terceros que se integran con ML y emiten con CAE de ARCA, por ejemplo Tributo Simple, YoFacturo y Facturel. Son páginas comerciales y no las verifiqué. — [Tributo Simple](https://tributosimple.com/argentina/facturacion/); [YoFacturo](https://yo-facturo.com/facturacion-mercado-libre/)

### Inferences
- Cuando un comprador "pide factura A", la venta trae su CUIT y su condición (billing info). Si el vendedor es RI, emite A con esos datos. Si es monotributista, emite C igual (ver A1). Con el Facturador de ML, el tipo A o B lo decide el perfil fiscal del comprador, según la doc de Developers.
- Las ventas anteriores a la configuración del Facturador hay que facturarlas por fuera y adjuntarlas.

### Gaps
- **No encontré un plazo oficial de ML para adjuntar la factura**, ni sanciones o efectos en la reputación por no adjuntarla. Lo indiqué así a propósito y no hay que inventarlo.
- No pude leer completa la página de ayuda del comprador sobre cómo pedir factura A ni la de cómo cargar datos fiscales en el checkout.
- No confirmé el texto exacto del flujo en el panel (sin API) para subir el PDF a la venta. La doc oficial que encontré es la de API.

---

## A3. Facturas de Mercado Libre al vendedor (comisiones) y retenciones/percepciones en Mercado Pago

### Takeaway
ML le factura al vendedor **una vez por mes** sus cargos (comisiones, envíos, etc.). Algunos se descuentan automáticamente de lo cobrado y otros quedan como saldo a pagar. ML y Mercado Pago actúan como **agentes de recaudación**: retención de IIBB en cada cobro, percepción de IIBB en la factura mensual y percepción de IVA según la condición del vendedor. Desde el **1/9/2024** (RG 5554/2024) ya **no se aplican retenciones de IVA y Ganancias** en los cobros.

### Cited Findings
- **[OFICIAL-ML]** Algunos cargos se debitan automáticamente y otros generan un saldo al cierre del mes que se paga a mano. La factura detalla número, emisión, vencimiento, cargos, subtotal, impuestos y total. Puede estar en pesos o en dólares y se descarga desde "Facturación". Tarda hasta ~10 días después del cierre en estar disponible. Las facturas son **tipo "B"**, salvo que la cuenta esté registrada como empresa o monotributista con documentación (en ese caso, A). — [ML Vendedores, Aprendé todo acerca de tus facturas](https://vendedores.mercadolibre.com.ar/nota/aprende-todo-acerca-de-tus-facturas) **(el buscador la marca con más de 3 años de antigüedad, posiblemente desactualizada)**
- **[OFICIAL-ML]** Después del cierre mensual hay 5 días para pagar antes del vencimiento. Si quedan facturas impagas, ML puede debitarlas del dinero disponible. — [ML Ayuda, Cómo pago mi factura](https://www.mercadolibre.com.ar/ayuda/Como-es-el-proceso-de-facturacion_873); [Tarifas y facturación](https://www.mercadolibre.com.ar/ayuda/Tarifas-y-facturacion_1044)
- **[OFICIAL-ML]** Si se cancela una venta, se reintegra la comisión: aparece como anulación en la misma factura o como nota de crédito si es de otro mes. El reporte de Facturación indica si cada cargo se descontó de Mercado Pago. — [ML Vendedores, Cómo se compone el reporte de Facturación](https://vendedores.mercadolibre.com.ar/nota/reporte-detalle-del-periodo-como-analizarlo)
- **[OFICIAL-ML]** Desde el **1/9/2024**, por la **RG 5554/2024**, ARCA eliminó las retenciones de IVA y Ganancias. — [ML Vendedores, Si sos responsable inscripto y cobrás con Mercado Pago](https://vendedores.mercadolibre.com.ar/nota/responsables-inscriptos-en-mercado-pago). Una nota más vieja del blog de ML todavía las menciona: [Retenciones y percepciones: qué debés saber](https://vendedores.mercadolibre.com.ar/blog/notas/retenciones-y-percepciones-sobre-tus-ventas-lo-que-debes-saber/) **(desactualizada)**
- **[OFICIAL-ML]** A los **RI**, ML les suma siempre la percepción general de IVA en la factura mensual por el uso de Mercado Pago: **3%** general y **1,5%** para quienes figuran al 50% en el padrón de promoción y exentos. — [ML Vendedores, Percepción de IVA para responsables inscriptos](https://vendedores.mercadolibre.com.ar/nota/iva-y-ganancias-para-responsables-inscriptos-en-mercado-pago)
- **[OFICIAL-ML]** A los **monotributistas** no se les percibe IVA, salvo que superen el precio unitario máximo de su categoría (la nota informa **$716.840,77, actualizado a agosto de 2026**) o el tope de facturación de ARCA. Sí tienen retención y percepción de IIBB según la provincia. — [ML Vendedores, Percepción de IVA para monotributistas](https://vendedores.mercadolibre.com.ar/nota/percepcion-de-iva-para-monotributistas-en-mercado-libre); [Si sos monotributista y vendés en ML](https://vendedores.mercadolibre.com.ar/nota/monotributistas-en-mercado-libre); [Retención de IIBB para monotributistas en Mercado Pago](https://vendedores.mercadolibre.com.ar/nota/retencion-de-iibb-para-monotributistas-en-mercado-pago)
- **[OFICIAL-ML]** A los **consumidores finales** (vendedores sin inscripción) que superen ciertos umbrales mensuales o cuatrimestrales se les aplica percepción de IVA del **8%**. Puede devolverse a quien vendió solo usados o reacondicionados de uso personal, con un tope de $1.500.000 por cuatrimestre. — [ML Vendedores, Percepción de IVA para consumidores finales](https://vendedores.mercadolibre.com.ar/aprender/nota/percepcion-iva-consumidores-finales-mercado-libre)
- **[OFICIAL-ML]** **Retención de IIBB** en cada cobro con Mercado Pago, con alícuotas por provincia según padrón. En jurisdicciones de **SIRTAC**, a quien no está inscripto se le retiene **3%** por cobro si supera los 10 cobros mensuales y $750.000. La **percepción de IIBB** se cobra al cierre de la factura mensual. Ambas son pagos a cuenta en las DDJJ. — [ML Vendedores, Retención de IIBB para consumidores finales en Mercado Pago](https://vendedores.mercadolibre.com.ar/aprender/nota/retencion-de-iibb-para-consumidores-finales-en-mercado-pago); [Percepción de IIBB para consumidores finales](https://vendedores.mercadolibre.com.ar/nota/percepcion-iibb-consumidores-finales-mercado-libre)

### Inferences
- Para un sex shop monotributista: la factura mensual de ML suele ser A (si la cuenta tiene la condición registrada) con los cargos, más la percepción de IIBB según provincia, y en Mercado Pago hay retención de IIBB. No hay percepción de IVA mientras no supere los topes.

### Gaps
- Los montos y umbrales (los $750.000, el precio unitario máximo, el umbral para consumidores finales) cambian seguido. Hay que verificarlos en la sección "Información fiscal" de la cuenta a la fecha del curso.
- No encontré una versión de "Aprendé todo acerca de tus facturas" con fecha 2026. Puede haber cambios en el formato o en el tipo de factura.

---

## B1. Política de Mercado Libre Argentina sobre productos para adultos (juguetes sexuales, lencería, lubricantes)

### Takeaway
Vender productos para adultos **está permitido**, pero **solo dentro de la categoría "Adultos"**. Esa categoría pide ser **mayor de 18 años** con capacidad legal para entrar, publicar y comprar, y muestra un aviso previo de aceptación. Afuera de esa categoría, el contenido sexual o con desnudez está prohibido y se remueve. Los productos de Adultos tampoco pueden aparecer en la página principal. No encontré una lista oficial específica de ítems prohibidos dentro de Adultos (más allá de la política general de prohibidos) ni reglas detalladas de títulos.

### Cited Findings
- **[OFICIAL-ML]** Los términos de la categoría Adultos dicen: "solo podrán ingresar, publicar y realizar compras dentro de esta categoría las personas mayores de 18 años con capacidad legal para contratar". El usuario acepta que puede encontrar material erótico o desnudos en fotos y descripciones. Los términos remiten a la ayuda "Contenidos no aptos para menores". — [ML, Estás ingresando en la categoría Adultos (adultstermsandconditions)](https://listado.mercadolibre.com.ar/adultstermsandconditions)
- **[OFICIAL-ML]** La política de Artículos Prohibidos alcanza a los artículos "de tipo pornográfico, erótico o no apto para menores". Define como no aptos los que muestran genitales con sugerencia de actividad sexual, personas en relaciones sexuales o material cuyo fin es generar excitación sexual. Las imágenes con connotación sexual o desnudez **no pueden publicarse en otras categorías**, salvo en publicaciones sin fines sexuales o dentro de Adultos. Los artículos de Adultos publicados en otra categoría se remueven. — [ML, Artículos Prohibidos](https://www.mercadolibre.com.ar/seguro_prohibidos.html) **(el buscador marca la página como muy antigua, de más de 10 años; la versión vigente puede ser otra)**
- **[OFICIAL-ML]** Ni los productos de la categoría Adultos ni las fotos provocativas se permiten en la página principal. Si una publicación infringe la política, puede quedar pausada o anulada, y en casos graves se inhabilita la cuenta. — [ML, Artículos Prohibidos](https://www.mercadolibre.com.ar/seguro_prohibidos.html); [ML, Políticas de Publicación](https://www.mercadolibre.com.ar/seguro_publicacion.html)
- **[OFICIAL-ML]** En las **opiniones** de productos no se permiten fotos con desnudez total o parcial ni con menores en ropa interior. — [ML Ayuda, Políticas sobre opiniones de productos](https://www.mercadolibre.com.ar/ayuda/26454)
- **[OFICIAL-ML]** ML tiene guías de moderación para evitar que se pausen publicaciones (infracciones de políticas). — [ML Vendedores, Cómo evitar moderaciones](https://vendedores.mercadolibre.com.ar/nota/como-evitar-moderaciones-para-cuidar-tu-negocio)
- **[OFICIAL-ML / otro país]** En un reporte de transparencia de **México**, ML informó que "productos para adultos mal categorizados" estaban entre las tres categorías con más infracciones. El dato **es de México (2022), no de Argentina**. — [Reporte de transparencia MLM, may-22 (PDF)](https://cdn.uc.assets.prezly.com/4f4c9f39-5886-431e-a79b-63b99137669b/-/inline/no/MLM%20Comunicado%203er%20Reporte%20de%20transparencia%20_%20may%2022.pdf)
- **[NO OFICIAL]** Según una guía de Nubimetrics, en Adultos se permiten juguetes sexuales, figuras eróticas y ropa o disfraces que exponen partes íntimas. Recomienda evitar imágenes explícitas o con desnudez y cuidar títulos, descripciones y categoría. — [Nubimetrics, productos eróticos](https://academia.nubimetrics.com/productos-eroticos); [Nubimetrics, Sin tabúes](https://academia.nubimetrics.com/sin-tabues-productos-eroticos-para-vender-online)
- **[OFICIAL-ML, observación del listado]** En la práctica, las búsquedas de "lencería erótica" o "juguetes íntimos para parejas" muestran productos que parecen estar en categorías generales (juegos de pareja, lencería, preservativos). Es una observación de resultados de búsqueda y no confirma la regla. — [Listado ML, kit lencería erótica](https://listado.mercadolibre.com.ar/kit-lenceria-erotica); [Listado ML, juguetes íntimos para parejas](https://listado.mercadolibre.com.ar/juguetes-intimos-para-parejas)

### Inferences
- Para el curso: publicar juguetes sexuales siempre en "Adultos" y usar fotos de producto sin desnudez ni actos sexuales. Esto es prudente aunque la categoría admita material erótico, porque así se reduce el riesgo de moderación y de quedar mal categorizado. La lencería y los lubricantes pueden estar en categorías generales (Ropa, Salud) si no tienen fines o imágenes sexuales. Esto **[NO VERIFICADO]** como regla explícita: es una inferencia de la excepción "publicaciones no creadas con fines sexuales".
- Los lubricantes y geles pueden tener requisitos sanitarios (ANMAT, productos médicos o cosméticos). **[NO VERIFICADO]**: no lo investigué ni encontré una regla de ML al respecto.

### Gaps
- No pude leer la página de ayuda "Contenidos no aptos para menores" ni una versión fechada 2025-2026 de Artículos Prohibidos. La versión que encontré puede ser vieja.
- No encontré reglas oficiales específicas de **títulos o descripciones** para Adultos (palabras prohibidas, por ejemplo) ni reglas de **fotos** específicas para juguetes. Solo están las reglas generales citadas arriba.
- No encontré una lista oficial de ítems prohibidos dentro del rubro (por ejemplo, muñecas con rasgos infantiles o sustancias "afrodisíacas"). Es razonable suponer que están prohibidos por normas generales, pero queda **[NO VERIFICADO]**.

---

## B2. Envío o embalaje discreto y privacidad del comprador

### Takeaway
**No encontré ninguna guía oficial de Mercado Libre Argentina sobre envío o embalaje discreto** para productos de adultos. Las reglas de embalaje oficiales que aparecieron son genéricas (protección, cierre, Full). Sobre privacidad, la Declaración de Privacidad de ML dice que el vendedor que recibe datos del comprador **pasa a ser responsable de su tratamiento** y **no puede cederlos a terceros sin consentimiento**.

### Cited Findings
- **[OFICIAL-ML]** Para enviar a Full, cada producto debe ir en un empaque individual (bolsa plástica transparente o caja, según el caso). No se menciona la discreción. — [ML Ayuda, Cómo debe ser el empaque para Full](https://www.mercadolibre.com.ar/ayuda/como-preparar-tus-productos-para-enviarlos-a-full_5216)
- **[OFICIAL-ML / México]** Las instrucciones de embalaje por tipo de producto piden un paquete cerrado sin partes del producto expuestas. **Esta página es de México**. — [ML Vendedores MX, Instrucciones para embalar cada tipo de producto](https://vendedores.mercadolibre.com.mx/nota/instrucciones-para-embalar-cada-tipo-de-producto)
- **[OFICIAL-ML]** "Bajo ninguna circunstancia, los vendedores podrán comunicar tus datos personales a terceros sin tu consentimiento". Quien recibe datos de otros usuarios "se constituye en responsable por el tratamiento de estos datos" con las obligaciones de la ley de protección de datos. Los usos permitidos son la transacción, los servicios de ML (envíos, reclamos) u otro fin que el usuario consienta expresamente. — [ML, Declaración de Privacidad – ¿Cómo pueden usar otros usuarios tus datos?](https://www.mercadolibre.com.ar/privacidad/declaracion-privacidad/31256); [Resumen Declaración de Privacidad](https://www.mercadolibre.com.ar/privacidad/resumen)
- **[OFICIAL-ML]** ML no acepta "el envío indiscriminado de mensajes" (spam) entre usuarios. — [ML, Políticas de Publicación](https://www.mercadolibre.com.ar/seguro_publicacion.html)
- **[NO OFICIAL]** Un blog afirma que en Latinoamérica marcas "como Mercado Libre" implementaron opciones de embalaje discreto. Es una afirmación **sin respaldo oficial**. — [Tienda Neolo, ¿Qué es el envío y embalaje discretos?](https://tiendaneolo.com/tutoriales/que-es-el-envio-y-embalaje-discretos/)

### Inferences
- Para el curso: el embalaje neutro (caja lisa, sin marca ni descripción del contenido) es **buena práctica del vendedor y no una regla de ML**. En Mercado Envíos, la etiqueta la genera ML. No encontré si muestra el título del producto, así que queda **[NO VERIFICADO]**.
- La Ley 25.326 (Protección de Datos Personales) es el marco legal de fondo. La Declaración de Privacidad de ML la menciona junto con la Agencia de Acceso a la Información Pública como órgano de control.

### Gaps
- No hay una guía oficial de ML Argentina sobre envío discreto. **Lo dejo dicho explícitamente.**
- No verifiqué qué información del producto aparece en la etiqueta de Mercado Envíos ni en el resumen de la tarjeta o de Mercado Pago (el descriptor de pago).
- Las notas de privacidad de Mercado Shops que aparecieron pueden no estar vigentes. **[NO VERIFICADO]**: no confirmé si Mercado Shops sigue operando en 2026.

---

## B3. Higiene y devoluciones de productos íntimos (ML + normas de consumo argentinas)

### Takeaway
La ayuda oficial de ML Argentina "Productos que no tienen devolución" incluye, según el extracto del buscador, **la categoría Adultos** entre los productos sin devolución. Para ropa interior, lencería y trajes de baño, ML acepta devoluciones solo si no se usaron (y, según otra página, con la etiqueta original). En cambio, la **Ley 24.240 (art. 34)** da **10 días corridos** para revocar compras a distancia, una facultad que "no puede ser dispensada ni renunciada". La ley tiene excepciones generales, pero **no encontré ninguna norma oficial que excluya expresamente los productos íntimos o sexuales**. Esta tensión hay que avisarla.

### Cited Findings
- **[OFICIAL-ML]** "Productos que no tienen devolución": el extracto del buscador indica que la lista incluye la categoría **Adultos**. — [ML Ayuda, Productos que no tienen devolución](https://www.mercadolibre.com.ar/ayuda/productos-sin-devolucion_4292) **(no pude leer el texto completo; confirmar)**
- **[OFICIAL-ML]** Según las condiciones de Compra Protegida, la ropa interior, los trajes de baño y la lencería deben estar sin uso. Higiene personal y protectores solares van con el envase cerrado o sin abrir. Farmacia no tiene devolución. — [ML Ayuda, Condiciones para la cobertura de Compra Protegida](https://www.mercadolibre.com.ar/ayuda/48243)
- **[OFICIAL-ML]** En "Ropa y accesorios" se aceptan devoluciones de prendas sin uso y con la etiqueta original. En higiene o cuidado personal, con el envase original cerrado y sin uso. Por arrepentimiento se pueden pedir hasta **30 días** desde la entrega. Hay una diferencia de matiz con la página de Compra Protegida (el requisito de la etiqueta). — [ML Ayuda, Políticas de devolución de productos](https://www.mercadolibre.com.ar/ayuda/16914); [ML Ayuda, Política de inspección de devoluciones](https://www.mercadolibre.com.ar/ayuda/18326)
- **[OFICIAL-GOB]** Ley 24.240, art. 34 (texto actualizado por la Ley 26.361): en las ventas a distancia, el consumidor "tiene derecho a revocar la aceptación durante el plazo de DIEZ (10) días corridos, contados a partir de la fecha en que se entregue el bien o se celebre el contrato, lo último que ocurra". Esa facultad no puede dispensarse ni renunciarse. — [Ley 24.240 texto actualizado (InfoLEG/argentina.gob.ar)](https://www.argentina.gob.ar/normativa/nacional/norma-638/actualizacion)
- **[OFICIAL-GOB]** Los gastos de devolución corren por cuenta del vendedor, y un aviso de "no se aceptan devoluciones" no tiene valor. Según esta fuente, no hay derecho de arrepentimiento para productos personalizados, que se deterioran rápido o que "por su naturaleza no pueden ser devueltos", grabaciones, software, diarios y revistas. — [Derecho Fácil, Ley simple: Botón de arrepentimiento](https://www.argentina.gob.ar/justicia/derechofacil/leysimple/boton-arrepentimiento) (sitio oficial de divulgación, no normativo)
- **[OFICIAL-GOB]** El "botón de arrepentimiento" lo creó la Res. 424/2020, que luego fue **derogada y reemplazada por la Disposición 954/2025** del Ministerio de Economía. Esa disposición prohíbe pedir registración previa u otros trámites para usarlo. No leí el texto completo de la Disposición 954/2025. — [Disposición 954/2025](https://www.argentina.gob.ar/normativa/nacional/norma-417152/texto); [Res. 424/2020](https://www.argentina.gob.ar/normativa/nacional/norma-342869/texto)
- **[NO OFICIAL]** Publicaciones de sex shop en ML dicen "no hay cambios ni devoluciones por cuestiones de higiene y uso personal, solo por fallas". Es texto de vendedores, no una regla. — [Publicación MLA-826402436](https://articulo.mercadolibre.com.ar/MLA-826402436-combo-juguetes-sexuales-vibrador-consolador-adultos-sex-shop-_JM)
- **[NO OFICIAL]** Una guía de Klicko (octubre 2026) coincide en que la categoría Adultos no tiene devolución en ML y recuerda los 10 días de la ley. — [Klicko, Devoluciones en Mercado Libre](https://klicko.com.ar/blog/devoluciones-mercado-libre-quien-paga-envio)

### Inferences
- Hay **tensión** entre la política de ML ("Adultos sin devolución") y el art. 34 de la Ley 24.240, que es irrenunciable. Un juguete sexual abierto o usado podría entrar en la excepción "por su naturaleza no pueden ser devueltos", pero eso **lo interpreta la autoridad de consumo y no está escrito para este rubro**. **[NO VERIFICADO]**: no encontré ninguna resolución ni dictamen al respecto.
- Para el curso, la recomendación prudente (sin ser asesoramiento legal) es aceptar devoluciones de productos cerrados o precintados y de fallas, y avisar que la exclusión de ML no anula los derechos legales del consumidor.

### Gaps
- No encontré una norma argentina oficial que excluya expresamente los productos íntimos o sexuales del derecho de arrepentimiento.
- No leí el texto completo de la Disposición 954/2025, que podría incluir una excepción por "producto utilizado" (el extracto era fragmentario).
- La ayuda de ML de "Productos que no tienen devolución" solo la vi como extracto del buscador: confirmar que siga listando Adultos en octubre de 2026.
