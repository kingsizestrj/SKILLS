"""Espera uma rodada de gerações (vídeo ou imagem) e baixa as concluídas.

Uso:
    python3 -I scripts/poll_round.py <ids.json> [--out PASTA] [--kind video|image] [--interval 20] [--maxwait 2400]

ids.json = {"T1_veo_v1": "<generation_id>", "T1_veo_v2": "<generation_id>", ...}
Cada geração concluída vira PASTA/<nome>_<generation_id>.<ext> (ex.: takes/T1r_veo_v1_bICA18jbanp0KfqE3fgS.mp4).
PASTA padrão: $REELS_TAKES, senão a pasta onde está o ids.json (na sessão: takes/veo_round2_ids.json -> takes/).
Imprime por geração: nome, id, status, failure_reason e error_message (falhas não são cobradas).
Só faz GET; não cria gerações nem gasta créditos.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import el  # noqa: E402

ap = argparse.ArgumentParser(description="polling + download de uma rodada de gerações")
ap.add_argument("ids_json")
ap.add_argument("--out", default=None, help="pasta de destino (padrão: $REELS_TAKES ou a pasta do ids.json)")
ap.add_argument("--kind", default="video", choices=["video", "image"])
ap.add_argument("--interval", type=float, default=20)
ap.add_argument("--maxwait", type=float, default=2400)
a = ap.parse_args()

with open(a.ids_json) as f:
    ids = json.load(f)
out_dir = a.out or os.environ.get("REELS_TAKES") or os.path.dirname(os.path.abspath(a.ids_json))
os.makedirs(out_dir, exist_ok=True)

res = el.wait(a.kind, list(ids.values()), interval=a.interval, maxwait=a.maxwait)
falhas = 0
for name, gid in ids.items():
    r = res[gid]
    print(name, gid, r.get("status"), r.get("failure_reason"), (r.get("error_message") or "")[:300])
    if r.get("status") == "completed":
        ext = el.ext_for(r.get("content_mime_type"), a.kind)
        dest = os.path.join(out_dir, f"{name}_{gid}.{ext}")
        try:
            el.download(r["content_url"], dest)
        except Exception:  # URL assinada expirou (~1 h): um GET novo devolve outra
            dest, _ = el.fetch(a.kind, gid, os.path.join(out_dir, f"{name}_{gid}"))
        print("   ->", dest)
    else:
        falhas += 1
sys.exit(1 if falhas else 0)
