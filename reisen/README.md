# Reisen

Daten für das Reisetagebuch auf trutzstaehler.de (Code-Block „Reisetagebuch“).

- `australien-2026/reise.json` – wird vom Website-Modul geladen
- `australien-2026/reise-config.json` – Titel, Daten (start/end), Reisende, geplante Route (`plan`) – von Hand pflegbar
- `australien-2026/img/` – verkleinerte Fotos ohne GPS-Daten
- `australien-2026/feed.xml` – RSS für E-Mail-Benachrichtigungen

Aktualisieren aus einem Polarsteps-Export (ZIP von polarsteps.com → Kontoeinstellungen → „Download my data“):

    python3 reisen/werkzeug/polarsteps-import.py export.zip --ziel reisen/australien-2026 --autor Insa

In Polarsteps-Texten: `#koala`, `#kaenguru` … haken das Tier-Bingo ab, `#privat` hält einen Step von der Website fern.
Die Route wird nur innerhalb Australiens übernommen (Wohnort bleibt privat).
