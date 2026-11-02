"""
Revisión integral del Portero Cannabismática en un navegador real (Chromium):
panel con doble toque, personas y PIN, coacción, bloqueo, pases, timbre con aviso push (botones de
respuesta que se ven en la pantalla) y WhatsApp, emergencia y horarios.
Usa un relevo ntfy simulado (tests/fake-ntfy.js) y captura los pedidos a CallMeBot.

Uso:  python3 tests/e2e.py      (requiere Node.js y Playwright)
"""
import json, os, subprocess, sys, threading, time
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, 'tests', 'screenshots'); os.makedirs(SHOTS, exist_ok=True)
ok = []
def check(name, cond, extra=''):
    ok.append((name, bool(cond))); print(('  ✔' if cond else '  ✘'), name, '' if cond else extra)

ntfy = subprocess.Popen(['node', os.path.join(ROOT, 'tests', 'fake-ntfy.js'), '0'], stdout=subprocess.PIPE, text=True)
NTFY = f'http://127.0.0.1:{ntfy.stdout.readline().strip()}'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
web = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=ROOT)); threading.Thread(target=web.serve_forever, daemon=True).start()
WEB = f'http://localhost:{web.server_address[1]}'
TOPIC = 'cannabismatica-prueba-0123456789'
def msgs():
    with urlopen(f'{NTFY}/{TOPIC}/json?since=all&poll=1', timeout=3) as r:
        return [json.loads(l) for l in r.read().decode().splitlines() if l.strip() and json.loads(l).get('event') == 'message']
def wait(fn, t=8):
    end = time.time() + t
    while time.time() < end:
        v = fn()
        if v: return v
        time.sleep(0.2)
    return fn()

SET = {'notif': {'ntfy': {'on': True, 'server': NTFY, 'topic': TOPIC}, 'wa': {'on': True},
       'recips': [{'id': 'r1', 'name': 'Ana', 'phone': '5493874000000', 'key': '999', 'area': ''}],
       'ev': {'bell': True, 'sos': True, 'duress': True, 'lock': True, 'off': True}}}
