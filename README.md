# Health Journal

Persönliche Web-App für Training, Ernährung und Gewicht. Läuft komplett im Browser, funktioniert offline und lässt sich auf dem Handy wie eine App installieren.

## Installieren

- **iPhone (Safari):** Seite öffnen → Teilen → „Zum Home-Bildschirm“
- **Android (Chrome):** Seite öffnen → Menü ⋮ → „App installieren“ bzw. „Zum Startbildschirm hinzufügen“

Danach startet das Journal im Vollbild mit eigenem Symbol – auch ohne Internet.

## Daten

Alle Einträge liegen **nur auf deinem Gerät** (Browser-Speicher). Es gibt keinen Server und kein Konto.

- **Sichern:** Ernährung → Ziele → „Sicherung speichern“ (oder Training → Verlauf). Die Datei z. B. in iCloud/Google Drive ablegen oder per Mail schicken.
- **Wiederherstellen / Gerät wechseln:** „Sicherung einspielen“ → Datei auswählen. Daten werden zusammengeführt, nichts wird überschrieben.

Die App erinnert dich, wenn die letzte Sicherung länger als 7 Tage her ist.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | die komplette App |
| `sw.js` | Offline-Cache (Service Worker) |
| `manifest.webmanifest` | App-Name, Farben, Symbole |
| `*.png` | App-Symbole |

## Weiterentwickeln

`source/journal.html` ist die gemeinsame Quelle (auch für die Version als Claude-Artefakt). `python3 tools/build_webapp.py` erzeugt daraus `index.html`. Nach Änderungen an `index.html` oder den Symbolen die Cache-Version in `sw.js` (`CACHE = 'hj-v…'`) hochzählen.
