OUT='/home/user/stream-daten/squarespace/'
DS = '<a href="/datenschutz" data-ts-native="Datenschutz">Datenschutzerklärung</a>'

LEGAL_CSS = r'''<style>
  .ts-legal { position: relative; isolation: isolate; overflow: hidden; overflow: clip; background: var(--ts-bg); }
  .ts-legal__orb { position: absolute; z-index: -1; right: -12%; top: -8%; width: 50vw; height: 50vw; max-width: 760px; max-height: 760px; border-radius: 50%; filter: blur(110px); background: radial-gradient(circle, rgba(46, 140, 108, .26), transparent 66%); pointer-events: none; }
  .ts-legal__intro { padding-top: clamp(8.5rem, 14vw, 12rem); padding-bottom: clamp(3rem, 6vw, 5rem); }
  .ts-legal__meta { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--ts-line); }
  .ts-legal .ts-line { padding-bottom: .16em; margin-bottom: -.16em; }
  .ts .ts-legal__title { margin-top: clamp(2.5rem, 5vw, 4rem); font-family: var(--ts-font-display); font-weight: 800; font-size: clamp(2.2rem, 7.4vw, 7rem); line-height: .95; letter-spacing: -0.03em; }
  .ts .ts-legal__lead { margin-top: 1.5rem; max-width: 40rem; font-size: clamp(17px, 1.5vw, 19px); line-height: 1.7; color: var(--ts-muted); }

  .ts-legal__grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 3rem; padding-bottom: clamp(6rem, 11vw, 10rem); }
  .ts-legal__toc { display: none; }
  .ts .ts-legal__toc ol { list-style: none; counter-reset: toc; }
  .ts .ts-legal__toc li { counter-increment: toc; }
  .ts .ts-legal__toc a { display: flex; gap: .75rem; padding: .55rem 0; border-bottom: 1px solid var(--ts-line); color: var(--ts-muted); font-size: 14px; line-height: 1.4; transition: color .3s; }
  .ts .ts-legal__toc a::before { content: counter(toc, decimal-leading-zero); font-family: var(--ts-font-mono); font-size: 11px; letter-spacing: .1em; color: var(--ts-mint); padding-top: .15em; }
  .ts .ts-legal__toc a:hover, .ts .ts-legal__toc a.is-active { color: var(--ts-text); }

  .ts-legal__body { max-width: 50rem; }
  .ts-legal-sec { padding: clamp(2rem, 4vw, 2.75rem) 0; border-top: 1px solid var(--ts-line); scroll-margin-top: 110px; }
  .ts-legal-sec:first-child { border-top: 0; padding-top: 0; }
  .ts .ts-legal-sec h2 { display: flex; align-items: baseline; gap: 1rem; font-family: var(--ts-font-display); font-weight: 700; font-size: clamp(1.4rem, 2.4vw, 2rem); line-height: 1.15; letter-spacing: -0.02em; }
  .ts .ts-legal-sec h2 span { flex: none; font-family: var(--ts-font-mono); font-size: 12px; letter-spacing: .14em; color: var(--ts-mint); font-weight: 400; }
  .ts .ts-legal-sec h3 { margin-top: 1.5rem; font-family: var(--ts-font-display); font-weight: 700; font-size: 18px; letter-spacing: -0.01em; }
  .ts .ts-legal-sec p, .ts .ts-legal-sec li { font-size: 16px; line-height: 1.75; color: var(--ts-muted); }
  .ts .ts-legal-sec p { margin-top: 1rem; }
  .ts .ts-legal-sec ul { margin-top: 1rem; display: grid; gap: .4rem; }
  .ts .ts-legal-sec li { position: relative; padding-left: 1.25rem; }
  .ts .ts-legal-sec li::before { content: ""; position: absolute; left: 0; top: .75em; width: 6px; height: 6px; border-radius: 50%; background: var(--ts-mint); }
  .ts .ts-legal-sec strong { color: var(--ts-text); font-weight: 500; }
  .ts .ts-legal-sec a { color: var(--ts-mint); border-bottom: 1px solid rgba(110, 231, 183, .35); transition: border-color .3s; }
  .ts .ts-legal-sec a:hover { border-color: var(--ts-mint); }
  .ts .ts-legal-card { margin-top: 1.25rem; padding: 1.5rem 1.75rem; border-radius: 20px; font-size: 17px; line-height: 1.75; color: var(--ts-text); }
  .ts .ts-legal-card p { margin-top: 0; color: var(--ts-text); }
  .ts .ts-legal-card p + p { margin-top: .75rem; }

  @media (min-width: 1024px) {
    .ts-legal__grid { grid-template-columns: minmax(0, 3fr) minmax(0, 8fr); column-gap: clamp(3rem, 6vw, 6rem); }
    .ts-legal__toc { display: block; position: sticky; top: 120px; align-self: start; }
  }
</style>
'''

