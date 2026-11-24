# Datenschutz – Datenflüsse und Entwurf für „Datensicherheit“ (Play Console)

Stand: 24.11.2026, Spielversion 1.5.12. **Verbindlich für Nutzer ist `www/privacy.html`** (Deutsch und Englisch, in der App unter Optionen verlinkt). Diese Datei ist die interne Übersicht dazu und der Entwurf für das Formular „Datensicherheit“ in der Play Console. Keine Rechtsberatung. Die Platzhalter `[[…]]` in `privacy.html` und `impressum.html` (Name, ladungsfähige Anschrift, E-Mail) liefert der Eigentümer; solange sie fehlen, bleiben Werbung, Käufe und Messung in der App gesperrt (`CONFIG.legalReady`).

## 1. Grundsatz

Kein Konto, kein eigener Server, keine Freitexte an Dritte. Spielstand, Spielername und Café-Name bleiben auf dem Gerät. Daten verlassen das Gerät nur über vier Dienste, und zwei davon (Werbung, Messung) erst nach Einwilligung.

## 2. Datenflüsse

| Dienst | Zweck | Daten | Rechtsgrundlage | Start in der App |
|---|---|---|---|---|
| Gerät (lokal) | Spielstand, Einstellungen, Profil | Fortschritt, Münzen, Brett, Name, Café, Figur | Art. 6 Abs. 1 lit. b DSGVO; § 25 Abs. 2 Nr. 2 TDDDG | immer; verlässt das Gerät nicht (Android-Geräte-Sicherung kann ihn ins Google-Konto sichern) |
| Google UMP (Einwilligung) | Einwilligungsfenster, „Werbe-Einstellungen“ | Einwilligungsstatus | Art. 6 Abs. 1 lit. a; § 25 Abs. 1 TDDDG | beim Start, vor Werbung und Messung |
| Google AdMob | belohnte Videos | IP-Adresse (grobe Region), Interaktionen (Start, Tippen, Videoansicht), Diagnose (Startzeit, Hänger, Energie), Werbe-ID, App-Set-ID | Art. 6 Abs. 1 lit. a | nur nach Einwilligung (`initAds`) |
| AppsFlyer | Herkunfts- und Ereignismessung; Weitergabe an Vermittler (z. B. Almedia) zur Abrechnung | IP (grober Ort), Werbe-ID, App-Starts, Ereignisse mit Zahlen (`docs/EVENTS.md`), Geräte- und Leistungsangaben (Betrugserkennung), Kauf mit Umsatz | Art. 6 Abs. 1 lit. a; § 25 Abs. 1 TDDDG | nur nach Einwilligung; stoppt beim Widerruf |
| RevenueCat | Käufe prüfen, Store-Preise | anonyme Kennung, Kaufbeleg, Produkt, Land, Währung, IP | Art. 6 Abs. 1 lit. b, f, c | in der App, unabhängig von der Werbe-Einwilligung, aber nur wenn `legalReady` |
| Google Play | Zahlung | nur Google (wir und RevenueCat bekommen keine Zahlungsdaten) | – | beim Kauf |
| GitHub Pages | Web-Version | IP und Zugriffsdaten in Server-Protokollen des Hosters; keine Cookies, keine Analyse, Schriften eingebettet | Art. 6 Abs. 1 lit. f | nur Web-Version |

Die Web-Version misst nichts, zeigt nur Demo-Werbung und hat keine echten Käufe. Ereignisse, die vor der Entscheidung im Einwilligungsfenster entstehen, werden gemerkt (höchstens 60) und nur bei Zustimmung gesendet, sonst verworfen (Tests S1 und S2).

## 3. Entwurf „Datensicherheit“ (Play Console → App-Inhalte)

Quellen der Angaben: Hinweise von Google zum Werbe-SDK, von AppsFlyer und von RevenueCat (Links unten, Stand 24.11.2026). **Verantwortlich für die Antworten ist der App-Entwickler**; Google prüft sie im Überprüfungsverfahren, nicht auf Richtigkeit. Nach dem ersten echten Build mit den dort aufgelösten SDK-Versionen (`versionen-<Nr>`) noch einmal gegen die dann gültigen Anbieterseiten abgleichen.

| Frage im Formular | Entwurf |
|---|---|
| Erhebt oder teilt die App Nutzerdaten? | **Ja** |
| Alle Daten bei der Übertragung verschlüsselt? | **Ja** (laut Angaben von Google und AppsFlyer TLS; bei RevenueCat und der Web-Version HTTPS, die Angabe von RevenueCat beim Ausfüllen gegenprüfen) |
| Können Nutzer die Löschung ihrer Daten verlangen? | **Ja**, per E-Mail (Abschnitt 4); den Spielstand löscht der Nutzer selbst (Optionen → Fortschritt löschen oder Deinstallieren) |
| Konto-Erstellung in der App? | **Nein**, keine Konten (keine Löschfunktion für Konten nötig) |

