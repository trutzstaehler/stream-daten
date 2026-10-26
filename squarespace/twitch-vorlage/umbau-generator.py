import re, sys, os
SRC = '/home/user/stream-daten/squarespace/twitch-vorlage/'
UP = '/root/.claude/uploads/e57bdc23-ff87-521a-aa57-1edd340107b8/'
OUT = '/home/user/stream-daten/squarespace/'

def parts(html):
    """head (links/scripts before the root div), style blocks, script blocks"""
    styles = re.findall(r'<style>.*?</style>', html, re.S)
    scripts = re.findall(r'<script>\n\(function.*?</script>', html, re.S)
    assert len(styles) == 1 and len(scripts) == 1, (len(styles), len(scripts))
    return styles[0], scripts[0]

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Asul:wght@400;700&family=Cinzel:wght@700&display=swap" rel="stylesheet">'''

def header(title, path, extra=''):
    return f'''<!-- =====================================================================
     TRUTZ STÄHLER · TWITCH-BEREICH (WoW Forever) · {title}
     Einfügen in: Seite {path} → einzige Sektion → Code-Block (volle Breite),
     „Quelltext anzeigen“ aus. Navigation, Unternavigation (mit Weg zurück zur
     Homepage) und Footer kommen aus dem globalen Header- und Footer-Code.
     Die Daten kommen wie bisher aus der Stream-Zentrale (CONFIG.dataUrl im Skript).{extra}
     ===================================================================== -->
'''

def hero_meta(left, right):
    return f'''      <div class="tsw-hero__meta">
        <p class="tsw-label" style="margin:0">{left}</p>
        <p class="tsw-label" style="margin:0">{right}</p>
      </div>'''

def title_lines(lines):
    out=[]
    for i,t in enumerate(lines):
        cls = ' class="ts-gradient-text"' if i==len(lines)-1 else ''
        out.append(f'          <span class="ts-line"><span{cls} style="transition-delay:{.1+i*.12:.2f}s">{t}</span></span>')
    return '\n'.join(out)

def sec_head(label, title, note=''):
    n = f'\n        <p class="tsw-sec-note">{note}</p>' if note else ''
    return f'''      <div class="tsw-sec-head">
        <div>
          <p class="tsw-label">{label}</p>
          <h2 class="tsw-sec-title">{title}</h2>
        </div>{n}
      </div>'''

# Gemeinsame Gestaltung: Rahmen eines Widgets auf volle Breite, Paneele im WoW-Glas-Stil
def frame_css(rid, prefix):
    return f'''  #{rid}.tsw {{ width: 100vw; max-width: none; margin: 0 0 0 calc(50% - 50vw); padding: 0; border-radius: 0; background: var(--tsw-bg); font: 400 16px/1.6 Asul, Georgia, serif; }}
  #{rid}.tsw {{ --{prefix}-panel: var(--tsw-panel); --{prefix}-line: rgba(199, 156, 56, 0.22); }}
'''

pages = {}

