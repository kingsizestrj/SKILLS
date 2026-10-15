"""Converte a saída do stt.py (palavras com início e fim) no formato de alignment do TTS, que o build_legendas.py lê:
{characters, character_start_times_seconds, character_end_times_seconds}.

Uso:
    python3 -I scripts/stt_alinhamento.py <stt.json> <saida_alignment.json> [--offset 0.0]

Modo falando (references/modo-falando.md §8): rode o stt.py --out na mix final (media/mix.wav), que já está no tempo
do vídeo, converta com este script e use ALIGN = esse arquivo e NARR_OFFSET = 0.0 no build_legendas.py.
- Só entram itens "word"; os "audio_event" (ex.: "[som de mar]") ficam de fora.
- O tempo de cada letra é dividido por igual entre o início e o fim da palavra; o espaço entre palavras ocupa a pausa.
- As palavras saem como o STT escreveu (ex.: algarismos em vez de números por extenso): escreva os PHRASES do
  build_legendas.py a partir do "texto" que este script imprime.
"""
import argparse
import json
import sys

ap = argparse.ArgumentParser(description="STT (stt.py) -> alignment por caractere (build_legendas.py)")
ap.add_argument("stt")
ap.add_argument("saida")
ap.add_argument("--offset", type=float, default=0.0, help="soma este valor (s) a todos os tempos")
a = ap.parse_args()

d = json.load(open(a.stt, encoding="utf-8"))
if "error" in d:
    sys.exit(f"stt_alinhamento.py: o JSON do STT tem erro: {d}")
words = [w for w in d.get("words", []) if w.get("type", "word") == "word" and w.get("text", "").strip()]
if not words:
    sys.exit("stt_alinhamento.py: nenhuma palavra no STT")

chars, starts, ends = [], [], []
for i, w in enumerate(words):
    t0, t1 = float(w["start"]) + a.offset, float(w["end"]) + a.offset
    txt = w["text"].strip()
    if i:
        chars.append(" ")
        starts.append(ends[-1])
        ends.append(max(ends[-1], round(t0, 4)))
    step = (t1 - t0) / len(txt)
    for k, c in enumerate(txt):
        chars.append(c)
        starts.append(round(t0 + k * step, 4))
        ends.append(round(t0 + (k + 1) * step, 4))

with open(a.saida, "w", encoding="utf-8") as f:
    json.dump({"characters": chars, "character_start_times_seconds": starts,
               "character_end_times_seconds": ends}, f, ensure_ascii=False)
print(json.dumps({"palavras": len(words), "inicio_s": starts[0], "fim_s": ends[-1],
                  "texto": " ".join(w["text"].strip() for w in words)}, ensure_ascii=False))
