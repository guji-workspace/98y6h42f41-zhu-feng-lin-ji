# -*- coding: utf-8 -*-
"""借库 × 匹配器比较（实验记录 2026-11-26-借库与匹配器比较）。

build  <名> <输出 db> <被借 store 目录>[,<目录>…]   建只含借来刻例（scope human+auto）的 glyph.db
score  <标签工作区> <实验工作区>…                    以标签工作区的 align_ref 对位字为标签，给各实验工作区 5a／seed_admit 打分

标签：align_ref 的 align_char（参校本对位到该格的字；不论 5a 是否认对，避免偏向取锚用的库）。
己已巳、日曰折叠。
"""
from __future__ import annotations

import json
import sqlite3
import sys
import time
from pathlib import Path

FOLD = {"已": "己", "巳": "己", "曰": "日"}


def f(c):
    return FOLD.get(c, c) if c else c


def build(name, out, stores):
    from open_guji_cv.clustering.glyph_db import borrowed_store, rebuild_from_store
    empty = Path(out).with_suffix(".empty_store")
    empty.mkdir(parents=True, exist_ok=True)
    extras = [borrowed_store(s, "human+auto", "") for s in stores.split(",")]
    t = time.time()
    r = rebuild_from_store(empty, out, extra_stores=extras, jobs=4)
    print(name, json.dumps({k: v for k, v in r.items() if not isinstance(v, dict)}, ensure_ascii=False), f"{time.time()-t:.0f}s")


def lib_chars(db):
    c = sqlite3.connect(db)
    try:
        return {f(r[0]) for r in c.execute("SELECT DISTINCT g.char FROM exemplars e JOIN glyphs g ON g.glyph_id=e.glyph_id")}
    finally:
        c.close()


def labels(ws):
    lab = {}
    for p in sorted(Path(ws, "products").glob("*/align_ref/p*.json")):
        for ch in json.loads(p.read_text(encoding="utf-8"))["align_ref"]["chars"]:
            if ch.get("align_char"):
                lab[ch["id"]] = f(ch["align_char"])
    return lab


def cells(ws, step):
    out = {}
    for p in sorted(Path(ws, "products").glob(f"*/{step}/p*.json")):
        for col in json.loads(p.read_text(encoding="utf-8"))[step]["columns"]:
            for ch in col["chars"]:
                out[ch["id"]] = ch
    return out


def score(label_ws, exp_ws):
    lab = labels(label_ws)
    for ws in exp_ws:
        meta = json.loads(Path(ws, "exp.json").read_text(encoding="utf-8")) if Path(ws, "exp.json").exists() else {}
        lc = lib_chars(meta["db"]) if meta.get("db") else set()
        gm, sa = cells(ws, "glyph_match"), cells(ws, "seed_admit")
        n = cov = top1 = top5 = same = same_wrong = 0
        for cid, y in lab.items():
            g = gm.get(cid)
            if not g:
                continue
            n += 1
            inlib = y in lc
            cov += inlib
            cands = g.get("candidates") or []
            top = f(cands[0][0]) if cands else None
            sc = cands[0][1] if cands else 0.0
            if inlib and top == y:
                top1 += 1
            if inlib and y in {f(c[0]) for c in cands[:5]}:
                top5 += 1
            # 借来的条目判 same 会被降成 unsure，所以按生产 same 门槛（首位分 ≥ 0.996）自己算「本该判 same」
            if sc >= 0.996:
                same += 1
                same_wrong += top != y
        all_cells = len(sa)
        pend = sum(1 for c in sa.values() if not c.get("admit"))
        r = dict(exp=Path(ws).name, n=n, cover=cov / n, top1=top1 / max(cov, 1), top5=top5 / max(cov, 1), same=same / n,
                 same_wrong=same_wrong / max(same, 1), same_wrong_n=same_wrong,
                 cells=all_cells, pending=pend, pending_rate=pend / max(all_cells, 1))
        print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build(*sys.argv[2:5])
    elif cmd == "score":
        score(sys.argv[2], sys.argv[3:])