# ---------------------------------------------------------------- STARTSEITE
html = open(UP+'789744b2-startseite-codeblock.html').read()
style, script = parts(html)
markup = '''<div id="tsz-home" class="th tsw ts-bleed">
  <section class="ts tsw-hero ts-container">
''' + hero_meta('[ 04 — Twitch ]', 'twitch.tv/einfach_trutz') + '''
    <div class="tsw-hero__grid tsw-hero__grid--split">
      <div class="th-hero-txt">
        <p class="tsw-label th-kicker">World of Warcraft Forever · live auf Twitch</p>
        <h1 class="th-h tsw-hero__title" data-ts-fit>Trutz Stahl</h1>
        <p class="th-lead tsw-hero__lead">Gemeinsam mit dem Chat durch Azeroth: Im Stream erstellt jeder seinen eigenen Helden, kämpft gegen Gegner und Bosse aus WoW Forever, lernt Berufe und spielt in den Pausen um Ruf und Beute.</p>
        <div class="th-btns">
          <a class="ts-btn ts-btn--primary ts-magnetic th-twitch" href="https://www.twitch.tv/einfach_trutz" target="_blank" rel="noopener"><span class="ts-btn__inner"><span class="ts-roll"><span data-text="Zum Stream">Zum Stream</span></span><svg class="ts-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg></span></a>
          <a class="ts-btn ts-btn--ghost ts-magnetic" href="/mitspielen"><span class="ts-btn__inner"><span class="ts-roll"><span data-text="Mitspielen">Mitspielen</span></span></span></a>
          <a class="ts-btn ts-btn--ghost ts-magnetic" href="/charakter"><span class="ts-btn__inner"><span class="ts-roll"><span data-text="Charaktere">Charaktere</span></span></span></a>
        </div>
      </div>
      <div class="tsw-hero__aside">
        <div class="th-player"></div>
      </div>
    </div>
  </section>

  <div class="tsw-body ts-container">
    <section class="tsw-sec">
''' + sec_head('[ Das Abenteuer in Zahlen ]', 'Azeroth mit dem Chat') + '''
      <div class="th-totals"></div>
    </section>

    <section class="tsw-sec th-card th-last" hidden>
      <div class="tsw-sec-head th-card-head">
        <div><p class="tsw-label">[ Stream ]</p><h2 class="tsw-sec-title">Letzter Stream</h2></div>
        <a class="tsw-more" href="/statistiken">Alle Statistiken →</a>
      </div>
      <div class="th-stats"></div>
    </section>

    <div class="tsw-sec th-cols">
      <section class="th-card">
        <div class="tsw-sec-head th-card-head">
          <div><p class="tsw-label">[ Beute ]</p><h2 class="tsw-sec-title">Zuletzt erbeutet</h2></div>
          <a class="tsw-more" href="/charakter">Alle Charaktere →</a>
        </div>
        <div class="th-loot"></div>
      </section>
      <section class="th-card">
        <div class="tsw-sec-head th-card-head">
          <div><p class="tsw-label">[ Ruhmeshalle ]</p><h2 class="tsw-sec-title">Die Besten</h2></div>
          <a class="tsw-more" href="/bestenliste">Bestenliste →</a>
        </div>
        <div class="th-best"></div>
      </section>
    </div>

    <section class="tsw-sec th-card">
      <div class="tsw-sec-head th-card-head">
        <div><p class="tsw-label">[ Neue Helden ]</p><h2 class="tsw-sec-title">Neu im Abenteuer</h2></div>
        <a class="tsw-more" href="/mitspielen">Selbst mitmachen →</a>
      </div>
      <div class="th-new"></div>
    </section>
    <p class="th-foot"></p>
  </div>
</div>
'''
override = '''<style>
  /* ---------- Gestaltung im Homepage-Layout (WoW-Forever-Farben) ---------- */
''' + frame_css('tsz-home','th') + '''  #tsz-home .tsw-more { color: var(--tsw-gold); font: 700 12px/1.4 Cinzel, Georgia, serif; letter-spacing: .16em; text-transform: uppercase; text-decoration: none; white-space: nowrap; }
  #tsz-home .tsw-more:hover { text-decoration: none; color: #fff4c4; }
  #tsz-home .th-kicker { margin: 0 0 1.25rem; color: var(--tsw-gold-soft); }
  #tsz-home .th-h { margin: 0; font: 700 clamp(2.6rem, 8vw, 7.4rem)/1 Cinzel, Georgia, serif; color: var(--tsw-gold); }
  #tsz-home .th-lead { margin: 1.5rem 0 0; color: #d9d0bb; }
  #tsz-home .th-btns { gap: .75rem; margin-top: 2rem; }
  #tsz-home .th-btns a:hover { text-decoration: none; }
  #tsz-home .th-btns .ts-btn--primary { color: #1a1206; }
  #tsz-home .th-btns .ts-btn--primary:hover { color: #ffe9a8; }
  #tsz-home .th-btns .ts-btn--ghost { color: var(--tsw-txt); }
  #tsz-home .tsw-sec-title { font: 700 clamp(1.7rem, 3.6vw, 3rem)/1.05 Cinzel, Georgia, serif; }
  #tsz-home .th-player { border: 0; border-radius: 22px; box-shadow: 0 0 0 1px rgba(199, 156, 56, .45), 0 40px 90px -40px rgba(0, 0, 0, .9), 0 0 80px -30px rgba(255, 209, 0, .35); }

  /* Zahlen wie auf der Homepage: Raster mit feinen Linien */
  #tsz-home .th-totals { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0; margin: 0; border-top: 1px solid var(--tsw-line); border-left: 1px solid var(--tsw-line); }
  #tsz-home .th-total { padding: 1.5rem 1.25rem 1.6rem; border: 0; border-right: 1px solid var(--tsw-line); border-bottom: 1px solid var(--tsw-line); border-radius: 0; background: transparent; transition: background-color .4s; }
  #tsz-home .th-total:hover { background: rgba(255, 209, 0, .04); }
  #tsz-home .th-total b { font-size: clamp(1.9rem, 4vw, 3.4rem); line-height: 1.05; }
  #tsz-home .th-total span { display: block; margin-top: .5rem; font-family: Cinzel, Georgia, serif; font-size: 11px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; }

  /* Karten */
  #tsz-home .th-card { margin-bottom: 0; padding: 0; border: 0; background: none; }
  #tsz-home .th-card-head { margin-bottom: clamp(1.25rem, 2.5vw, 1.75rem); }
  #tsz-home .th-card-head h2 { font: 700 clamp(1.7rem, 3.6vw, 3rem)/1.05 Cinzel, Georgia, serif; }
  #tsz-home .th-loot, #tsz-home .th-best, #tsz-home .th-new, #tsz-home .th-stats { padding: 1.25rem 1.5rem; border: 1px solid var(--tsw-line); border-radius: 22px; background: var(--tsw-panel); }
  #tsz-home .th-stats { gap: 0; padding: 0; overflow: hidden; }
  #tsz-home .th-stat { padding: 1.25rem 1.5rem; border-right: 1px solid var(--tsw-line); }
  #tsz-home .th-stat b { font-size: clamp(1.25rem, 2vw, 1.6rem); }
  #tsz-home .th-cols { display: grid; grid-template-columns: minmax(0, 1fr); gap: clamp(3rem, 6vw, 4rem); }
  #tsz-home .th-row { padding: .7rem 0; border-top-color: rgba(199, 156, 56, .12); }
  #tsz-home .th-best h3 { margin: 1.25rem 0 .25rem; font: 700 11px/1.5 Cinzel, Georgia, serif; letter-spacing: .2em; text-transform: uppercase; color: var(--tsw-muted); }
  #tsz-home .th-best h3:first-child { margin-top: 0; }
  #tsz-home .th-ic, #tsz-home .th-pic { width: 40px; height: 40px; }
  #tsz-home .th-new { gap: 0 2rem; }
  #tsz-home .th-foot { margin-top: 2rem; }

  @media (min-width: 768px) { #tsz-home .th-totals { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
  @media (min-width: 1024px) { #tsz-home .th-cols { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); } }
  @media (max-width: 820px) { #tsz-home .th-hero { grid-template-columns: 1fr; } }
</style>
'''
head_scripts = '''<script>window.whTooltips = { colorLinks: false, iconizeLinks: false, renameLinks: false }; // Tooltips aus dem Spiel – die Symbole zeichnet der Block selbst</script>
<script src="https://wow.zamimg.com/js/tooltips.js"></script>
'''
pages['12-twitch-startseite-codeblock.html'] = header('STARTSEITE', '/twitch-startseite') + FONTS + '\n' + head_scripts + '\n' + markup + '\n' + style + '\n' + override + '\n' + script + '\n'

