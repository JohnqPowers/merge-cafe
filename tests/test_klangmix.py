"""Klang-Mischung (Experiment exp/klangmix; Schalter CONFIG.features.mix, im Web ?mix=0 / ?mix=1).
Befund (Messung hinter dem Verdichter, Chrome): Musik lag über einen Handy-Lautsprecher (Hochpass 300 Hz) rund 20 dB unter den Effekten.
Geprüft werden:
  A  Schalter aus = alte Pegel exakt (Bus-Werte 0,85 / 0,16 / 0,05, kein zusätzlicher Bass-Zweig), an = neue Werte (0,6 / 0,5 / 0,156 / Bass 0,45)
  B  Pegel in beiden Zuständen gemessen (Effekte: Spitze und kurzes RMS; Musik in drei Welten): Musik hörbar lauter, Effekte leiser, Abstand auf dem Handy rund 5 bis 14 dB statt über 15 dB
  C  Reserve: alle lauten Effekte gleichzeitig über laufender Musik bleiben unter -3 dBFS (kein Übersteuern)
  D  Absenkung der Musik bei Werbung (duck) weiter um rund 10 dB, Musik aus = still, Effekte aus = still
  E  keine Fehler
Gemessen wird mit einem Abgriff hinter dem Verdichter (Test-Skript, nicht im Spiel). Aufruf: python3 -I tests/test_klangmix.py"""
import asyncio, json, datetime, sys, os, math
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helfer import CHROME, STATE, server

URL = server()
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
BASE = json.load(open(STATE))
res = []


def ok(name, cond, extra=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra != '' else ''), flush=True)


# Abgriff: hinter dem Verdichter (= was das Gerät bekommt), einmal voll, einmal mit Hochpass 300 Hz (kleiner Handy-Lautsprecher); dazu Protokoll der Pegel-Schreibzugriffe
TAP = """(() => { const AC = window.AudioContext || window.webkitAudioContext; const orig = AC.prototype.createDynamicsCompressor;
  const A = window.__aud = { full: [], hp: [], writes: [], targets: [], gains: 0, ctx: null, err: null };
  const D = Object.getOwnPropertyDescriptor(AudioParam.prototype, 'value');
  Object.defineProperty(AudioParam.prototype, 'value', { get() { return D.get.call(this); }, set(v) { A.writes.push(v); D.set.call(this, v); }, configurable: true });
  const T = AudioParam.prototype.setTargetAtTime; AudioParam.prototype.setTargetAtTime = function (v, t, k) { A.targets.push(v); return T.call(this, v, t, k); };
  const G = AC.prototype.createGain; AC.prototype.createGain = function () { A.gains++; return G.call(this); };
  const grab = (ctx, src, out) => { const sp = ctx.createScriptProcessor(1024, 1, 1), z = ctx.createGain(); z.gain.value = 0;
    sp.onaudioprocess = e => { const d = e.inputBuffer.getChannelData(0); let s = 0, m = 0; for (let i = 0; i < d.length; i++) { const a = d[i]; s += a * a; const b = a < 0 ? -a : a; if (b > m) m = b; }
      out.push([ctx.currentTime, s / d.length, m]); if (out.length > 4e5) out.splice(0, 2e5); };
    src.connect(sp); sp.connect(z); z.connect(ctx.destination); };
  AC.prototype.createDynamicsCompressor = function () { const c = orig.call(this);
    try { A.ctx = this; grab(this, c, A.full); const hf = this.createBiquadFilter(); hf.type = 'highpass'; hf.frequency.value = 300; c.connect(hf); grab(this, hf, A.hp); } catch (e) { A.err = String(e); }
    return c; }; })();"""


def db(x):
    return -120 if x <= 1e-12 else 20 * math.log10(x)


def stats(bl):
    if not bl: return None
    ms = sum(b[1] for b in bl) / len(bl); pk = max(b[2] for b in bl); best = 0
    for i in range(0, max(1, len(bl) - 2)):
        w = bl[i:i + 3]; best = max(best, sum(b[1] for b in w) / len(w))          # lautestes Fenster von ca. 64 ms
    return dict(rms=db(math.sqrt(ms)), peak=db(pk), short=db(math.sqrt(best)))