wa = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 1280, 'height': 860})
        ctx.add_init_script(f"if(!localStorage.getItem('cnb_ver')){{localStorage.setItem('cnb_ver','2');localStorage.setItem('cnb_set',JSON.stringify({json.dumps(SET)}))}}")
        ctx.route('https://api.callmebot.com/**', lambda route: (wa.append(parse_qs(urlparse(route.request.url).query)), route.fulfill(status=200, body='Message queued')))
        errs = []
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(WEB + '/index.html'); pg.wait_for_timeout(1200)
        check('Pantalla principal con timbre, PIN, pase y emergencia', all(pg.locator(f'.tile[data-act="{a}"]').count() for a in ['bell', 'pin', 'pass', 'sos']))
        check('Datos del desarrollador SVB visibles', '(387) 4484132' in pg.inner_text('#ft'))
        # Panel con doble toque en zona libre
        h = pg.locator('.hero h1').bounding_box(); x, y = h['x'] + 5, h['y'] + h['height'] / 2
        pg.mouse.click(x, y); pg.wait_for_timeout(120); pg.mouse.click(x, y); pg.wait_for_timeout(500)
        check('Doble toque abre el teclado de administración', 'Panel de ingeniería' in pg.inner_text('#v_keypad'))
        for d in '1234': pg.locator(f'#kpad [data-d="{d}"]').click()
        pg.locator('#kpad [data-act="kok"]').click(); pg.wait_for_timeout(600)
        check('PIN 1234 abre el panel con la puesta en marcha', 'Puesta en marcha' in pg.inner_text('#v_admin'))
        # Persona con PIN
        pg.locator('[data-act="tab"][data-t="personas"]').first.click(); pg.wait_for_timeout(300)
        pg.locator('[data-act="uadd"]').click(); pg.wait_for_timeout(300)
        card = pg.locator('[data-u]').last
        card.locator('[data-uf="name"]').fill('Laura'); card.locator('[data-uf="name"]').dispatch_event('change')
        card = pg.locator('[data-u]').last
        card.locator('[data-upin]').fill('4321'); card.locator('[data-act="usetpin"]').click(); pg.wait_for_timeout(400)
        check('Persona con PIN guardada', 'Laura' in pg.locator('[data-u]').last.locator('[data-uf="name"]').input_value())
        # Avisos: prueba push y WhatsApp
        pg.locator('[data-act="tab"][data-t="avisos"]').first.click(); pg.wait_for_timeout(300)
        pg.locator('[data-act="ntfytest"]').click()
        check('Prueba push llega al tema', wait(lambda: any('Prueba' in (m.get('title') or '') for m in msgs())))
        pg.locator('[data-act="watest"]').first.click()
        check('Prueba WhatsApp a CallMeBot con +código de país', wait(lambda: any(c.get('phone') == ['+5493874000000'] and c.get('apikey') == ['999'] for c in wa)), wa)
        pg.screenshot(path=os.path.join(SHOTS, 'c1-avisos.png'), full_page=True)
        # Pase de visita de 1 uso
        pg.locator('[data-act="tab"][data-t="pases"]').first.click(); pg.wait_for_timeout(300)
        pg.fill('#pname', 'Proveedor limpieza'); pg.locator('[data-act="padd"]').click(); pg.wait_for_timeout(300)
        code = pg.evaluate("[...document.querySelectorAll('#v_admin div')].map(d=>d.textContent).find(t=>/^\\d{6}$/.test(t.trim())).trim()")
        pg.locator('[data-act="exitadm"]').first.click(); pg.wait_for_timeout(400)

        def keypad(act, digits):
            pg.locator(f'.tile[data-act="{act}"]').click(); pg.wait_for_timeout(300)
            for d in digits: pg.locator(f'#kpad [data-d="{d}"]').click()
            pg.wait_for_timeout(700)
        keypad('pin', '4321')
        check('PIN de la persona abre la puerta', 'Puerta abierta' in pg.inner_text('#ov') and 'Laura' in pg.inner_text('#ov'))
        pg.wait_for_timeout(5600)
        keypad('pass', code)
        check('Pase de visita abre', 'Puerta abierta' in pg.inner_text('#ov'))
        pg.wait_for_timeout(5600)
        keypad('pass', code)
        check('Pase de 1 uso no se puede reutilizar', 'ya utilizado' in pg.inner_text('#v_keypad'))
        pg.locator('#v_keypad [data-act="home"]').click(); pg.wait_for_timeout(300)
        # Coacción: abre sin aviso en pantalla y avisa en silencio
        keypad('pin', '9999')
        check('Coacción abre igual que un PIN normal', 'Puerta abierta' in pg.inner_text('#ov'))
        check('Coacción avisa en silencio al celular', wait(lambda: any('silenciosa' in (m.get('title') or '') for m in msgs())))
        pg.wait_for_timeout(5600)
        # Bloqueo por intentos fallidos
        pg.locator('.tile[data-act="pin"]').click(); pg.wait_for_timeout(300)
        for i in range(5):
            for d in '1111': pg.locator(f'#kpad [data-d="{d}"]').click()
            pg.wait_for_timeout(600)
        check('5 intentos fallidos bloquean el teclado', 'bloqueado' in pg.inner_text('#v_keypad').lower())
        check('Bloqueo avisa al celular', wait(lambda: any('Intentos fallidos' in (m.get('title') or '') for m in msgs())))
        pg.evaluate("localStorage.setItem('cnb_fail', JSON.stringify({n:0,until:0}))")
        pg.reload(); pg.wait_for_timeout(1000)
        # Timbre → push con botones → la respuesta aparece en la pantalla
        n = len(wa)
        pg.locator('.tile[data-act="bell"]').click(); pg.wait_for_timeout(300)
        pg.locator('.area[data-act="ring"]').first.click(); pg.wait_for_timeout(300)
        ring = wait(lambda: [m for m in msgs() if (m.get('title') or '').startswith('🔔 Timbre')])
        check('Timbre: push con 3 botones de respuesta', ring and len(ring[-1].get('actions') or []) == 3, ring and ring[-1])
        check('Timbre: WhatsApp a los dueños (sin texto de botones)', wait(lambda: any('Timbre' in c.get('text', [''])[0] and 'botones' not in c.get('text', [''])[0] for c in wa[n:])))
        act = ring[-1]['actions'][0]
        urlopen(Request(act['url'], data=act['body'].encode(), method='POST'), timeout=3)
        pg.wait_for_function("document.querySelector('#cstate') && document.querySelector('#cstate').textContent.includes('Ya vamos')", timeout=8000)
        check('Respuesta «Ya voy» se muestra en la pantalla del portero', True)
        pg.screenshot(path=os.path.join(SHOTS, 'c2-respuesta-timbre.png'))
        pg.locator('#v_bell [data-act="cancelbell"]').click(); pg.locator('[data-act="home"]').first.click(); pg.wait_for_timeout(300)
        # Horarios: apagado manual → fuera de servicio
        pg.evaluate("(()=>{const s=JSON.parse(localStorage.getItem('cnb_set'));s.enMode='off';localStorage.setItem('cnb_set',JSON.stringify(s))})()")
        pg.reload(); pg.wait_for_timeout(1000)
        check('Fuera de horario: aviso y timbre deshabilitado', 'fuera de servicio' in pg.inner_text('#v_home').lower() and pg.locator('.tile[data-act="bell"]').is_disabled())
        check('Fuera de horario: la emergencia sigue disponible', pg.locator('.tile[data-act="sos"]').is_enabled())
        # Emergencia
        pg.locator('.tile[data-act="sos"]').click(); pg.wait_for_timeout(300)
        pg.locator('[data-act="sos911"]').click(); pg.wait_for_timeout(3800)
        sos = wait(lambda: [m for m in msgs() if 'EMERGENCIA' in (m.get('title') or '')])
        check('Emergencia: aviso urgente al celular', sos and sos[-1].get('priority') == 5, sos)
        check('Emergencia: WhatsApp', wait(lambda: any('EMERGENCIA' in c.get('text', [''])[0] for c in wa)))
        check('Sin errores de JavaScript', not errs, errs)
        b.close()
finally:
    ntfy.terminate(); web.shutdown()
print(f'RESULTADO {sum(1 for _, c in ok if c)} / {len(ok)}')
sys.exit(0 if all(c for _, c in ok) else 1)
