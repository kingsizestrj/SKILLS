# Edição no HyperFrames: dos takes aprovados ao MP4 entregue

Pipeline de edição de qualquer vídeo realista da Voltec com a persona (qualquer campanha, estação, tema ou cenário): HyperFrames 0.8.161, ffmpeg 8.0.1, Python 3 (só biblioteca padrão, sem numpy), Node 22. Caso de referência testado: o Reels "Verão Conectado" (15/10/2026, entregue na v5).

Os moldes foram testados com os arquivos reais do Verão Conectado, preenchidos com os valores dele (conferido de novo em 15/10/2026, depois da generalização):
- `prep.py` gerou a mesma base de vídeo (md5 dos quadros igual). O mix saiu igual a menos de ±2 LSB, a mesma variação que o ffmpeg tem entre duas execuções.
- `build_legendas.py` regravou o `index.html` entregue byte a byte.
- `index_template.html`, com os tokens preenchidos, renderizou um MP4 idêntico, byte a byte, ao v5 entregue (master sem legenda).

Neste guia, o que é **geral** vale para qualquer anúncio com IA. O que aparece como **Voltec:** é exemplo do projeto da Voltec ou dado dela; o que é só da campanha Verão Conectado traz esse nome e muda num vídeo novo (seção 12). O que muda a cada vídeo é **slot**: textos da tela, tempos, trechos dos takes, narração e cama. A seção 13 diz como preencher o template e os scripts, com o Verão Conectado como exemplo preenchido.

Os scripts ficam em `scripts/`, na pasta da skill. Os comandos usam `$SKILL` (essa pasta), `$PROJ`, `$HF`, `$QA`, `$FERR` e `NODE_PATH`, todos definidos no preâmbulo da seção 2. Repita o preâmbulo em cada chamada do Bash, porque as variáveis não passam de uma chamada para outra. Os caminhos relativos `snapshots/`, `takes/`, `audio/` e `qa/` partem de `$PROJ`; `assets/`, `media/` e `renders/` partem de `$HF`. `prep.py`, `build_legendas.py` e `index_template.html` são **moldes**: copie para o projeto, preencha os tokens do index e os campos `PREENCHA` dos scripts (seção 13).

---

## 0. Fluxo em uma tela

```
snapshots aprovados ──(normalizar 9:16 se precisar)──> start_frame dos vídeos (Veo)
takes Veo: 1080x1920, 24 fps, 8,000 s = 192 quadros, H.264 + AAC 48 kHz estéreo
   └─ QA de cada variação (qa-checklist.md) → escolher in/out em QUADROS → SEGMENTS
narração final (WAV 48 kHz + <nome>_alignment.json) + cama de SFX (audio/ambiente_sfx.mp3, ≥ duração final)
   └─ prep.py → media/base.mp4 (vídeo cortado, fim congelado, grão) + media/mix.wav (−14 LUFS)
index.html (de scripts/index_template.html, tokens preenchidos, seção 13) + assets/ (logos + qr.svg gerado ANTES do render, seção 11.1)
   + build_legendas.py (legendas pelo alignment)
   └─ busca de tokens vazia → lint/check → render SEM legenda e COM legenda (--variables) a 24 fps
   └─ versões Instagram (ffmpeg, faststart) → QR decodificado (11.2) + QA final (qa-checklist.md) → entrega
```

## 1. Pastas do projeto

O layout abaixo é geral. Ele separa o que é gerado (caro) do que é edição (barata e refazível).

```
$PROJ/          = $HOME/hyperframes/<campanha>
  prompts/      textos finais enviados (snapshots, vídeo, negativos, narração)
  bodies/       corpos JSON enviados à API (um por geração)
  refs/         referências de persona (recortes sem logo/dedos)
  locais/       fotos reais com licença + creditos.json
  snapshots/    PNGs gerados (+ normalizados/ em 1080x1920) e *_ids.json
  takes/        MP4 baixados (<nome>_<generation_id>.mp4) e *_ids.json
  audio/        narração (wav + _alignment.json), frases regravadas, cama SFX, COMO_FOI_MONTADA_*.txt
  qa/           = $QA: folhas, tiras, quadros do QR, espectrogramas e STT do QA (qa-checklist.md)
  reels-final/  = $HF: projeto HyperFrames (index.html, prep.py, build_legendas.py, assets/, media/, renders/)
```

**Voltec (Verão Conectado):** o projeto de referência fica em `/home/syllas/hyperframes/voltec-reels-ia/`, com a edição em `reels-final/`. É só para leitura: os comandos desta página gravam arquivos, então rode-os num projeto novo. Os takes usados estão em `takes/T1r_veo_v1_*.mp4`, `takes/T2r_veo_v1_*.mp4` e `takes/T3r_veo_v2_*.mp4`, e a narração final em `audio/narracao_v3.wav`.

O projeto HyperFrames não precisa de `hyperframes init`: uma pasta com `index.html`, `assets/` e `media/` já passa no lint e renderiza (testado na 0.8.161). O `init` só acrescenta package.json com a versão fixada, CLAUDE.md e meta.json.

```bash
# antes destas linhas: o preâmbulo da seção 2
mkdir -p "$HF"/{assets,media,renders} "$QA"
cp "$SKILL/scripts/index_template.html" "$HF/index.html"
cp "$SKILL/scripts/prep.py" "$SKILL/scripts/build_legendas.py" "$HF/"
# Voltec: logo oficial para fundo claro (NUNCA redesenhar a logo)
cp /home/syllas/hyperframes/verao-conectado/assets/logo-voltec.png "$HF/assets/logo.png"
cp "$HF/assets/logo.png" "$HF/assets/logo-cta.png"   # o CTA usa uma cópia do mesmo PNG
# QR: gere AGORA o "$HF/assets/qr.svg" com a URL respondida no portão 1 (seção 11.1), antes do prep.py e do render
```

O template carrega `assets/logo.png` (cartão da marca), `assets/logo-cta.png` e `assets/qr.svg` (cartão final). Sem `--no-best-effort`, o render não falha quando falta um deles: o vídeo sai sem a imagem que faltou, por exemplo o CTA sem QR (seções 9 e 11.1).

## 2. Preâmbulo (em toda chamada do Bash) e ferramentas (uma vez por máquina)

```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
```

- Nunca aponte `PROJ` para `/home/syllas/hyperframes/voltec-reels-ia/`: é o projeto de referência do Verão Conectado, só para leitura.
- O `NODE_PATH` fica escrito por extenso de propósito: num mesmo `export`, o `$FERR` ainda não vale (testado no bash).
- `hyperframes --version` deve mostrar `0.8.161`, a versão usada e testada. Chame com `npx --no-install hyperframes ...` (como na sessão) ou só `hyperframes ...`.
- `ffmpeg` e `ffprobe` no PATH. O `drawtext` das tiras de QA usa a fonte padrão do sistema (fontconfig).
- Pacotes npm do QR (`qrcode`, `jsqr`, `pngjs`), uma vez por máquina, em `$FERR`, **fora** do projeto do vídeo. Precisa de rede na 1ª vez:
  ```bash
  [ -d "$FERR/qr/node_modules/jsqr" ] || (mkdir -p "$FERR/qr" && cd "$FERR/qr" && npm i qrcode@1.5.4 jsqr@1.4.0 pngjs@7.0.0)
  ```
  `scripts/decode.cjs` e o gerador de QR (seção 11) acham os pacotes pelo `NODE_PATH` do preâmbulo.
