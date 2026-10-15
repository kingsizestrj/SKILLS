"""Heurística de tonicidade: mede duração e energia (RMS) das duas partes de uma palavra no áudio do TTS,
usando o alignment por caractere do endpoint with-timestamps. Serve para conferir se a marca saiu
com a sílaba tônica certa (ex.: "Voltéc" = vol-TÉC) antes de mostrar a narração ao cliente.

Uso:
    python3 -I scripts/stress.py [--palavra REGEX] [--corte N] <audio.wav> <alignment.json> [<audio2.wav> <alignment2.json> ...]
      --palavra  regex da palavra no texto enviado ao TTS (padrão "Volt[eé]c")
      --corte    nº de caracteres da 1ª parte (padrão 3: "Vol" | "téc")

Saída por ocorrência: início, duração e RMS de cada parte e o veredito
"tônica no fim" (2ª parte mais longa e com RMS >= 0,8 x a 1ª) ou "tônica no início?".
É heurística, e você não ouve áudio: liste na página do portão o instante de cada ocorrência (tempo no WAV; no
vídeo, some o NARR_OFFSET) e peça ao cliente para confirmar ouvindo no portão. O WAV tem de ser a saída do próprio
TTS (PCM 16 bits, sem corte nem atraso), porque os tempos do alignment são relativos ao início dele.
"""
import argparse
import json
import math
import re
import struct
import sys
import wave


def rms(samples):
    return math.sqrt(sum(s * s for s in samples) / max(1, len(samples)))


ap = argparse.ArgumentParser(description="tonicidade aproximada de uma palavra pelo alignment do TTS")
ap.add_argument("--palavra", default=r"Volt[eé]c")
ap.add_argument("--corte", type=int, default=3)
ap.add_argument("pares", nargs="+", help="<audio.wav> <alignment.json> ...")
a = ap.parse_args()
if len(a.pares) % 2:
    sys.exit("passe pares <audio.wav> <alignment.json>")

for wav_path, al_path in zip(a.pares[0::2], a.pares[1::2]):
    w = wave.open(wav_path)
    if w.getsampwidth() != 2:
        sys.exit(f"{wav_path}: esperado PCM 16 bits (use output_format wav_48000)")
    sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
    data = struct.unpack("<%dh" % (n * ch), w.readframes(n))
    if ch > 1:
        data = data[::ch]
    with open(al_path) as f:
        al = json.load(f)
    chars, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    text = "".join(chars)
    print("==", wav_path.split("/")[-1])
    achou = False
    for m in re.finditer(a.palavra, text):
        achou = True
        i, j = m.start(), m.end() - 1          # j = último caractere da palavra
        k = i + a.corte                        # 1ª parte: i .. k-1 | 2ª parte: k .. j
        a1, b1 = s[i], e[k - 1]
        a2, b2 = s[k], e[j]
        r1 = rms(data[int(a1 * sr):int(b1 * sr)])
        r2 = rms(data[int(a2 * sr):int(b2 * sr)])
        p1, p2 = text[i:k], text[k:j + 1]
        veredito = "tônica no fim" if (b2 - a2) > (b1 - a1) and r2 > 0.8 * r1 else "tônica no início?"
        print("  %s @%.2fs  '%s' %.0f ms rms %.0f | '%s' %.0f ms rms %.0f  -> %s"
              % (m.group(), a1, p1, (b1 - a1) * 1000, r1, p2, (b2 - a2) * 1000, r2, veredito))
    if not achou:
        print("  (palavra não encontrada no alignment)")
