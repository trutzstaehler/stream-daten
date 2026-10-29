"""Kontaktbogen: python3 vorschau.py <ausgabe.png> [prefix...]"""
import sys, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kritzel, motive  # noqa

out = sys.argv[1]; pre = sys.argv[2:]
keys = [k for k in kritzel.MOTIFS if not pre or any(k.startswith(p) for p in pre)]
cells = ''.join(f'<div class="c">{kritzel.motif_svg(k, with_name=True)}<small>{k}</small></div>' for k in keys)
html = f'''<html><body style="margin:0;background:#ddd;font:12px sans-serif">
<div style="display:grid;grid-template-columns:repeat(4,300px);gap:10px;padding:10px">{cells}</div>
<style>.c{{background:#fff;padding:6px}} .c svg{{width:288px;height:317px;display:block}}</style></body></html>'''
tmp = out + '.html'
open(tmp, 'w').write(html)
subprocess.run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render.js'), tmp, out, '1250', '400'], check=True)
os.remove(tmp); print(out, len(keys))