- Esta máquina usa locale pt_BR: o `awk` escreve "3,11" em vez de "3.11", e o `printf` do bash recusa "3.5" ("número inválido"). O ffmpeg só aceita ponto. Conta com decimal no shell vai com `LC_ALL=C` na frente (exemplo em `qa-checklist.md` §C.4).

## 3. Snapshots em 9:16

- O `gpt-image-2.5-sunburst` em `9:16` + `2K` sai em 1152x2048, que já é 9:16 exato. O `gemini-3-pro-image` 2K sai em 1536x2752, que **não** é 9:16 exato.
- Na sessão, o Veo recebeu o snapshot aprovado direto da geração: `"start_frame": {"type": "generation", "generation_id": "<id do snapshot>"}`. Nesse caso não é preciso normalizar.
- Normalize quando o snapshot não for 9:16 exato, quando for subir como asset (start_frame/end_frame) ou para comparação lado a lado. O comando abaixo recorta para 9:16 e escala com lanczos. Ele reproduziu exatamente os arquivos de `snapshots/normalizados/` da sessão:
  ```bash
  ffmpeg -i snapshots/T1_id_a_<id>.png \
    -vf "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920:flags=lanczos" \
    -pix_fmt rgb24 -frames:v 1 snapshots/normalizados/T1_a_id_1080x1920.png
  ```
  O `-pix_fmt rgb24` tira o canal alfa. A revisão técnica alertou que um PNG RGBA pode ser recusado como frame.

## 4. Escolher os trechos: in/out em quadros de 24 fps

O take do Veo tem 192 quadros (0–191). Quadro = segundos × 24. Escolher bem o trecho resolve muita coisa sem gerar de novo.

1. **Faça o QA de cada variação** (contact sheet, tiras, STT; ver `qa-checklist.md`) e anote em que quadro começa cada defeito.
2. **Ache o quadro exato** com uma tira numerada, a 24 fps no ponto crítico e a 8 fps nos movimentos de mão ou objeto:
   ```bash
   # quadros 96–107 do take, recorte na boca, cada quadro com o número (24 fps)
   ffmpeg -i takes/T1_veo_v1_<id>.mp4 -vf "select='between(n\,96\,107)',crop=480:420:300:420,scale=240:-2,\
   drawtext=text='%{eif\:round(t*24)\:d}':x=6:y=6:fontsize=24:fontcolor=yellow:box=1:boxcolor=black@0.6,\
   tile=12x1:padding=4:color=white" -fps_mode passthrough -frames:v 1 qa/T1v1_boca.jpg
   # um quadro só, pelo número
   ffmpeg -i takes/T1_veo_v1_<id>.mp4 -vf "select=eq(n\,101)" -fps_mode passthrough -frames:v 1 qa/f101.png
   ```
   **Voltec (Verão Conectado):** nessa tira do T1 v1, os lábios começam a se projetar em 101–102 e abrem em "O" a partir de 103. O corte `(in 12, 89 quadros)` usa os quadros 12–100 e para antes do defeito. Foi a correção imediata, sem custo, do feedback "parece que está falando um O".
3. **Monte o `SEGMENTS`** do `prep.py`: `(arquivo, quadro_inicial, nº_de_quadros)`. O `trim` usa `end_frame` exclusivo, ou seja, `(19, 89)` = quadros 19–107.
4. **Ancore os cortes na narração.** Cada corte cai logo antes do início de uma frase, e o fim do último take congela por baixo do CTA (`TOTAL` maior que a soma dos trechos). Deixe cerca de 1 s depois da última palavra.

**Voltec (Verão Conectado v5), exemplo preenchido do `SEGMENTS`:**

| Take | Arquivo | In | Quadros | No vídeo | Por quê |
|---|---|---|---|---|---|
| T1 | `T1r_veo_v1_bICA18jbanp0KfqE3fgS.mp4` | 19 | 89 | 0–3,71 s | celular erguido, desce e franze a testa, boca fechada |
| T2 | `T2r_veo_v1_RvTRU6nLzVKOEUqVWUh5.mp4` | 62 | 101 | 3,71–7,92 s | sorri com o celular firme (a v2 deformava o celular ao abaixar) |
| T3 | `T3r_veo_v2_R41wQEvLdexHBvaXIRsl.mp4` | 5 | 187 | 7,92–15,71 s | selfie na areia |
| congelado | último quadro do T3 | — | 115 | 15,71–20,5 s | por baixo do CTA |

`TOTAL = 492` quadros (20,5 s). A fala vai até 19,44 s, e "Agora" (3,82 s) e "Tem Voltec" (7,93 s) começam logo depois dos cortes. Num vídeo novo, o número de takes, os trechos e o `TOTAL` saem do roteiro de takes e da narração dele.

## 5. `prep.py`: base de vídeo e mixagem

```bash
cd "$HF"                 # depois do preâmbulo da seção 2
python3 prep.py          # vídeo + áudio  ->  Verão Conectado: "377 quadros de takes + 115 congelados = 492 (20.50 s)"
python3 prep.py audio    # só o áudio (troca de narração, ganhos, cama)
python3 prep.py video    # só o vídeo (troca de take/in/out)
```

Edite só o bloco `CONFIGURAÇÃO`. `SEGMENTS`, `TOTAL` e `NARR` mudam a cada vídeo: começam vazios, e o script para com uma mensagem até você preencher (seção 13.3; o exemplo do Verão Conectado fica nos comentários). Ele também para se `TOTAL` vier em segundos ou se um trecho do `SEGMENTS` tiver número quebrado. `NARR_OFFSET` (0,30 s), `BED`, `TAKES` e os níveis são o padrão testado. Por padrão `PROJ` é a pasta acima do projeto HyperFrames; para apontar outra, use a variável de ambiente `REELS_PROJ`.

- `BED` padrão: `audio/ambiente_sfx.mp3` (no Verão Conectado era `audio/ambiente_praia_sfx.mp3`). A cama deve durar pelo menos `TOTAL/24` s (pedido à API: no máximo 30 s; `api-elevenlabs.md` §7). O `prep.py` corta o que sobra e completa com silêncio o que falta. O texto da cama é da cena da campanha.

### Vídeo
- `trim` por quadro → `concat` → `tpad=stop_mode=clone:stop=<TOTAL−soma>` congela o último quadro por baixo do CTA. Uma base única pré-cortada é mais robusta que vários clipes na composição.
- `noise=alls=3:allf=t` aplica grão temporal leve, igual em todos os takes.
- Codificação H.264 CRF 18, preset medium, GOP 24, `-r 24`, sem áudio → `media/base.mp4`.

### Áudio: o que cada etapa faz

