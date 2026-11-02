# Portero Digital · Cannabismática

Portero digital **sin cámaras** para Cannabismática (asociación civil de cannabis medicinal, Salta). Un solo archivo `index.html` (HTML5 + CSS + JavaScript puro), sin dependencias ni servidor. Funciona en cualquier navegador, en celular o tablet, se puede instalar como PWA y empaquetar para Windows con Electron o Tauri.

Desarrollado por **SVB · Sistema VB** (Vincular Business)
WhatsApp (387) 4484132 · vincularbusiness@gmail.com

## Primer uso

1. Abrir `index.html` (o el link de GitHub Pages) en el dispositivo que va a quedar en la puerta.
2. **Entrar al panel con doble toque** en una zona libre de la pantalla (no sobre un botón). En computadora, doble clic.
3. PIN de administrador de fábrica: `1234`. El panel muestra una lista de **puesta en marcha** que pide:
   - cambiar el PIN de administrador y el PIN de coacción de fábrica (`9999`);
   - cargar al menos una persona con PIN;
   - cargar el WhatsApp de aviso de cada área;
   - cargar el contacto de confianza para emergencias.
4. Definir los horarios en la pestaña **Horarios**.

Los datos se guardan en el propio dispositivo (`localStorage`). Al cambiar de dispositivo o de navegador hay que configurar de nuevo.

## Funciones

- **Sin cámaras ni biometría.** No captura imágenes de nadie; solo guarda el registro de eventos del dispositivo.
- **Timbre por áreas** (Recepción, Consultas, Asesoría y trámites, Talleres, Cuota social): suena el timbre en el dispositivo, queda registrado, se puede avisar por WhatsApp a cada área y, si se configura un webhook, se envía el evento `BELL` a un sistema externo.
- **Ingreso por PIN** (con bloqueo por intentos fallidos), **pases de visita temporales** (código y QR), **tarjeta NFC** (Web NFC en Android) y lector QR USB/Bluetooth tipo teclado.
- **PIN de coacción:** abre la puerta sin ningún aviso en pantalla y registra `CRITICAL_DURESS_EVENT`.
- **Horarios de habilitación:** siempre habilitado, según franjas semanales (varias por día, también cruzando la medianoche) o apagado manual. Fuera de horario se bloquean timbre, pases, NFC y voz; el personal puede entrar con PIN si se deja activado, y la emergencia siempre funciona.
- **Emergencia:** cuenta regresiva de 3 s para cancelar y llamada al 911 o a un contacto de confianza.
- **Asistente de voz** (Web Speech API, sin servicios de pago): "abrir puerta", "tocar timbre", "horarios", "emergencia".
- **Panel:** marca y logo, horarios, accesos, áreas, pases, emergencias, voz, relé, NFC/QR, firmware ESP32, auditoría exportable (JSON/CSV) y soporte del desarrollador.
- **Cerradura:** pulso de relé por HTTP a un ESP32 (firmware incluido en el panel), puerto serie (Web Serial) o API de escritorio (`window.electronAPI` / `window.__TAURI__`).

## Límites de esta versión

- No hay servidor: el personal no puede abrir la puerta desde su celular. El aviso al personal es por WhatsApp (o webhook) y la apertura se hace con PIN, tarjeta, pase o el pulsador del relé.
- Web NFC solo funciona en Android con Chrome y HTTPS.
- Para instalarlo como app se necesita servirlo por HTTPS con manifest y service worker, o empaquetarlo con Capacitor.

## Paleta (tomada del sitio de Cannabismática)

Lima `#A8E600` · menta `#1F8A70` · negro `#070806` / `#0B0E09` · texto `#ECF3E6` · fuente Inter.

## Créditos

El generador de QR es *QR Code Generator for JavaScript* de Kazuhiko Arase (licencia MIT), embebido en el archivo.
