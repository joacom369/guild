# Fuentes y datos: el detalle

## El interrogatorio a una cifra externa
- ¿Qué mide exactamente? ¿Es la categoría que yo necesito o sólo se llama parecido?
- ¿Qué incluye? Impuestos, flete, montaje, honorarios, amortizaciones, alcance.
- ¿Qué precio es? FOB, FAS, mayorista, minorista, de lista, negociado; nominal o real; en qué moneda.
- ¿Ex ante o ex post? ¿Esperado o realizado?
- ¿De cuándo es el período que representa? La fecha de acceso no lo dice.
- ¿De dónde y de qué escala? Región, tamaño, tecnología.
- ¿Cuál es su metodología y quién la publica? ¿Es oficial, de un gremio, de un vendedor?
- ¿Qué rango tiene? Si hay varias fuentes, mínimo y máximo, y por qué difieren.

Ejemplos de trampa: una vivienda no es un galpón; un salario de convenio no es
el costo laboral; un aviso no es un precio de mercado; un precio FOB no es un
precio puesto en destino; un catálogo «desde USD X» es el modelo más básico.

## Verificación por dimensión, no un «verificado» único
Marcar por separado: acceso al origen · integridad de la copia · período
representado · alcance y completitud · condiciones de uso · exactitud. Un
metadato documenta sólo lo que describe: no se extiende a otras capas o
versiones.

## Reproducir sin volver a la fuente
Guardar la copia, la consulta, la URL, la fecha, la versión de la herramienta y
un hash. Antes de recalcular, verificar el hash. Una corrida nueva no pisa la
anterior. Los datos descargados no van al control de versiones; la consulta sí.

## Descargas por servicio (WFS, APIs)
Filtrar del lado del servidor; paginar con orden estable; comparar el total
anunciado con el recibido; detectar páginas repetidas o truncas; pausar entre
pedidos; poner tope de tamaño. Un intento fallido queda documentado como caso,
no se ofrece como dato.

## Limpieza
- Contar faltantes antes de decidir, y registrar cuántas filas se pierden y por qué.
- Las herramientas descartan faltantes en silencio (un `filter` que tira los NA): incluirlos o excluirlos a propósito.
- Filtrar lo inválido para una transformación (ceros antes de un logaritmo) con una nota del motivo.
- Después de limpiar, **todo** chequeo y modelo apunta al objeto limpio.
- Códigos desconocidos quedan nulos; siglas no documentadas no se interpretan.
- Mezclar fuentes exige advertir diferencias de definición, cobertura, unidad y período.
- Ficha de cada base: variable, tipo, unidad, fuente.
- Rutas relativas, no absolutas; nombres de paquetes con su espacio de nombres cuando chocan.

## Datos espaciales
- Medir en un sistema métrico local; nunca superficies ni distancias en Web Mercator (a latitudes medias el error supera el 20–40 %).
- La matriz de vecindad (W) es una decisión del analista con parámetros documentados, no un atributo de la capa.
- Testear autocorrelación en la variable y en los residuos: residuo autocorrelacionado es modelo mal especificado.
- Un conteo de puntos por unidad no es acceso, capacidad ni tasa; una tasa necesita un denominador compatible.
- Declarar el predicado de borde y revisar casos límite (antimeridiano, bordes de la grilla).
- Una vista previa es una vista previa, no una muestra estadística.

## Series, agregados y unidades
- Cada serie con su definición según la bibliografía, la metodología con que se
  obtuvo y la fuente citada al pie de cada cuadro o gráfico.
- Preferir una serie uniforme desde un año base a una muy empalmada; si se
  empalma, documentar la fórmula (razón de solapamiento entre bases).
- Fecha de corte de la información y símbolos distintos para «no disponible» e
  «inexistente».
- Agregados que parecen iguales no lo son (M1, M2, base monetaria; presión
  tributaria nacional o provincial; interno o nacional): nombrar el exacto.
- Crecimiento con la variación del nivel real, no del nominal ni del deflactor.
- Decir qué se divide: hectáreas físicas o hectáreas-cultivo, por ave alojada o
  por ave viva, en pesos o en quintales (para aislar el efecto precio).
- Precio relevante: de mercado o puesto en el lugar (neto de flete y
  comercialización).
- Devengado no es percibido: el resultado va al período en que se gana o se
  incurre, no al del cobro o el pago.
- Desestacionalizar antes de comparar; una caída conjunta en un año de crisis
  no prueba relación.
- Precisión no es presentación: más decimales no hacen más exacto un dato.
- Comparar con casos similares como referencia externa.

## Representación
- El mismo mapa por cuantiles, por intervalos iguales o por cajas cuenta
  historias distintas: declarar cuál se usa y por qué.
- Los gráficos llevan ejes, unidades y fuente.