| Etapa | Valor | Por quê |
|---|---|---|
| Som nativo de cada take | normalizado a **−30 LUFS** (medido com `ebur128` na janela usada) | ambiente real do celular, baixo |
| J-cut / L-cut | **0,2 s** | o som do take seguinte entra antes da imagem; o anterior deixa um rabo; fades nas bordas |
| Cama de SFX contínua | **−36 LUFS**; fade-in 0,3 s; fade-out 1,2 s | cola os cortes; nunca silêncio absoluto entre takes |
| Cama no congelamento | ×2,2 com **rampa de 0,8 s** | dá presença ao fim sem voz; **nunca degrau** |
| Ambiente somado | passa-alta 60 Hz | tira o subgrave abaixo de 60 Hz |
| Narração | passa-alta 80 Hz → compressor 3:1 (−20 dB, 5/120 ms, makeup 2) → `loudnorm` **−16 LUFS**, TP −2, LRA 9 → `aresample=48000` → `adelay` NARR_OFFSET | voz seca e próxima, nível estável |
| Ducking | `sidechaincompress` threshold 0,04, ratio 5, attack 25 ms, release 350 ms (chave = voz) | o ambiente abaixa sob a fala e volta nas pausas |
| Master | `loudnorm` em **2 passagens**: −14 LUFS, −1,5 dBTP, LRA 11, `linear=true` | padrão de redes; medido no v5: −14,0 LUFS e −1,7 dBTP |
| Música | nenhuma | parece mais vídeo real de celular (decisão aprovada) |

Se o cliente pedir música, a pesquisa recomenda deixá-la entre −18 e −24 dB sob a voz. Isso não foi testado na sessão.

### Armadilhas do ffmpeg que pegaram
1. **Depois de `loudnorm` ou `adelay`, rode `asetpts=N/SR/TB` antes do `atrim`.** Sem isso os timestamps ficam tortos e a faixa sai mais curta.
2. **O `loudnorm` só aceita TP de −9 a 0.**
3. **O `loudnorm` devolve 192 kHz** (conferido). Por isso o `aresample=48000` vem logo depois.
4. **Nunca use degrau de ganho.** `volume='if(gte(t,X),2.2,1)'` gerou um estalo em 15,41 s. Enquanto a voz cobria, ninguém ouviu; com a frase nova, o ponto caiu numa pausa e ficou exposto. Use rampa: `volume='1+1.2*clip((t-X)/0.8,0,1)':eval=frame`, ou fades.
5. **Use `amix=...:normalize=0`.** Com o padrão, o amix reescala as entradas e muda os níveis calibrados.
6. **Na 2ª passagem do master, passe os valores medidos** (`measured_I/TP/LRA/thresh`, `offset`) e `linear=true`. O `prep.py` lê o JSON do stderr da 1ª passagem.

## 6. Narração: gerar, conferir, trocar uma frase e registrar

O guia de bolso da API está em `api-elevenlabs.md`. Aqui vai só o que a edição precisa.

### 6.1 Gerar com timestamps
Gere a narração inteira numa request, para a prosódia ser contínua. O `scripts/el.py tts` grava `<saída>.wav` e `<saída>_alignment.json`, o formato que `build_legendas.py` e `stress.py` leem.

```bash
python3 -I "$SKILL/scripts/el.py" tts <voice_id> bodies/tts_v1_s20261015.json audio/narracao_v1_s20261015   # GASTA ~1 crédito/caractere
```

Convenção de nomes da skill (projetos novos): `bodies/tts_<vN>_s<seed>.json` → `audio/narracao_<vN>_s<seed>.wav` + `audio/narracao_<vN>_s<seed>_alignment.json`. No Verão Conectado os nomes eram outros (`narracao_radassa100.wav`, `narracao_v2_A_s1.wav`, `narracao_v3.wav`).

`bodies/tts_v1_s20261015.json` (o texto é o roteiro inteiro, com as tags; este é o do Verão Conectado):
```json
{"text": "[frustrated] Casa de praia sem internet? Ninguém merece...\n[relieved, smiling] Agora sim! Com a Voltéc eu fico conectada o verão inteiro.\n...",
 "model_id": "eleven_v4", "language_code": "pt",
 "voice_settings": {"stability": 0.45, "similarity_boost": 0.85},
 "apply_text_normalization": "auto", "seed": 20261015}
```

**Voltec:** a voz é "Radassa 100%" `4yvYc2GSakxLWMhlsd6b`. "Voltéc" é a grafia fonética para sair vol-TÉC; na tela, o `FIX` do `build_legendas.py` escreve "Voltec". As tags `[frustrated]` e afins não são lidas em voz alta (duram ~0,1 s no alignment).

### 6.2 Conferir a tônica da marca
Faça isso antes de mostrar ao cliente. É heurística, e você não ouve áudio: confira também o texto com STT (`stt.py`, inteiro e em janela com `--ss/--t`) e liste na página do portão o instante de cada "Voltec" para o cliente ouvir.

```bash
python3 -I "$SKILL/scripts/stress.py" audio/narracao_v1_s20261015.wav audio/narracao_v1_s20261015_alignment.json
#   Voltéc @5.12s  'Vol' 120 ms rms 1770 | 'téc' 200 ms rms 5676  -> tônica no fim   (saída real do narracao_v2_A_s1.wav)
python3 -I "$SKILL/scripts/stress.py" --palavra 'Grussaí' --corte 4 audio/narracao_v1_s20261015.wav audio/narracao_v1_s20261015_alignment.json
```

### 6.3 Trocar uma frase sem regravar tudo
Na sessão, o CTA mudou de "link na bio" para "Saiba mais + QR".

**1. Gere só a frase nova.** Use a mesma voz e os mesmos settings, um seed novo e `previous_text` com as frases que vêm antes (na sessão, as frases 3 e 4). Saíram 3 versões (seeds 20261015, 20261016 e 20261017, em `audio/cta_v3_<seed>.wav`), e a escolhida foi a 20261017.

```bash
python3 -I "$SKILL/scripts/el.py" tts <voice_id> bodies/cta_v3_20261017.json audio/cta_v3_20261017   # GASTA créditos
```

Corpo (reconstruído; o JSON do TTS não foi salvo na sessão). Grave-o em `bodies/cta_v3_20261017.json` antes de rodar o comando acima:
```json
{"text": "[excited] Clica no botão Saiba Mais ou escaneia o QR code na tela!",
 "model_id": "eleven_v4", "language_code": "pt",
 "voice_settings": {"stability": 0.45, "similarity_boost": 0.85},
 "apply_text_normalization": "auto", "seed": 20261017,
 "previous_text": "Tem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra. Sem fidelidade: planos de dois a cinco meses."}
```
O registro (`audio/COMO_FOI_MONTADA_narracao_v3.txt`) diz só "previous_text = frases 3 e 4"; não se sabe se a tag `[upbeat]` foi junto.

**2. Emende num ponto de silêncio** (fade de 20 ms, alguns centésimos de silêncio e ganho para casar com a frase anterior). Na sessão: corte em 15,05 s (silêncio depois de "meses"), 0,17 s de silêncio e −3 dB na frase nova. Este comando reproduz o `narracao_v3.wav` byte a byte (conferido de novo em 15/10/2026). Rode dentro de `audio/` de um projeto NOVO, trocando os nomes, o ponto de corte e o ganho:

```bash
ffmpeg -i narracao_v2_A_s1.wav -i cta_v3_20261017.wav -filter_complex \
"[0:a]atrim=end=15.05,asetpts=N/SR/TB,afade=t=out:st=15.03:d=0.02[a];\
anullsrc=r=48000:cl=mono,atrim=duration=0.17[g];\
[1:a]aresample=48000,aformat=channel_layouts=mono,volume=-3.0dB,asetpts=N/SR/TB[b];\
[a][g][b]concat=n=3:v=0:a=1[out]" -map "[out]" -ar 48000 -ac 1 narracao_v3.wav
```

