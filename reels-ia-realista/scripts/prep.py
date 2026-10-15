"""Monta a base do Reels a partir dos takes aprovados: vídeo cortado (media/base.mp4) e mix de áudio (media/mix.wav).

Uso: copie para a pasta do projeto HyperFrames (ao lado do index.html), edite o bloco CONFIGURAÇÃO e rode
    python3 prep.py          # vídeo + áudio
    python3 prep.py audio    # refaz só o áudio (troca de narração, ganho, cama)
    python3 prep.py video    # refaz só o vídeo

Vale para qualquer vídeo da Voltec com a persona. SEGMENTS, TOTAL e NARR mudam a cada vídeo: começam vazios e o
script para com uma mensagem até você preencher. Os valores do Verão Conectado (v5) ficam nos comentários, só como
exemplo. Os níveis e o resto do bloco são o padrão testado: não mexa sem motivo.

O que faz (pipeline testado no Reels "Verão Conectado" da Voltec):
  vídeo: corta cada take em QUADROS de 24 fps, concatena, congela o último quadro (tpad clone) até TOTAL
         quadros para ficar por baixo do CTA, aplica grão leve e codifica H.264 CRF 18, GOP 24, sem áudio.
  áudio: som nativo de cada take a -30 LUFS (medido na janela usada) com J/L-cut de 0,2 s; cama de SFX
         contínua a -36 LUFS com rampa (nunca degrau) no congelamento final; narração com passa-alta,
         compressor e loudnorm -16 LUFS, atrasada NARR_OFFSET s; ducking (sidechain) do ambiente pela voz;
         master em 2 passagens de loudnorm: -14 LUFS integrado, -1,5 dBTP, LRA 11.
Precisa de ffmpeg no PATH. Não usa numpy.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

# ============================ CONFIGURAÇÃO (edite aqui) ============================
ROOT = Path(__file__).resolve().parent            # pasta do projeto HyperFrames (index.html, media/)
PROJ = Path(os.environ.get("REELS_PROJ", ROOT.parent))  # raiz do projeto do vídeo (takes/, audio/)
FPS = 24                                           # Veo entrega 24 fps; renderize o HyperFrames com --fps 24
TAKES = PROJ / "takes"                             # pasta dos takes baixados (poll_round.py)

# PREENCHA: (arquivo do take em TAKES, quadro de entrada, nº de quadros), na ordem do vídeo. Quadro = segundo x 24.
# Escolha in/out olhando tiras de 6-24 fps nos pontos críticos (references/qa-checklist.md §B).
SEGMENTS = []
# Verão Conectado v5:
# SEGMENTS = [
#     ("T1r_veo_v1_bICA18jbanp0KfqE3fgS.mp4", 19, 89),   # sinal: celular erguido, desce e franze a testa (boca fechada)
#     ("T2r_veo_v1_RvTRU6nLzVKOEUqVWUh5.mp4", 62, 101),  # rede: sorri com o celular firme (a v2 deformava o celular ao abaixar)
#     ("T3r_veo_v2_R41wQEvLdexHBvaXIRsl.mp4", 5, 187),   # selfie na areia
# ]
# PREENCHA: duração final em QUADROS (inteiro) = (última palavra no vídeo + ~1 s) x 24. O que passar da soma dos
# SEGMENTS congela o último quadro por baixo do CTA. Verão Conectado: TOTAL = 492 (20,5 s).
TOTAL = None
# PREENCHA: narração final (ver como foi montada: audio/COMO_FOI_MONTADA_*.txt). Projeto novo:
# PROJ / "audio" / "narracao_<vN>_s<seed>.wav" ou a narração emendada (references/api-elevenlabs.md §5.5).
# Verão Conectado: NARR = PROJ / "audio" / "narracao_v3.wav"
NARR = None
NARR_OFFSET = 0.30   # s em que a narração começa no vídeo (padrão testado; use o MESMO valor no build_legendas.py)
# cama de ambiente (SFX ElevenLabs, references/api-elevenlabs.md §7), com o texto da cena DESTA campanha:
# duration_seconds >= TOTAL/FPS (máx. 30 s); este script corta no fim do vídeo e completa com silêncio.
# Verão Conectado: audio/ambiente_praia_sfx.mp3 (cena de praia), de 20 s para um vídeo de 20,5 s, então o mix
# entregue ficou em silêncio de 20,0 a 20,5 s.
BED = PROJ / "audio" / "ambiente_sfx.mp3"
BED_LEN = None       # duração da cama em s; None = mede com ffprobe

AMB_LUFS = -30.0     # som nativo de cada take
BED_LUFS = -36.0     # cama contínua
BED_TAIL_BOOST = 1.2 # ganho linear extra da cama no congelamento final (1 + 1,2 = x2,2), em rampa
BED_RAMP_S = 0.8     # duração da rampa (degrau seco de ganho gerou estalo audível)
XFADE_S = 0.2        # J-cut (som do take seguinte entra antes) e L-cut (rabo do anterior)
VO_LUFS = -16.0      # narração antes da master
MASTER = dict(I=-14, TP=-1.5, LRA=11)  # loudnorm TP aceita só de -9 a 0
MAX_GAIN_DB = 20.0   # trava de segurança: take quase mudo não ganha mais que isso
OUT = ROOT / "media"
# ===================================================================================


def run(args):
    subprocess.run(args, check=True)


def lufs(path, start=0.0, dur=None):
    """Loudness integrada (LUFS) de um trecho, para aplicar ganho estático."""
    args = ["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{start:.4f}"]
    if dur:
        args += ["-t", f"{dur:.4f}"]
    args += ["-i", str(path), "-vn", "-af", "ebur128", "-f", "null", "-"]
    err = subprocess.run(args, capture_output=True, text=True).stderr
    line = [l for l in err.splitlines() if l.strip().startswith("I:")][-1]
    return float(line.split()[1])


def gain_to(target, path, start=0.0, dur=None):
    g = target - lufs(path, start, dur)
    if g > MAX_GAIN_DB:
        print(f"AVISO: {Path(path).name} quase mudo nessa janela; ganho {g:.1f} dB limitado a {MAX_GAIN_DB} dB")
        g = MAX_GAIN_DB
    return g


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


def check():
    faltam = [nome for nome, v in (("SEGMENTS", SEGMENTS), ("TOTAL", TOTAL), ("NARR", NARR)) if not v]
    if faltam:
        sys.exit(f"prep.py: preencha {', '.join(faltam)} no bloco CONFIGURAÇÃO "
                 "(começam vazios; o exemplo do Verão Conectado está nos comentários)")
    if not isinstance(TOTAL, int):
        sys.exit(f"prep.py: TOTAL é em QUADROS (inteiro), não em segundos: {TOTAL!r} (ex.: 20,5 s x 24 = 492)")
    for seg in SEGMENTS:
        if len(seg) != 3 or not all(isinstance(x, int) for x in seg[1:]):
            sys.exit(f"prep.py: cada item de SEGMENTS é (arquivo, quadro_inicial, nº_de_quadros), com inteiros: {seg!r}")
    used = sum(n for _, _, n in SEGMENTS)
    if used > TOTAL:
        sys.exit(f"SEGMENTS somam {used} quadros, mais que TOTAL={TOTAL}")
    for f, start, n in SEGMENTS:
        p = TAKES / f
        if not p.exists():
            sys.exit(f"take não encontrado: {p} (ajuste TAKES/SEGMENTS no bloco CONFIGURAÇÃO)")
    for p in (NARR, BED):
        if not Path(p).exists():
            sys.exit(f"arquivo não encontrado: {p} (ajuste NARR/BED no bloco CONFIGURAÇÃO)")
    print(f"{used} quadros de takes + {TOTAL - used} congelados = {TOTAL} ({TOTAL / FPS:.2f} s)")


def video():
    parts, labels = [], []
    for i, (f, start, n) in enumerate(SEGMENTS):
        parts.append(f"[{i}:v]trim=start_frame={start}:end_frame={start + n},setpts=PTS-STARTPTS[v{i}]")
        labels.append(f"[v{i}]")
    used = sum(n for _, _, n in SEGMENTS)
    parts.append("".join(labels) + f"concat=n={len(SEGMENTS)}:v=1:a=0,"
                 f"tpad=stop_mode=clone:stop={TOTAL - used},"
                 "noise=alls=3:allf=t,format=yuv420p[v]")
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for f, _, _ in SEGMENTS:
        args += ["-i", str(TAKES / f)]
    args += ["-filter_complex", ";".join(parts), "-map", "[v]", "-r", str(FPS),
             "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-g", str(FPS), "-an", str(OUT / "base.mp4")]
    run(args)


def audio():
    total_s = TOTAL / FPS
    bed_len = BED_LEN or duration(BED)
    if bed_len < total_s - 0.05:
        print(f"AVISO: a cama tem {bed_len:.2f} s e o vídeo {total_s:.2f} s: o ambiente some em fade a partir de "
              f"{bed_len - 1.2:.2f} s (gere a cama com duration_seconds >= {total_s:.2f}; máx. 30)")
    parts, mixes, t = [], [], 0.0
    for i, (f, start, n) in enumerate(SEGMENTS):
        a = start / FPS
        d = n / FPS
        pre = XFADE_S if i > 0 else 0.0                    # J-cut: o som do take seguinte entra antes
        post = XFADE_S if i < len(SEGMENTS) - 1 else 0.0   # L-cut: rabo do take anterior
        a0 = max(0.0, a - pre)
        pre = a - a0
        dur = d + pre + post
        delay = int(round((t - pre) * 1000))
        parts.append(
            f"[{i}:a]atrim=start={a0:.4f}:duration={dur:.4f},asetpts=PTS-STARTPTS,"
            f"volume={gain_to(AMB_LUFS, TAKES / f, a0, dur):.2f}dB,"
            f"afade=t=in:d={max(pre, 0.05):.3f},afade=t=out:st={dur - max(post, 0.08):.3f}:d={max(post, 0.08):.3f},"
            f"adelay={delay}|{delay}[a{i}]")
        mixes.append(f"[a{i}]")
        t += d
    nb = len(SEGMENTS)
    # cama de ambiente contínua (baixa), um pouco mais presente no congelamento final.
    # Rampa de BED_RAMP_S: o degrau seco volume='if(gte(t,X),2.2,1)' gerou estalo quando a voz parou.
    tail = t
    parts.append(f"[{nb}:a]atrim=duration={total_s:.3f},asetpts=PTS-STARTPTS,volume={gain_to(BED_LUFS, BED, 0, total_s):.2f}dB,"
                 f"volume='1+{BED_TAIL_BOOST}*clip((t-{tail - 0.1:.2f})/{BED_RAMP_S},0,1)':eval=frame,"
                 f"afade=t=in:d=0.3,afade=t=out:st={min(total_s, bed_len) - 1.2:.3f}:d=1.2,apad=whole_dur={total_s:.3f}[bed]")
    mixes.append("[bed]")
    parts.append("".join(mixes) + f"amix=inputs={len(mixes)}:normalize=0:duration=longest,"
                 f"highpass=f=60,atrim=duration={total_s:.3f}[amb]")
    d = int(NARR_OFFSET * 1000)
    # depois de loudnorm/adelay os timestamps ficam tortos: asetpts=N/SR/TB ANTES do atrim, senão a faixa sai mais curta
    parts.append(f"[{nb + 1}:a]aformat=channel_layouts=stereo,highpass=f=80,"
                 "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
                 f"loudnorm=I={VO_LUFS}:TP=-2:LRA=9,aresample=48000,adelay={d}|{d},asetpts=N/SR/TB,"
                 f"apad=whole_dur={total_s:.3f},atrim=end={total_s:.3f},asplit=2[vo][key]")
    parts.append("[amb][key]sidechaincompress=threshold=0.04:ratio=5:attack=25:release=350[ambd]")
    parts.append("[vo][ambd]amix=inputs=2:normalize=0:duration=first[mix]")
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for f, _, _ in SEGMENTS:
        args += ["-i", str(TAKES / f)]
    args += ["-i", str(BED), "-i", str(NARR), "-filter_complex", ";".join(parts),
             "-map", "[mix]", "-ar", "48000", "-ac", "2", str(OUT / "mix_pre.wav")]
    run(args)
    # loudnorm em duas passagens (medição + aplicação linear) para o padrão de redes sociais
    ln = f"loudnorm=I={MASTER['I']}:TP={MASTER['TP']}:LRA={MASTER['LRA']}"
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(OUT / "mix_pre.wav"),
                        "-af", ln + ":print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    i = p.stderr.rindex("{")
    m = json.loads(p.stderr[i:p.stderr.index("}", i) + 1])
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(OUT / "mix_pre.wav"), "-af",
         f"{ln}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
         f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
         "-ar", "48000", str(OUT / "mix.wav")])


if __name__ == "__main__":
    check()
    OUT.mkdir(exist_ok=True)
    args = sys.argv[1:]
    if "audio" not in args:
        video()
    if "video" not in args:
        audio()
    print("ok:", OUT / "base.mp4", OUT / "mix.wav")
