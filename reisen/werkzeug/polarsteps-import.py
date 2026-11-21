#!/usr/bin/env python3
"""
Polarsteps-Export → Reisetagebuch auf trutzstaehler.de

Aufruf:
  python3 import.py <export.zip oder Ordner> --ziel <repo>/reisen/<reise> [--autor Insa] [--reise-name Australien]

Schreibt:
  <ziel>/reise.json      – Daten für das Website-Modul (gleiches Format wie die Reise-API)
  <ziel>/img/*.jpg       – verkleinerte Fotos ohne EXIF/GPS (1600 px) + Vorschauen (_t, 600 px)
  <ziel>/reise-config.json – Titel, Daten, Reisende, Plan (wird angelegt, wenn nicht vorhanden; von Hand pflegbar)

Mehrfach ausführbar: gleiche Steps werden aktualisiert, Einträge anderer Autorinnen bleiben erhalten,
vorhandene Fotos werden nicht neu erzeugt. Steps mit #privat im Text werden nicht übernommen.
"""
import argparse, json, math, os, re, sys, tempfile, zipfile, datetime
from PIL import Image, ImageOps

TIERE = {
    "kaenguru": ["kaenguru", "känguru", "kaengurus", "kängurus", "kangaroo", "wallaby", "wallabies", "roo"],
    "koala": ["koala", "koalas"], "wombat": ["wombat", "wombats"], "kookaburra": ["kookaburra", "lachhans"],
    "quokka": ["quokka", "quokkas"], "emu": ["emu", "emus"], "kakadu": ["kakadu", "kakadus", "cockatoo", "galah"],
    "schnabeltier": ["schnabeltier", "platypus"], "ameisenigel": ["ameisenigel", "echidna"],
    "krokodil": ["krokodil", "krokodile", "croc", "crocodile"], "delfin": ["delfin", "delfine", "dolphin"],
    "schildkroete": ["schildkroete", "schildkröte", "schildkröten", "turtle"], "wal": ["wal", "wale", "buckelwal", "whale"],
    "dingo": ["dingo", "dingos"], "possum": ["possum", "opossum"], "hai": ["hai", "haie", "riffhai", "shark"],
}
ALIAS = {a: k for k, v in TIERE.items() for a in v}
AU = (-45.0, -9.5, 110.0, 158.0)  # lat_min, lat_max, lng_min, lng_max


def in_au(lat, lng):
    return AU[0] <= lat <= AU[1] and AU[2] <= lng <= AU[3]


def tz_for(lat, lng):
    if not in_au(lat, lng): return None
    if lng < 129: return "Australia/Perth"
    if lng < 138: return "Australia/Darwin" if lat > -26 else "Australia/Adelaide"
    if lng < 141 and lat < -26: return "Australia/Adelaide"
    if lng >= 138 and lat > (-29 if lng < 150.5 else -28.17): return "Australia/Brisbane"
    if lat < -39.5: return "Australia/Hobart"
    return "Australia/Sydney"


