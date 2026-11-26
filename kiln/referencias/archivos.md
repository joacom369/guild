# Entregables que no son HTML: documento, planilla, presentación, PDF

`kiln` es dueño de **qué** se construye y de **cómo se ve** cualquier entregable. Con un archivo cambia el material,
no el método: la entrevista (paso 2), el contrato de dirección (paso 3), el piso, la mirada antes de mostrar (paso 5)
y el registro valen igual.

## Quién pone la mecánica

La mecánica de cada formato (crear, editar, convertir) la ponen las skills de archivos que tenga la plataforma (por
ejemplo, `docx`, `xlsx`, `pptx`, `pdf`). Si no hay ninguna, una biblioteca con versión fija (`python-docx`,
`openpyxl`, `python-pptx`). `kiln` no repite sus instrucciones: les pasa el contrato.

## El contrato, traducido a cada formato

| Formato | Qué fija el contrato |
|---|---|
| Documento (Word) | Estilos de título y cuerpo, márgenes, encabezado y pie, tabla de contenido si pasa de ~6 páginas, cómo se citan las cifras |
| Planilla (Excel) | Una hoja por propósito, encabezados fijos, formato numérico por columna (separador regional), fórmulas visibles, sin celdas combinadas en los datos |
| Presentación | Una idea por diapositiva, título que dice la conclusión, tamaño mínimo de letra, gráfico dominante por diapositiva |
| PDF | El del documento o la página de origen, más que el texto se pueda copiar y buscar |

Si el archivo comunica análisis o datos (informe económico, deck, resumen de modelo), ofrecer al usuario la opción de aplicar el enfoque visual de [narrativa-creativa.md](narrativa-creativa.md) (objetos del dominio, grillas 10×10 de frecuencias, comparadores limpios) adaptado a lectura estática.

## El piso, en archivos

- Abre sin advertencias en la aplicación de destino.
- Cifras con su fuente y su fecha; las de un análisis salen de su carpeta de salidas, nunca tipeadas.
- En una planilla: fórmulas con valor, sin `#REF!` ni `#DIV/0!`, sin filas o columnas ocultas que cambien un total.
- Texto alternativo en imágenes y gráficos con contenido.

## Mirarse antes de mostrar

Un archivo se mira **convertido a imagen**, no por su código: exportar a PDF (o capturar cada página o diapositiva) y
revisar contra el contrato en una sola ronda, como en el paso 5. Si la plataforma no puede convertir, se dice qué no se
miró.
