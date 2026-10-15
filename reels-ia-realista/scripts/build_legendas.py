"""Gera as legendas (blocos curtos, palavra falada em destaque) a partir do alignment do TTS e injeta no
index.html entre os marcadores LEGENDAS (HTML: <!-- LEGENDAS:INICIO/FIM -->; JS: /* LEGENDAS:DADOS */ ... /* LEGENDAS:FIM */).

Uso: copie para a pasta do projeto HyperFrames (ao lado do index.html), edite o bloco CONFIGURAÇÃO e rode
    python3 build_legendas.py
Depois renderize a versão legendada com --variables '{"legendas":true}' (sem a variável, a composição esconde as legendas).

Vale para qualquer vídeo da Voltec com a persona. ALIGN, PHRASES e CTA_START (= T.cta do index.html) vêm da narração
e do index DESTE vídeo: começam vazios e o script para com uma mensagem até você preencher. START_FIX e LOW_RANGES
começam VAZIOS e só recebem o que for medido neste projeto (START_FIX: stt.py --ss/--t + NARR_OFFSET; LOW_RANGES:
trechos em que a legenda cobriria o objeto na mão). Os valores do Verão Conectado ficam nos comentários, só como
exemplo; com eles, este script gera o mesmo bloco de legendas do index entregue (conferido em 15/10/2026).

Regras que funcionaram:
  - Blocos definidos à mão em PHRASES (frase natural, não "N palavras"); o script confere palavra por palavra
    contra o alignment e para com AssertionError se o texto não bater (narração mudou -> atualize PHRASES).
  - Grafia fonética do TTS -> grafia correta na tela via FIX (ex.: "Voltéc" -> "Voltec", "dois" -> "2").
  - O alignment do TTS às vezes erra inícios de palavra (pausa inexistente, palavra atrasada): meça no áudio
    (STT/envelope) e corrija em START_FIX.
  - Legendas somem quando entra o cartão final (CTA_START); posição mais baixa por trecho (LOW_RANGES) quando a
    legenda cobriria o objeto que a pessoa segura.
"""
import json
import re
from pathlib import Path

# ============================ CONFIGURAÇÃO (edite aqui) ============================
ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"                                    # composição com os marcadores LEGENDAS
# PREENCHA: alignment da narração FINAL (com emendas já deslocadas): ROOT.parent / "audio" /
# "narracao_<vN>_s<seed>_alignment.json" ou o da narração emendada (references/api-elevenlabs.md §5.5).
# Verão Conectado: ALIGN = ROOT.parent / "audio" / "narracao_v3_alignment.json"
ALIGN = None
NARR_OFFSET = 0.30          # mesmo atraso da narração no prep.py (padrão testado)
CTA_START = None            # PREENCHA: = T.cta do index.html; as legendas somem quando entra o cartão final (Verão Conectado: 15.40)
MAX_CHARS = 21              # bloco mais longo que coube numa linha no layout padrão (Montserrat 800, 54 px, 866 px)
# grafia fonética/por extenso -> grafia na tela. "Voltéc" -> "Voltec" é fixo da Voltec; acrescente os números que a
# narração fala por extenso e devem sair em algarismo (Verão Conectado: "dois": "2", "cinco": "5"). Nunca "um" (artigo).
FIX = {"Voltéc": "Voltec"}

# inícios medidos no áudio que o alignment errou: (texto JÁ corrigido pelo FIX, ocorrência 1..n, início no VÍDEO em s).
# Projeto novo: vazio até medir nesta narração (stt.py --ss/--t + NARR_OFFSET).
START_FIX = []   # Verão Conectado: [("internet?", 1, 1.38), ("Voltec", 1, 5.32), ("Voltec", 2, 8.03)]
# trechos (início, fim) do vídeo em que a legenda vai para a posição baixa (classe "low"), ex.: take com o celular no alto.
# Projeto novo: vazio até ver a legenda cobrindo o objeto.
LOW_RANGES = []  # Verão Conectado: [(0.0, 3.70)]

# PREENCHA: blocos na ordem da fala, já com a grafia de tela do FIX; o nº de palavras de cada bloco tem de bater com o
# texto da narração (sem as tags [..]). Frase natural de até MAX_CHARS caracteres.
PHRASES = []
# Verão Conectado:
# PHRASES = ["Casa de praia", "sem internet?", "Ninguém merece",
#            "Agora sim!", "Com a Voltec", "eu fico conectada", "o verão inteiro",
#            "Tem Voltec em", "Grussaí", "Atafona", "Chapéu do Sol", "e São João da Barra",
#            "Sem fidelidade", "planos de 2 a 5 meses", "Clica no botão Saiba Mais", "ou escaneia o QR code na tela!"]
# ===================================================================================