LEGAL_JS = r'''<script>
(() => {
  /* Inhaltsverzeichnis: aktiven Abschnitt markieren */
  const links = [...document.querySelectorAll('.ts-legal__toc a')];
  if (!links.length || !('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      links.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id));
    });
  }, { rootMargin: '-30% 0px -60% 0px' });
  document.querySelectorAll('.ts-legal-sec[id]').forEach(s => io.observe(s));
})();
</script>
'''

def legal_page(comment, label, right, title_lines, lead, secs):
    lines = '\n'.join(f'      <span class="ts-line"><span{" class=\"ts-gradient-text\"" if i==len(title_lines)-1 else ""} style="transition-delay:{.1+i*.12:.2f}s">{t}</span></span>' for i,t in enumerate(title_lines))
    toc = '\n'.join(f'        <li><a href="#{sid}">{t}</a></li>' for sid,t,_ in secs)
    body = '\n'.join(f'''      <section class="ts-legal-sec ts-reveal" id="{sid}" aria-labelledby="{sid}-h">
        <h2 id="{sid}-h"><span>{i+1:02d}</span>{t}</h2>
{html}
      </section>''' for i,(sid,t,html) in enumerate(secs))
    return f'''{comment}{LEGAL_CSS}
<div class="ts ts-legal ts-bleed">
  <div class="ts-legal__orb" aria-hidden="true"></div>
  <section class="ts-container ts-legal__intro" aria-labelledby="ts-legal-title">
    <div class="ts-legal__meta ts-reveal">
      <p class="ts-label ts-muted">{label}</p>
      <p class="ts-label ts-muted">{right}</p>
    </div>
    <h1 id="ts-legal-title" class="ts-legal__title" data-ts-fit>
{lines}
    </h1>
    <p class="ts-legal__lead ts-reveal">{lead}</p>
  </section>
  <div class="ts-container ts-legal__grid">
    <nav class="ts-legal__toc" aria-label="Inhalt">
      <p class="ts-label ts-muted" style="margin-bottom:1rem">Inhalt</p>
      <ol>
{toc}
      </ol>
    </nav>
    <div class="ts-legal__body">
{body}
    </div>
  </div>
</div>
{LEGAL_JS}'''

ADDR = '<p>Trutz Stähler<br>Vizelinstraße 45<br>22529 Hamburg<br>Deutschland</p>'
MAIL = '<a href="mailto:moin@trutzstaehler.de">moin@trutzstaehler.de</a>'

