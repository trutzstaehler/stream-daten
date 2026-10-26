# Squarespace-Einbau · trutzstaehler.de

Design: Dark Editorial · Hintergrund `#060608` · Nebenfarbe Markengrün `#1d4d3f` · Akzente in Grüntönen: Mint `#6ee7b7`, Hellgrün `#4ade80`, Blassgrün `#a7f3d0` · Text `#f6faf7`, Muted `#9aaba3`.

| Datei | Wohin in Squarespace |
|---|---|
| `01-code-injection-header.html` | Website → Seiten → Benutzerdefinierter Code → Code Injection → **Header** |
| `02-code-injection-footer.html` | dieselbe Stelle → **Footer** |
| `03-startseite-hero-codeblock.html` | Startseite → oberste Sektion → **Code-Block** über die volle Rasterbreite |
| `04-startseite-neuerscheinung-codeblock.html` | Startseite → Sektion unter der Hero → **Code-Block** über die volle Rasterbreite |
| `05-kreativhafen-codeblock.html` | Seite `/kreativhafen` → einzige Sektion → **Code-Block** über die volle Rasterbreite |
| `06-ueber-mich-codeblock.html` | Seite `/ueber-mich` → einzige Sektion → **Code-Block** über die volle Rasterbreite |

Die Datei 01 ist das globale Design-System und wird nur einmal eingefügt. Die Datei 02 enthält Navigation und JavaScript für alle Seiten.
Jede neue Sektion kommt später als eigener Code-Block dazu.

Seiten-URLs in der Navigation (in Datei 02 und 03 anpassen, falls deine anders lauten):
`/ueber-mich`, `/kreativhafen`, `/running`, `/twitch`, `/kontakt`
