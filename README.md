# Merge Café – Build & Release

Casual merge game (genre of top Freecash earners such as *Merge Restaurant*). One code base → Android (Google Play), iOS (App Store), web (itch.io, CrazyGames, Poki, GameDistribution, own PWA).

```
www/            the game (index.html = complete game, PWA files, icons)
store/          app icon 512, Play feature graphic, store screenshots
docs/           LAUNCH_PLAN.md (Almedia), STORE_LISTING.md, EVENTS.md, PRIVACY.md
package.json    Capacitor + SDKs (AppsFlyer, AdMob, RevenueCat)
```

## ⚡ Automatisch über GitHub (empfohlen)
Jeder Push auf `main`:
- **Web-Version** → https://johnqpowers.github.io/merge-cafe/ (einmalig: Settings → Pages → Source: *GitHub Actions*)
- **Test-APK** zum direkten Installieren → Actions → letzter Lauf → Artifacts
- **Signierte .aab** und Upload in Google Play (internal), sobald die Secrets gesetzt sind

Secrets (Settings → Secrets and variables → Actions):

| Secret | Inhalt |
|---|---|
| `ANDROID_KEYSTORE_BASE64` | Keystore als Base64 (`certutil -encode merge-cafe.jks ks.txt`, dann den Inhalt ohne die BEGIN/END-Zeilen) |
| `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD` | Passwörter/Alias des Keystores |
| `PLAY_SERVICE_ACCOUNT_JSON` | JSON des Google-Cloud-Servicekontos mit Play-Console-Zugriff |
| `APPSFLYER_DEV_KEY`, `APPSFLYER_API_TOKEN` | AppsFlyer Dev Key und API-Token (für die täglichen Berichte) |
| `ADMOB_APP_ID_ANDROID`, `ADMOB_REWARDED_ANDROID` | AdMob App-ID und Rewarded-Anzeigenblock |
| `REVENUECAT_ANDROID_KEY` | RevenueCat Public SDK Key (Android) |

Fehlt ein Secret, läuft der jeweilige Schritt mit Test-IDs oder wird übersprungen.
Hinweis: Die **allererste** .aab muss einmal von Hand in der Play Console hochgeladen werden. Danach übernimmt die Pipeline.

## 0. Test locally (Windows CMD)
```cmd
cd merge-cafe
npx http-server www -p 8080 -c-1
```
Open http://localhost:8080 – or just double-click `www\index.html`.

## 1. Android (priority 1)
Prerequisites: Node 20+, Android Studio, Google Play Console account (USD 25 one-time).
```cmd
cd merge-cafe
npm install
npx cap add android
npx capacitor-assets generate --iconBackgroundColor "#C8553D" --splashBackgroundColor "#F6EBDD"
npx cap sync android
npx cap open android
```
In Android Studio: **Build → Generate Signed App Bundle → .aab** → upload to Play Console → *Internal testing* → *Production*.

## 2. iOS (priority 2, after Android KPIs are proven)
Requires a Mac + Xcode + Apple Developer account (USD 99/year).
```cmd
npx cap add ios
npx cap sync ios
npx cap open ios
```
Xcode: **Product → Archive → Distribute App → App Store Connect**.
Add `NSUserTrackingUsageDescription` to `Info.plist` (AppsFlyer/ATT).

## 3. Web portals
```cmd
cd www
tar -a -c -f ..\merge-cafe-web.zip *
```
Upload `merge-cafe-web.zip` to itch.io (Kind: HTML), CrazyGames / Poki / GameDistribution developer portals.
Web builds use demo ads & no purchases automatically; portals usually require their own ad SDK – add it in `Platform.showRewarded()`.

## 4. Before release – replace placeholders
All in `www/index.html` → `CONFIG` and in `capacitor.config.json`:

| What | Where | Source |
|---|---|---|
| AppsFlyer Dev Key, iOS App ID | `CONFIG.appsflyer` | AppsFlyer dashboard |
| AdMob app IDs + rewarded unit IDs | `capacitor.config.json`, `CONFIG.admob` | AdMob (currently Google **test IDs**) |
| RevenueCat API keys | `CONFIG.revenuecat` | RevenueCat dashboard |
| In-app products | `starter_pack`, `gems_small`, `gems_large` | create identically in Play Console / App Store Connect + RevenueCat |
| Privacy policy URL | settings screen (`johnqpowers.github.io/merge-cafe/privacy.html`) | host `docs/PRIVACY.md` |
| App ID `io.github.johnqpowers.mergecafe` | `capacitor.config.json` | your own reverse domain |

## 5. Native plugin notes
- All SDKs are optional at runtime – the game checks `window.Capacitor.Plugins.*` and falls back gracefully.
- Plugin APIs change between major versions. After `npm install`, compare the calls in `Platform` (`index.html`) with each plugin README (AppsFlyer `initSDK/logEvent`, AdMob `prepareRewardVideoAd/showRewardVideoAd`, RevenueCat `configure/getProducts/purchaseStoreProduct`).
- Debug events in any browser console: `MC.events()`.
