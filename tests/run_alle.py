#!/usr/bin/env python3
"""Führt alle Tests nacheinander aus und zeigt eine Ergebnistabelle. Grundlage für das Vorher-Nachher vor jedem Zusammenführen
(Regel 6 der Entwicklungsregeln, Ablauf in docs/EXPERIMENTE.md).

Aufruf aus dem Projektordner:
  python3 -I tests/run_alle.py                                 alle Tests, Tabelle am Ende, Ausgang 1 bei Fehlern
  python3 -I tests/run_alle.py --json nachher.json             zusätzlich als JSON speichern
  python3 -I tests/run_alle.py --wurzel /tmp/ref --json v.json läuft in einem anderen Arbeitsverzeichnis (z. B. `git worktree add --detach /tmp/ref 0c1bd88`)
  python3 -I tests/run_alle.py --nur test_katze,test_store     nur diese Tests
  python3 -I tests/run_alle.py --vergleich vorher.json nachher.json   Vorher-Nachher-Tabelle (Ausgang 1 bei Rückschritt)

Gefunden werden alle `tests/test_*.py` der Wurzel, neue Tests laufen also automatisch mit. Ergebnis eines Tests ist seine Zeile
„ERGEBNIS: …“ (nicht alle Tests setzen einen Exit-Code). `test_gesamt` läuft in zwei Fenstergrößen."""
import json, os, re, subprocess, sys, time
from pathlib import Path

ARGS = {'test_gesamt': [['390', '844'], ['360', '640']]}      # Tests, die Parameter brauchen; alle anderen laufen ohne
TIMEOUT = 900


def bewerten(text, rc):
    zeile = next((z for z in reversed(text.splitlines()) if z.startswith('ERGEBNIS:')), '')
    if not zeile:
        return False, 'kein Ergebnis'
    s = zeile.removeprefix('ERGEBNIS:').strip()
    if 'ALLE bestanden' in s:
        return rc == 0, 'ALLE'
    m = re.search(r'(\d+)/(\d+) bestanden', s)
    if m:
        return rc == 0 and m.group(1) == m.group(2) and 'FEHLER' not in s, f'{m.group(1)}/{m.group(2)}'
    m = re.search(r'(\d+) FEHLER', s)
    return False, (f'{m.group(1)} Fehler' if m else s[:40])


def laufen(wurzel, nur):
    tests = sorted(p for p in (wurzel / 'tests').glob('test_*.py') if not nur or p.stem in nur)
    out = []
    for p in tests:
        for a in ARGS.get(p.stem, [[]]):
            name = p.stem + (' ' + 'x'.join(a) if a else '')
            t0 = time.time()
            try:
                r = subprocess.run([sys.executable, '-I', str(p), *a], cwd=wurzel, capture_output=True, text=True, errors='replace', timeout=TIMEOUT)
                ok, label = bewerten(r.stdout + '\n' + r.stderr, r.returncode)
                tail = '\n'.join((r.stdout + r.stderr).strip().splitlines()[-12:])
            except subprocess.TimeoutExpired:
                ok, label, tail = False, 'Zeitüberschreitung', ''
            out.append({'name': name, 'ok': ok, 'ergebnis': label, 'sek': round(time.time() - t0, 1), 'ende': tail})
            print(f'{"OK  " if ok else "FEHL"} {name:<28} {label:<10} {out[-1]["sek"]:>6.1f} s', file=sys.stderr, flush=True)
    return out


def tabelle(zeilen, kopf):
    w = [max(len(str(z[i])) for z in [kopf] + zeilen) for i in range(len(kopf))]
    f = lambda z: '| ' + ' | '.join(str(c).ljust(w[i]) for i, c in enumerate(z)) + ' |'
    return '\n'.join([f(kopf), '|' + '|'.join('-' * (x + 2) for x in w) + '|'] + [f(z) for z in zeilen])


def vergleich(a, b):
    va = {r['name']: r for r in json.load(open(a, encoding='utf-8'))}
    vb = {r['name']: r for r in json.load(open(b, encoding='utf-8'))}
    zeilen, schlecht = [], False
    for n in list(va) + [n for n in vb if n not in va]:
        x, y = va.get(n), vb.get(n)
        if x and y:
            bew = 'gleich' if x['ergebnis'] == y['ergebnis'] and x['ok'] == y['ok'] else ('Rückschritt' if x['ok'] and not y['ok'] else 'geändert')
        else:
            bew = 'neu' if y else 'entfallen'
        schlecht |= bew in ('Rückschritt', 'entfallen') or (y is not None and not y['ok'])
        zeilen.append([n, x['ergebnis'] if x else '–', y['ergebnis'] if y else '–', bew])
    print(tabelle(zeilen, ['Test', 'Vorher', 'Nachher', 'Bewertung']))
    return 1 if schlecht else 0


def main():
    a = sys.argv[1:]
    if '--vergleich' in a:
        i = a.index('--vergleich')
        sys.exit(vergleich(a[i + 1], a[i + 2]))
    arg = lambda k: a[a.index(k) + 1] if k in a else None
    wurzel = Path(arg('--wurzel') or Path(__file__).resolve().parent.parent).resolve()
    nur = set((arg('--nur') or '').split(',')) - {''}
    res = laufen(wurzel, nur)
    print('\n' + tabelle([[r['name'], r['ergebnis'], 'ja' if r['ok'] else 'NEIN', f'{r["sek"]:.0f} s'] for r in res], ['Test', 'Ergebnis', 'bestanden', 'Dauer']))
    fehl = [r['name'] for r in res if not r['ok']]
    print(f'\nERGEBNIS: {"ALLE bestanden" if not fehl else str(len(fehl)) + " FEHLER: " + ", ".join(fehl)}  ({len(res)} Läufe)')
    if arg('--json'):
        json.dump(res, open(arg('--json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.exit(1 if fehl else 0)


if __name__ == '__main__':
    main()
