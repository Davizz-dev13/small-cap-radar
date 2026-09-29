# Sharpe Lab: detector precatalizador v2 (prototipo de investigación)

La idea corregida por David: detectar compañías de calidad **antes** de un evento aún incierto, en cualquier sector y bolsa. No se buscan solo medicamentos ni acciones de céntimos. La cifra nominal de 0,10–20 €/USD es **dato visible, nunca filtro**: precio bajo no hace barata una empresa. El programa no compra; el workflow semanal publica solo datos de investigación en GitHub Pages y avisa por Telegram únicamente en cruces nuevos de 6/7.

## Ejecución

```
python3 -m pip install -r requirements.txt
python3 scanner.py
```

Lee `universe.json` con fuentes y notas revisadas manualmente, consulta precios/historial a Yahoo vía yfinance, imprime tabla ordenada y guarda `docs/scan.json`. A diferencia de v1 no usa SEC automáticamente: la SEC cubre emisores estadounidenses, no estados IFRS paneuropeos. Los datos financieros y fechas de eventos de esta versión se transcriben a mano de fuentes primarias; añadir un emisor exige comprobar emisores, titularidad del proyecto, estado real del evento, ventana esperada, caja, gasto y financiación en informes actuales. `financial_as_of` no debe superar 120 días. **No es un barrido mundial**, pese a que el diseño acepta tickers de otras plazas. Faltan un proveedor global de emisiones y una fuente universal de eventos fechados con derechos económicos verificables. Sin estos, fingir exhaustividad daría falsos positivos.

## Siete banderas (sí/no)

1. Próximo catalizador identificable, ventana <=18 meses y URL primaria del emisor/regulador/cliente. Una meta prometida por un socio no es contrato propio. No confundir presentación de solicitud con aprobación: registrar qué se espera exactamente y su incertidumbre.
2. Capitalización equivalente USD entre 300M y 3B. Convierte GBP/EUR/SEK con FX Yahoo; LSE cotiza en peniques GBp, pero su `marketCap` Yahoo está en libras GBP, no centésimos. Otras monedas no cubiertas detienen el valor con ERROR hasta añadir cambio contrastado.
3. Caja / quema mensual histórica llega al final de la ventana del evento **más seis meses**; si la dirección ofrece una guía más corta, manda la más corta. Se excluyen tramos de deuda todavía condicionales. La caja de empresas con ingresos irregulares requiere inspección adicional.
4. Retorno de las últimas 60 sesiones completas <100% (evita euforia reciente; pérdida intensa tampoco demuestra oportunidad).
5. Cuentas no más antiguas de 120 días.
6. Anti-dilución revisada y sin financiación inminente. Sin revisión formal de emisiones, warrants, deuda, compromisos, tramos condicionales y nuevas cotizaciones, el indicador queda **falso**. Las cinco semillas no lo superan, por prudencia.
7. Negocio revisado contra los documentos citados: producto, cliente, validación técnica y derechos. Esta bandera no garantiza que sea una empresa de calidad. La calidad real también exige márgenes, concentración de clientes, gobierno e historial de emisiones; se documenta a mano en la nota.

Por ticker devuelve magnitudes, banderas falsas y notas. No calcula probabilidad de x5, ni usa objetivos de analistas como verdad, ni promete que la fecha del evento sea firme. El volumen 20/40 sesiones se informa sin imponerse como condición: entrada de volumen no prueba calidad. **La puntuación es completitud de condiciones, no recomendación de invertir ni ranking de retorno esperado.** El Excel/JSON del usuario debe revisarse antes de comprar; la caída hasta cero o un retraso del catalizador son posibles.

La ventana `profit_inflection` de SEYE.ST es solo una hipótesis analítica, no anuncio de fecha por la empresa: se mantiene como comparador descartado, no como candidato verificable. CWR.L sí anuncia producción piloto del socio Delta hacia fin de 2026, pero esa producción tampoco genera ingreso garantizado para Ceres. RGNX y ANNX tienen ventanas clínicas anunciadas, pero siguen sujetas a resultado binario. IVA presenta un caso claro de *runway*: la guía propia solo alcanza fin Q2 2027, ~5,9 meses después de Q4 2026; la ampliación opcional para Q1 2028 no se cuenta.

Las cotizaciones y tipos de cambio se consultaron el 29 sep 2026 y pueden variar; precios EUR, USD, SEK y GBp se dejan con su unidad. Un ADR (IVA) y una cotización local representan la misma compañía: no duplicar como oportunidades distintas. La divisa del ADR no es la divisa de sus cuentas. En `universe.json`, `cash_m_local` tiene la divisa funcional declarada en el informe financiero, que se explica por ticker.

## Operación semanal

El workflow de GitHub Actions ejecuta el scanner los lunes y publica `docs/scan.json` en Pages. Solo envía Telegram cuando un ticker pasa de menos de 6 a 6/7 o más; `alert_state.json` inicial evita notificaciones retrospectivas. El envío necesita los secretos `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` en este repositorio. Una credencial ausente deja el estado intacto y falla antes de marcar una alerta enviada. Si el mercado no da datos, ese ticker se marca error y no genera alerta; cualquier señal de inversión requiere lectura humana.
