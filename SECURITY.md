# Seguridad y publicación responsable

**Proyecto en desarrollo.** Este repositorio es público: toda información que se suba puede ser leída y conservada por terceros.

## Nunca publicar

- Semillas, claves privadas, contraseñas, carteras, archivos de custodia o credenciales.
- Direcciones y configuraciones privadas de nodos, redes o servidores cuando identifiquen infraestructuras no públicas.
- Registros reales sin depurar que contengan tokens, identificadores privados, rutas personales o información de terceros.
- Datos bancarios o personales, volcados de memoria, ficheros de entorno o resultados confidenciales.
- Código de otras personas sin revisar permisos, licencias y avisos de atribución.

El archivo `.gitignore` es una defensa adicional, **no una garantía de seguridad**. Revisar manualmente cada cambio antes de publicarlo.

## Límites de la versión pública actual

- El directorio `prototipos/ui-v0.2/` contiene una interfaz **de solo lectura por defecto**, sin minero incorporado.
- No ajusta potencia, voltaje, frecuencias ni ventiladores y no inicia SOAT ni nodos por sí solo.
- El argumento opcional `--command` ejecuta **exactamente el programa elegido por quien lo utiliza**, bajo sus permisos. No lo uses salvo después de auditar el exportador JSON: un programa externo puede producir efectos secundarios.
- El hecho de que un JSON o un log cambie no confirma actividad minera actual.
- Los contadores de soluciones de SOAT **no prueban** que un bloque sea aceptado ni confirmado por la red.
- No utilizar la interfaz para tomar decisiones de seguridad térmica. Las protecciones deben permanecer independientes del monitor.
- No hay auditoría de seguridad externa ni validación de minería pública.

## Comunicación de vulnerabilidades

No publiques contraseñas, claves, ejemplos explotables contra nodos privados ni otros secretos en incidencias públicas. Utiliza, cuando esté habilitado, el canal privado de reporte de seguridad del repositorio.

**No se autoriza el overclock** como parte del desarrollo oficial de SYPcoin Miner. Cualquier prueba posterior de minería requiere autorización y límites operativos independientes.

**Nota sobre licencias:** la publicación del código no concede automáticamente permisos de reutilización. La licencia del código original del proyecto está pendiente de aprobación. Cualquier integración futura de SOAT u otro tercero deberá respetar su licencia correspondiente.
