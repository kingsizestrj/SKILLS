"""Troca a voz da fala de um take (ou de um áudio) para a voz da persona, mantendo o tempo: speech-to-speech da ElevenLabs.

Uso:
    python3 -I scripts/sts.py <voice_id> <entrada.mp4|.wav> <saida.wav> [--seed 20261015] [--stability 0.45]
                              [--similarity 0.85] [--manter-fundo] [--modelo eleven_multilingual_sts_v2]

Modo falando (references/modo-falando.md): o Veo 3.1 gera o take já com a fala, e este script troca a voz do Veo pela
voz da persona ([Voltec] Radassa 100% 4yvYc2GSakxLWMhlsd6b). O tempo da fala é o da fonte, então os lábios do take
continuam batendo com a voz nova.
- Extrai o áudio da entrada com ffmpeg (WAV 48 kHz mono) e envia para POST /v1/speech-to-speech/<voice_id>
  ?output_format=wav_48000 (multipart). GASTA CRÉDITOS (o custo do STS ainda não foi medido nesta skill: compare o
  saldo antes e depois na 1ª vez, references/modo-falando.md §6).
- remove_background_noise=true por padrão: tira o ambiente do Veo e devolve só a voz (o ambiente volta pela cama de
  SFX na edição). --manter-fundo desliga isso.
- Modelo eleven_multilingual_sts_v2: o único de STS com português na conta (GET /v1/models, 15/10/2026).
- Confere a duração: a saída tem de durar o mesmo que a entrada (diferença acima de 1 quadro de 24 fps vira aviso).
- Lê a chave pelo el.py, sem imprimir.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import el  # noqa: E402

ap = argparse.ArgumentParser(description="Speech-to-speech (ElevenLabs): troca a voz e mantém o tempo da fala")
ap.add_argument("voice_id")
ap.add_argument("entrada", help="take do Veo (.mp4) ou áudio")
ap.add_argument("saida", help="WAV de saída (48 kHz)")
ap.add_argument("--seed", type=int, default=20261015)
ap.add_argument("--stability", type=float, default=0.45)
ap.add_argument("--similarity", type=float, default=0.85)
ap.add_argument("--manter-fundo", action="store_true", help="não remove o ambiente da fonte")
ap.add_argument("--modelo", default="eleven_multilingual_sts_v2")
a = ap.parse_args()


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


with tempfile.TemporaryDirectory() as td:
    wav = os.path.join(td, "fala.wav")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", a.entrada, "-vn",
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", wav], check=True)
    d_in = dur(wav)
    campos = {
        "model_id": a.modelo,
        "voice_settings": json.dumps({"stability": a.stability, "similarity_boost": a.similarity}),
        "seed": str(a.seed),
        "remove_background_noise": "false" if a.manter_fundo else "true",
    }
    b = "----el" + uuid.uuid4().hex
    parts = [f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in campos.items()]
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="audio"; filename="fala.wav"\r\n'
                 'Content-Type: audio/wav\r\n\r\n'.encode())
    with open(wav, "rb") as f:
        parts.append(f.read())
    parts.append(f"\r\n--{b}--\r\n".encode())
    st, r = el.req("POST", f"/speech-to-speech/{a.voice_id}?output_format=wav_48000", b"".join(parts),
                   {"Content-Type": f"multipart/form-data; boundary={b}"}, raw=True)

if st != 200:
    detalhe = r.decode(errors="replace") if isinstance(r, (bytes, bytearray)) else r
    print(json.dumps({"error": st, "detail": str(detalhe)[:400]}, ensure_ascii=False))
    sys.exit(1)
os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
with open(a.saida, "wb") as f:
    f.write(r)
d_out = dur(a.saida)
print(json.dumps({"saida": a.saida, "entrada_s": round(d_in, 3), "saida_s": round(d_out, 3),
                  "diferenca_s": round(d_out - d_in, 3)}, ensure_ascii=False))
if abs(d_out - d_in) > 1 / 24:
    print(f"AVISO: a duração mudou {d_out - d_in:+.3f} s; confira a deriva palavra a palavra "
          "(references/modo-falando.md §7) antes de usar: a boca pode sair de sincronia", file=sys.stderr)