**3. Junte os alignments**, deslocando a frase nova em corte + silêncio (na sessão, 15,05 + 0,17 = 15,22 s). Use o código de `api-elevenlabs.md` §5.5 (passo 3), a única versão na skill: ele reproduz as palavras e os tempos usados nas legendas. Grave a saída com nome novo, nunca por cima do alignment aprovado. No Verão Conectado, a saída foi `audio/narracao_v3_alignment.json`.

**4. Atualize e refaça.** Ajuste `NARR`, `TOTAL` (o vídeo passou de 19 s para 20,5 s), `PHRASES`, `CTA_START`, os tempos `T` do index e a duração (5 lugares). Depois rode `python3 prep.py audio` e `python3 build_legendas.py` e renderize as duas versões.

### 6.4 Registrar e conferir
- **Registre SEMPRE como a narração final foi montada**, num `audio/COMO_FOI_MONTADA_<nome>.txt` (origem, settings, seed, corte, ganho, comando) e no `prompts/narracao_vN.txt`. Sem isso, uma regeração futura traz o texto antigo de volta.
- Confira o texto falado com STT (`qa-checklist.md`, seção C).

## 7. A composição (`index.html`)

Comece de `scripts/index_template.html`. É o index do v5 generalizado: os textos da campanha viraram tokens `__X__` (gancho, título do cartão da marca e oferta; tabela na seção 13), o ícone do cartão é opcional (`#icone`), os tempos estão reunidos num objeto `T`, os assets têm nomes genéricos (`assets/logo.png`, `assets/logo-cta.png`, `assets/qr.svg`) e os marcadores de legenda estão vazios. Os outros pontos de troca estão marcados com `EDITAR`. Cidades, cores, fontes, logo e o CTA de anúncio pago são fixos da Voltec e ficam como estão.

### Estrutura que o HyperFrames exige
- O root tem `data-composition-id="main"`, `data-start="0"`, `data-duration`, `data-fps="24"`, `data-width="1080"` e `data-height="1920"`.
- `<video id="base" class="clip" src="media/base.mp4" muted ...>` leva o vídeo **mudo**. O som entra separado, em `<audio id="mix" src="media/mix.wav">`.
- `<div id="gfx" class="clip">` contém todos os overlays.
- Há uma timeline GSAP `paused: true`, registrada em `window.__timelines["main"]`, terminando com `tl.set({}, {}, DUR)`.
- Só lógica determinística: nada de `Date.now()`, `Math.random()` ou fetch.
- **A duração aparece em 5 lugares:** root, `#base`, `#mix`, `#gfx` e `DUR`. Tem de ser `TOTAL/24` do `prep.py`.

### Layout (geral)
- **Zona segura do Reels: texto só em x 64–930 e y 220–1480.** Topo, rodapé e a coluna de botões à direita ficam livres. Nunca ponha texto sobre o rosto ou sobre o objeto que a pessoa segura.
- **Legenda logo abaixo do rosto (y ≈ 1000) e acima dos cartões.** Ela some quando entra o CTA. Quando cobriria o objeto na mão, vai para a posição baixa daquele trecho (classe `low`, ver seção 8).
- **Cartões brancos** (`.card`, raio 26 px, sombra suave). Logo para fundo claro sempre sobre painel branco.
- **Texto de gancho no estilo nativo do Instagram:** caixa branca, Montserrat 800, numa área lisa e livre do quadro, do lado oposto ao braço erguido. Deixe essa área livre já no snapshot. **Verão Conectado:** o céu, no alto à direita do take 1.
- **CTA sobre o vídeo desfocado e escurecido.** O vídeo ganha `blur(14px)`, o véu escuro sobe e o cartão central entra com leve escala.

### Tempos: ancore no alignment (+ NARR_OFFSET) e nos cortes (quadros/24)
Regra que funcionou: o elemento entra entre 0 e 0,15 s **antes** da palavra.

| Elemento (ex.: Verão Conectado v5) | Tempo | Âncora |
|---|---|---|
| Gancho `#q1` | 0,30–3,52 s | take 1 (0–3,71 s) |
| Cartão da marca | 3,85–7,72 s | "Agora" em 3,82 s |
| Cidades acendem | 8,50 / 9,25 / 9,92 / 10,95 s | Grussaí 8,62 · Atafona 9,38 · Chapéu 10,06 · São 11,10 |
| Oferta | 12,30 (+ sub 13,55) – 15,30 s | "Sem" 12,30; "planos" 13,46 |
| CTA (blur + véu) / cartão | 15,40 / 15,55 s | "Clica" 15,59 s |
| Pulso "Saiba mais" / QR | 16,35 / 17,90 s | "Saiba" 16,40 · "QR" 17,96 |

Para tirar os tempos de qualquer palavra (rode em `$PROJ`; o arquivo é o mesmo do `ALIGN` do `build_legendas.py`):
```bash
python3 -I - <<'EOF'
import json
a = json.load(open("audio/narracao_v3_alignment.json")); t = "".join(a["characters"])   # Verão Conectado; troque pelo ALIGN
for w in ["Agora", "Grussaí", "Saiba", "QR"]:   # palavras-âncora do Verão Conectado; troque pelas do roteiro novo
    i = t.find(w); print(w, round(a["character_start_times_seconds"][i] + 0.30, 3))   # + NARR_OFFSET
EOF
```

### Detalhes que deram problema e a correção
- **O blur puxa o preto de fora do quadro para as bordas.** A escala tem de subir **junto** com o blur: escala ≥ 1 + 6σ/largura, ou seja, 1,08 para blur de 14 px (`tl.to("#base", {filter: "blur(14px)", scale: 1.08, ...})`).
- **Um pulso de escala numa palavra inline encostou na palavra anterior.** Use `display: inline-block` e `transform-origin` no lado fixo (`#saiba { transform-origin: 0% 60% }`).
- **Lista que acende no ritmo da fala:** o cartão mostra todos os itens com opacity 0,3 e cada um vai a 1 na sua palavra, com o pino pulando.
- **Oferta com revelação por `clip-path`** (`inset(0 100% 0 0)` → 0), que o lint aceita.

## 8. Legendas: versão com e sem, pelo mesmo index