# ---------------------------------------------------------------- LIVE & STREAM-PLAN
html = open(UP+'97f3646a-streamplan-codeblock.html').read()
style, script = parts(html)
markup = '''<div id="tsz-plan" class="tl tsw ts-bleed">
  <section class="ts tsw-hero ts-container">
''' + hero_meta('[ Twitch · Live ]', 'Deutsche Zeit · Countdown in deiner Uhrzeit') + '''
    <div class="tsw-hero__grid tsw-hero__grid--split">
      <div>
        <h1 class="tsw-hero__title" data-ts-fit>
''' + title_lines(['Live &amp;', 'Stream-Plan.']) + '''
        </h1>
        <p class="tl-lead tsw-hero__lead"></p>
      </div>
      <div class="tsw-hero__aside"><div class="tl-next"></div></div>
    </div>
  </section>

  <div class="tsw-body ts-container">
    <section class="tsw-sec">
''' + sec_head('[ Jetzt im Stream ]', 'Stream &amp; Chat') + '''
      <div class="tl-live">
        <div class="tl-player"></div>
        <div class="tl-chat"></div>
      </div>
    </section>
    <section class="tsw-sec">
''' + sec_head('[ Wochenplan ]', 'Wann ich live bin', 'Folgen lohnt sich – dann meldet Twitch jeden Stream.') + '''
      <div class="tl-week"></div>
      <p class="tl-foot"></p>
    </section>
  </div>
</div>
'''
override = '''<style>
  /* ---------- Gestaltung im Homepage-Layout (WoW-Forever-Farben) ---------- */
''' + frame_css('tsz-plan','tl') + '''  #tsz-plan .tl-lead { margin-top: 1.5rem; }
  #tsz-plan .tl-next { display: inline-block; min-width: min(100%, 340px); padding: 1.5rem 1.75rem; border-radius: 22px; text-align: left; border-color: rgba(199, 156, 56, .55); background: radial-gradient(120% 140% at 0% 0%, rgba(255, 209, 0, .14), rgba(12, 9, 7, .7) 60%); box-shadow: 0 30px 70px -40px rgba(0, 0, 0, .9); }
  #tsz-plan .tl-next b { font-size: clamp(1.6rem, 3vw, 2.4rem); }
  #tsz-plan .tl-next span { display: block; margin-top: .4rem; }
  #tsz-plan .tl-live { grid-template-columns: minmax(0, 1fr) 360px; gap: 1rem; margin: 0; }
  #tsz-plan .tl-player { border-radius: 22px; box-shadow: 0 0 0 1px rgba(199, 156, 56, .45), 0 40px 90px -40px rgba(0, 0, 0, .9); }
  #tsz-plan .tl-chat { border-radius: 22px; box-shadow: 0 0 0 1px var(--tsw-line); }
  #tsz-plan .tl-week { gap: .75rem; }
  #tsz-plan .tl-day { min-height: 150px; padding: 1rem; border-radius: 18px; border-color: var(--tsw-line); }
  #tsz-plan .tl-day-h { font: 700 11px/1.5 Cinzel, Georgia, serif; letter-spacing: .18em; text-transform: uppercase; margin-bottom: .75rem; }
  #tsz-plan .tl-slot { border-radius: 10px; }
  #tsz-plan .tl-empty { padding: 1.5rem 1.75rem; border-radius: 22px; }
  #tsz-plan .tl-foot { margin-top: 1.5rem; }
  @media (max-width: 1100px) { #tsz-plan .tl-live { grid-template-columns: minmax(0, 1fr); } #tsz-plan .tl-chat { min-height: 420px; } }
  @media (max-width: 640px) { #tsz-plan .tl-next { width: 100%; } }
</style>
'''
pages['13-live-codeblock.html'] = header('LIVE & STREAM-PLAN', '/live', '\n     Den Wochenplan trägst du wie bisher im Skript bei CONFIG.schedule ein.') + FONTS + '\n\n' + markup + '\n' + style + '\n' + override + '\n' + script + '\n'

