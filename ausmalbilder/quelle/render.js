// node render.js <in.html> <out.png|out.pdf> [breite] [hoehe] [fullpage=1] [scale=1]
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const [inp, out, w = '1250', h = '900', full = '1', scale = '1'] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: +w, height: +h}, deviceScaleFactor: +scale});
  await p.goto('file://' + path.resolve(inp), {waitUntil: 'networkidle'});
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(150);
  if (out.endsWith('.pdf')) await p.pdf({path: out, preferCSSPageSize: true, printBackground: true});
  else await p.screenshot({path: out, fullPage: full === '1'});
  await b.close();
})();
