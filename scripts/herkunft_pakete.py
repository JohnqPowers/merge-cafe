#!/usr/bin/env python3
"""Haelt fest, was in einer Lieferung steckt: Dateiname, Groesse und SHA-256 jeder Datei eines ZIP-Pakets (oder Ordners).

Schreibt die Zeilen in docs/herkunft/pakete_dateiliste_sha256.csv (Zeilen desselben Pakets werden ersetzt) und vermerkt,
ob die Pruefsumme im Verzeichnis des Eigentuemers steht (docs/herkunft/bibliothek_113_dateien.csv).

Aufruf:  python3 -I scripts/herkunft_pakete.py <ZIP-oder-Ordner> [<weiteres>] [--datum JJJJ-MM-TT]

Zusaetzlich festhalten (docs/HERKUNFT_BILDER.md, Abschnitt 6): Datum, Werkzeug, Briefing oder Prompt der Lieferung.
Die Originale und Prompts selbst gehoeren in die Bibliothek des Eigentuemers, nicht in das oeffentliche Repo.
"""
import argparse, csv, datetime, hashlib, io, re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERK = ROOT / 'docs' / 'herkunft'
PAK = HERK / 'pakete_dateiliste_sha256.csv'
LIB = HERK / 'bibliothek_113_dateien.csv'
SPALTEN = ['paket', 'datei', 'bytes', 'sha256', 'im_verzeichnis', 'eingetragen']


def verzeichnis_hashes():
    with open(LIB, encoding='utf-8-sig', newline='') as f:
        return {r['SHA256'] for r in csv.DictReader(f)}


def paketname(p):
    """Dateiname ohne vorangestellte Upload-Kennung (acht Hex-Zeichen und Bindestrich)."""
    return re.sub(r'^[0-9a-f]{8}-', '', Path(p).name)


def zeilen_aus(quelle, lib, datum):
    """Liefert (paket, datei, bytes, sha256, im_verzeichnis, eingetragen) fuer alle Dateien eines ZIPs oder Ordners."""
    q = Path(quelle)
    paket = paketname(q)
    out = []
    if q.is_dir():
        for p in sorted(x for x in q.rglob('*') if x.is_file()):
            d = p.read_bytes()
            h = hashlib.sha256(d).hexdigest()
            out.append((paket, p.relative_to(q).as_posix(), len(d), h, 'ja' if h in lib else 'nein', datum))
    else:
        with zipfile.ZipFile(q) as z:
            for i in sorted((x for x in z.infolist() if not x.is_dir()), key=lambda x: x.filename):
                d = z.read(i)
                h = hashlib.sha256(d).hexdigest()
                out.append((paket, i.filename, len(d), h, 'ja' if h in lib else 'nein', datum))
    return out


def schreiben(neue):
    alt = []
    if PAK.exists():
        with open(PAK, encoding='utf-8', newline='') as f:
            alt = [tuple(r[s] for s in SPALTEN) for r in csv.DictReader(f)]
    pakete = {z[0] for z in neue}
    behalten = [z for z in alt if z[0] not in pakete]
    alle = sorted(behalten + [tuple(str(x) for x in z) for z in neue], key=lambda z: (z[0], z[1]))
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(SPALTEN)
    w.writerows(alle)
    PAK.write_text(buf.getvalue(), encoding='utf-8')
    return len(alle)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('quellen', nargs='+', help='ZIP-Paket(e) oder Ordner')
    ap.add_argument('--datum', default=datetime.date.today().isoformat(), help='Eintragsdatum (Standard: heute)')
    a = ap.parse_args()
    lib = verzeichnis_hashes()
    neue = []
    for q in a.quellen:
        z = zeilen_aus(q, lib, a.datum)
        print(f'{paketname(q)}: {len(z)} Dateien, davon im Verzeichnis: {sum(1 for x in z if x[4] == "ja")}')
        neue += z
    print(f'{PAK.relative_to(ROOT)}: {schreiben(neue)} Zeilen')


if __name__ == '__main__':
    main()