# ------------------------------------------------------------------ IMPRESSUM
impressum = legal_page('''<!-- ==================================================================
     TRUTZ STÄHLER · SEITE „IMPRESSUM“
     Einfügen in: Seite /impressum → einzige Sektion → Code-Block (volle Breite)
     Alle anderen Blöcke dieser Seite können gelöscht werden.
=================================================================== -->
''', '[ Rechtliches ]', 'Stand: Oktober 2026', ['Impressum.'],
 'Wer hinter trutzstaehler.de steht – und wie du mich erreichst.',
 [
  ('anbieter','Angaben gemäß § 5 DDG', f'''        <div class="ts-legal-card ts-glass">
          {ADDR}
        </div>'''),
  ('kontakt','Kontakt', f'''        <p>E-Mail: {MAIL}</p>'''),
  ('verantwortlich','Verantwortlich für den Inhalt', f'''        <p>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV:</p>
        {ADDR}'''),
  ('bilder','Bildnachweise', '''        <ul>
          <li>Fotos vom Hella Half Marathon 2025, gekennzeichnet mit „by Pascal Lieleg“: © Pascal Lieleg</li>
          <li>Alle übrigen Fotos und Texte: © Trutz Stähler</li>
          <li>Buchcover: © Trutz Stähler, Darstellung über Amazon</li>
          <li>Symbole aus World of Warcraft im Twitch-Bereich: © Blizzard Entertainment, eingebunden über Wowhead</li>
        </ul>'''),
  ('fanprojekt','Hinweis zum Twitch-Bereich', '''        <p>World of Warcraft ist eine Marke von Blizzard Entertainment, Inc. Der Twitch-Bereich dieser Website ist ein Fan-Projekt und steht in keiner Verbindung zu Blizzard Entertainment.</p>'''),
  ('haftung','Haftung für Inhalte und Links', '''        <p>Die Inhalte dieser Seiten wurden mit Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität kann ich jedoch keine Gewähr übernehmen. Als Diensteanbieter bin ich nach den allgemeinen Gesetzen für eigene Inhalte verantwortlich.</p>
        <p>Diese Website enthält Links zu externen Websites Dritter, zum Beispiel Amazon, Twitch, Instagram und LinkedIn. Auf deren Inhalte habe ich keinen Einfluss; verantwortlich ist stets der jeweilige Anbieter. Werden mir Rechtsverletzungen bekannt, entferne ich entsprechende Links umgehend.</p>'''),
  ('urheberrecht','Urheberrecht', '''        <p>Die Texte, Fotos und Bücher auf dieser Website unterliegen dem deutschen Urheberrecht. Vervielfältigung, Bearbeitung und Verbreitung außerhalb der Grenzen des Urheberrechts bedürfen meiner schriftlichen Zustimmung bzw. der des jeweiligen Urhebers.</p>'''),
 ])
open(OUT+'19-impressum-codeblock.html','w').write(impressum)

