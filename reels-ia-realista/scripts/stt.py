"""Transcreve áudio/vídeo com ElevenLabs Speech-to-Text (scribe_v1) e imprime JSON:
{"text": ..., "words": [{"text", "start", "end", "type"}]}   (type: "word" = fala; "audio_event" = som, ex. "[som de mar]")

Uso:
    python3 -I scripts/stt.py <arquivo> [--ss 15.0] [--t 3.5] [--lang por] [--out saida.json]
      --ss/--t  transcreve só a janela [ss, ss+t] do arquivo; os tempos impressos ficam na linha do tempo do arquivo
      --lang    language_code do scribe (padrão "por")

Para que serve no QA: provar que o áudio nativo de um take não tem fala nem música (só audio_event) e que a
narração/vídeo final diz exatamente o texto aprovado. Converte para WAV mono 16 kHz com ffmpeg em memória
(não cria arquivo temporário). Usa scripts/el.py para a chamada; não imprime a chave. A chamada consome créditos de STT.
"""
import argparse
import io
import json
import os
import subprocess
import sys
import uuid
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import el  # noqa: E402

ap = argparse.ArgumentParser(description="STT scribe_v1 (ElevenLabs) com timestamps por palavra")
ap.add_argument("arquivo")
ap.add_argument("--ss", type=float, default=0.0, help="início da janela em segundos")
ap.add_argument("--t", type=float, default=None, help="duração da janela em segundos")
ap.add_argument("--lang", default="por", help='language_code (padrão "por")')
ap.add_argument("--out", default=None, help="também grava o JSON neste arquivo")
a = ap.parse_args()

cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin"]
if a.ss:
    cmd += ["-ss", f"{a.ss:.3f}"]
if a.t:
    cmd += ["-t", f"{a.t:.3f}"]
cmd += ["-i", a.arquivo, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-acodec", "pcm_s16le", "-"]
pcm = subprocess.run(cmd, check=True, capture_output=True).stdout
buf = io.BytesIO()  # WAV com cabeçalho correto (ffmpeg em pipe não consegue gravar os tamanhos do RIFF)
with wave.open(buf, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(pcm)
wav = buf.getvalue()

b = "----el" + uuid.uuid4().hex
parts = []
for k, v in [("model_id", "scribe_v1"), ("language_code", a.lang), ("tag_audio_events", "true"), ("timestamps_granularity", "word")]:
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
parts.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode())
parts.append(wav)
parts.append(f"\r\n--{b}--\r\n".encode())

st, r = el.req("POST", "/speech-to-text", b"".join(parts), {"Content-Type": f"multipart/form-data; boundary={b}"})
if st != 200:
    print(json.dumps({"error": st, "detail": str(r)[:300]}, ensure_ascii=False))
    sys.exit(1)

words = []
for w in r.get("words", []):
    if w.get("type") == "spacing":
        continue
    d = {k: w.get(k) for k in ("text", "start", "end", "type")}
    for k in ("start", "end"):
        if isinstance(d[k], (int, float)):
            d[k] = round(d[k] + a.ss, 3)
    words.append(d)
out = json.dumps({"text": r.get("text"), "words": words}, ensure_ascii=False)
print(out)
if a.out:
    with open(a.out, "w") as f:
        f.write(out)