# ---------------------------------------------------------------- MITSPIELEN
html = open(UP+'f5650036-mitspielen-codeblock.html').read()
style, script = parts(html)
markup = '''<div id="tsz-play" class="tp tsw ts-bleed">
  <section class="ts tsw-hero ts-container">
''' + hero_meta('[ Twitch · Mitspielen ]', 'Alles läuft über den Twitch-Chat') + '''
    <div class="tsw-hero__grid">
      <div>
        <h1 class="tsw-hero__title" data-ts-fit>
''' + title_lines(['Mitspielen.']) + '''
        </h1>
        <p class="tp-lead tsw-hero__lead">Im Stream spielt der Chat mit: Jeder kann einen eigenen Helden aus WoW Forever erstellen, mit ihm kämpfen, Berufe lernen und in den Pausen um Ruf und Beute spielen. Alles läuft über den Twitch-Chat – hier steht, wie.</p>
      </div>
    </div>
  </section>

  <div class="tsw-body ts-container">
    <section class="tsw-sec">
''' + sec_head('[ Schritt für Schritt ]', 'So spielst du mit') + '''
      <ol class="tp-steps"></ol>
    </section>

    <section class="tsw-sec">
      <div class="tsw-sec-head">
        <div><p class="tsw-label">[ Chat-Befehle ]</p><h2 class="tsw-sec-title">Alle Befehle</h2></div>
        <input class="tp-search" type="search" placeholder="Befehl suchen …" aria-label="Befehl suchen">
      </div>
      <div class="tp-card">
        <div class="tp-cmds"></div>
        <p class="tp-note tp-cmd-note"></p>
      </div>
    </section>

    <section class="tsw-sec">
''' + sec_head('[ Azeroth ]', 'Völker, Klassen &amp; Ruf') + '''
      <div class="tp-grid">
        <div class="tp-card">
          <h3>Völker &amp; Klassen in WoW Forever</h3>
          <div class="tp-races"></div>
          <p class="tp-note">Himmelsgeborene gibt es auf beiden Seiten: <code>!charakter Horde Himmelsgeborene Druide</code>. Für eine Heldin ein <code>w</code> dazuschreiben.</p>
        </div>
        <div class="tp-card">
          <h3 class="tp-rep-h">Ruf bei der Stahlgarde</h3>
          <div class="tp-ladder"></div>
          <p class="tp-note">Ruf gibt es fürs Zuschauen, Schreiben, Kämpfe und die Pausen-Spiele – nie für Spam: eine Nachricht zählt höchstens einmal pro Minute.</p>
        </div>
      </div>
    </section>

    <section class="tsw-sec tp-card tp-pace">
      <p class="tsw-label">[ Die lange Reise ]</p>
      <h3>Wie lange dauert das?</h3>
      <p>Alles ist auf eine lange Reise ausgelegt – wie in WoW Forever selbst. Bei rund zehn Stream-Stunden pro Woche braucht selbst jemand, der jeden Stream mitmacht, etwa <b>ein Jahr</b> bis Stufe 60, bis Ehrfürchtig und bis ein Beruf auf 300 steht. Die Erfahrungstabelle ist dieselbe wie im Spiel. Wer seltener dabei ist, kommt langsamer voran – verloren geht nichts.</p>
    </section>
  </div>
</div>
'''
override = '''<style>
  /* ---------- Gestaltung im Homepage-Layout (WoW-Forever-Farben) ---------- */
''' + frame_css('tsz-play','tp') + '''  #tsz-play .tp-lead { margin: 1.5rem 0 0; max-width: 40rem; color: #d9d0bb; }
  #tsz-play .tp-steps { grid-template-columns: repeat(auto-fill, minmax(min(100%, 340px), 1fr)); gap: 1rem; margin: 0; }
  #tsz-play .tp-step { gap: 1rem; padding: 1.5rem; border-radius: 22px; border-color: var(--tsw-line); transition: transform .6s cubic-bezier(.16,1,.3,1), border-color .4s; }
  #tsz-play .tp-step:hover { transform: translateY(-4px); border-color: rgba(199, 156, 56, .45); }
  #tsz-play .tp-step img { width: 48px; height: 48px; border-radius: 10px; }
  #tsz-play .tp-step h4 { font: 700 19px/1.3 Cinzel, Georgia, serif; margin-bottom: .5rem; }
  #tsz-play .tp-step h4::before { content: counter(tp, decimal-leading-zero) "  "; color: var(--tsw-brass); }
  #tsz-play .tp-card { margin-bottom: 0; padding: 1.5rem 1.75rem; border-radius: 22px; border-color: var(--tsw-line); }
  #tsz-play .tp-card h3 { font-size: clamp(1.3rem, 2.2vw, 1.7rem); margin-bottom: 1rem; }
  #tsz-play .tp-search { width: 320px; padding: 12px 18px; border-radius: 999px; border-color: rgba(199, 156, 56, .45); background: rgba(12, 9, 7, .7); font-size: 16px; }
  #tsz-play .tp-group { margin: 1.5rem 0 .5rem; font: 700 11px/1.5 Cinzel, Georgia, serif; letter-spacing: .2em; text-transform: uppercase; }
  #tsz-play td { padding: .7rem .75rem; border-top-color: rgba(199, 156, 56, .12); }
  #tsz-play .tp-grid { gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 380px), 1fr)); }
  #tsz-play .tp-pace { padding: clamp(1.75rem, 4vw, 3rem); background: radial-gradient(120% 140% at 0% 0%, rgba(255, 209, 0, .12), rgba(12, 9, 7, .7) 60%); border-color: rgba(199, 156, 56, .4); }
  #tsz-play .tp-pace h3 { font-size: clamp(1.7rem, 3.6vw, 3rem); }
  #tsz-play .tp-pace p:last-child { max-width: 52rem; font-size: 17px; line-height: 1.75; }
</style>
'''
pages['14-mitspielen-codeblock.html'] = header('MITSPIELEN', '/mitspielen') + FONTS + '\n\n' + markup + '\n' + style + '\n' + override + '\n' + script + '\n'