- A variável fica declarada no `<html>`: `data-composition-variables='[{"id":"legendas","type":"boolean","label":"Legendas","default":false}]'`. O script lê com `window.__hyperframes.getVariables()`; sem a variável, o container `#legendas` é escondido.
- **`build_legendas.py`** (copie para o projeto HyperFrames e edite o topo):
  - **Projeto novo:** `ALIGN`, `PHRASES` e `CTA_START` (= `T.cta` do index) começam vazios, e o script para com uma mensagem até você preencher (seção 13.4). `START_FIX` e `LOW_RANGES` começam vazios (`[]`) e só são preenchidos depois de medir com `stt.py --ss/--t` (e de ver a legenda cobrindo o objeto, no caso do `LOW_RANGES`). Os valores do Verão Conectado ficam só nos comentários do molde.
  - `ALIGN` aponta para o alignment da narração FINAL, com emendas já deslocadas: `audio/narracao_<vN>_s<seed>_alignment.json` ou o da narração emendada (seção 6.3). No Verão Conectado, `audio/narracao_v3_alignment.json`.
  - `NARR_OFFSET` tem o mesmo valor do `prep.py`.
  - `PHRASES` traz os blocos **definidos à mão**, como frases naturais. O script confere palavra por palavra e para com `AssertionError` se o texto não bater.
  - `FIX` converte a grafia fonética/por extenso para a grafia na tela. `"Voltéc" → "Voltec"` é fixo da Voltec e já vem no molde. Os números falados por extenso que devem sair em algarismo são da campanha (Verão Conectado: `"dois" → "2"`, `"cinco" → "5"`); nunca ponha `"um"`, que também é artigo. O `PHRASES` já vem escrito com a grafia de tela.
  - `START_FIX` corrige inícios que o alignment errou. Na sessão, o alignment criou uma pausa inexistente antes de "internet?" (+0,25 s) e atrasou "Voltec" ~0,1 s; o Verão Conectado usou `[("internet?", 1, 1.38), ("Voltec", 1, 5.32), ("Voltec", 2, 8.03)]`. Meça no áudio com STT de janela (`python3 -I "$SKILL/scripts/stt.py" audio/narracao_<vN>_s<seed>.wav --ss 1.0 --t 1.5`) e some o `NARR_OFFSET`.
  - `CTA_START` é quando as legendas somem (entrada do cartão final) = `T.cta`. Verão Conectado: 15.40.
  - `LOW_RANGES` lista os trechos em que a legenda vai para a posição baixa. Verão Conectado: `[(0.0, 3.70)]`, porque no take 1 a legenda baixa deixava o celular livre.
  - `MAX_CHARS = 21` é o bloco mais longo que coube numa linha nesse layout (Montserrat 800, 54 px, 866 px de largura); fica igual em todo vídeo. No Verão Conectado, foi "planos de 2 a 5 meses".
  ```bash
  python3 build_legendas.py     # imprime um bloco por linha (Verão Conectado: "  0.32-  1.13  Casa de praia" ...) e grava os blocos no index.html
  ```
- A palavra falada ganha destaque (`#ffd36b`) do seu início até o início da próxima palavra.
- Ligação de palavras engana o STT; mostre esses pontos ao cliente. **Verão Conectado:** o STT ouviu "conectado" no lugar de "conectada" (ligação "conectada‿o"). Se incomodar, regere só a frase com vírgula ("conectada, o verão inteiro") e emende (seção 6).

## 9. Lint, check e render

```bash
cd "$HF"                              # depois do preâmbulo; assets/qr.svg já gerado (seção 11.1)
V="<campanha>_vN"                     # Verão Conectado v5: V=verao-conectado-reels-ia_v5
grep -n '__[A-Z0-9_]*__' index.html   # tem de sair vazio: token que sobrou vira texto na tela (seção 13; qa-checklist.md §C.0)
npx --no-install hyperframes lint     # rápido
npx --no-install hyperframes check    # lint + runtime + layout + motion + contraste (abre Chrome)
npx --no-install hyperframes render -o "renders/$V.mp4" --fps 24 --quality delivery --no-best-effort
npx --no-install hyperframes render -o "renders/${V}_legendas.mp4" --fps 24 --quality delivery --no-best-effort \
    --variables '{"legendas":true}'   # opcional: --strict-variables falha se a variável não existir
```
- **`--no-best-effort`: o render da 0.8.161 é best-effort por padrão.** Se falta mídia (um `assets/qr.svg` que não foi gerado, por exemplo), ele termina sem erro, só com o aviso `[media_load_failed] image media failed to load before capture`, e o CTA sai sem QR. Com `--no-best-effort`, o mesmo caso falha ("Render blocked by 1 correctness warning") e não grava o MP4. Testado em 15/10/2026 numa composição mínima sem o QR; o index do v5, com toda a mídia, renderizou com a flag (teste em `--quality draft`). Se ela bloquear, leia o aviso e corrija a mídia: não tire a flag para "passar".
- **Comandos demorados:** rode `check` e `render` com timeout de 600000 ms no Bash ou em segundo plano (o tempo do render está no item `--quality delivery`, abaixo).
- **Use sempre `--fps 24`.** As fontes são 24 fps, e a 30 fps o render cria judder com quadros duplicados. Sem a flag, o CLI usa o `data-fps` do root e, na falta dele, 30.
- **`--quality delivery`:** H.264 High, 1080x1920, yuv420p, bt709, AAC 48 kHz estéreo a 192 kb/s. O v5 saiu com x264 CRF 15, ~39 Mb/s e ~100 MB para 20,5 s, já com o moov no início. Leva ~2 min nesta máquina.
- **Regras do lint/check que pegaram (0.8.161):**
  - `gsap_non_transform_motion` **(erro)**: tween de propriedade de layout. No teste, `marginTop` disparou a regra. Anime só `opacity`, `transform` (x/y/scale/rotation) ou `clip-path`; a sessão também evitou animar `height`.
  - **Estado inicial escondido no CSS** (`#brand, #cities, #offer, #cta { opacity: 0 }`), e não com `tl.set(..., 0)`. É regra da sessão.
  - `nested_structure_needs_subcomposition` **(aviso)** sobre o `#gfx`. Aparece também no v5 entregue e não afeta o render, só a visualização no Studio.
  - `container_overflow` **(info)** de `g.gira` dentro do `#icone` no check (no index do Verão Conectado, o `#sun-rays`): os raios giram para fora da caixa do ícone. Inofensivo.
  - `page_error` **(erro do check)** `oferta: N linha(s) .offer-sub no HTML e M instante(s) em T.offerSub`: é a trava do template. Iguale as linhas da oferta e os instantes. O lint não pega (é erro de execução); o `render --no-best-effort` bloqueia com `sub_timeline_script_failure` e não grava o MP4 (testado em 15/10/2026). Por isso rode o `check` antes do render.
- Fontes: o compilador baixa as Google Fonts do `<link>` (no template, com `display=block`) e guarda em cache (`~/.cache/hyperframes/fonts`).

## 10. Versões para Instagram e entrega

Recodificação usada (os parâmetros x264 batem com os do arquivo entregue): CRF 19 com teto de 20 Mb/s, level 4.2, AAC 256k e faststart. Resultado: ~16 Mb/s, ~42 MB.
```bash
cd "$HF"                 # depois do preâmbulo
V="<campanha>_vN"        # Verão Conectado v5: V=verao-conectado-reels-ia_v5
for v in "$V" "${V}_legendas"; do
  ffmpeg -loglevel error -y -i "renders/$v.mp4" -c:v libx264 -preset slow -crf 19 -maxrate 20M -bufsize 40M \
    -profile:v high -level 4.2 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart "renders/${v}_instagram.mp4"
done
```
- O `-y` importa: sem ele, o ffmpeg pergunta antes de sobrescrever e, sem terminal, não sobrescreve. Ao renderizar de novo a mesma vN, as versões Instagram ficariam velhas.
- Rode o QA final (`qa-checklist.md`, seção C) **nos 4 arquivos**: master e Instagram, com e sem legenda. O QR tem de ser decodificado também na versão do Instagram (seção 11.2).
- **Entrega:** 4 arquivos com nome de campanha e versão. **Voltec (Verão Conectado):** enviados ao cliente como `Verao_Conectado_REELS_IA_v5_{instagram,master}.mp4` e `..._v5_legendas_{instagram,master}.mp4`; as cópias estão em `/home/syllas/hyperframes/voltec-reels-ia/reels-final/renders/verao-conectado-reels-ia_v5{,_instagram,_legendas,_legendas_instagram}.mp4` (a v3 e a v4 são antigas; a v3 ainda tem o CTA "link na bio").
- Na publicação, ative o rótulo **"Informações de IA"** da Meta (vídeo realista feito com IA). Anúncio pago usa o botão "Saiba mais" + QR; "link na bio" é só para post orgânico.

