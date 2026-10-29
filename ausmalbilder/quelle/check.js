// node check.js <build-html...>  -> meldet Text-Ueberlauf in .txt-Boxen und Elemente, die in die Fusszeile ragen
const {chromium} = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 794, height: 1123}});
  let bad = 0;
  for (const f of process.argv.slice(2)) {
    await p.goto('file://' + path.resolve(f)); await p.evaluate(() => document.fonts.ready);
    const r = await p.evaluate(() => [...document.querySelectorAll('section.pg')].map((s, i) => {
      const ft = s.querySelector('.ft'); const ftTop = ft ? ft.getBoundingClientRect().top : 1e9;
      const issues = [];
      s.querySelectorAll('.txt').forEach(t => { if (t.scrollHeight > t.clientHeight + 2) issues.push('txt-ueberlauf ' + (t.scrollHeight - t.clientHeight) + 'px'); });
      s.querySelectorAll('.txt > *, .hd, .art').forEach(e => { const bb = e.getBoundingClientRect(); if (bb.bottom > ftTop + 1 && bb.height > 0) issues.push('ragt in Fusszeile: ' + e.tagName + '.' + e.className); });
      return issues.length ? `Seite ${i + 1}: ${issues.join('; ')}` : null; }).filter(Boolean));
    if (r.length) { bad++; console.log(path.basename(f)); r.forEach(x => console.log('  ' + x)); }
  }
  console.log(bad ? 'PROBLEME gefunden' : 'OK – kein Überlauf'); await b.close();
})();