# ---------------------------------------------------------------- CHARAKTER
html = open(SRC+'charaktere-codeblock.html').read()
style, script = parts(html)
markup = '''<div id="tsz-chars" class="tc tsw ts-bleed">
  <section class="ts tsw-hero ts-container">
''' + hero_meta('[ Twitch · Charakter ]', 'Helden aus dem Chat') + '''
    <div class="tsw-hero__grid tsw-hero__grid--split">
      <div>
        <h1 class="tsw-hero__title" data-ts-fit>
''' + title_lines(['Charaktere', 'aus dem Chat.']) + '''
        </h1>
        <p class="tc-lead tsw-hero__lead">Im Stream mit <b>!charakter</b> einen Helden erstellen – hier findest du ihn mit seinem vollständigen Namen.</p>
      </div>
      <div class="tsw-hero__aside">
        <label class="tsw-label" for="tc-search-input">Charakter suchen</label>
        <input id="tc-search-input" class="tc-search" type="search" placeholder="Vollständiger Name …" aria-label="Charakter mit vollständigem Namen suchen" autocomplete="off" spellcheck="false">
      </div>
    </div>
  </section>

  <div class="tsw-body ts-container">
    <div class="tc-sheet" hidden></div>
    <div class="tc-list"></div>
    <p class="tc-foot"></p>
  </div>
</div>
'''
override = '''<style>
  /* ---------- Gestaltung im Homepage-Layout (WoW-Forever-Farben) ---------- */
''' + frame_css('tsz-chars','tc') + '''  #tsz-chars .tc-lead { margin: 1.5rem 0 0; color: #d9d0bb; }
  #tsz-chars .tsw-hero__aside .tsw-label { display: block; }
  #tsz-chars .tc-search { width: 100%; padding: 16px 22px; border-radius: 999px; border-color: rgba(199, 156, 56, .55); background: rgba(12, 9, 7, .75); font-size: 18px; box-shadow: inset 0 0 10px #000, 0 20px 50px -30px rgba(0, 0, 0, .9); }
  #tsz-chars .tc-search:focus { border-color: #ffd100; box-shadow: inset 0 0 10px #000, 0 0 0 4px rgba(255, 209, 0, .12); }
  #tsz-chars .tc-sheet { margin-bottom: clamp(3rem, 6vw, 4.5rem); }
  #tsz-chars .tc-box { border-radius: 14px; }
  #tsz-chars .tc-title { border-radius: 12px 12px 0 0; }
  #tsz-chars .tc-list { grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 1rem; }
  #tsz-chars .tc-card { padding: 1rem 1.25rem; border-radius: 18px; border-color: var(--tsw-line); transition: transform .6s cubic-bezier(.16,1,.3,1), border-color .4s; }
  #tsz-chars .tc-card:hover { transform: translateY(-4px); border-color: rgba(199, 156, 56, .5); }
  #tsz-chars .tc-empty { padding: clamp(2rem, 5vw, 3.5rem); border: 1px dashed var(--tsw-line-strong); border-radius: 22px; font-size: 17px; }
  #tsz-chars .tc-foot { margin-top: 1.5rem; }
</style>
'''
pages['15-charakter-codeblock.html'] = header('CHARAKTER', '/charakter', '\n     Ein Charakter öffnet sich direkt über /charakter#login (Links aus Chat, Bestenliste, Startseite).') + FONTS + '\n\n' + markup + '\n' + style + '\n' + override + '\n' + script + '\n'