## 11. Receitas de ajuste rápido (sem gerar de novo) e QR

| Pedido | O que mexer | Comandos |
|---|---|---|
| Defeito num take (boca, mão, objeto) | in/out em `SEGMENTS`; se não houver janela limpa, a outra variação | `python3 prep.py` → render |
| Trocar a variação de um take | arquivo em `SEGMENTS` | `python3 prep.py` → render |
| Trocar uma frase/CTA | seção 6 (frase nova + emenda + alignment) → `NARR`, `TOTAL`, `PHRASES`, `CTA_START`, tempos `T`, duração (5 lugares) | `python3 prep.py` → `python3 build_legendas.py` → render ×2 |
| Legenda cobre o objeto/rosto | `LOW_RANGES` ou o `top` de `.leg.low` | `python3 build_legendas.py` → render com legenda |
| Legenda adiantada/atrasada numa palavra | `START_FIX` (medir com STT de janela) | idem |
| Estalo/degrau no áudio | rampa ou fade no ganho; conferir J/L-cut | `python3 prep.py audio` → render |
| Ambiente alto/baixo | `AMB_LUFS` / `BED_LUFS` | `python3 prep.py audio` → render |
| Mudar texto, cor ou tempo de cartão | `index.html` (texto que entrou no lugar do token, objeto `T`, CSS; seção 13) | lint → check → render |
| Trocar ou tirar o ícone do cartão da marca | `#icone` (troque o desenho ou apague o `<svg>`; seção 13.2) | lint → check → render |
| Trocar o destino do QR | gerar o SVG de novo com a URL nova (11.1) | 11.1 → render ×2 → Instagram → 11.2 |

### 11.1 QR: gerar `assets/qr.svg` ANTES do render

O template carrega `assets/qr.svg` no cartão final (`<img id="qr-img">`). Gere o arquivo logo depois de copiar o template (seção 1), antes do `prep.py` e do render. A URL é a que o cliente respondeu no portão 1; nunca reaproveite a de outra campanha.

```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (seção 2)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
[ -d "$FERR/qr/node_modules/jsqr" ] || (mkdir -p "$FERR/qr" && cd "$FERR/qr" && npm i qrcode@1.5.4 jsqr@1.4.0 pngjs@7.0.0)   # uma vez; rede na 1ª vez
URL_QR="<URL respondida no portão 1>"   # Verão Conectado: https://provedorvoltecinternet.online/?page_id=674
# o destino está no ar? tem de imprimir 200 (o site da Voltec devolve 406 a curl sem headers de navegador)
curl -sS -o /dev/null -w '%{http_code}\n' -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" -H "Accept: text/html" "$URL_QR"
cd "$HF" && node -e '
require("qrcode").toString(process.argv[1], {type: "svg", errorCorrectionLevel: "M", margin: 0,
  color: {dark: "#111111", light: "#ffffff"}}, (e, s) => { if (e) throw e; require("fs").writeFileSync("assets/qr.svg", s); });
' "$URL_QR" && ls -l assets/qr.svg
```
- Pacote npm `qrcode`, nível M, margem 0, módulos #111111 sobre branco. A área clara em volta do QR vem do cartão branco do CTA.
- Com a URL do Verão Conectado, o comando gera um arquivo idêntico, byte a byte, ao `assets/qr-checkout.svg` daquele projeto (conferido em 15/10/2026). Lá o nome era esse; o template da skill espera `assets/qr.svg`.
- **O render é best-effort.** Sem `assets/qr.svg`, o HyperFrames 0.8.161 renderiza sem erro: o CTA sai sem QR, e o log mostra só o aviso `[media_load_failed]`. A falha só aparece na decodificação (11.2), e os renders têm de ser refeitos. Por isso a seção 9 usa `--no-best-effort`, que nesse caso faz o render falhar sem gravar o MP4.

**Voltec (Verão Conectado):** o QR aponta para `https://provedorvoltecinternet.online/?page_id=674`, a página "Verão Conectado 2026", **não** para o WhatsApp. Numa campanha nova, o destino é perguntado ao cliente.

### 11.2 QR: decodificar no vídeo final (master e Instagram)

Depois dos renders (seção 9) e das versões Instagram (seção 10), extraia um quadro do CTA de cada arquivo e decodifique com `scripts/decode.cjs`. Ele tem de imprimir a URL do portão 1. O bloco automático da `qa-checklist.md` §C.1 faz o mesmo em 3 instantes; aqui vai o mínimo:

```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (seção 2)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
URL_QR="<URL respondida no portão 1>"                  # Verão Conectado: https://provedorvoltecinternet.online/?page_id=674
T_QR="<instante com o cartão final inteiro na tela>"   # ~T.ctaCard + 1 s; Verão Conectado: 16.5 (também 18.6 e 20.4)
V="<campanha>_vN"                                      # Verão Conectado v5: V=verao-conectado-reels-ia_v5
for v in "$V" "${V}_instagram" "${V}_legendas" "${V}_legendas_instagram"; do
  ffmpeg -hide_banner -loglevel error -y -ss "$T_QR" -i "$HF/renders/$v.mp4" -frames:v 1 "$QA/${v}_qr.png"
  q=$(node "$SKILL/scripts/decode.cjs" "$QA/${v}_qr.png")
  [ "$q" = "$URL_QR" ] && echo "QR OK: $v" || echo "FALHA QR: $v -> $q"
done
```
- O `decode.cjs` imprime "nenhum QR" e sai com código 1 quando não lê. Se falhar, confira se `assets/qr.svg` existe e tem a URL certa, se o instante cai com o cartão final inteiro na tela e se o log do render tem `media_load_failed`.
- **Voltec (Verão Conectado):** no v5, o QR foi lido na master e no Instagram, com e sem legenda, em 15,9, 16,5, 18,6 e 20,4 s, e também com o quadro reduzido a 540 e a 360 px de largura (conferido de novo em 15/10/2026; teste de robustez em `qa-checklist.md` §C.1).

## 12. Fixos da Voltec × dados da campanha neste pipeline (outro cliente: troque os fixos)

**Fixos da Voltec** (valem em todo vídeo com a persona; ficam no template e nos moldes):
- **Marca:**
  - Logo oficial para fundo claro: `/home/syllas/hyperframes/verao-conectado/assets/logo-voltec.png`. Nunca redesenhar.
  - Cores: `--red #d7262f` e `--dark #2f2f33`.
  - Fontes: Montserrat 800/900 (títulos) e Barlow 600/700 (apoio).
