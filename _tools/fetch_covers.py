# -*- coding: utf-8 -*-
"""为 static/music 的 13 首曲目抓取专辑封面到 static/music/covers/NN.jpg"""
import json, os, subprocess, urllib.parse, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "static", "music", "covers")
os.makedirs(OUT, exist_ok=True)

TRACKS = [
    (1,  "堕",                 "巨礁Focus"),
    (2,  "感官过载",            "残像音阶"),
    (3,  "露珠",               "子弥"),
    (4,  "Towards the Light",  "Jacoo"),
    (5,  "Lifeline",           "Zeraphym 六翼使徒"),
    (6,  "秋色",               "463XIII"),
    (7,  "空心人札记",          "Calia-林焰"),
    (8,  "与花逝去的我",        "归尘回梦"),
    (9,  "夏日尽头的我们",      "命运结构"),
    (10, "落点",               "王子健"),
    (11, "反乌托邦",            "乌托邦P"),
    (12, "反乌托邦Pt.2",        "亞細亞曠世奇才"),
    (13, "Montagem pitty",     "见过夏天P"),
]

# 歌单详情接口已确认的封面（含专辑图的 7 首）
KNOWN = {
    "堕":                "http://p1.music.126.net/zyyTVHJ430XRZCJXJOtiHw==/109951164948712028.jpg",
    "感官过载":           "http://p2.music.126.net/qGLgEziAdCXsk9SbhiYjbw==/109951173214324887.jpg",
    "Towards the Light": "http://p2.music.126.net/aPhtHl1SEVgH9CNi7rtFZw==/109951164062929481.jpg",
    "落点":              "http://p1.music.126.net/hYq9YkybnkXMtBKl1XVy1g==/109951173145439197.jpg",
    "反乌托邦":           "http://p2.music.126.net/jn43eEp6_DbdC6bjmregvg==/109951170450400298.jpg",
    "反乌托邦Pt.2":      "http://p1.music.126.net/gH89vjqKtN6YAkHE2OsCPQ==/109951172460612010.jpg",
    "Montagem pitty":    "http://p2.music.126.net/pkKMhxyvW2Y1Vq7x65SX4g==/109951173083612810.jpg",
}


def fetch_json(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://music.163.com/"})
    with urllib.request.urlopen(r, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_id(name, artist):
    q = urllib.parse.quote("%s %s" % (name, artist))
    try:
        d = fetch_json("https://music.163.com/api/search/get/?s=%s&type=1&limit=3" % q)
        songs = (d.get("result") or {}).get("songs") or []
        for s in songs:
            if s.get("name") == name:
                return s.get("id")
        return songs[0]["id"] if songs else None
    except Exception as e:
        print("  search fail:", e)
        return None


def detail_pic(song_id):
    try:
        d = fetch_json("https://music.163.com/api/song/detail/?id=%s&ids=[%s]" % (song_id, song_id))
        songs = d.get("songs") or []
        if songs:
            return ((songs[0].get("album") or {}).get("picUrl")) or None
    except Exception as e:
        print("  detail fail:", e)
    return None


def download(url, path):
    if url.startswith("http://"):
        url = "https://" + url[7:]
    url = url + "?param=300y300"
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://music.163.com/"})
    with urllib.request.urlopen(r, timeout=30) as resp, open(path, "wb") as f:
        f.write(resp.read())
    return os.path.getsize(path)


results = {}
for idx, name, artist in TRACKS:
    path = os.path.join(OUT, "%02d.jpg" % idx)
    pic = KNOWN.get(name)
    if not pic:
        sid = search_id(name, artist)
        print("[%02d] %s -> song id %s" % (idx, name, sid))
        if sid:
            pic = detail_pic(sid)
    if pic:
        try:
            size = download(pic, path)
            results[idx] = "covers/%02d.jpg" % idx
            print("  OK %d bytes" % size)
            continue
        except Exception as e:
            print("  download fail:", e)
    results[idx] = None
    print("  !! 未获取到封面:", name)

print("\n=== 结果 ===")
for idx, name, artist in TRACKS:
    print(idx, name, "->", results[idx])
