# -*- coding: utf-8 -*-
"""char_card 人审结果（review-pages expand 出的 decisions.jsonl）→ confirm 人裁事件并落库。

照 guji-manager review_pages/char_review.cmd_ingest 的写法，source 改 cold_start_char_card（字形快速入库第四节）。
只写 ok／pick（人点过或整页确认的格）；follow（跟随格）不写；seg／unclear／unknown／notchar 另列。
用法：python tools/ingest_char_card.py <decisions.jsonl> <批次> [--dry-run]
"""
import json
import re
import sys

from guji_manager._cv import EventLog, EventTarget, make_event
from guji_manager.feedback.consumers import route_and_consume

dec, batch = sys.argv[1], sys.argv[2]
dry = "--dry-run" in sys.argv
rows = [json.loads(l) for l in open(dec, encoding="utf-8") if l.strip()]
log = EventLog()
base = log.latest_seq(batch) + 1
evs, other = [], {}
for r in rows:
    if r["status"] not in ("ok", "pick"):
        other.setdefault(r["status"], []).append(r["id"])
        continue
    vol, page, col, slot = r["id"].split(":")
    m = re.fullmatch(r"(-?\d+)([ab]?)", slot)
    evs.append(make_event(batch, base + len(evs), "confirm",
                          EventTarget(step="seed_admit", unit="cell", key=r["id"], book=vol,
                                      page=int(page), col=int(col), slot=int(m.group(1))),
                          {"v": "confirm", "shape": r["char"], "source": "cold_start_char_card", "via": "char_card"}))
print(json.dumps({"confirm": len(evs), "另列": {k: len(v) for k, v in other.items()}}, ensure_ascii=False))
print(json.dumps(other, ensure_ascii=False))
if not dry:
    log.append(evs)
    print(json.dumps(route_and_consume(log, batch=batch), ensure_ascii=False)[:1500])