# ---------------------------------------------------------------- BESTENLISTE
html = open(UP+'1c04b60e-bestenliste-codeblock.html').read()
style, script = parts(html)
markup = '''<div id="tsz-board" class="tb tsw ts-bleed">
  <section class="ts tsw-hero ts-container">
''' + hero_meta('[ Twitch · Bestenliste ]', 'Die stärksten Helden aus dem Chat') + '''
    <div class="tsw-hero__grid tsw-hero__grid--split">
      <div>
        <h1 class="tsw-hero__title" data-ts-fit>
''' + title_lines(['Bestenliste.']) + '''
        </h1>
        <p class="tb-lead tsw-hero__lead">Die stärksten Helden aus dem Chat – wer mitmacht, steigt auf.</p>
      </div>
      <div class="tsw-hero__aside">
        <p class="tsw-label">Seite wählen</p>
        <div class="tb-side" role="group" aria-label="Seite">
          <button type="button" data-side="" class="on">Alle</button>
          <button type="button" data-side="allianz">Allianz</button>
          <button type="button" data-side="horde">Horde</button>
        </div>
      </div>
    </div>
  </section>

  <div class="tsw-body ts-container">
    <section class="tsw-sec">
      <div class="tb-totals"></div>
    </section>
    <section class="tsw-sec">
''' + sec_head('[ Ranglisten ]', 'Wer führt?') + '''
      <div class="tb-tabs" role="tablist"></div>
      <div class="tb-body"></div>
      <p class="tb-foot"></p>
    </section>
  </div>
</div>
'''
override = '''<style>
  /* ---------- Gestaltung im Homepage-Layout (WoW-Forever-Farben) ---------- */
''' + frame_css('tsz-board','tb') + '''  #tsz-board .tb-lead { margin: 1.5rem 0 0; color: #d9d0bb; }
  #tsz-board .tb-side { display: inline-flex; border-radius: 999px; border-color: rgba(199, 156, 56, .55); }
  #tsz-board .tb-side button { padding: 10px 20px; font-family: Cinzel, Georgia, serif; letter-spacing: .06em; }
  #tsz-board .tb-totals { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0; margin: 0; border-top: 1px solid var(--tsw-line); border-left: 1px solid var(--tsw-line); }
  #tsz-board .tb-total { padding: 1.5rem 1.25rem 1.6rem; border: 0; border-right: 1px solid var(--tsw-line); border-bottom: 1px solid var(--tsw-line); border-radius: 0; background: transparent; }
  #tsz-board .tb-total b { font-size: clamp(1.9rem, 4vw, 3.4rem); line-height: 1.05; }
  #tsz-board .tb-total span { display: block; margin-top: .5rem; font-family: Cinzel, Georgia, serif; font-size: 11px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; }
  #tsz-board .tb-tabs { gap: .5rem; margin-bottom: 1.5rem; }
  #tsz-board .tb-tab { padding: 7px 16px 7px 7px; border-radius: 999px; border-color: var(--tsw-line); }
  #tsz-board .tb-tab img { border-radius: 50%; }
  #tsz-board .tb-list { border-radius: 22px; border-color: var(--tsw-line); }
  #tsz-board .tb-row { gap: 1rem; padding: .9rem 1.5rem; border-top-color: rgba(199, 156, 56, .12); transition: background-color .3s; }
  #tsz-board .tb-place { font-size: 22px; }
  #tsz-board .tb-pic { width: 44px; height: 44px; }
  #tsz-board .tb-profs { gap: 1rem; }
  #tsz-board .tb-prof { padding: 1.25rem; border-radius: 18px; border-color: var(--tsw-line); }
  #tsz-board .tb-empty { padding: clamp(2rem, 5vw, 3.5rem); border: 1px dashed var(--tsw-line-strong); border-radius: 22px; }
  #tsz-board .tb-foot { margin-top: 1.5rem; }
  @media (min-width: 768px) { #tsz-board .tb-totals { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
  @media (max-width: 640px) { #tsz-board .tb-row { grid-template-columns: 30px 36px 1fr auto; gap: 8px; padding: .8rem 1rem; } #tsz-board .tb-pic { width: 36px; height: 36px; } }
</style>
'''
pages['16-bestenliste-codeblock.html'] = header('BESTENLISTE', '/bestenliste') + FONTS + '\n\n' + markup + '\n' + style + '\n' + override + '\n' + script + '\n'