def hav(a, b):
    r = math.pi / 180
    dl, dg = (b[0] - a[0]) * r, (b[1] - a[1]) * r
    h = math.sin(dl / 2) ** 2 + math.cos(a[0] * r) * math.cos(b[0] * r) * math.sin(dg / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def num(v):
    try:
        f = float(v)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def iso(ts, tzname=None):
    d = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    if tzname:
        try:
            from zoneinfo import ZoneInfo
            d = d.astimezone(ZoneInfo(tzname))
        except Exception:
            pass
    return d.isoformat(timespec="seconds")


def find_root(path):
    if zipfile.is_zipfile(path):
        tmp = tempfile.mkdtemp(prefix="ps_")
        with zipfile.ZipFile(path) as z:
            for m in z.infolist():
                n = os.path.normpath(m.filename)
                if n.startswith("..") or os.path.isabs(n):
                    continue  # unsichere Pfade im Archiv ignorieren
                z.extract(m, tmp)
        return tmp
    return path


def find_trips(root):
    trips = []
    for d, _, files in os.walk(root):
        if "trip.json" in files:
            trips.append(d)
    return trips


def find_user(root):
    for d, _, files in os.walk(root):
        if "user.json" in files:
            try:
                return json.load(open(os.path.join(d, "user.json"), encoding="utf-8"))
            except Exception:
                return {}
    return {}


def split_hashtags(text):
    animals, tags, private = [], [], False
    def repl(m):
        nonlocal private
        w = m.group(1).lower()
        if w in ("privat", "private"):
            private = True
        elif w in ALIAS:
            if ALIAS[w] not in animals: animals.append(ALIAS[w])
        elif w not in tags:
            tags.append(w)
        return ""
    clean = re.sub(r"(?<![\w&])#([0-9A-Za-zÄÖÜäöüß_]+)", repl, text or "")
    clean = re.sub(r"[ \t]+\n", "\n", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean).strip()
    clean = re.sub(r"[ \t]{2,}", " ", clean)
    return clean, animals, tags, private


def save_img(src, dst_full, dst_thumb):
    if os.path.exists(dst_full) and os.path.exists(dst_thumb):
        with Image.open(dst_full) as im:
            return im.size
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        full = im.copy(); full.thumbnail((1600, 1600), Image.LANCZOS)
        full.save(dst_full, "JPEG", quality=80, optimize=True, progressive=True)  # ohne EXIF → kein GPS im Bild
        th = im.copy(); th.thumbnail((600, 600), Image.LANCZOS)
        th.save(dst_thumb, "JPEG", quality=72, optimize=True, progressive=True)
        return full.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("--ziel", required=True)
    ap.add_argument("--autor", help="Name der Autorin (Standard: Vorname aus user.json)")
    ap.add_argument("--reise-name", help="Teil des Polarsteps-Reisenamens, falls der Export mehrere Reisen enthält")
    ap.add_argument("--slug", default=None)
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows-Konsole: Umlaute/Pfeile nicht abstürzen lassen
    except Exception: pass
    a = ap.parse_args()

    root = find_root(a.export)
    trips = find_trips(root)
    if not trips: sys.exit("Im Export wurde keine trip.json gefunden.")
    tdata = [(d, json.load(open(os.path.join(d, "trip.json"), encoding="utf-8"))) for d in trips]
    if a.reise_name:
        tdata = [t for t in tdata if a.reise_name.lower() in str(t[1].get("name", "")).lower()]
        if not tdata: sys.exit("Keine Reise mit diesem Namen im Export.")
    tdir, trip = max(tdata, key=lambda t: num(t[1].get("start_date")) or 0)  # neueste Reise

    user = find_user(root)
    autor = a.autor or user.get("first_name") or "Insa"
    os.makedirs(os.path.join(a.ziel, "img"), exist_ok=True)
    slug = a.slug or os.path.basename(os.path.normpath(a.ziel))

    cfg_path = os.path.join(a.ziel, "reise-config.json")
    if os.path.exists(cfg_path):
        cfg = json.load(open(cfg_path, encoding="utf-8"))
    else:
        sd, ed = num(trip.get("start_date")), num(trip.get("end_date"))
        cfg = {"slug": slug, "title": "Insa & Wiebke", "subtitle": "in Australien", "pageUrl": "https://trutzstaehler.de/down-under",
               "lead": "Zwei Schwestern, ein Sommer am anderen Ende der Welt. Jeder Eintrag ist ein Schritt auf der Karte – von Hamburg bis ans Riff.",
               "start": iso(sd)[:10] if sd else datetime.date.today().isoformat(),
               "end": iso(ed)[:10] if ed else "", "home": {"name": "Hamburg", "lat": 53.55, "lng": 9.99}, "plan": [],
               "travelers": [{"id": "t_insa", "name": "Insa", "color": "#E0793F"}, {"id": "t_wiebke", "name": "Wiebke", "color": "#4FA3A5"}]}
        json.dump(cfg, open(cfg_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    if not cfg.get("end"):  # Rückflug nicht von Hand eingetragen → geplantes Ende aus Polarsteps
        ed = num(trip.get("end_date"))
        if ed: cfg["end"] = iso(ed)[:10]
    trav = next((t for t in cfg["travelers"] if t["name"].lower() == autor.lower()), None)
    if not trav:
        trav = {"id": "t_" + re.sub(r"\W", "", autor.lower()), "name": autor, "color": "#E9C58F"}
        cfg["travelers"].append(trav)
        json.dump(cfg, open(cfg_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    out_path = os.path.join(a.ziel, "reise.json")
    old = json.load(open(out_path, encoding="utf-8")) if os.path.exists(out_path) else {"entries": [], "tracks": {}}
    keep = [e for e in old.get("entries", []) if e.get("author", {}).get("id") != trav["id"]]

    # Step-Ordner: „<name>_<stepid>“
    folders = {}
    for d in os.listdir(tdir):
        m = re.search(r"_(\d+)$", d)
        if m and os.path.isdir(os.path.join(tdir, d)): folders[m.group(1)] = os.path.join(tdir, d)

    entries, n_photos, skipped_private = [], 0, 0
    for s in trip.get("all_steps") or trip.get("steps") or []:
        if not isinstance(s, dict) or s.get("id") is None: continue
        sid = str(s["id"])
        text, animals, tags, private = split_hashtags(str(s.get("description") or ""))
        if private: skipped_private += 1; continue
        loc = s.get("location") or {}
        lat, lng = num(loc.get("lat")), num(loc.get("lon", loc.get("lng")))
        ts = num(s.get("start_time")) or num(s.get("creation_time")) or 0
        tz = tz_for(lat, lng) if lat is not None and lng is not None else None
        tz = tz or s.get("timezone_id") or "Australia/Sydney"
        photos = []
        pdir = os.path.join(folders.get(sid, ""), "photos")
        if os.path.isdir(pdir):
            for i, fn in enumerate(sorted(f for f in os.listdir(pdir) if f.lower().endswith((".jpg", ".jpeg", ".png", ".heic", ".webp")))):
                key = f"{sid}-{i + 1}"
                try:
                    w, h = save_img(os.path.join(pdir, fn), os.path.join(a.ziel, "img", key + ".jpg"), os.path.join(a.ziel, "img", key + "_t.jpg"))
                    photos.append({"key": key, "w": w, "h": h}); n_photos += 1
                except Exception as ex:
                    print(f"  Foto übersprungen ({fn}): {ex}")
        entries.append({
            "id": "ps_" + sid, "trip": slug, "author": trav,
            "title": str(s.get("display_name") or s.get("name") or loc.get("name") or "Etappe")[:200],
            "text": text, "place": str(loc.get("name") or loc.get("detail") or "")[:120],
            "lat": round(lat, 2) if lat is not None else None, "lng": round(lng, 2) if lng is not None else None,
            "tz": tz, "createdAt": iso(ts, tz) if ts else None, "tags": tags, "animals": animals,
            "photos": photos, "visibility": "public", "hearts": 0,
        })

    # Route: nur Punkte in Australien (Zuhause in Hamburg bleibt privat), ausgedünnt (≥ 2 km Abstand)
    lp = os.path.join(tdir, "locations.json")
    track = []
    if os.path.exists(lp):
        raw = json.load(open(lp, encoding="utf-8"))
        arr = raw.get("locations", []) if isinstance(raw, dict) else raw
        pts = sorted(([num(p.get("lat")), num(p.get("lon", p.get("lng"))), num(p.get("time"))] for p in arr if isinstance(p, dict)), key=lambda p: p[2] or 0)
        for p in pts:
            if None in p or not in_au(p[0], p[1]): continue
            if track and hav(track[-1], p) < 2: continue
            track.append([round(p[0], 3), round(p[1], 3), int(p[2])])
    tracks = old.get("tracks", {}); tracks[trav["id"]] = track
    merged_track = sorted((pt for t in tracks.values() for pt in t), key=lambda p: p[2])

    all_entries = sorted(keep + entries, key=lambda e: e.get("createdAt") or "", reverse=True)
    trip_out = {k: cfg[k] for k in ("slug", "title", "subtitle", "lead", "start", "end", "home", "plan", "travelers", "pageUrl") if k in cfg}
    out = {"trip": trip_out, "entries": all_entries, "track": merged_track, "tracks": tracks, "weather": None,
           "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "quelle": "polarsteps"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    # RSS-Feed (z. B. für Mailchimp „RSS to Email“)
    from xml.sax.saxutils import escape
    page = cfg.get("pageUrl", "https://trutzstaehler.de/down-under")
    base = cfg.get("dataBase", f"https://raw.githubusercontent.com/trutzstaehler/stream-daten/main/reisen/{slug}/")
    items = []
    for e in all_entries[:30]:
        if not e.get("createdAt"): continue
        d = datetime.datetime.fromisoformat(e["createdAt"]).astimezone(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
        body = "".join(f"<p>{escape(x)}</p>" for x in e["text"].split("\n\n") if x.strip())
        img = f'<p><img src="{base}img/{e["photos"][0]["key"]}.jpg" width="600" alt=""></p>' if e["photos"] else ""
        items.append(f"<item><title>{escape((e['place'] + ': ' if e['place'] else '') + e['title'])}</title><link>{escape(page)}#rt-{e['id']}</link>"
                     f"<guid isPermaLink=\"false\">{e['id']}</guid><pubDate>{d}</pubDate><dc:creator>{escape(e['author']['name'])}</dc:creator>"
                     f"<description>{escape(img + body)}</description></item>")
    feed = ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel>'
            f"<title>{escape((cfg['title'] + ' ' + cfg.get('subtitle', '')).strip())}</title><link>{escape(page)}</link><language>de</language>"
            f"<description>{escape(cfg.get('lead', ''))}</description>" + "".join(items) + "</channel></rss>")
    open(os.path.join(a.ziel, "feed.xml"), "w", encoding="utf-8").write(feed)

    print(f"{autor}: {len(entries)} Einträge, {n_photos} Fotos, {len(track)} Routenpunkte"
          + (f", {skipped_private} privat übersprungen" if skipped_private else "") + f" → {out_path}")


if __name__ == "__main__":
    main()