# ------------------------------------------------------------------ DATENSCHUTZ
datenschutz = legal_page('''<!-- ==================================================================
     TRUTZ STÄHLER · SEITE „DATENSCHUTZERKLÄRUNG“
     Einfügen in: Seite Datenschutzerklärung → einzige Sektion → Code-Block (volle Breite)
     Bitte prüfen: Abschnitt 04 (Cookies & Statistik) muss zu deinen Squarespace-Einstellungen passen.
=================================================================== -->
''', '[ Rechtliches ]', 'Stand: Oktober 2026', ['Datenschutz.'],
 'Der Schutz deiner persönlichen Daten ist mir ein besonderes Anliegen. Hier steht, welche Daten beim Besuch dieser Website verarbeitet werden – und welche Rechte du hast.',
 [
  ('verantwortlicher','Verantwortlicher', f'''        <p>Verantwortlich für die Datenverarbeitung auf dieser Website ist:</p>
        <div class="ts-legal-card ts-glass">
          {ADDR}
          <p>E-Mail: {MAIL}</p>
        </div>'''),
  ('allgemein','Allgemeines &amp; Rechtsgrundlagen', '''        <p>Ich behandle deine personenbezogenen Daten vertraulich und entsprechend der Datenschutz-Grundverordnung (DSGVO), dem Bundesdatenschutzgesetz (BDSG) und dem Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz (TDDDG).</p>
        <p>Rechtsgrundlagen sind je nach Zweck:</p>
        <ul>
          <li><strong>Art. 6 Abs. 1 lit. a DSGVO</strong> – deine Einwilligung</li>
          <li><strong>Art. 6 Abs. 1 lit. b DSGVO</strong> – Bearbeitung deiner Anfrage</li>
          <li><strong>Art. 6 Abs. 1 lit. f DSGVO</strong> – mein berechtigtes Interesse an einer sicheren, funktionierenden und ansprechenden Website</li>
        </ul>
        <p>Die Verbindung zu dieser Website ist per TLS/SSL verschlüsselt – erkennbar am Schloss-Symbol und „https://“ in der Adresszeile.</p>'''),
  ('hosting','Hosting &amp; Zugriffsdaten', '''        <p>Diese Website wird bei <strong>Squarespace</strong> gehostet (Squarespace Ireland Limited, Le Pole House, Ship Street Great, Dublin 8, Irland). Squarespace verarbeitet die Daten in meinem Auftrag; Daten können dabei auch an die Squarespace, Inc. in den USA übermittelt werden. Die Übermittlung stützt sich auf das EU-US Data Privacy Framework bzw. auf EU-Standardvertragsklauseln.</p>
        <p>Beim Aufruf der Website werden automatisch Informationen in sogenannten Server-Logfiles gespeichert, die dein Browser übermittelt:</p>
        <ul>
          <li>Browsertyp und Browserversion</li>
          <li>verwendetes Betriebssystem</li>
          <li>Referrer-URL</li>
          <li>Hostname bzw. IP-Adresse des zugreifenden Rechners</li>
          <li>Uhrzeit der Serveranfrage</li>
        </ul>
        <p>Diese Daten sind technisch notwendig, um die Website auszuliefern und ihre Sicherheit zu gewährleisten (Art. 6 Abs. 1 lit. f DSGVO). Eine Zusammenführung mit anderen Datenquellen nehme ich nicht vor.</p>'''),
  ('cookies','Cookies &amp; Statistik', '''        <p>Squarespace setzt technisch notwendige Cookies, damit die Website funktioniert und sicher ausgeliefert wird (§ 25 Abs. 2 TDDDG, Art. 6 Abs. 1 lit. f DSGVO).</p>
        <p>Für die Besucherstatistik nutze ich die Analysefunktion von Squarespace. Statistik- oder Analyse-Cookies werden nur gesetzt, wenn du im Cookie-Banner zustimmst (§ 25 Abs. 1 TDDDG, Art. 6 Abs. 1 lit. a DSGVO). Deine Einwilligung kannst du jederzeit mit Wirkung für die Zukunft widerrufen, indem du deine Cookie-Einstellungen änderst oder die Cookies in deinem Browser löschst.</p>'''),
  ('kontakt','Kontakt per E-Mail &amp; Social Media', '''        <p>Wenn du mir per E-Mail oder über Instagram oder LinkedIn schreibst, verarbeite ich deine Angaben (zum Beispiel Name, E-Mail-Adresse bzw. Profilname und deine Nachricht), um deine Anfrage zu beantworten und für mögliche Anschlussfragen (Art. 6 Abs. 1 lit. b und f DSGVO). Für Nachrichten über Instagram und LinkedIn gelten zusätzlich die Datenschutzbestimmungen des jeweiligen Netzwerks.</p>
        <p>Ich gebe diese Daten nicht ohne deine Einwilligung weiter und lösche sie, sobald deine Anfrage abschließend bearbeitet ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>'''),
  ('schriften','Schriftarten (Google Fonts &amp; Adobe Fonts)', '''        <p>Für eine einheitliche Darstellung nutzt diese Website Schriftarten von <strong>Google Fonts</strong> (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland). Beim Aufruf einer Seite lädt dein Browser die Schriften von Servern von Google; dabei wird deine IP-Adresse an Google übermittelt, auch in die USA (EU-US Data Privacy Framework).</p>
        <p>Rechtsgrundlage ist mein berechtigtes Interesse an einer einheitlichen und ansprechenden Darstellung (Art. 6 Abs. 1 lit. f DSGVO). Mehr dazu: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Datenschutzerklärung von Google</a>.</p>
        <p>Zusätzlich lädt Squarespace die Schriften des Website-Designs über <strong>Adobe Fonts</strong> (Adobe Systems Software Ireland Limited, 4–6 Riverwalk, Citywest Business Campus, Dublin 24, Irland; Server use.typekit.net und p.typekit.net). Dabei wird deine IP-Adresse an Adobe übermittelt, gegebenenfalls auch in die USA (EU-US Data Privacy Framework). Rechtsgrundlage ist ebenfalls mein berechtigtes Interesse an einer einheitlichen Darstellung (Art. 6 Abs. 1 lit. f DSGVO). Mehr dazu: <a href="https://www.adobe.com/de/privacy/policies/adobe-fonts.html" target="_blank" rel="noopener">Datenschutzhinweise zu Adobe Fonts</a>.</p>'''),
  ('eingebettet','Eingebettete Inhalte', '''        <p>Einige Seiten laden Inhalte von anderen Anbietern. Dabei erhält der jeweilige Anbieter technisch bedingt deine IP-Adresse und die Information, welche Seite du aufgerufen hast.</p>
        <h3>Twitch</h3>
        <p>Im Twitch-Bereich (Twitch-Startseite und Live) kannst du den Stream-Player und den Chat von <strong>Twitch</strong> anzeigen (Twitch Interactive, Inc., 350 Bush Street, San Francisco, CA 94104, USA). Beides lädt erst, wenn du auf <strong>„Stream laden“</strong> bzw. <strong>„Chat laden“</strong> klickst – vorher werden keine Daten an Twitch übertragen. Ab dem Klick kann Twitch Cookies setzen und Daten in die USA übertragen (EU-US Data Privacy Framework). Bist du bei Twitch angemeldet, kann Twitch den Besuch deinem Konto zuordnen. Rechtsgrundlage ist deine Einwilligung durch den Klick (§ 25 Abs. 1 TDDDG, Art. 6 Abs. 1 lit. a DSGVO).</p>
        <p>Wählst du <strong>„Immer laden“</strong>, merkt sich dein Browser diese Entscheidung im lokalen Speicher (localStorage, Eintrag „ts-twitch-ok“) und lädt Twitch künftig direkt. Du kannst das jederzeit widerrufen, indem du die Website-Daten für trutzstaehler.de in deinem Browser löschst. Mehr dazu: <a href="https://www.twitch.tv/p/de-de/legal/privacy-notice/" target="_blank" rel="noopener">Datenschutzhinweis von Twitch</a>.</p>
        <h3>Wowhead</h3>
        <p>Im Twitch-Bereich werden Symbole und Gegenstands-Infos aus World of Warcraft von <strong>Wowhead</strong> geladen (wowhead.com, Bildserver zamimg.com). Dabei wird deine IP-Adresse an die Server von Wowhead übermittelt, gegebenenfalls auch in die USA.</p>
        <h3>GitHub</h3>
        <p>Die Spielstände aus dem Stream (Helden, Bestenliste, Statistiken) liegen als Datei bei <strong>GitHub</strong> (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA) und werden beim Aufruf der Twitch-Seiten von dort geladen. Dabei wird deine IP-Adresse an GitHub übermittelt.</p>
        <h3>Amazon-Bilder</h3>
        <p>Buchcover werden teilweise von Servern von <strong>Amazon</strong> geladen (Amazon Europe Core S.à r.l., 38 Avenue John F. Kennedy, L-1855 Luxemburg). Dabei wird deine IP-Adresse an Amazon übermittelt.</p>
        <p>Rechtsgrundlage für diese Einbindungen ist mein berechtigtes Interesse an der Darstellung meiner Streams, Spielstände und Bücher (Art. 6 Abs. 1 lit. f DSGVO). Soweit dabei Cookies gesetzt werden, die nicht unbedingt erforderlich sind, geschieht das nur mit deiner Einwilligung (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG).</p>'''),
  ('stream','Mitspielen im Stream', '''        <p>Wer im Twitch-Chat meines Streams mitspielt (zum Beispiel mit <strong>!charakter</strong>), dessen <strong>Twitch-Name</strong> und Spielfortschritt – Held, Stufe, Ruf, Beute, Platzierungen und Chat-Aktivität im Stream – werden gespeichert und im Twitch-Bereich dieser Website angezeigt, etwa in der Bestenliste, den Statistiken und im Charakterfenster.</p>
        <p>Rechtsgrundlage ist mein berechtigtes Interesse, das gemeinsame Spiel mit der Community darzustellen (Art. 6 Abs. 1 lit. f DSGVO). Wenn du nicht (mehr) angezeigt werden möchtest, schreib mir eine kurze Nachricht – ich entferne deinen Helden und deine Daten dann.</p>'''),
  ('links','Links zu anderen Websites', '''        <p>Diese Website verlinkt auf Instagram, LinkedIn, Twitch und Amazon. Die Links sind einfache Verweise: Daten werden erst übertragen, wenn du einen Link anklickst. Ab dann gelten die Datenschutzbestimmungen des jeweiligen Anbieters.</p>'''),
  ('speicherdauer','Speicherdauer', '''        <p>Ich speichere personenbezogene Daten nur so lange, wie es für den jeweiligen Zweck nötig ist oder gesetzliche Aufbewahrungsfristen es verlangen. Danach werden sie gelöscht.</p>'''),
  ('rechte','Deine Rechte', '''        <p>Du hast jederzeit das Recht auf:</p>
        <ul>
          <li>Auskunft über deine gespeicherten Daten (Art. 15 DSGVO)</li>
          <li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
          <li>Löschung (Art. 17 DSGVO)</li>
          <li>Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
          <li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
          <li>Widerruf einer Einwilligung mit Wirkung für die Zukunft (Art. 7 Abs. 3 DSGVO)</li>
        </ul>
        <p><strong>Widerspruchsrecht:</strong> Verarbeite ich Daten auf Grundlage meines berechtigten Interesses (Art. 6 Abs. 1 lit. f DSGVO), kannst du dieser Verarbeitung aus Gründen, die sich aus deiner besonderen Situation ergeben, jederzeit widersprechen (Art. 21 DSGVO).</p>
        <p>Schreib mir dazu einfach an die oben genannte Adresse. Wenn du glaubst, dass die Verarbeitung deiner Daten gegen Datenschutzrecht verstößt, kannst du dich bei einer Aufsichtsbehörde beschweren, zum Beispiel bei der für mich zuständigen:</p>
        <div class="ts-legal-card ts-glass">
          <p>Der Hamburgische Beauftragte für Datenschutz und Informationsfreiheit<br>Ludwig-Erhard-Straße 22, 20459 Hamburg</p>
        </div>'''),
 ])