# ---------------------------------------------------------------- STATISTIKEN (Klassen ts- → tst-, damit nichts mit dem Design-System kollidiert)
html = open(UP+'05d185c1-statistiken-codeblock.html').read()
style, script = parts(html)
def ren(s):
    s = re.sub(r'--ts-', '--tst-', s)
    s = re.sub(r'(?<![\w-])ts-(?=[a-z0-9])', 'tst-', s)
    return s
style, script = ren(style), ren(script)
markup = '''<div id="tsz-stats" class="tst tsw ts-bleed">
  <section class="ts tsw-hero ts-container">
''' + hero_meta('[ Twitch · Statistiken ]', 'Zahlen aus der Stream-Zentrale') + '''
    <div class="tsw-hero__grid tsw-hero__grid--split">
      <div>
        <h1 class="tsw-hero__title" data-ts-fit>
''' + title_lines(['Statistiken.']) + '''
        </h1>
        <p class="tst-lead tsw-hero__lead">Im Stream passieren die Dinge – hier steht, was dabei herausgekommen ist.</p>
      </div>
      <div class="tsw-hero__aside"><div class="tst-state"></div></div>
    </div>
  </section>

  <div class="tsw-body ts-container">
    <div class="tst-tabs" role="tablist" aria-label="Bereiche"></div>
    <div class="tst-body" role="tabpanel"></div>
    <p class="tst-foot"></p>
  </div>
</div>
'''
override = '''<style>
  /* ---------- Gestaltung im Homepage-Layout (WoW-Forever-Farben) ---------- */
''' + frame_css('tsz-stats','tst') + '''  #tsz-stats .tst-lead { margin: 1.5rem 0 0; color: #d9d0bb; }
  #tsz-stats .tst-state { display: inline-block; padding: 1rem 1.5rem; border-radius: 999px; border-color: rgba(199, 156, 56, .45); font-size: 16px; }
  #tsz-stats .tst-tabs { gap: .5rem; margin-bottom: clamp(2rem, 4vw, 3rem); padding-bottom: 1.5rem; border-bottom: 1px solid var(--tsw-line); }
  #tsz-stats .tst-tab { padding: 8px 18px 8px 8px; border-radius: 999px; border-color: var(--tsw-line); }
  #tsz-stats .tst-tab img { border-radius: 50%; }
  #tsz-stats .tst-sec { margin-top: clamp(2.5rem, 5vw, 4rem); }
  #tsz-stats .tst-sec-h { font-size: clamp(1.3rem, 2.4vw, 1.9rem); padding-bottom: .75rem; margin-bottom: 1.25rem; border-bottom: 1px solid var(--tsw-line); }
  #tsz-stats .tst-cols, #tsz-stats .tst-cols3 { gap: 1.5rem; }
  #tsz-stats .tst-gap { height: 1.5rem; }
  #tsz-stats .tst-tiles { gap: 0; border-top: 1px solid var(--tsw-line); border-left: 1px solid var(--tsw-line); }
  #tsz-stats .tst-tile { padding: 1.4rem 1.25rem 1.5rem; border: 0; border-right: 1px solid var(--tsw-line); border-bottom: 1px solid var(--tsw-line); border-radius: 0; background: transparent; }
  #tsz-stats .tst-tile b { font-size: clamp(1.6rem, 3vw, 2.6rem); line-height: 1.1; }
  #tsz-stats .tst-tile span { margin-top: .35rem; font-family: Cinzel, Georgia, serif; font-size: 11px; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }
  #tsz-stats .tst-box { border-radius: 20px; border-color: var(--tsw-line); }
  #tsz-stats .tst-row { padding: .8rem 1.25rem; border-top-color: rgba(199, 156, 56, .12); }
  #tsz-stats .tst-label { font-family: Cinzel, Georgia, serif; font-size: 11px; letter-spacing: .18em; text-transform: uppercase; }
  #tsz-stats .tst-foot { margin-top: 2rem; }
  @media (max-width: 640px) { #tsz-stats .tst-tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
</style>
'''
pages['17-statistiken-codeblock.html'] = header('STATISTIKEN', '/statistiken', '\n     Direkt zu einem Reiter: /statistiken#stream, #kanal, #spiele, #bosse, #gluecksrad') + FONTS + '\n\n' + markup + '\n' + style + '\n' + override + '\n' + script + '\n'

for name, content in pages.items():
    open(OUT+name, 'w').write(content)
    print(name, len(content))
