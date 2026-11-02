# Portero Digital · Cannabismática

Portero digital **sin cámaras** para Cannabismática (asociación civil de cannabis medicinal, Salta). Un solo archivo `index.html` (HTML5 + CSS + JavaScript puro), sin dependencias ni servidor. Se abre en cualquier navegador, se puede instalar como PWA en una tablet y empaquetar para Windows con Electron o Tauri.

Desarrollado por **SVB · Sistema VB** (Vincular Business)
WhatsApp (387) 4484132 · vincularbusiness@gmail.com

## Cómo probarlo

Abrir `index.html` en el navegador (mejor en Chrome o Edge, en pantalla completa). Si usás GitHub Pages, la raíz del repo ya sirve el archivo.

Datos de demo:

| Qué | Valor |
|---|---|
| PIN de socio | `2580` |
| PIN de equipo (rol Personal) | `1111` |
| Pase de visita | `246810` |
| Panel admin | mantener presionado el logo 2 s, PIN `1234` |
| PIN de coacción | `9999` (abre sin avisar en pantalla y registra `CRITICAL_DURESS_EVENT`) |

Antes de una instalación real hay que cambiar todos esos PIN y desactivar la "Guía demo" desde el panel admin.

## Funciones

- **Sin cámaras ni biometría.** No captura imágenes de nadie; solo guarda el registro de eventos del dispositivo.
- **Timbre por áreas** (Recepción, Consultas, Asesoría y trámites, Talleres, Cuota social), con 5 timbres sintetizados y aviso por WhatsApp a cada área.
- **Ingreso por PIN**, con bloqueo por intentos fallidos, **pases de visita temporales** (código y QR), **tarjeta NFC** (Web NFC en Android) y lector QR USB/Bluetooth tipo teclado.
- **Horarios de habilitación:** siempre habilitado, según franjas semanales (con varias franjas por día y franjas que cruzan la medianoche) o apagado manual. Fuera de horario se bloquean timbre, pases, NFC y voz; el personal puede entrar con PIN si se deja activado, y la emergencia siempre funciona.
- **Emergencia:** cuenta regresiva de 3 s para cancelar y llamada al 911 o a un contacto de confianza.
- **Asistente de voz** (Web Speech API, sin servicios de pago): "abrir puerta", "tocar timbre", "horarios", "emergencia".
- **Panel admin:** marca y logo, accesos, áreas, pases, emergencias, voz, relé, NFC/QR, firmware ESP32, auditoría exportable (JSON/CSV) y soporte del desarrollador.
- **Cerradura:** pulso de relé por HTTP a un ESP32 (firmware incluido en el panel), puerto serie (Web Serial) o API de escritorio (`window.electronAPI` / `window.__TAURI__`).

## Límites de esta versión

- Los datos (usuarios, pases, log, ajustes) se guardan en `localStorage` del dispositivo; no hay servidor. En el modo demo, la respuesta del personal al timbre es simulada.
- Web NFC solo funciona en Android con Chrome y HTTPS.
- Para instalarlo como app se necesita servirlo por HTTPS con manifest y service worker, o empaquetarlo con Capacitor.

## Paleta (tomada del sitio de Cannabismática)

Lima `#A8E600` · menta `#1F8A70` · negro `#070806` / `#0B0E09` · texto `#ECF3E6` · fuente Inter.

## Créditos

El generador de QR es *QR Code Generator for JavaScript* de Kazuhiko Arase (licencia MIT), embebido en el archivo.