async def window(pg, t0, t1):
    full = await pg.evaluate('window.__aud.full.filter(b => b[0] >= %f && b[0] <= %f)' % (t0, t1))
    hp = await pg.evaluate('window.__aud.hp.filter(b => b[0] >= %f && b[0] <= %f)' % (t0, t1))
    r = stats(full); r['hp'] = stats(hp); return r


async def now(pg):
    return await pg.evaluate('window.__aud.ctx.currentTime')


async def mk(b, q):
    st = json.loads(json.dumps(BASE)); st['level'] = 3; st['tut'] = 3; st['music'] = False; st['sound'] = True
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, locale='de-DE')
    pg = await ctx.new_page(); pg.ctx = ctx; pg.errs = []
    pg.on('pageerror', lambda e: pg.errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: pg.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    await pg.add_init_script(TAP)
    s = json.dumps(st).replace('@@TODAY@@', today)
    await pg.add_init_script("if(!localStorage.getItem('mergecafe_v1')){const s=%s;s.eTs=Date.now();s.created=Date.now();localStorage.setItem('mergecafe_v1',JSON.stringify(s))}" % s)
    await pg.goto(URL + q); await pg.wait_for_timeout(1800)
    await pg.click('#spPlay', force=True); await pg.wait_for_timeout(2500)
    return pg


EFX = [('tap', 'tap()'), ('plop', 'plop()'), ('merge', 'merge(1,1)'), ('deliver', 'deliver()'), ('coin', 'coin(0)'), ('levelUp', 'levelUp()'), ('stamp', 'stamp()')]
WORLDS = [(0, 3), (3, 17), (8, 55)]


async def messen(b, q):
    """Misst einen Zustand: Schreibzugriffe auf Pegel, Effekte, Musik, Überlagerung, Absenkung, Stille."""
    pg = await mk(b, q); R = {}
    R['audio'] = await pg.evaluate('MC.audio()')
    R['writes'] = await pg.evaluate('window.__aud.writes')
    await pg.evaluate('MC.snd.musicOn()'); await pg.wait_for_timeout(300)
    R['targets_on'] = list(await pg.evaluate('window.__aud.targets'))
    await pg.evaluate('MC.snd.duck(true)'); await pg.wait_for_timeout(100)
    R['targets_duck'] = (await pg.evaluate('window.__aud.targets'))[-1]
    await pg.evaluate('MC.snd.duck(false)'); await pg.evaluate('MC.snd.musicOff()'); await pg.wait_for_timeout(1500)
    # Effekte einzeln, Musik aus
    R['fx'] = {}
    for name, call in EFX:
        await pg.wait_for_timeout(1300); t0 = await now(pg)
        await pg.evaluate('MC.snd.' + call); await pg.wait_for_timeout(1500)
        R['fx'][name] = await window(pg, t0 - .02, t0 + 1.4)
    # Musik allein, drei Welten
    R['mus'] = {}
    for w, L in WORLDS:
        await pg.evaluate(f'MC.world({L})'); await pg.evaluate('MC.snd.musicOff()'); await pg.wait_for_timeout(1500)
        await pg.evaluate('MC.snd.musicOn()'); await pg.wait_for_timeout(3500)
        t0 = await now(pg); await pg.wait_for_timeout(9000); t1 = await now(pg)
        R['mus'][w] = await window(pg, t0, t1)
    # Überlagerung: laufende Musik (Welt 8) + alle lauten Effekte gleichzeitig
    await pg.wait_for_timeout(500); t0 = await now(pg)
    await pg.evaluate('MC.snd.levelUp(); MC.snd.stamp(); MC.snd.merge(3,1); MC.snd.deliver(); MC.snd.word(9); MC.snd.discover()'); await pg.wait_for_timeout(2200)
    R['all'] = await window(pg, t0 - .02, t0 + 2.0)
    # Absenkung bei Werbung: Musik vor und nach duck(true)
    await pg.wait_for_timeout(2500); t0 = await now(pg); await pg.wait_for_timeout(5000); t1 = await now(pg)
    R['pre'] = await window(pg, t0, t1)
    await pg.evaluate('MC.snd.duck(true)'); await pg.wait_for_timeout(2500); t0 = await now(pg); await pg.wait_for_timeout(5000); t1 = await now(pg)
    R['duck'] = await window(pg, t0, t1)
    await pg.evaluate('MC.snd.duck(false)')
    # Musik aus = still
    await pg.evaluate('MC.snd.musicOff()'); await pg.wait_for_timeout(2500); t0 = await now(pg); await pg.wait_for_timeout(1500); t1 = await now(pg)
    R['still'] = await window(pg, t0, t1)
    # Effekte aus (S.sound = false) = still
    await pg.evaluate('MC.state().sound = false'); await pg.wait_for_timeout(300); t0 = await now(pg)
    await pg.evaluate('MC.snd.merge(3,1); MC.snd.levelUp(); MC.snd.deliver()'); await pg.wait_for_timeout(1500)
    R['sfxaus'] = await window(pg, t0 - .02, t0 + 1.4)
    R['errs'] = list(pg.errs); R['tap_err'] = await pg.evaluate('window.__aud.err')
    await pg.ctx.close()
    return R


def avg(xs):
    return sum(xs) / len(xs)


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--autoplay-policy=no-user-gesture-required'])
        OFF = await messen(b, '?mix=0')
        ON = await messen(b, '?mix=1')
        await b.close()

    ok('Vorbereitung: Ton läuft in beiden Zuständen, Abgriff funktioniert', OFF['audio'] == 'running' == ON['audio'] and not OFF['tap_err'] and not ON['tap_err'], [OFF['audio'], ON['audio'], OFF['tap_err']])

    # ---------- A: Schalter, Bus-Werte ----------
    ok('A aus: Effekt-Bus 0,85 und Musik-Ziel 0,16, kein Bass-Zweig (0,45), kein neuer Effekt-Wert 0,6', .85 in OFF['writes'] and .45 not in OFF['writes'] and .6 not in OFF['writes'] and OFF['targets_on'] == [.16], [OFF['writes'][:12], OFF['targets_on']])
    ok('A aus: Absenkung bei Werbung 0,05 wie bisher', OFF['targets_duck'] == .05, OFF['targets_duck'])
    ok('A an: Effekt-Bus 0,6, Bass-Zweig 0,45, Musik-Ziel 0,5, Absenkung 0,156; die alten Werte 0,85 und 0,16 kommen nicht mehr vor', .6 in ON['writes'] and .45 in ON['writes'] and .85 not in ON['writes'] and ON['targets_on'] == [.5] and ON['targets_duck'] == .156, [ON['writes'][:12], ON['targets_on'], ON['targets_duck']])
    ok('A Master 0,9 und Verdichter unverändert (beide Zustände)', .9 in OFF['writes'] and .9 in ON['writes'] and -14 in OFF['writes'] and -14 in ON['writes'])

    # ---------- B: Pegel ----------
    print('\n  Pegel in dBFS hinter dem Verdichter (Spitze | kurzes RMS | Handy-kurzes-RMS):  aus -> an')
    for name, _ in EFX:
        o, n = OFF['fx'][name], ON['fx'][name]
        print(f"  {name:8s} {o['peak']:6.1f} {o['short']:6.1f} {o['hp']['short']:6.1f}  ->  {n['peak']:6.1f} {n['short']:6.1f} {n['hp']['short']:6.1f}   (Spitze {n['peak'] - o['peak']:+.1f} dB)")
    for w, _ in WORLDS:
        o, n = OFF['mus'][w], ON['mus'][w]
        print(f"  Musik W{w}  {o['peak']:6.1f} {o['short']:6.1f} {o['hp']['short']:6.1f}  ->  {n['peak']:6.1f} {n['short']:6.1f} {n['hp']['short']:6.1f}   (Handy {n['hp']['short'] - o['hp']['short']:+.1f} dB)")
    mus_off = avg([OFF['mus'][w]['hp']['short'] for w, _ in WORLDS]); mus_on = avg([ON['mus'][w]['hp']['short'] for w, _ in WORLDS])
    sfx_off = avg([OFF['fx'][k]['hp']['short'] for k in ('merge', 'deliver')]); sfx_on = avg([ON['fx'][k]['hp']['short'] for k in ('merge', 'deliver')])
    gap_off, gap_on = sfx_off - mus_off, sfx_on - mus_on
    print(f"  Handy-Abstand Effekte (Zusammenführen, Liefern) zu Musik: {gap_off:.1f} dB -> {gap_on:.1f} dB; Musik {mus_on - mus_off:+.1f} dB, Effekte {sfx_on - sfx_off:+.1f} dB\n")
    ok('B Ausgangslage gemessen: aus = Musik auf dem Handy mehr als 15 dB unter den Effekten (das ist der Befund)', gap_off > 15, round(gap_off, 1))
    ok('B an: Musik auf dem Handy 7 bis 13 dB lauter', 7 <= mus_on - mus_off <= 13, round(mus_on - mus_off, 1))
    ok('B an: Effekte 2 bis 4 dB leiser (Zusammenführen, Liefern, Münze, Tippen)', all(1.5 <= OFF['fx'][k]['peak'] - ON['fx'][k]['peak'] <= 4.5 for k in ('merge', 'deliver', 'coin', 'tap')), {k: round(OFF['fx'][k]['peak'] - ON['fx'][k]['peak'], 1) for k in ('merge', 'deliver', 'coin', 'tap')})
    ok('B an: Abstand Effekte zu Musik auf dem Handy 5 bis 14 dB (vorher über 20)', 5 <= gap_on <= 14, round(gap_on, 1))
    ok('B an: in jeder einzelnen Welt ist die Musik auf dem Handy mindestens 6 dB lauter als vorher (Mittelwert über 10 s)', all(ON['mus'][w]['hp']['rms'] - OFF['mus'][w]['hp']['rms'] >= 6 for w, _ in WORLDS), {w: round(ON['mus'][w]['hp']['rms'] - OFF['mus'][w]['hp']['rms'], 1) for w, _ in WORLDS})
    ok('B an: Musik auf dem Handy im Mittel über 10 s besser als -45 dBFS (aus: schlechter als -46)', all(ON['mus'][w]['hp']['rms'] > -45 for w, _ in WORLDS) and all(OFF['mus'][w]['hp']['rms'] < -46 for w, _ in WORLDS), {w: [round(OFF['mus'][w]['hp']['rms'], 1), round(ON['mus'][w]['hp']['rms'], 1)] for w, _ in WORLDS})
    ok('B an: Musik-Spitze in keiner Welt über -8 dBFS', all(ON['mus'][w]['peak'] <= -8 for w, _ in WORLDS), {w: round(ON['mus'][w]['peak'], 1) for w, _ in WORLDS})
    ok('B an: Spitzen der lautesten Effekte (Level-Up, Stempel) unter -5 dBFS', ON['fx']['levelUp']['peak'] <= -5 and ON['fx']['stamp']['peak'] <= -5, [round(ON['fx']['levelUp']['peak'], 1), round(ON['fx']['stamp']['peak'], 1)])

    # ---------- C: Reserve ----------
    print(f"  alle lauten Effekte gleichzeitig über Musik: Spitze aus {OFF['all']['peak']:.1f} -> an {ON['all']['peak']:.1f} dBFS")
    ok('C an: Musik plus alle lauten Effekte gleichzeitig bleibt unter -3 dBFS (kein Übersteuern)', ON['all']['peak'] <= -3, round(ON['all']['peak'], 1))
    ok('C an: nicht lauter als vorher (Spitze höchstens wie aus + 1 dB)', ON['all']['peak'] <= OFF['all']['peak'] + 1, [round(ON['all']['peak'], 1), round(OFF['all']['peak'], 1)])

    # ---------- D: Absenkung, Stille ----------
    for tag, R in (('aus', OFF), ('an', ON)):
        d = R['duck']['hp']['rms'] - R['pre']['hp']['rms']
        ok(f'D {tag}: Musik bei Werbung etwa 10 dB leiser (7 bis 13 dB; Messung schwankt mit der Melodie)', -13 <= d <= -7, round(d, 1))
        ok(f'D {tag}: Musik aus = still (Pegel unter -70 dBFS)', R['still']['peak'] < -70, round(R['still']['peak'], 1))
        ok(f'D {tag}: Effekte aus (Schalter in den Optionen) = still', R['sfxaus']['peak'] < -70, round(R['sfxaus']['peak'], 1))

    # ---------- E: Fehler ----------
    ok('E keine Fehler (beide Zustände)', not OFF['errs'] and not ON['errs'], OFF['errs'] + ON['errs'])

    n = len(res); g_ = sum(res)
    print(f'\nERGEBNIS: {g_}/{n} bestanden' + ('' if g_ == n else f' ({n - g_} FEHLER)'))
    sys.exit(0 if g_ == n else 1)


asyncio.run(main())
