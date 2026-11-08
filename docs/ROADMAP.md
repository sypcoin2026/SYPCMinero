# Hoja de ruta pública — SYPCMinero

**Fecha de referencia:** 08/11/2026. Estos puntos expresan objetivos de desarrollo, no funcionalidades productivas.

## Etapa 0 — Base visual pública

- [x] Definir dos presentaciones previstas: Terminal PRO y GUI.
- [x] Crear prototipo de visualización ANSI y Tkinter sin control minero.
- [x] Añadir pruebas unitarias sintéticas y separadas de telemetría real: 11/11 ejecutadas localmente.
- [x] Publicar código revisado de esta base visual en repositorio independiente.
- [ ] Obtener y auditar el SYPminer operativo más reciente antes de integrarlo.

## Etapa 1 — Fuentes reales y estados independientes

- [ ] Adaptar el formato JSON vigente de SYPminer, sin duplicar adaptadores.
- [ ] Leer porcentaje de uso de GPU AMD solo desde fuente identificada y validada; mostrar N/D si falta.
- [ ] Verificar temperaturas, potencia, hotspot, frecuencias y ventiladores en hardware real.
- [ ] Distinguir vigencia del archivo SOAT, vigencia de su contenido y actividad real del proceso.
- [ ] Distinguir soluciones de SOAT, bloques aceptados por nodo y bloques confirmados por ambos nodos.
- [ ] Mostrar N/D, DESCONECTADO o DESACTIVADO sin inferir métricas.
- [ ] Mantener el Guardián externo y no depender del estado visual para cortar operaciones inseguras.

## Etapa 2 — Calidad de interfaces

- [ ] Igualar la Terminal PRO con la maqueta aprobada respetando limitaciones ANSI.
- [ ] Mejorar la GUI con gráficos de métricas observadas, diseño adaptable y navegación real.
- [ ] Mantener un único contrato de datos de lectura para ambas interfaces.
- [ ] Optimizar refresco, ancho de terminal, errores y cargas prolongadas.
- [ ] Localización en español de errores, etiquetas y mensajes.

## Etapa 3 — Integración y distribución

- [ ] Integrar con el motor minero seleccionado sin copiar algoritmos ni cambiar consenso.
- [ ] Revisar licencias y atribuciones antes de redistribuir componentes de terceros.
- [ ] Validar configuraciones por plataforma y GPU en ensayos específicos.
- [ ] Publicar instrucciones de instalación seguras, firmadas o verificables cuando existan entregas reproducibles.
- [ ] Evaluar paquetes Linux/Windows cuando las pruebas funcionales lo justifiquen.

## Criterios para declarar una capacidad «verificada»

Debe existir prueba reproducible específica, datos reales y ausencia de datos ficticios. Para un bloque minado, **solución de SOAT**, **admisión de nodo** y **confirmación por nodos** son eventos distintos. Nunca deducir recompensas de un contador sin evidencia de emisión y registro contable.

La red y la moneda SYPcoin todavía están **EN DESARROLLO**. No anunciar exchanges, minería pública, billeteras listas o compatibilidad certificada sin respaldo.
