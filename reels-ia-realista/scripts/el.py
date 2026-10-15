"""Helper da API ElevenLabs: assets, Flows (imagem/vídeo), polling, download e TTS com timestamps.

NUNCA imprime a chave. Ela vem de ELEVENLABS_API_KEY (se já estiver no ambiente) ou do arquivo
~/.config/elevenlabs/env (linha ELEVENLABS_API_KEY=..., com ou sem "export"); outro arquivo: ELEVENLABS_ENV_FILE=/caminho.

Como biblioteca (de qualquer pasta; SKILL exportado no preâmbulo do shell):
    import os, sys, json; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
    st, r = el.upload_asset("refs/rosto.jpg")                        # (200, {"asset_id": ...})  sem custo
    st, r = el.submit("image", json.load(open("bodies/T1_a.json")))  # (200, {"id": ..., "status": "pending"})  GASTA CRÉDITOS
    res = el.wait("image", [r["id"]])                                # {id: resposta final}
    el.fetch("image", r["id"], "snapshots/T1_a")                     # baixa com a extensão do content_mime_type

Pela linha de comando:
    python3 -I scripts/el.py upload <arquivo> [nome]                  sobe um asset (sem custo)
    python3 -I scripts/el.py submit <image|video> <body.json>         cria a geração e imprime o id   (GASTA CRÉDITOS)
    python3 -I scripts/el.py get <image|video> <generation_id>        status (sem content_url no print)
    python3 -I scripts/el.py wait <image|video> <saida_sem_ext> <id>  espera e baixa <saida>.<ext>
    python3 -I scripts/el.py tts <voice_id> <body.json> <saida_sem_ext> [output_format]
        POST /v1/text-to-speech/<voice>/with-timestamps -> <saida>.wav + <saida>_alignment.json  (GASTA CRÉDITOS)

Falhas (failed), moderação e erros 422 de validação não são cobrados. Guarde o generation_id, não a URL:
o content_url é assinado e expira (~1 h); um novo GET devolve URL nova.
"""
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

API = "https://api.elevenlabs.io/v1"
_KEY = None


def _key():
    """Lê a chave sem imprimir: ambiente primeiro, depois o arquivo env."""
    global _KEY
    if _KEY:
        return _KEY
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not k:
        path = os.path.expanduser(os.environ.get("ELEVENLABS_ENV_FILE", "~/.config/elevenlabs/env"))
        try:
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("export "):
                        line = line[7:].strip()
                    if line.startswith("ELEVENLABS_API_KEY="):
                        k = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
        except FileNotFoundError:
            pass
    if not k:
        raise SystemExit("chave não encontrada: defina ELEVENLABS_API_KEY ou crie ~/.config/elevenlabs/env (chmod 600)")
    _KEY = k
    return k