- **Voz:** Radassa 100% `4yvYc2GSakxLWMhlsd6b`, eleven_v4, stability 0.45, similarity 0.85, `"pt"`. Grafia fonética "Voltéc" e "Voltec" na tela (`FIX` do `build_legendas.py`).
- **Cidades:** Grussaí, Atafona, Chapéu do Sol e São João da Barra, nesta ordem (cartão "Tem Voltec em" e linha do CTA).
- **CTA:** o cartão final do template é o de anúncio pago ("ASSINE AGORA", "clique em Saiba mais", QR); narração "Clica no botão Saiba Mais ou escaneia o QR code na tela!". Post orgânico: "link na bio" no cartão e "Assina pelo link na bio!" na voz (`persona-e-marca-voltec.md` §7). Qual dos dois vale é slot de cada vídeo.
- **Áudio:** sem música; mixagem e níveis da seção 5.
- **Layout:** zona segura, cartões brancos, legenda abaixo do rosto, CTA sobre o vídeo desfocado (seção 7).

**Da campanha** (slots: pergunte ou refaça a cada vídeo; como preencher: seção 13). Exemplo preenchido, o Verão Conectado:
- **Caminhos:** `/home/syllas/hyperframes/voltec-reels-ia/` (projeto de referência, só leitura) e `reels-final/` (HyperFrames).
- **Textos da tela:** gancho "Casa de praia" / "sem internet?"; título do cartão "VERÃO" + "CONECTADO", com o sol no `#icone`.
- **Oferta:** "Planos sem fidelidade de 2 a 5 meses" (na tela: "Planos sem fidelidade" / "de 2 a 5 meses").
- **CTA:** anúncio pago (com botão).
- **QR:** `https://provedorvoltecinternet.online/?page_id=674`, a página "Verão Conectado 2026" (seção 11).
- **Cama de SFX:** `audio/ambiente_praia_sfx.mp3`, com o texto da cena de praia no fim de tarde.
- **Trechos e tempos do v5:** `SEGMENTS`/`TOTAL`/`NARR` do `prep.py`, a tabela da seção 7, o objeto `T` do template e, no `build_legendas.py`, `ALIGN`, `PHRASES`, `CTA_START`, `START_FIX`, `LOW_RANGES` e os números do `FIX`, que ficam nos comentários dos moldes.

## 13. Preencher o template para um vídeo novo

Vale para qualquer vídeo da Voltec com a persona. O Verão Conectado é o exemplo preenchido: com os valores da última coluna, o template e os scripts reproduzem o v5 entregue (início deste arquivo). Os textos saem do roteiro aprovado no portão do roteiro (`SKILL.md` §2). Oferta, preço, prazo, CTA (pago × orgânico) e destino do QR vêm sempre do cliente: nunca invente.

Ordem:
1. Copie os moldes e a logo e gere o QR (seções 1 e 11.1).
2. Preencha os tokens do `index.html` (13.1) e decida ícone, oferta e CTA (13.2).
3. Preencha o `prep.py` (13.3) e rode `python3 prep.py`.
4. Ajuste os tempos `T` e a duração nos 5 lugares (13.2), preencha o `build_legendas.py` (13.4) e rode-o.
5. Antes do render: busca de tokens vazia, `lint` com 0 erros e `check` sem `page_error` (seção 9; `qa-checklist.md` §C.0).

### 13.1 Tokens do `index.html`

Cada token aparece uma vez no template, só em texto visível (nunca em comentário). Troque o token inteiro, com os sublinhados.

| Token | Onde aparece | O que pôr | Verão Conectado |
|---|---|---|---|
| `__GANCHO_L1__` | `#q1`: 1ª linha do gancho, o 1º texto na tela (sobre o 1º take) | A pergunta ou o problema do vídeo, em poucas palavras | "Casa de praia" |
| `__GANCHO_L2__` | `#q1`: 2ª linha | O complemento. Gancho de uma linha: apague o `<br />` e este token | "sem internet?" |
| `__TITULO_1__` | `#brand .t1`: parte vermelha do título do cartão da marca, abaixo da logo | O nome da campanha (ou a 1ª parte), em MAIÚSCULAS | "VERÃO" |
| `__TITULO_2__` | `#brand .t2`: parte grafite, depois do `#icone` | A 2ª parte, em MAIÚSCULAS. Título de uma parte só: apague o `<span class="t2">` | "CONECTADO" |
| `__OFERTA_TITULO__` | `#offer-main`: faixa vermelha | O título da oferta, do cliente | "Planos sem fidelidade" |
| `__OFERTA_LINHA_1__` | 1ª `.offer-sub`: faixa grafite embaixo do título | A condição ou o prazo, do cliente | "de 2 a 5 meses" |

Medidas do layout, conferidas com `hyperframes snapshot` sobre os takes do Verão Conectado (15/10/2026). Só o caso do Verão Conectado foi entregue; os outros são [não testado] com cliente:
- **Gancho:** linhas curtas (no Verão Conectado, 13 caracteres cada). Um gancho de 3 linhas cobriu o celular erguido do take 1. A caixa vai até 866 px de largura e quebra o texto sozinha.
- **Título:** cabe numa linha até ~834 px. "VERÃO ☀ CONECTADO" mede ~821 px e já encosta na borda direita do cartão. Mais largo que isso, a parte `.t2` desce para a 2ª linha e o cartão cresce para cima: a base fica em y 1426 e o topo sobe de y 1214 para 1138 (teste com "INVERNO ☀ / CONECTADO"). Uma parte longa quebra dentro dela: com "INAUGURAÇÃO DA LOJA NOVA" + "CONECTADO", o título foi a 3 linhas (topo em y 1068). Encurte.
- **Oferta:** título + 2 linhas terminam em y 1480, o limite da zona segura; 3 linhas não cabem. Título longo quebra dentro da faixa (largura máxima de 866 px).

### 13.2 O que não é token: ícone, oferta, CTA, cidades, tempos e duração