open(OUT+'20-datenschutz-codeblock.html','w').write(datenschutz)

# ------------------------------------------------------------------ KONTAKT
kontakt = '''<!-- ==================================================================
     TRUTZ STÄHLER · SEITE „KONTAKT“
     Einfügen in: Seite /kontakt → einzige Sektion → Code-Block (volle Breite)
     Alle anderen Blöcke und Sektionen dieser Seite können gelöscht werden.
=================================================================== -->
<style>
  .ts-contact { position: relative; isolation: isolate; overflow: hidden; overflow: clip; background: var(--ts-bg); }
  .ts-contact__orb { position: absolute; z-index: -1; left: -12%; top: 10%; width: 52vw; height: 52vw; max-width: 800px; max-height: 800px; border-radius: 50%; filter: blur(110px); background: radial-gradient(circle, rgba(46, 140, 108, .32), transparent 66%); pointer-events: none; }
  .ts-contact__intro { padding-top: clamp(8.5rem, 14vw, 12rem); padding-bottom: clamp(6rem, 11vw, 10rem); }
  .ts-contact__meta { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--ts-line); }
  .ts-contact .ts-line { padding-bottom: .16em; margin-bottom: -.16em; }
  .ts-contact__grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: 3rem; padding-top: clamp(2.5rem, 5vw, 4rem); }
  .ts .ts-contact__title { font-family: var(--ts-font-display); font-weight: 800; font-size: clamp(2.3rem, 7.6vw, 7.2rem); line-height: .95; letter-spacing: -0.03em; }
  .ts .ts-contact__text p { max-width: 36rem; font-size: clamp(17px, 1.5vw, 19px); line-height: 1.75; color: var(--ts-muted); }
  .ts .ts-contact__text p + p { margin-top: 1.1rem; }
  .ts .ts-contact__text strong { color: var(--ts-text); font-weight: 500; }
  .ts .ts-contact__text a { color: var(--ts-mint); border-bottom: 1px solid rgba(110, 231, 183, .35); }
  .ts .ts-contact__note { margin-top: 1.75rem; padding: 1.1rem 1.35rem; border-radius: 16px; font-size: 14.5px; line-height: 1.65; color: var(--ts-muted); }
  .ts .ts-contact__note strong { color: var(--ts-text); font-weight: 500; }
  .ts .ts-contact__ways { display: grid; gap: .75rem; }
  .ts .ts-way { display: flex; align-items: center; gap: 1rem; padding: 1.1rem 1.25rem; border-radius: 18px; transition: transform .6s var(--ts-ease-out), border-color .4s; }
  .ts .ts-way:hover { transform: translateY(-3px); border-color: rgba(110, 231, 183, .35); }
  .ts-way__icon { display: grid; place-items: center; flex: none; width: 44px; height: 44px; border-radius: 14px; border: 1px solid var(--ts-line); background: rgba(29, 77, 63, .4); color: var(--ts-mint); }
  .ts-way__txt { display: flex; flex-direction: column; min-width: 0; }
  .ts .ts-way__label { color: var(--ts-muted); font-size: 10.5px; }
  .ts .ts-way__value { margin-top: .15rem; font-size: 16px; color: var(--ts-text); overflow-wrap: anywhere; }
  .ts-way__go { margin-left: auto; color: var(--ts-muted); transition: color .3s, transform .5s var(--ts-ease-out); }
  .ts-way:hover .ts-way__go { color: var(--ts-mint); transform: translate(2px, -2px); }

  @media (min-width: 1024px) {
    .ts-contact__grid { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); column-gap: clamp(3rem, 6vw, 6rem); align-items: start; }
  }

  /* Auf der Kontaktseite braucht der Footer keine zweite Kontakt-Einladung */
  body:has(.ts-contact) .ts-footer__cta { display: none; }
  body:has(.ts-contact) .ts-footer { padding-top: 0; }
</style>

<div class="ts ts-contact ts-bleed">
  <div class="ts-contact__orb" aria-hidden="true" data-ts-parallax="0.03"></div>
  <section class="ts-container ts-contact__intro" aria-labelledby="ts-contact-title">
    <div class="ts-contact__meta ts-reveal">
      <p class="ts-label ts-muted">[ 05 — Kontakt ]</p>
      <p class="ts-label ts-muted">Ich melde mich fix zurück</p>
    </div>

    <div class="ts-contact__grid">
      <div>
        <h1 id="ts-contact-title" class="ts-contact__title" data-ts-fit>
          <span class="ts-line"><span style="transition-delay:.1s">Melde dich</span></span>
          <span class="ts-line"><span class="ts-gradient-text" style="transition-delay:.22s">bei mir.</span></span>
        </h1>
        <div class="ts-contact__text" style="margin-top:2rem">
          <p class="ts-reveal">Moin! Hast du Fragen, Anregungen oder willst mir einfach mal 'n netten Gruß dalassen?</p>
          <p class="ts-reveal">Dann schreib mir gern – per E-Mail oder auf Instagram und LinkedIn. Ich beiß nicht (höchstens ins <strong>Franzbrötchen</strong>) und melde mich fix bei dir zurück.</p>
        </div>
        <p class="ts-contact__note ts-glass ts-reveal"><strong>Datenschutz:</strong> Deine Angaben werden natürlich nur dafür genutzt, dir zu antworten. Mehr dazu findest du in meiner <a href="/datenschutz" data-ts-native="Datenschutz" style="color:var(--ts-mint);border-bottom:1px solid rgba(110,231,183,.35)">Datenschutzerklärung</a>.</p>
      </div>

      <div class="ts-contact__ways ts-reveal" aria-label="Kontaktwege">
        <p class="ts-label ts-muted" style="margin-bottom:.25rem">So erreichst du mich</p>
        <a class="ts-way ts-glass" href="mailto:moin@trutzstaehler.de">
          <span class="ts-way__icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></svg></span>
          <span class="ts-way__txt"><span class="ts-label ts-way__label">E-Mail</span><span class="ts-way__value">moin@trutzstaehler.de</span></span>
          <svg class="ts-way__go" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>
        </a>
        <a class="ts-way ts-glass" href="https://www.instagram.com/trutzstaehler/" target="_blank" rel="noopener">
          <span class="ts-way__icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg></span>
          <span class="ts-way__txt"><span class="ts-label ts-way__label">Instagram · Papa, Laufen &amp; Bücher</span><span class="ts-way__value">@trutzstaehler</span></span>
          <svg class="ts-way__go" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>
        </a>
        <a class="ts-way ts-glass" href="https://www.instagram.com/trutz.stahl/" target="_blank" rel="noopener">
          <span class="ts-way__icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg></span>
          <span class="ts-way__txt"><span class="ts-label ts-way__label">Instagram · World of Warcraft &amp; Twitch</span><span class="ts-way__value">@trutz.stahl</span></span>
          <svg class="ts-way__go" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>
        </a>
        <a class="ts-way ts-glass" href="https://www.linkedin.com/in/trutz-st%C3%A4hler" target="_blank" rel="noopener">
          <span class="ts-way__icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/></svg></span>
          <span class="ts-way__txt"><span class="ts-label ts-way__label">LinkedIn</span><span class="ts-way__value">Trutz Stähler</span></span>
          <svg class="ts-way__go" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>
        </a>
      </div>
    </div>

  </section>
</div>
'''
open(OUT+'18-kontakt-codeblock.html','w').write(kontakt)
print('ok')