def req(method, path, body=None, headers=None, raw=False):
    """Chama a API. body dict -> JSON; bytes -> enviado como está. Devolve (status_http, json|bytes|texto)."""
    h = {"xi-api-key": _key()}
    if headers:
        h.update(headers)
    data = None
    if body is not None and not isinstance(body, (bytes, bytearray)):
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json"
    elif body is not None:
        data = body
    r = urllib.request.Request(API + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            out = resp.read()
            return resp.status, (out if raw else json.loads(out or b"{}"))
    except urllib.error.HTTPError as e:
        txt = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(txt)
        except Exception:
            return e.code, txt


def upload_asset(path, name=None):
    """POST /v1/assets (multipart: campos asset e name). Não gasta créditos; ocupa cota de armazenamento."""
    name = name or os.path.basename(path)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    b = "----el" + uuid.uuid4().hex
    parts = [
        f'--{b}\r\nContent-Disposition: form-data; name="name"\r\n\r\n{name}\r\n'.encode(),
        f'--{b}\r\nContent-Disposition: form-data; name="asset"; filename="{name}"\r\nContent-Type: {mime}\r\n\r\n'.encode(),
    ]
    with open(path, "rb") as f:
        parts.append(f.read())
    parts.append(f"\r\n--{b}--\r\n".encode())
    return req("POST", "/assets", b"".join(parts), {"Content-Type": f"multipart/form-data; boundary={b}"})


def submit(kind, body):
    """POST /v1/flows/<image|video>. GASTA CRÉDITOS se for aceito (resposta 200 com id)."""
    return req("POST", f"/flows/{kind}", body)


def get(kind, gid):
    """GET /v1/flows/<image|video>/<id>: status pending/generating/completed/failed."""
    return req("GET", f"/flows/{kind}/{gid}")


def download(url, out):
    """Baixa um content_url assinado (não precisa de header)."""
    d = os.path.dirname(os.path.abspath(out))
    os.makedirs(d, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as r, open(out, "wb") as f:
        f.write(r.read())
    return out


def wait(kind, ids, interval=None, maxwait=900):
    """Polling de várias gerações; devolve {id: resposta_final}. Intervalo padrão: 3 s (imagem) / 15 s (vídeo)."""
    interval = interval or (3 if kind == "image" else 15)
    pending, done, t0 = set(ids), {}, time.time()
    while pending and time.time() - t0 < maxwait:
        throttled = False
        for gid in list(pending):
            st, r = get(kind, gid)
            if st == 429:
                throttled = True
            elif st == 200 and r.get("status") in ("completed", "failed"):
                done[gid] = r
                pending.discard(gid)
        if pending:
            time.sleep(interval * (2 if throttled else 1))
    for gid in pending:
        done[gid] = {"id": gid, "status": "timeout_local"}
    return done


def ext_for(mime, kind="video"):
    """Extensão de arquivo a partir do content_mime_type (jpeg -> jpg)."""
    if not mime:
        return "mp4" if kind == "video" else "png"
    e = mime.split("/")[-1].split(";")[0]
    return "jpg" if e == "jpeg" else e


def fetch(kind, gid, outbase):
    """GET da geração e, se completed, baixa para <outbase>.<ext>. Devolve (caminho|None, resposta)."""
    st, r = get(kind, gid)
    if st != 200 or r.get("status") != "completed":
        return None, r
    out = f"{outbase}.{ext_for(r.get('content_mime_type'), kind)}"
    return download(r["content_url"], out), r


def tts(voice_id, body, outbase, output_format="wav_48000"):
    """TTS com timestamps. Salva <outbase>.wav (ou outro formato) e <outbase>_alignment.json
    ({characters, character_start_times_seconds, character_end_times_seconds}) - o formato que
    build_legendas.py e stress.py leem. GASTA CRÉDITOS (~1 crédito/caractere no eleven_v4)."""
    st, r = req("POST", f"/text-to-speech/{voice_id}/with-timestamps?output_format={output_format}", body)
    if st != 200:
        return st, r
    ext = "wav" if output_format.startswith("wav") else ("mp3" if output_format.startswith("mp3") else "pcm")
    audio_path = f"{outbase}.{ext}"
    os.makedirs(os.path.dirname(os.path.abspath(audio_path)), exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(base64.b64decode(r["audio_base64"]))
    al = r.get("alignment") or r.get("normalized_alignment")
    with open(f"{outbase}_alignment.json", "w") as f:
        json.dump(al, f, ensure_ascii=False)
    return st, {"audio": audio_path, "alignment": f"{outbase}_alignment.json", "chars": len(al["characters"]) if al else 0}


def _safe(r):
    """Cópia da resposta sem URLs assinadas, para imprimir."""
    if isinstance(r, dict):
        return {k: v for k, v in r.items() if k != "content_url"}
    return r


def _main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == "upload" and len(argv) >= 3:
        st, r = upload_asset(argv[2], argv[3] if len(argv) > 3 else None)
        print(st, json.dumps(_safe(r), ensure_ascii=False))
        return 0 if st == 200 else 1
    if cmd == "submit" and len(argv) == 4:
        with open(argv[3]) as f:
            st, r = submit(argv[2], json.load(f))
        print(st, json.dumps(_safe(r), ensure_ascii=False))
        return 0 if st == 200 else 1
    if cmd == "get" and len(argv) == 4:
        st, r = get(argv[2], argv[3])
        print(st, json.dumps(_safe(r), ensure_ascii=False))
        return 0 if st == 200 else 1
    if cmd == "wait" and len(argv) == 5:
        kind, outbase, gid = argv[2], argv[3], argv[4]
        r = wait(kind, [gid], maxwait=1800 if kind == "video" else 300)[gid]
        if r.get("status") != "completed":
            print(json.dumps(_safe(r), ensure_ascii=False))
            return 2
        path, _ = fetch(kind, gid, outbase)
        print("ok:", path)
        return 0
    if cmd == "tts" and len(argv) in (5, 6):
        with open(argv[3]) as f:
            body = json.load(f)
        st, r = tts(argv[2], body, argv[4], argv[5] if len(argv) == 6 else "wav_48000")
        print(st, json.dumps(r, ensure_ascii=False)[:600])
        return 0 if st == 200 else 1
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