| Datentyp (Play-Bezeichnung) | Erhoben | Geteilt | Zweck | Optional | Woher |
|---|---|---|---|---|---|
| Ungefährer Standort (aus der IP) | ja | ja | Werbung oder Marketing, Analyse, Betrugsprävention | ja (nach Einwilligung) | AdMob, AppsFlyer |
| Geräte- oder andere Kennungen (Werbe-ID, App-Set-ID, AppsFlyer-ID, RevenueCat-Kennung) | ja | ja | Werbung oder Marketing, Analyse, Betrugsprävention, App-Funktionalität (Käufe) | ja für Werbung und Messung; RevenueCat nur bei Käufen nötig | AdMob, AppsFlyer, RevenueCat |
| App-Aktivität (App-Interaktionen) | ja | ja | Analyse, Werbung oder Marketing | ja (nach Einwilligung) | AdMob, AppsFlyer |
| App-Informationen und Leistung (Diagnose) | ja | ja | Analyse, Betrugsprävention | ja (nach Einwilligung) | AdMob, AppsFlyer |
| Finanzinfos → Kaufverlauf | ja | ja | App-Funktionalität (Käufe prüfen), Analyse | ja (Käufe sind freiwillig) | RevenueCat, AppsFlyer (Ereignis `purchase`) |

**Geteilt = ja,** weil AppsFlyer Ereignisse an Werbepartner und Vermittlungsplattformen (z. B. Prämien-Apps) weitergibt und das Werbe-SDK Daten an Google-Werbedienste sendet. Das steht so auch in `www/privacy.html`.

**Nicht erhoben:** Name, E-Mail, Adresse, Telefonnummer, genauer Standort, Kontakte, Fotos und Videos, Audio, Dateien, Nachrichten, Kalender, Gesundheit, Browserverlauf (der Spielername bleibt auf dem Gerät und gilt nach Googles Definition nicht als erhoben).

**Weitere Angaben in der Play Console:**
- **Werbe-ID:** „Ja“ (Berechtigung `AD_ID` im Manifest, `docs/TECHNIK.md`, Abschnitt 6); Zweck: Werbung oder Marketing, Analyse.
- **Datenschutz-URL:** `https://johnqpowers.github.io/merge-cafe/privacy.html`. Die Seite ist öffentlich erreichbar, sobald der nächste Push die Web-Version veröffentlicht hat (die jetzt online stehende Fassung ist älter).
- **Zielgruppe:** 16+ (`docs/ALTERSFREIGABE.md`). Damit gilt das Families-Programm nicht.
- **iOS (später):** eigene Angaben „App-Datenschutz“ in App Store Connect und die Abfrage zur App-Tracking-Transparenz.

## 4. Anfragen von Nutzern (Auskunft, Löschung, Widerruf)

1. Anfragen kommen per E-Mail an die Adresse aus der Datenschutzseite. Wir speichern keine Namen oder Konten; Messdaten lassen sich nur zuordnen, wenn der Nutzer seine Werbe-ID oder AppsFlyer-Kennung nennt (Android: Einstellungen → Google → Werbung).
2. **AppsFlyer:** Löschanfragen für einzelne Endnutzer unterstützt der Anbieter über das OpenGDPR-Verfahren (Angabe von AppsFlyer).
3. **RevenueCat:** Löschung über dessen Dashboard bzw. Datenschutzfunktion; Einzelheiten beim Anbieter prüfen.
4. **Werbe-ID:** Nutzer können sie in den Android-Einstellungen zurücksetzen oder löschen (Angabe von Google).
5. **Widerruf der Einwilligung:** im Spiel unter Optionen → Werbe-Einstellungen; wirkt sofort auf Werbung und Messung (Test S6).

## 5. Verträge und Pflichtunterlagen (Eigentümer)

- [ ] Platzhalter in `privacy.html` und `impressum.html` ersetzen (Name oder Firma, ladungsfähige Anschrift, E-Mail).
- [ ] Datenverarbeitungsverträge (Auftragsverarbeitung) bzw. Datenschutzbedingungen der Anbieter in den jeweiligen Konten annehmen oder abschließen: AppsFlyer, RevenueCat; für AdMob die Google-Bedingungen zur Datennutzung. Welche Rolle (Auftragsverarbeiter oder eigener Verantwortlicher) jeweils gilt, fachlich prüfen lassen.
- [ ] Kurzes Verzeichnis der Verarbeitungstätigkeiten anlegen (Tabelle aus Abschnitt 2 als Grundlage); ob eine Datenschutz-Folgenabschätzung nötig ist, fachlich prüfen und die Begründung festhalten.
- [ ] Einwilligungsnachricht (UMP) in der AdMob-Konsole einrichten (`docs/MONETARISIERUNG.md`, Abschnitt 10).
- [ ] Nach der Veröffentlichung der Web-Version prüfen, dass die Datenschutz-URL die neue Fassung zeigt.
- [ ] Formular „Datensicherheit“ nach Abschnitt 3 ausfüllen und nach dem ersten echten Build gegenprüfen.

## Quellen (Stand 24.11.2026)
- Google, Google Mobile Ads SDK: Offenlegung bei Google Play (Datentypen, TLS, Werbe-ID optional): https://developers.google.com/admob/android/privacy/play-data-disclosure
- AppsFlyer, Hinweise zum Formular „Datensicherheit“: https://support.appsflyer.com/hc/en-us/articles/4417197430289
- RevenueCat, „Google Play's Data Safety“: https://www.revenuecat.com/docs/google-plays-data-safety
- Google Play Hilfe, „Provide information for Google Play's Data safety section“: https://support.google.com/googleplay/android-developer/answer/10787469
