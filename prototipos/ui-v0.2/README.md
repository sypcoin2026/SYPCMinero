# Prototipo UI v0.2 — Terminal PRO y GUI

Este subdirectorio contiene **exclusivamente una base visual experimental** de SYPminer, escrita en Python 3 con biblioteca estándar.

**No es el minero operativo, no ejecuta pruebas de GPU y no inicia SOAT.** El objetivo es desarrollar dos presentaciones (ANSI y Tkinter) que lean el mismo estado JSON sin inventar métricas.

## Ejecución

Desde esta carpeta:

```bash
python3 main.py --terminal --once --no-color
python3 main.py --gui
python3 -m unittest discover -s tests -v
```

Para usar un archivo JSON existente:

```bash
python3 main.py --terminal --once --json-file /ruta/al/estado.json
python3 main.py --gui --json-file /ruta/al/estado.json
```

Si no se configura origen, muestra N/D. El módulo Tkinter puede requerir que el sistema lo incluya.

`--command` es **opcional y potencialmente peligroso si se utiliza mal**: lanza un programa explícitamente indicado por quien lo ejecuta para obtener JSON. No garantiza que ese programa externo sea de solo lectura. No pasar mineros, lanzadores de nodos ni comandos de ajuste de GPU; usar solo un exportador JSON previamente auditado. El programa no lo invoca por defecto.

## Implementado

- Vista ANSI de columnas y adaptación básica al ancho.
- Ventana Tkinter oscura con métricas, estados, gráfica de muestras presentes y registro visual.
- Lectura de JSON desde archivo y normalización conservadora.
- Estados de fuentes separados y valores desconocidos como N/D.
- Control de tamaño de JSON; pruebas unitarias sintéticas en directorios temporales.
- 11/11 pruebas unitarias comprobadas localmente el 08/11/2026.

## Limitaciones pendientes

- Falta adaptar el esquema de la versión actual del SYPminer operativo; no está incluido aquí.
- La antigüedad del archivo no demuestra que los datos internos de SOAT estén actualizados.
- La GUI muestra observaciones, no certifica minería activa ni bloques confirmados.
- La GUI se ha probado en entorno gráfico de laboratorio, no sobre todas las versiones de Kubuntu/Windows.
- Falta mejorar accesibilidad, escalado visual, protección de datos y pruebas de integración.
- No incluye carteras, claves, nodos, supervisores, controladores de GPU ni algoritmos PoW.

El diseño definitivo deberá distinguir datos actuales, históricos y no disponibles sin rellenar huecos con datos simulados. Los controles de seguridad y parada de minería pertenecen a componentes independientes de este prototipo.
