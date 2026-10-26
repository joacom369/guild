---
name: hallmark
description: Control ejecutable de un entregable (informe, tablero, planilla, presentación, respuesta con cifras) antes de dárselo a alguien. Busca cada cifra del entregable en las salidas del cálculo y lista las huérfanas, hace cerrar las identidades (totales, partes, conteos), mira el resultado como lo va a ver el lector y, en las rondas grandes, pide una revisión independiente. Termina con un acta de lo que se verificó, lo que no y lo que no prueba cada control. Usar antes de entregar o publicar algo con números, al cerrar una tanda de cambios, cuando el usuario pregunta «¿está bien?» o «¿lo revisaste?», o con /hallmark. No juzga si el análisis es bueno ni si la conclusión se sostiene (`provenance`), ni pule el diseño de una página (`kiln`, `impeccable`).
argument-hint: "[entregable y dónde están las salidas]"
---

# Hallmark: sin sello no sale

En la platería, una pieza no sale a la venta hasta que la ensayan y le ponen el sello de contraste. El sello no dice
que la pieza es linda: dice que el metal es lo que dice ser. Esta skill hace eso con un entregable. No juzga si el
análisis es bueno (eso es `provenance`); controla que **lo que se muestra sea lo que se calculó** y deja escrito qué
se controló.

## Las reglas (no se negocian)

1. **Se verifica el entregable final, el mismo archivo que va a recibir el lector.** No un borrador, no la consulta,
   no «lo que debería decir».
2. **Un control que no se corrió no se informa como hecho.** Si un nivel se salteó, el acta lo dice.
3. **Cada control declara lo que no prueba.** Que los totales cierren no prueba que estén bien; que una cifra
   aparezca en las salidas no prueba que sea la que corresponde.
4. **Lo que falla se corrige en el proceso, no en la presentación.** Una cifra huérfana se rastrea hasta su cálculo;
   no se ajusta el texto para que coincida.
5. **Una ronda de controles por tanda de cambios**, al final, sin editar en paralelo lo que se está verificando.

## Los niveles

Elegí el nivel según lo que está en juego y decilo en una línea antes de empezar. El 1 y el 2 van siempre que el
entregable tiene cifras; el 3, en las rondas grandes o cuando el usuario lo pide.

### Nivel 1 · Las cifras salen de las salidas

```bash
python scripts/cifras.py informe.md --fuentes salidas/ --decimal ,
python scripts/cifras.py tablero.html resumen.docx --fuentes salidas/ resultados.xlsx --decimal , --escala 1000
```

Saca cada número del entregable (Markdown, texto, HTML, Word, Excel, CSV, JSON) y lo busca en las salidas (la
carpeta de la corrida de `assay`, si el análisis pasó por ahí), con el
redondeo que muestra el entregable: «0,59» coincide con 0.587 y «0,52» no. Agrupa en **encontradas**, **huérfanas**
(no hay valor compatible), **ambiguas** (el formato no encaja con el separador declarado) y **triviales** (años y
enteros de un dígito, que se listan sin verificar).

- `--decimal` es obligatorio: «1.234» es otro número según el separador, y no se adivina.
- Los sufijos (mil, M, MM) no se escalan solos; se declaran con `--escala`.
- Cada huérfana se resuelve: o sale de un cálculo que hay que agregar a las salidas, o está mal. Una cifra que el
  texto deriva a mano («la diferencia es 12 %») también es huérfana hasta que su cálculo esté en las salidas.
- Límite: una cifra corta encuentra pareja con facilidad. Para las que importan, mirá en qué archivo y fila apareció.

### Nivel 2 · Identidades y lectura

**Identidades:** lo que tiene que cerrar, cerrado en código y con la diferencia a la vista, no a ojo.

- Total = suma de las partes; total = asignados + sin coincidencia + ambiguos.
- El mismo agregado calculado por dos caminos da lo mismo (por fila y por grupo, desde la base y desde la tabla final).
- Conteos antes y después de cada cruce y de cada filtro, con la explicación de la diferencia.
- Porcentajes que suman 100 (o la razón por la que no).
- Unidades, período y base iguales en todo el entregable.

Un control así es un `assert` o una tabla con una columna «diferencia» que tiene que dar cero (o sólo redondeo). Si
el proyecto ya tiene pruebas o un control de paridad, se corren y su resultado se informa tal como salió.

**Lectura:** abrí el entregable como lo va a abrir quien lo usa (la página renderizada, la planilla, el PDF) y leelo
de punta a punta.

- Una página se mira renderizada en escritorio y celular. Si `kiln` está instalada, su script `foto_pagina.py` hace las
  dos y reporta errores de consola.
- Una planilla, abierta: fórmulas con valor, sin `#REF!`, filtros y celdas ocultas a la vista.
- Seguí un caso concreto de punta a punta («el cliente 100»): que sus valores tengan sentido en cada paso.
- Cada cifra con su unidad, su período y su naturaleza, con el vocabulario de `provenance`
  (observado · calculado · reconstruido · supuesto · escenario · pendiente).
- Lo que no se sabe está a la vista, no en una nota al pie.

### Nivel 3 · Revisión independiente

Alguien que no vio tu plan ni tu razonamiento revisa el entregable contra sus fuentes. Un solo revisor por ronda
grande, con un modelo fuerte. Antes de lanzarlo, pedilo con la ficha de delegación de `tokenwise`. Cómo armar el encargo y cómo
tratar lo que devuelve, en [referencias/revisor.md](referencias/revisor.md).

Sus hallazgos **se verifican antes de aceptarlos**: un revisor también se equivoca, y con la misma seguridad.

## El acta

Cerrá siempre con el acta, corta, en este orden. Va al usuario y, si el proyecto lleva registro, a ese registro.

```markdown
**Hallmark · <entregable> · <fecha>** — <sale / sale con observaciones / no sale>

| Control | Resultado | Qué no prueba |
|---|---|---|
| Cifras (nivel 1) | 48 encontradas, 0 huérfanas, 2 triviales | que cada cifra sea la que corresponde |
| Identidades (nivel 2) | 4 de 4 cierran (dif. máx. 0,01 por redondeo) | que los datos de entrada estén bien |
| Lectura (nivel 2) | escritorio y celular, sin errores de consola | otros navegadores, lector de pantalla |
| Revisión independiente (nivel 3) | no se hizo | — |

Corregido en esta ronda: …
Queda abierto: …
```

«No sale» quiere decir que hay una huérfana sin resolver, una identidad que no cierra o un error de lectura que
cambia lo que entiende el lector. Esa decisión se le muestra al usuario; **entregar igual es decisión suya**.

## Scripts

`cifras.py` usa sólo la biblioteca estándar de Python. Para `.xlsx` hace falta `openpyxl`. Ayuda completa con
`python scripts/cifras.py -h`. Sale con código 1 si hay huérfanas o ambiguas, así que sirve en un control automático.

## Cómo se combina

- `provenance`: qué es cada cifra y cuándo una conclusión es preliminar. Hallmark controla que el entregable lo respete.
- `quarry`: la foto de datos con su ficha. Antes de recalcular, `ficha.py --verificar`.
- `kiln`: en una página, el pulido y las capturas. Hallmark agrega las cifras y el acta.
- `tokenwise`: el pedido de delegación del revisor del nivel 3 (el contenido del encargo es de esta skill).