faltam = [nome for nome, v in (("ALIGN", ALIGN), ("PHRASES", PHRASES or None), ("CTA_START", CTA_START)) if v is None]
if faltam:
    raise SystemExit(f"build_legendas.py: preencha {', '.join(faltam)} no bloco CONFIGURAÇÃO (CTA_START = T.cta do "
                     "index.html; o exemplo do Verão Conectado está nos comentários)")
if not Path(ALIGN).exists():
    raise SystemExit(f"build_legendas.py: alignment não encontrado: {ALIGN} (ajuste ALIGN no bloco CONFIGURAÇÃO)")

al = json.load(open(ALIGN))
chars, starts, ends = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]

# palavras com tempo (ignora as tags [..] de emoção, que o TTS não fala)
words, cur, in_tag = [], None, False
for c, s, e in zip(chars, starts, ends):
    if c == "[":
        in_tag = True
    if in_tag:
        if c == "]":
            in_tag = False
        continue
    if c.isspace():
        if cur:
            words.append(cur)
            cur = None
        continue
    if cur is None:
        cur = {"raw": "", "start": s, "end": e}
    cur["raw"] += c
    cur["end"] = e
if cur:
    words.append(cur)

for w in words:
    core = re.sub(r"[^\wÀ-ÿ]", "", w["raw"])
    trail = w["raw"][len(w["raw"].rstrip(".,:;!?…")):]
    w["brk"] = bool(re.search(r"[.,:;!?…]", trail))           # pausa natural depois da palavra
    keep = "".join(ch for ch in trail if ch in "?!").replace("...", "")
    w["text"] = FIX.get(core, core) + keep[:1]
    w["start"] += NARR_OFFSET
    w["end"] += NARR_OFFSET

for txt, occ, start in START_FIX:
    hits = [w for w in words if w["text"] == txt]
    if len(hits) >= occ:
        hits[occ - 1]["start"] = start
    else:
        print(f"AVISO: START_FIX {txt!r} ocorrência {occ} não encontrada")

chunks, i = [], 0
for ph in PHRASES:
    n = len(ph.split())
    ch = words[i:i + n]
    i += n
    got = " ".join(w["text"] for w in ch)
    assert got.rstrip("?!").lower() == ph.rstrip("?!").lower(), (got, ph)
    chunks.append(ch)
assert i == len(words), (i, len(words), "palavras sobrando no alignment: falta bloco em PHRASES")

data = []
for i, ch in enumerate(chunks):
    start = ch[0]["start"] - 0.05
    nxt = chunks[i + 1][0]["start"] - 0.05 if i + 1 < len(chunks) else None
    end = min(ch[-1]["end"] + 0.35, nxt) if nxt else ch[-1]["end"] + 0.5
    if start >= CTA_START:
        continue
    end = min(end, CTA_START)
    data.append({"s": round(start, 3), "e": round(end, 3),
                 "w": [[w["text"], round(w["start"], 3), round(w["end"], 3)] for w in ch]})


def is_low(t):
    return any(a <= t < b for a, b in LOW_RANGES)


html = "\n".join(
    f'        <div class="leg{" low" if is_low(d["s"]) else ""}">' + " ".join(f'<span class="w">{w[0]}</span>' for w in d["w"]) + "</div>"
    for d in data)
idx = INDEX.read_text()
if "<!-- LEGENDAS:INICIO -->" not in idx or "/* LEGENDAS:DADOS */" not in idx:
    raise SystemExit(f"{INDEX} não tem os marcadores LEGENDAS (use scripts/index_template.html como base)")
idx = re.sub(r"(<!-- LEGENDAS:INICIO -->).*?(<!-- LEGENDAS:FIM -->)",
             lambda m: m.group(1) + "\n" + html + "\n          " + m.group(2), idx, flags=re.S)
idx = re.sub(r"(/\* LEGENDAS:DADOS \*/).*?(/\* LEGENDAS:FIM \*/)",
             lambda m: m.group(1) + " const LEGENDAS = " + json.dumps(data, ensure_ascii=False) + "; " + m.group(2), idx, flags=re.S)
INDEX.write_text(idx)
for d in data:
    txt = " ".join(w[0] for w in d["w"])
    aviso = "   <- AVISO: bloco longo, confira se cabe" if len(txt) > MAX_CHARS else ""
    print(f'{d["s"]:6.2f}-{d["e"]:6.2f}  {txt}{aviso}')
