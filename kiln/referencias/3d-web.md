# 3D en la web

Lo aprendido al construir un gemelo digital navegable con Three.js. Usar sólo si el brief pide 3D.

## Base

- Three.js con **versión fija** desde un CDN permitido (o empaquetado). Si se usan cargadores del ecosistema
  (`GLTFLoader`, `RGBELoader`, `SkeletonUtils`), de la misma versión y en el orden correcto; una prueba que
  verifique ese orden evita pantallas en blanco.
- Iluminación por entorno: un HDRI chico (1k) pasado por `PMREMGenerator` a `scene.environment`, más una luz
  direccional para las sombras. Si la cámara entra a un interior, bajar la intensidad del reflejo
  (`envMapIntensity`); si no, el interior se lava.
- Materiales por familia (acero inoxidable, chapa, hormigón): un material compartido por familia, no uno por
  objeto. Las texturas tienen escala real; una chapa estampada en una máquina se ve mal.
- Instancias (`InstancedMesh`) para lo que se repite (jaulas, aves, postes).

## Modelos y recursos

- Sólo con licencia libre y **con su LEEME**: autor, licencia, URL de origen. CC0 primero (Quaternius, Kenney,
  Poly Haven).
- Los que se descartan van a un archivo de descartes, no se borran sin mirar.
- No descargar ni guardar imágenes satelitales cuando la licencia lo prohíbe: se cargan en vivo desde el
  proveedor.

## Cámara y recorrido

- Cada vista con nombre y una función para ir a ella; el recorrido es una secuencia de esas vistas, con texto que
  explica qué se ve.
- Etiquetas: que no se tapen entre sí ni tapen lo importante. Un control automático de superposición sobre todas
  las combinaciones de vista y escenario vale más que mirar unas pocas.
- Hora del día y estaciones sólo si cuentan algo.

## Rendimiento y entrega

- Medir antes de decir que entra: FPS en un equipo modesto, peso de la escena, tiempo hasta el primer cuadro.
- Para un archivo autónomo (sin servidor), embeber modelos y HDRI en base64 y vigilar el peso total.
- Captura con Chrome sin ventana: con `--use-angle=swiftshader` el WebGL anda; esperar unos 9 segundos antes de
  actuar (`--espera 9` en `foto_pagina.py`). Si un bucle de animación cuelga la captura, matar el navegador
  y volver a empezar; nunca dejarlo colgado.
- Versión sin 3D (imagen o plano) para celulares sin WebGL o con poca memoria.