- **`#icone` (opcional):** o desenho entre `.t1` e `.t2`. O do template é o sol do Verão Conectado, com os raios no grupo `.gira`, que gira enquanto o cartão está na tela. Em outra campanha, troque o desenho mantendo `id="icone"` (o grupo `.gira` é opcional) ou apague o `<svg>` inteiro; o script só anima o que existir. Não deixe o sol numa campanha que não seja de verão.
- **Linhas da oferta:** cada `<div class="offer-sub">` precisa de um instante na lista `T.offerSub`. Mais uma linha: duplique o div e acrescente o instante. **Vídeo sem oferta** (institucional, dica de Wi-Fi, suporte): apague o `<div id="offer">` inteiro e deixe `offerSub: []` [não testado com cliente; conferido no check e no snapshot]. Se linhas e instantes não baterem, a trava do script faz o `check` acusar `page_error` e o `render --no-best-effort` bloquear (seção 9).
- **CTA (fixo da Voltec):** o template sai com o cartão de anúncio pago ("ASSINE AGORA", "clique em **Saiba mais**", QR e cidades). Post orgânico: troque "clique em `<b id="saiba">Saiba mais</b>`" por "link na bio" e a frase da narração por "Assina pelo link na bio!" (`persona-e-marca-voltec.md` §7). A voz orgânica não fala "Saiba Mais" nem "QR code": reancore `T.pulseSaiba` e `T.pulseQr` numa palavra que ela fala ou ponha `null` (sem pulso) [não testado com cliente; conferido no check e no snapshot]. Vídeo sem venda (dica, suporte): o cartão final continua o padrão; outro texto só se o cliente pedir.
- **Cidades (fixo):** as 4, nesta ordem. Só mudam os instantes `T.cities`, um por cidade, na palavra falada. Vídeo curto (ex.: o teste do modo falando, 13 s): apague o `<div id="cities">` inteiro e deixe `cities: []`; o script só anima o cartão se ele existir, e as cidades seguem na linha do cartão final [vivido].
- **Posição do gancho:** `right: 150px; top: 250px` foi o céu do take 1 no Verão Conectado. Se a área livre do take for outra, mude `right`/`top` (e o `transform-origin` para o canto fixo), dentro da zona segura. Selfie com o rosto grande (teste do modo falando): `top: 1130px`, abaixo do rosto e da legenda [vivido].
- **Tempos `T` e duração:** os valores do template são os do v5 do Verão Conectado (tabela abaixo e seção 7). Ancore cada um no alignment (+ `NARR_OFFSET`) e nos cortes (quadros/24): o elemento entra de 0 a 0,15 s antes da palavra. `T.cta` = `CTA_START` do `build_legendas.py`. A duração (`TOTAL/24`) aparece em 5 lugares: `data-duration` do root, do `#base`, do `#mix` e do `#gfx`, e `DUR`.

| Chave de `T` | O que marca | Verão Conectado v5 |
|---|---|---|
| `q1In`, `q1Out` | entrada e saída do gancho, dentro do 1º take | 0,30 e 3,52 s |
| `brandIn`, `brandOut` | cartão da marca, na frase da virada | 3,85 e 7,72 s ("Agora" em 3,82 s) |
| `citiesIn`, `cities` (4), `citiesOut` | cartão das cidades e o instante de cada nome | 8,05; 8,50 / 9,25 / 9,92 / 10,95; 12,08 s |
| `offerIn`, `offerSub` (lista), `offerOut` | oferta e cada linha grafite | 12,30; [13,55]; 15,30 s |
| `cta`, `ctaCard` | desfoque + véu (e fim das legendas); cartão final | 15,40 e 15,55 s |
| `pulseSaiba`, `pulseQr` | pulsos nas palavras do CTA (`null` = sem pulso) | 16,35 e 17,90 s |

### 13.3 `prep.py`: o que preencher

Sem os campos `PREENCHA`, o script para com `prep.py: preencha SEGMENTS, TOTAL, NARR no bloco CONFIGURAÇÃO ...` e não cria nada.

| Campo | O que pôr | Verão Conectado v5 |
|---|---|---|
| `SEGMENTS` (PREENCHA) | `(arquivo em takes/, quadro_inicial, nº_de_quadros)` por take, na ordem do vídeo (seção 4) | `("T1r_veo_v1_bICA18jbanp0KfqE3fgS.mp4", 19, 89)`, `("T2r_veo_v1_RvTRU6nLzVKOEUqVWUh5.mp4", 62, 101)`, `("T3r_veo_v2_R41wQEvLdexHBvaXIRsl.mp4", 5, 187)` |
| `TOTAL` (PREENCHA) | duração em quadros, inteiro: (última palavra no vídeo + ~1 s) × 24 | `492` (20,5 s) |
| `NARR` (PREENCHA) | `PROJ / "audio" / "narracao_<vN>_s<seed>.wav"` ou a narração emendada (`api-elevenlabs.md` §5.5) | `PROJ / "audio" / "narracao_v3.wav"` |
| `NARR_OFFSET` | padrão testado; o mesmo valor no `build_legendas.py` | `0.30` |
| `BED` | padrão `audio/ambiente_sfx.mp3`, gerada com o texto da cena desta campanha e `duration_seconds` ≥ `TOTAL/24` | `audio/ambiente_praia_sfx.mp3`, de 20 s para 20,5 s (o script avisa que a cama é curta) |
| níveis (`AMB_LUFS`, `BED_LUFS` ...) | não mexa sem motivo (seção 5) | os do molde |

### 13.4 `build_legendas.py`: o que preencher

Sem os campos `PREENCHA`, o script para com `build_legendas.py: preencha ALIGN, PHRASES, CTA_START no bloco CONFIGURAÇÃO ...` e não mexe no index.

| Campo | O que pôr | Verão Conectado |
|---|---|---|
| `ALIGN` (PREENCHA) | alignment da narração final, com as emendas já deslocadas | `ROOT.parent / "audio" / "narracao_v3_alignment.json"` |
| `PHRASES` (PREENCHA) | blocos na ordem da fala: frases naturais de até `MAX_CHARS` (21) caracteres, já com a grafia de tela | 16 blocos, de "Casa de praia" a "ou escaneia o QR code na tela!"; os 2 últimos começam depois do `CTA_START` e ficam fora (14 na tela) |
| `CTA_START` (PREENCHA) | = `T.cta` do index | `15.40` |
| `FIX` | `"Voltéc": "Voltec"` (fixo) + os números falados por extenso | + `"dois": "2"`, `"cinco": "5"` |
| `START_FIX` | vazio até medir com `stt.py --ss/--t` (+ `NARR_OFFSET`) | `[("internet?", 1, 1.38), ("Voltec", 1, 5.32), ("Voltec", 2, 8.03)]` |
| `LOW_RANGES` | vazio até ver a legenda cobrir o objeto na mão | `[(0.0, 3.70)]` |
| `NARR_OFFSET`, `MAX_CHARS` | padrão testado | `0.30`, `21` |

### 13.5 Cenário ou formato ainda não gerado: o que muda na edição [não testado]

Derivado das regras que funcionaram. Confira tudo no QA (`qa-checklist.md` §A–§C) e avise no portão que a cena é nova.
- **Cena interna (casa, loja, carro; o que se sabe de cada um: `locais-grussai.md` §10):** o gancho precisa de uma área lisa e livre (parede ou teto claro, no lugar do céu); reserve-a já no snapshot. Se o objeto na mão cair na faixa da legenda (y ≈ 1000), use `LOW_RANGES`. Reescreva o texto da cama de SFX para o som do lugar (`api-elevenlabs.md` §7): a cama de praia não serve.
- **Loja ou uniforme:** o letreiro VOLTEC da loja e o logo bordado do uniforme vazam texto para a geração (risco que as refs da conta já mostraram). A marca entra só no overlay; take com texto ou logo no fundo é reprovado no QA (`qa-checklist.md` §B) e não se esconde com cartão, que só fica alguns segundos na tela.
- **Noite:** cartões brancos, legenda com fundo escuro e véu do CTA não dependem da luz da cena; confira a legibilidade nos quadros do `qa-checklist.md` §C.2 e o "Contrast" do `check`.
- **Outra estação em Grussaí:** a edição não muda; mudam a cama de SFX (o vento fora do verão não foi pesquisado) e a luz do snapshot (`locais-grussai.md` §3).
- **Stories:** a mesma composição 9:16 deve servir, mas a zona segura usada é a do Reels; a zona segura de Stories não foi pesquisada.
