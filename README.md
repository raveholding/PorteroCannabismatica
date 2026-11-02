# Portero Digital · Cannabismática

Portero digital **sin cámaras** para Cannabismática (asociación civil de cannabis medicinal, Salta). Un solo archivo `index.html` (HTML5 + CSS + JavaScript puro), sin dependencias ni servidor. La carpeta `face/` es opcional y solo se necesita para el reconocimiento facial. Funciona en cualquier navegador, en celular o tablet, se puede instalar como PWA y empaquetar para Windows con Electron o Tauri.

Desarrollado por **SVB · Sistema VB** (Vincular Business)
WhatsApp (387) 4484132 · vincularbusiness@gmail.com

## Primer uso

1. Abrir `index.html` (o el link de GitHub Pages) en el dispositivo que va a quedar en la puerta.
2. **Entrar al panel con doble toque** en una zona libre de la pantalla (no sobre un botón). En computadora, doble clic.
3. PIN de administrador de fábrica: `1234`. El panel muestra una lista de **puesta en marcha** que pide:
   - cambiar el PIN de administrador y el PIN de coacción de fábrica (`9999`);
   - cargar al menos una persona con PIN;
   - cargar el WhatsApp de aviso de cada área;
   - cargar el contacto de confianza para emergencias;
   - activar los avisos al celular (push o WhatsApp).
4. Definir los horarios en la pestaña **Horarios**.

Los datos se guardan en el propio dispositivo (`localStorage`). Al cambiar de dispositivo o de navegador hay que configurar de nuevo.

## Funciones

- **Sin cámaras ni biometría.** No captura imágenes de nadie; solo guarda el registro de eventos del dispositivo.
- **Timbre por áreas** (Recepción, Consultas, Asesoría y trámites, Talleres, Cuota social): suena el timbre en el dispositivo, queda registrado, avisa a los celulares configurados (ver Avisos), permite que la visita avise por WhatsApp a cada área y, si se configura un webhook, envía el evento `BELL` a un sistema externo.
- **Avisos al celular** (panel → Avisos al celular), a elección de los dueños:
  - **Notificación push con [ntfy](https://ntfy.sh)** (recomendado): gratis y sin cuentas. Cada persona instala la app ntfy y se suscribe al tema que genera el panel (el tema funciona como contraseña; el panel muestra un QR). El aviso del timbre trae botones **Ya voy · Un momento · No podemos**: la respuesta se muestra y se escucha en la pantalla del portero.
  - **WhatsApp automático con CallMeBot** (opcional): cada persona lo activa una vez desde su WhatsApp y carga su apikey en el panel; se puede limitar por área. Es un servicio gratuito no oficial y de uso personal.
  - Se pueden elegir los eventos: timbre, emergencia, alerta silenciosa (PIN de coacción), bloqueo por intentos fallidos e intentos fuera de horario. Si no hay internet, los avisos quedan en cola y se reintentan durante 15 minutos.
- **Ingreso por PIN** (con bloqueo por intentos fallidos), **pases de visita temporales** (código y QR), **tarjeta NFC** (Web NFC en Android) y lector QR USB/Bluetooth tipo teclado.
- **PIN de coacción:** abre la puerta sin ningún aviso en pantalla y registra `CRITICAL_DURESS_EVENT`.
- **Personal autorizado con huella o rostro** (opcional, desactivado de fábrica): ver la sección siguiente.
- **Horarios de habilitación:** siempre habilitado, según franjas semanales (varias por día, también cruzando la medianoche) o apagado manual. Fuera de horario se bloquean timbre, pases, NFC y voz; el personal puede entrar con PIN si se deja activado, y la emergencia siempre funciona.
- **Emergencia:** cuenta regresiva de 3 s para cancelar y llamada al 911 o a un contacto de confianza.
- **Asistente de voz** (Web Speech API, sin servicios de pago): "abrir puerta", "tocar timbre", "horarios", "emergencia".
- **Panel:** marca y logo, horarios, accesos, áreas, pases, emergencias, voz, relé, NFC/QR, firmware ESP32, auditoría exportable (JSON/CSV) y soporte del desarrollador.
- **Cerradura:** pulso de relé por HTTP a un ESP32 (firmware incluido en el panel), puerto serie (Web Serial) o API de escritorio (`window.electronAPI` / `window.__TAURI__`).

## Huella y reconocimiento facial del personal

Para personal autorizado (roles *Personal* y *Profesional*) registrado previamente desde **Panel → Accesos**. Cada persona necesita que el administrador marque su **consentimiento informado y por escrito** antes de poder registrar su huella o su rostro; el panel lo anota en la auditoría y, si se retira, borra sus datos biométricos.

- **Huella** (passkeys / WebAuthn): se verifica en el celular de la persona (se registra escaneando un QR) o en el sensor del dispositivo. El portero nunca ve la huella: recibe una firma y la verifica con la clave pública guardada. No usa cámara.
  - Requiere abrir el portero por **HTTPS** (por ejemplo GitHub Pages) o `localhost`; no funciona desde un archivo local. Si cambia la dirección web hay que volver a registrar.
  - Si se registra la huella del propio dispositivo, el portero acepta cualquier huella cargada en ese dispositivo y la asigna a la persona elegida; para saber con certeza quién entró conviene que cada persona use su celular.
- **Rostro**: la cámara se enciende solo cuando alguien toca "Reconocimiento facial". No se guardan fotos ni videos: solo una plantilla numérica de 5 muestras por persona, guardada en el dispositivo. El texto de privacidad de la pantalla principal cambia a "Cámara solo para personal registrado · no se guardan fotos" cuando está activo.
  - Usa [face-api](https://github.com/vladmandic/face-api) (licencia MIT) y sus modelos, incluidos en `face/` (unos 8 MB), cargados solo al usarlo. Requiere servir `index.html` junto con la carpeta `face/` por HTTPS o `localhost`.
  - Exige un **parpadeo** para frenar fotos y ajusta la exigencia de coincidencia (0,5 por defecto; más bajo es más estricto). Es menos seguro que la huella: un video de la persona podría engañarlo. No conviene usarlo como única barrera si hay riesgo real.

## Pruebas

```bash
python3 tests/e2e.py    # 22 pruebas en navegador: panel, personas, PIN, coacción, bloqueo, pases, timbre con push y WhatsApp, respuesta desde el celular, horarios y emergencia
```

## Límites de esta versión

- No hay servidor propio: el personal recibe avisos en su celular pero no puede abrir la puerta desde él. La apertura se hace con PIN, tarjeta, pase o el pulsador del relé.
- Los avisos necesitan que el dispositivo del portero tenga internet y dependen de servicios de terceros (ntfy y CallMeBot). Para un servicio oficial de WhatsApp haría falta la API de WhatsApp Business con un servidor.
- Web NFC solo funciona en Android con Chrome y HTTPS.
- La huella y el rostro dependen de HTTPS/`localhost`, de un dispositivo con sensor o cámara y de que los datos biométricos se manejen con consentimiento: son datos personales sensibles.
- Para instalarlo como app se necesita servirlo por HTTPS con manifest y service worker, o empaquetarlo con Capacitor.

## Paleta (tomada del sitio de Cannabismática)

Lima `#A8E600` · menta `#1F8A70` · negro `#070806` / `#0B0E09` · texto `#ECF3E6` · fuente Inter.

## Créditos

El generador de QR es *QR Code Generator for JavaScript* de Kazuhiko Arase (licencia MIT), embebido en el archivo.

El reconocimiento facial usa *face-api* de Vladimir Mandic (licencia MIT, copia en `face/LICENSE-face-api.txt`).
