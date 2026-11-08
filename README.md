# SYPCMinero — SYPcoin Miner

**Estado: EN DESARROLLO · repositorio público**

SYPCMinero es el proyecto del minero y sus interfaces para **SYPcoin (SYPC)**, una criptomoneda en desarrollo basada en PoW **Autolykos2**.

Este repositorio documenta el progreso público de las interfaces **Terminal PRO (ANSI)** y **GUI (panel gráfico)**. La intención es utilizar una misma fuente de datos y un único motor de minería, sin duplicar lógica de consenso.

> **Importante:** el código publicado inicialmente es un **prototipo experimental de visualización**. No constituye una versión minable, una testnet pública, ni acredita minería continua, bloques confirmados o recompensas reales. La instalación local de SYPCMinero/SYPminer utilizada en ensayos privados **no se ha publicado aquí**.

## Estado de desarrollo

| Componente | Estado |
| --- | --- |
| Diseño y arquitectura de las dos interfaces | En desarrollo |
| Prototipo ANSI de solo lectura | Prototipo |
| Prototipo GUI con Python/Tkinter | Prototipo |
| Pruebas automatizadas del prototipo visual | 11/11 comprobadas localmente el 08/11/2026 |
| Integración con el SYPminer operativo más reciente | Pendiente de revisión |
| Telemetría actual de GPU, SOAT y nodos | Pendiente de integración y verificación en esta versión |
| Minería desde estas interfaces / paquetes instalables | No disponible |

La telemetría nunca debe inventarse. Una muestra de SOAT no equivale a un bloque confirmado; el estado de un archivo no demuestra que el proceso minero siga vivo. Los valores ausentes se presentan como **N/D**, **DESCONECTADO** o **DESACTIVADO**, según proceda.

## Prototipo visual

En `prototipos/ui-v0.2/` se publica una primera implementación de **solo lectura**, con ANSI y Tkinter. No inicia minería ni modifica sensores, potencia, ventiladores o frecuencias. No requiere paquetes Python externos; Tkinter debe estar disponible en el sistema para la GUI.

```bash
cd prototipos/ui-v0.2
python3 main.py --terminal --once --no-color
python3 main.py --gui
python3 -m unittest discover -s tests -v
```

Sin un origen JSON configurado, las cifras se muestran como **N/D**. **No** interpretes los estados de ejemplo en ilustraciones conceptuales como resultados reales. El prototipo visual y el SYPminer de laboratorio son trabajos distintos hasta su integración validada.

## Desarrollo y seguridad

Consulta [la hoja de ruta](docs/ROADMAP.md) y [la política de publicación segura](SECURITY.md).

- Nada de claves, semillas, contraseñas, direcciones privadas, carteras, datos personales ni configuraciones sensibles en GitHub.
- Sin overclock ni modificaciones automáticas de la GPU.
- Sin arranque de SOAT, nodos o minería desde un monitor de solo lectura.
- Sin afirmar soporte AMD/NVIDIA/Intel, Windows/Linux o garantías de consenso antes de verificarlo.
- No se ha elegido aún una licencia de redistribución para el código original de este repositorio; **visibilidad pública no equivale por sí misma a licencia open source**.
- Toda integración futura con proyectos de terceros deberá respetar sus licencias y atribuciones.

Nombre oficial de la moneda: **SYPcoin** · ticker: **SYPC**.
