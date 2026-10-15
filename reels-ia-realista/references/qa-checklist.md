# QA: checklists objetivos com comandos

Há três portões, e cada um tem comandos e itens de sim/não. Só avance quando todos os itens forem "sim".

- **A. Snapshot:** antes de mostrar ao cliente. Defeito no 1º quadro piora no vídeo.
- **B. Vídeo gerado:** cada variação, antes de escolher o trecho e editar.
- **C. Vídeo final:** na master antes do portão 4 (o cliente só vê o corte que passou); nos 4 arquivos (master e Instagram, com e sem legenda) antes de entregar.
- **D. Verificação independente:** revisores separados, na master antes do portão 4, e de novo se algo mudar depois dele.

Vale para qualquer vídeo realista da Voltec com a persona, em qualquer campanha, estação ou cenário. Os comandos foram testados em 15/10/2026 com os arquivos do Reels "Verão Conectado", o caso de referência; o bloco automático da seção C passou no v5 entregue. **Voltec:** marca o que é da Voltec ou de Grussaí; **Verão Conectado:** marca o que é só daquela campanha, como exemplo (troque num vídeo novo). **[não testado]:** item para cenário ou roupa que nunca foi gerado (loja, carro, casa, uniforme, noite, inverno), derivado das regras que funcionaram. O resto vale para qualquer anúncio com IA.

## Preâmbulo (repita em toda chamada do Bash; o npm i é uma vez só)

```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"                                           # tudo o que o QA gera vai para cá
# uma vez por máquina (precisa de rede na 1ª vez); o decode.cjs acha jsqr/pngjs pelo NODE_PATH
[ -d "$FERR/qr/node_modules/jsqr" ] || (mkdir -p "$FERR/qr" && cd "$FERR/qr" && npm i qrcode@1.5.4 jsqr@1.4.0 pngjs@7.0.0)
```

- **Por que repetir:** as variáveis não passam de uma chamada do Bash para outra. Por isso todo bloco de comandos abaixo começa pelas 4 linhas `export` e pelo `mkdir` (troque `<campanha>`). Sem elas, `$QA` fica vazio e o ffmpeg tenta gravar em `/`, `$HF/renders/...` vira `/renders/...` e o `decode.cjs` não acha o jsqr: o resultado é "FALHA QR" e "FALHA quadros" falsos.
- `PROJ` é a raiz do projeto (`snapshots/`, `takes/`, `audio/`, `refs/`) e `HF` é o projeto HyperFrames (`index.html`, `renders/`).
- **Voltec (Verão Conectado):** para revisar os arquivos de `/home/syllas/hyperframes/voltec-reels-ia/`, aponte `PROJ` para lá e troque `QA` por uma pasta fora dele. Esse projeto é só para leitura, e o QA grava arquivos.
- **Imagens:** para olhar as imagens geradas, use a ferramenta Read no PNG/JPG. Folha reduzida serve para visão geral. Grafia, acentos, dedos e boca se conferem em recorte a 100%.
- **STT** (`scripts/stt.py`): usa a API (scribe_v1) e consome créditos, mas o custo é baixo. Não imprime a chave.

---

## A. Snapshot (antes de mostrar ao cliente)

### Comandos
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (topo deste arquivo)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
S="$PROJ/snapshots/T1_gpt25_a_<id>.png"; N=$(basename "${S%.*}")
# 1) formato: 9:16 exato (largura*16 == altura*9). gpt-image-2.5 2K = 1152x2048 (ok); Gemini 2K = 1536x2752 (recortar)
ffprobe -v error -show_entries stream=width,height,pix_fmt -of csv=p=0 "$S"
# 2) revisão a 100%: 6 recortes sem reduzir (olhe cada um)
mkdir -p "$QA/$N" && for i in 0 1 2; do for j in 0 1; do
  ffmpeg -loglevel error -y -i "$S" -vf "crop=iw/2:ih/3:$j*iw/2:$i*ih/3" "$QA/$N/t_$i$j.png"; done; done
# 3) A/B lado a lado com a referência de rosto (identidade e para a página de aprovação)
ffmpeg -loglevel error -y -i "$PROJ/snapshots/T1_gpt25_a_<id>.png" -i "$PROJ/snapshots/T1_gpt25_b_<id>.png" -i "$PROJ/refs/rosto_sem_dedos.jpg" -filter_complex \
  "[0]scale=-2:960[a];[1]scale=-2:960[b];[2]scale=-2:960[c];[a][b][c]hstack=inputs=3" "$QA/T1_ab_ref.jpg"
```
Se não for 9:16 exato, normalize (`edicao-hyperframes.md` §3).

### Checklist
**Pessoa**
- [ ] É o mesmo rosto das referências: formato do rosto, olhos, sobrancelhas, nariz, boca, tom de pele, cabelo e risca.
  - Se derivou, faça **edição de identidade**: Image 1 = snapshot aprovado + refs de rosto e corpo, pedindo para mudar só a semelhança. Não regere do zero.
  - Na sessão, o `gemini-3-pro-image` afinou o rosto e o `gpt-image-2.5-sunburst` manteve a identidade.
- [ ] O rosto tem tamanho razoável (plano médio). Rosto pequeno faz a identidade derivar no vídeo.
- [ ] Ela está na **pose inicial** da ação, com boca fechada ou sorriso leve.
- [ ] Mãos com 5 dedos cada, pegada coerente, nada fundido, unhas iguais à âncora. **Voltec:** curtas, bordô escuro.
- [ ] Há **um único objeto** na mão, já no quadro. Se for celular, só o verso aparece (tela virada para ela, sem interface).
- [ ] A pele é real: poros visíveis, brilho leve, pequenas assimetrias. Nada de pele plástica ou filtro de beleza.
- [ ] A roupa bate com a âncora do vídeo, é opaca e não tem estampa nem logo. O padrão da roupa (no Verão Conectado, crochê) é coerente e o cabelo não funde com a roupa.
  - Uniforme da Voltec [não testado]: só liso, sem o logo bordado. O logo bordado e o letreiro da loja vazam texto para a geração.
- [ ] Nada vazou das referências: headset, letreiro, logo do uniforme, fundo do carro, colar fino. São os riscos que as refs da conta já mostraram, e valem também em cena de loja, carro ou casa.

**Cena e câmera**
- [ ] A câmera tem dono, com altura e distância de quem filma (amiga ~1,2 m na altura do peito; selfie a um braço). Foco profundo, sem bokeh, sem cara de estúdio ou DSLR.
- [ ] Se há inclinação, é o quadro inteiro rolado (parapeito e horizonte paralelos), não só uma linha torta.
- [ ] Não há **texto, placa, número, logo nem marca d'água**, nem no fundo nem na roupa.
- [ ] Ninguém mais no quadro, ou só 1–2 adultos pequenos e distantes.
- [ ] A luz é coerente com o lugar e a hora, com uma direção de sombra só. Linhas retas não curvam.
- [ ] Há uma área lisa e livre para o gancho, do lado oposto ao braço erguido (Verão Conectado: o céu, no alto à direita do T1).

**Voltec / Grussaí** (cena externa em Grussaí)
- [ ] Relevo plano: sem morro, ilha, costão, pedra, píer ou prédio alto. Nada que lembre Copacabana.
- [ ] Mar cinza-azulado ou oliva, nunca turquesa. Horizonte reto e vazio. Casuarinas tortas pelo vento e capim de duna amarelado.
- [ ] A praia olha para o leste, então **o sol nunca se põe no mar**, em qualquer estação. A luz bate com a hora e a estação da cena: no Verão Conectado (~17h no verão), a varanda fica em sombra aberta com o fundo ensolarado e um pouco estourado, sem laranja de golden hour. Outras estações: `locais-grussai.md` §3.
- [ ] Outro lugar externo da área (Chapéu do Sol, centro de São João da Barra): o que já se sabe está em `locais-grussai.md` §10; o resto é **não pesquisado: pesquise com `locais-grussai.md` §7–§9** e escreva os itens do lugar antes de revisar. Atafona: a pesquisa recomendou não usar como cenário de anúncio (erosão).

**Cena interna ou à noite** [não testado] (casa, loja, carro; o que se sabe de cada um: `locais-grussai.md` §10)
- [ ] A luz vem de uma fonte real que aparece ou se explica na cena (janela, luminária, poste), com a mesma direção em todo o quadro.
- [ ] Nenhum texto: letreiro VOLTEC da loja fora do quadro, nada de logo bordado no uniforme, telas (TV, monitor, celular, roteador) sem interface nem texto.
- [ ] O rosto continua em plano médio. Rosto pequeno não serve, como a ref da passarela.

**Depois**
- [ ] Guarde o `generation_id` do aprovado: ele é o `start_frame` do vídeo.
- [ ] Mostre 2 opções ao cliente (página de aprovação com A/B) e **pare até a aprovação**.

---

## B. Vídeo gerado (cada variação, antes de editar)

### Comandos
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (topo deste arquivo)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
V=$PROJ/takes/T2r_veo_v2_<id>.mp4; N=$(basename "${V%.*}")
# 1) formato esperado do Veo 3.1: h264 1080x1920 24/1 com 192 quadros + aac 48000 Hz 2 canais, 8.000 s
ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames,sample_rate,channels:format=duration \
  -of compact=p=0 "$V"
# 2) folha de contato a 2 fps: 16 quadros em 8x2 (visão geral: identidade, cenário, objetos, câmera)
ffmpeg -loglevel error -y -i "$V" -vf "fps=2,scale=270:-2,tile=8x2:padding=6:color=white" -frames:v 1 "$QA/${N}_sheet.jpg"
# 3) tira de detalhe NUMERADA no ponto crítico. Escolha a taxa pelo filtro select:
#    24 fps = todos os quadros (boca, quadro exato do corte) | 8 fps = not(mod(n\,3)) (mãos/objeto) | 6 fps = not(mod(n\,4))
#    crop=L:A:X:Y recorta a região (aqui: metade de baixo, onde estão mãos e celular)
ffmpeg -loglevel error -y -i "$V" -vf "select='between(n\,96\,144)*not(mod(n\,3))',crop=1080:900:0:900,scale=360:-2,\
drawtext=text='%{eif\:round(t*24)\:d}':x=8:y=8:fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6,\
tile=6x3:padding=4:color=white" -fps_mode passthrough -frames:v 1 "$QA/${N}_maos_8fps.jpg"
# 4) STT do áudio nativo: deve ter só itens "audio_event" (ex.: {"text": "[som de mar]", "type": "audio_event"})
python3 -I "$SKILL/scripts/stt.py" "$V" --out "$QA/${N}_stt.json"
python3 -I -c "import json,sys; w=json.load(open(sys.argv[1]))['words']; f=[x for x in w if x['type']=='word']; print('FALA NO TAKE:' if f else 'ok: sem fala', [(x['text'],x['start']) for x in f])" "$QA/${N}_stt.json"
# 5) espectrograma do áudio nativo (eixo = tempo do take, 0–8 s): clique ou degrau = linha vertical fina em todas as frequências
ffmpeg -loglevel error -y -i "$V" -vn -lavfi "showspectrumpic=s=1600x400:legend=1" "$QA/${N}_espectro.png"
```
O número em cada quadro da tira é o índice do quadro no take (24 fps). É esse número que vai para o `SEGMENTS` do `prep.py`.

### Checklist
**Rosto e boca**
- [ ] A identidade fica estável do 1º ao último quadro, sem morph.
- [ ] **Sob narração em off, os lábios ficam fechados.** Reprove sopro com boca em "O", risada de boca aberta (parece dublagem) e mão na boca (bocejo). Olhe a 24 fps a janela das expressões.
  - **Voltec (Verão Conectado):** no T1 v1, a boca começou a projetar no quadro 101 e abriu em "O" a partir do 103. O prompt pedia "huffs once through her nose".
- [ ] O olhar é natural: para o rosto de quem filma, ou para a própria imagem na selfie. Olhar cravado na lente denuncia anúncio.

**Mãos e objetos**
- [ ] Os dedos não fundem. O objeto mantém **forma, cor e quantidade** o tempo todo.
  - Revise a **8 fps** todo momento de manipulação (abaixar, girar, guardar): é onde o Veo mais erra.
  - **Voltec (Verão Conectado):** no T2r v2, o celular virou uma "barra" fina com dedos fundidos ao descer para o colo (a partir do quadro ~138 na tira de 8 fps). O v5 usa a v1, em que ela segura o celular firme.
- [ ] O celular de quem filma **não aparece**. **Voltec (Verão Conectado):** no T1r v2, ele surgiu no topo do quadro aos 4,5 s.
- [ ] Nada aparece nem some, e o padrão da roupa não tremula.

**Cena, câmera e luz**
- [ ] O lugar continua o do 1º quadro: sem troca de ambiente, sem revelar área nova, parede e horizonte retos, nada derretendo.
- [ ] A câmera é de celular crível: micro-tremor, sem zoom, sem gimbal nem drone. Sem pulsar de brilho ou exposição.
- [ ] **Sem legenda, texto, logo ou marca.** O Veo já queimou legenda em português numa geração antiga desta conta. Em loja, carro ou com uniforme [não testado], confira o take inteiro, não só o 1º quadro: letreiro, logo bordado e telas podem aparecer com o movimento.

**Áudio nativo**
- [ ] No STT, nenhuma entrada `"type": "word"`, e os eventos são coerentes com a cena (Verão Conectado: mar e vento).
- [ ] Sem música, sem vozes e sem clique dentro do trecho que será usado (de in/24 a (in+n)/24 s). Você não ouve áudio: confira no STT (texto e `audio_event`: nenhuma palavra, nenhum evento de música ou de voz) e no espectrograma do comando 5 (nenhuma linha vertical fina em todas as frequências dentro do trecho). Na dúvida, ponha o trecho na página do portão, com o instante, para o cliente ouvir. O `prep.py` já põe fade nas bordas.

**Decisão**
- [ ] Anote, para cada variação, os quadros com defeito e escolha in/out que os evitam → `SEGMENTS` (`edicao-hyperframes.md` §4). Recortar não custa nada.
- [ ] Se não há janela limpa na variação A, use a B. Se as duas falharem, mude **uma** variável no prompt e regere. Exemplo: "lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth" + negativos "open mouth, pursed lips, blowing air, whistling, yawning, hand over mouth". Custo medido: 19.391 créditos por take Veo 3.1 1080p de 8 s.
- [ ] Gere 2 variações por take. Em toda rodada da sessão, pelo menos uma teve problema.

---

## C. Vídeo final (master e Instagram, com e sem legenda)

### 0. Antes do render: tokens preenchidos, duração e textos da campanha
Rode depois de preencher o `index.html` e os moldes (`edicao-hyperframes.md` §13) e antes do lint, do check e do render:
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (topo deste arquivo)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
# 1) tokens __X__ do template: tem de sair vazio (sem achado, o grep sai com código 1: é o esperado)
grep -n '__[A-Z0-9_]*__' "$HF/index.html"
# 2) duração: os 4 data-duration (root, #base, #mix, #gfx) e o DUR iguais a TOTAL/24 do prep.py
python3 -I - "$HF/index.html" "$HF/prep.py" <<'EOF'
import re, sys
idx, prep = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
durs = re.findall(r'data-duration="([0-9.]+)"', idx) + re.findall(r"const DUR = ([0-9.]+)", idx)
m = re.search(r"(?m)^TOTAL = (\d+)", prep)
alvo = int(m.group(1)) / 24 if m else None
ok = alvo is not None and len(durs) == 5 and all(abs(float(d) - alvo) < 1e-6 for d in durs)
print(("duração OK: " if ok else "FALHA duração: ") + f"{durs} no index; TOTAL/24 = {alvo}")
EOF
```
- [ ] A busca de tokens não imprime nada. Token que sobra vira texto na tela.
- [ ] `duração OK`, com os 5 valores iguais a `TOTAL/24` (Verão Conectado: 20.5).
- [ ] Os textos da tela batem com o roteiro aprovado: gancho, título do cartão da marca, oferta (do cliente, sem preço nem prazo inventado) e CTA (anúncio pago: "Saiba mais" + QR; post orgânico: "link na bio").
- [ ] O `#icone` é o da campanha atual ou foi apagado (o sol é do Verão Conectado).
- [ ] O `check` (`edicao-hyperframes.md` §9) passou sem `page_error`: o número de linhas `.offer-sub` é igual ao de instantes em `T.offerSub` (vídeo sem oferta: nenhum dos dois).

### 1. Bloco automático (cole, troque `<campanha>`, `vN` e as 3 variáveis da campanha e rode nos 4 arquivos)
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (topo deste arquivo)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
URL_QR="<URL respondida no portão 1>"            # Verão Conectado: https://provedorvoltecinternet.online/?page_id=674 (NÃO WhatsApp)
CTA_T="<3 instantes (s) com o QR na tela>"       # Verão Conectado: "16.5 18.6 20.4" (~T.ctaCard + 1 s, meio do CTA, fim − 0,1 s)
FRAMES_ESPERADOS="<TOTAL do prep.py>"            # Verão Conectado: 492
qa_final() {
  local f="$1" b; b=$(basename "${f%.*}")
  echo "== $b"
  ffprobe -v error -count_frames -show_entries stream=codec_name,profile,width,height,pix_fmt,r_frame_rate,nb_read_frames,sample_rate,channels:format=duration -of compact=p=0 "$f"
  local n; n=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$f")
  [ "$n" = "$FRAMES_ESPERADOS" ] && echo "quadros OK ($n)" || echo "FALHA quadros: $n (esperado $FRAMES_ESPERADOS)"
  ffmpeg -hide_banner -nostats -i "$f" -vn -af ebur128=peak=true -f null - 2>&1 | grep -A16 Summary | grep -E "^ +(I|Peak):"
  for t in $CTA_T; do
    ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$f" -frames:v 1 "$QA/${b}_qr_$t.png"
    local q; q=$(node "$SKILL/scripts/decode.cjs" "$QA/${b}_qr_$t.png")
    [ "$q" = "$URL_QR" ] && echo "QR $t s OK" || echo "FALHA QR $t s: $q"
  done
  local pretos; pretos=$(ffmpeg -hide_banner -nostats -sseof -1.5 -i "$f" -an -vf blackdetect=d=0.04:pix_th=0.10 -f null - 2>&1 | grep -c black_start)
  [ "$pretos" = 0 ] && echo "fim sem quadro preto OK" || echo "FALHA: $pretos trecho(s) preto(s) no último 1,5 s"
  ffmpeg -hide_banner -loglevel error -y -sseof -0.1 -i "$f" -frames:v 1 "$QA/${b}_ultimo.png"   # olhe este quadro
  ffprobe -v trace -i "$f" 2>&1 | grep -o "type:'\(moov\|mdat\)'" | head -2 | tr '\n' ' ' | grep -q "^type:'moov'" \
    && echo "faststart OK (moov antes do mdat)" || echo "FALHA: moov depois do mdat"
}
V="<campanha>_vN"                                # Verão Conectado v5: V=verao-conectado-reels-ia_v5
for v in "$V" "${V}_instagram" "${V}_legendas" "${V}_legendas_instagram"; do qa_final "$HF/renders/$v.mp4"; done
```
**Saída esperada** (v5 do Verão Conectado, master e Instagram; num vídeo novo, mudam a duração e o nº de quadros):
- `h264|profile=High|width=1080|height=1920|pix_fmt=yuv420p|r_frame_rate=24/1|nb_read_frames=492`, `aac|...|sample_rate=48000|channels=2` e `duration=20.5`
- `quadros OK (492)`
- `I: -14.0 LUFS` e `Peak: -1.7 dBFS`. Esse Peak está na seção "True peak", então é dBTP. Alvo: −14 LUFS e ≤ −1,5 dBTP.
- `QR ... OK` nos 3 instantes, `fim sem quadro preto OK` e `faststart OK`.

**Teste de robustez do QR (opcional):** reduza o quadro e decodifique de novo. No v5, o QR foi lido a 540 e a 360 px de largura.
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (topo deste arquivo)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
T_QR="<um dos CTA_T>"   # Verão Conectado: 18.6
for w in 540 360; do ffmpeg -loglevel error -y -ss "$T_QR" -i "$HF/renders/<campanha>_vN_instagram.mp4" -frames:v 1 -vf scale=$w:-2 "$QA/qr_$w.png"; done
node "$SKILL/scripts/decode.cjs" "$QA/qr_540.png" "$QA/qr_360.png"
```

### 2. Imagem
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (topo deste arquivo)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
F="$HF/renders/<campanha>_vN.mp4"
CORTES="<quadro de cada corte = somas acumuladas dos nº de quadros do SEGMENTS; o último é o início do congelamento>"   # Verão Conectado v5: "89 190 377"
# visão geral a 1 fps (21 quadros em 7x3 para ~20 s): cartões na zona segura, nada sobre o rosto, CTA
ffmpeg -loglevel error -y -i "$F" -vf "fps=1,scale=216:-2,tile=7x3:padding=6:color=white" -frames:v 1 "$QA/final_sheet.jpg"
# 4 quadros em volta de cada corte (2 antes, o do corte e o seguinte), numa tira só
SEL=$(for c in $CORTES; do printf '+between(n\\,%d\\,%d)' $((c - 2)) $((c + 1)); done); SEL=${SEL#+}; NQ=$(( $(wc -w <<< "$CORTES") * 4 ))
ffmpeg -loglevel error -y -i "$F" -vf "select='$SEL',scale=216:-2,\
drawtext=text='%{eif\:round(t*24)\:d}':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=${NQ}x1:padding=4:color=white" \
  -fps_mode passthrough -frames:v 1 "$QA/cortes.jpg"
```
- [ ] O texto fica dentro da **zona segura** (x 64–930, y 220–1480), nunca sobre o rosto nem sobre o objeto na mão.
- [ ] Os cortes caem limpos: sem quadro piscando, e a ação continua coerente de um take para o outro.
- [ ] No CTA, o desfoque **não escurece as bordas**. A escala sobe junto com o blur: ≥ 1 + 6σ/largura, ou 1,08 para 14 px.
- [ ] O pulso de palavra (anúncio pago: "Saiba mais") não encosta na palavra vizinha. Olhe 2–3 quadros no pico do pulso.
- [ ] A grafia e os acentos estão certos, conferidos em recorte a 100%. A folha reduzida engana: "Grussaí" parecia sem acento no cartão e estava certo.
- [ ] O último quadro (`$QA/<arquivo>_ultimo.png`) é imagem com CTA, não preto. No v5 do Verão Conectado, a luminância média dos últimos quadros ficou em ~144 (YAVG do `signalstats`; preto fica perto de 16).
- [ ] Os textos da tela são os da campanha atual, conferidos quadro a quadro na folha: gancho, título do cartão, `#icone`, oferta e CTA (nada do Verão Conectado sobrou).

### 3. Legendas (só nas versões legendadas)
Gere uma folha com um quadro por bloco, no meio da **última** palavra de cada bloco, que deve estar em destaque:
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (topo deste arquivo)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
python3 -I - "$HF/index.html" "$HF/renders/<campanha>_vN_legendas.mp4" "$QA" <<'EOF'
import json, re, subprocess, sys
idx, video, qa = sys.argv[1], sys.argv[2], sys.argv[3]
leg = json.loads(re.search(r"const LEGENDAS = (.*?); /\* LEGENDAS:FIM", open(idx).read(), re.S).group(1))
for k, d in enumerate(leg):
    w = d["w"][-1]
    t = (w[1] + min(w[2], d["e"])) / 2          # meio da última palavra do bloco
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                    "-vf", "crop=1080:700:0:900,scale=360:-2", f"{qa}/leg_{k:02d}.png"], check=True)
    print(f"leg_{k:02d}.png {t:6.2f}s  " + " ".join(x[0] for x in d["w"]))
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "1", "-i", f"{qa}/leg_%02d.png",
                "-vf", f"tile=4x{(len(leg) + 3) // 4}:padding=6:color=white", "-frames:v", "1", f"{qa}/legendas_sheet.jpg"], check=True)
EOF
```
O recorte `crop=1080:700:0:900` (y 900–1600) pega a faixa da legenda e dos cartões no layout do template. Ajuste se mudar o layout.
- [ ] O texto de cada bloco é o da narração, com a grafia de tela correta (**Voltec:** "Voltec", não "Voltéc"; números em algarismo).
- [ ] A palavra em destaque é a que está sendo falada. Se uma palavra entra antes ou depois da voz, corrija em `START_FIX`, medindo com `stt.py --ss/--t`.
- [ ] A legenda não cobre rosto nem objeto. **Verão Conectado:** no take 1, ficou na posição baixa para não cobrir o celular (`LOW_RANGES`).
- [ ] As legendas somem quando entra o CTA (`CTA_START`).
- [ ] A versão **sem** legenda não tem legenda: confira 1 quadro.

### 4. Áudio e texto falado
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # preâmbulo (topo deste arquivo)
export PROJ="$HOME/hyperframes/<campanha>"
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA"
# narração do vídeo final: o texto tem de bater com o roteiro aprovado
python3 -I "$SKILL/scripts/stt.py" "$HF/renders/<campanha>_vN.mp4" --out "$QA/final_stt.json"
python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))['text'])" "$QA/final_stt.json"
# CTA errado (no texto visível do index e na fala): as duas listas têm de sair []. Os comentários do template citam
# "link na bio" e "Saiba mais" de propósito, por isso a busca ignora comentários. WhatsApp: fora a pedido do cliente (persona §7)
PROIBIDO="link na bio"   # anúncio pago (padrão do template); post orgânico: PROIBIDO="saiba mais"
python3 -I - "$HF/index.html" "$QA/final_stt.json" "$PROIBIDO" <<'EOF'
import json, re, sys
idx = re.sub(r"<!--.*?-->|/\*.*?\*/", " ", open(sys.argv[1], encoding="utf-8").read(), flags=re.S)
idx = re.sub(r"(?m)(^|\s)//[^\n]*", " ", idx)
fala, pad = json.load(open(sys.argv[2]))["text"], "(?i)" + re.escape(sys.argv[3]) + "|whatsapp"
print("index:", re.findall(pad, idx), "| fala:", re.findall(pad, fala))
EOF
# espectrograma de cada ponto sensível (cortes, emenda, rampa da cama, fim): janela de 1,6 s que começa 0,6 s antes
# do ponto, então o ponto fica em 0,6 s no eixo. Verão Conectado v5: "3.71 7.92 15.35 15.61 19.5" = cortes 89/24 e
# 190/24, emenda 15,05 + NARR_OFFSET, início da rampa (congelamento − 0,1) e fim = DUR − 1 (a janela acaba no último quadro)
PONTOS="<instantes (s) dos cortes, emenda, rampa e fim>"
for p in $PONTOS; do
  s=$(LC_ALL=C awk -v p="$p" 'BEGIN{print (p > 0.6) ? p - 0.6 : 0}')   # LC_ALL=C: no pt_BR o awk escreve "3,11"
  ffmpeg -loglevel error -y -ss "$s" -t 1.6 -i "$HF/renders/<campanha>_vN.mp4" -lavfi "showspectrumpic=s=1200x400:legend=1" "$QA/espectro_$p.png"
done
```
- [ ] O STT traz o roteiro inteiro, na ordem, **com o CTA atual**. Sem o registro de como a narração foi montada, uma regeração futura pode trazer o CTA antigo de volta.
- [ ] Cada corte (J/L-cut), a emenda da frase regravada, a rampa da cama e o fim (fade, sem corte seco) estão sem clique e sem degrau. Você não ouve áudio: olhe o espectrograma de cada ponto (Read no PNG), confira o STT (texto e `audio_event`) e os níveis do `ebur128` no bloco automático. Liste na página do portão os instantes para o cliente ouvir: cortes, emenda, rampa e cada "Voltec".
  - Clique ou degrau de ganho aparece no espectrograma como linha vertical fina em todas as frequências. Conferido em 15/10/2026: no v4, o estalo de 15,41 s aparece como uma linha de 0 a ~21 kHz, acima do teto de ~19 kHz do resto do áudio; no v5, no mesmo ponto e nos cortes, não há linha.
  - A coluna em 0 s (borda esquerda) sai clara em toda janela. É o início do trecho, não um clique.
  - **Voltec:** o estalo que passou no v4 estava em 15,41 s; era um degrau de ganho da cama.
- [ ] Quirks do STT (não reprove só pelo texto; leve o ponto para o cliente ouvir na página do portão):
  - Ligação de palavras. **Verão Conectado:** "conectada o verão" saiu "conectado". Mostre ao cliente; se incomodar, regere só a frase com vírgula.
  - Nome próprio com grafia livre. **Voltec:** "Grossai" para Grussaí. A tônica se confere com `stress.py`.
  - Evento falso no fim. **Verão Conectado:** "[música alegre]" no master, sem música no mix; o ambiente isolado deu só "[som de mar]".
- [ ] Os níveis estão no alvo do bloco automático (−14 LUFS e ≤ −1,5 dBTP).

### 5. Entrega
- [ ] Os 4 arquivos (master/Instagram × com/sem legenda) passaram no bloco automático. O QR foi decodificado **também nas versões Instagram**.
- [ ] `audio/COMO_FOI_MONTADA_<nome>.txt`, `prompts/` e `bodies/` estão atualizados com o que foi realmente usado.
- [ ] Recado ao cliente: ativar o rótulo **"Informações de IA"** da Meta. CTA "Saiba mais" + QR é para anúncio pago; "link na bio" é só para post orgânico.

---

## D. Verificação independente (na master antes do portão 4; de novo se algo mudar)

Na sessão, 3 revisores em paralelo (áudio, imagem e técnico/sincronia) examinaram os arquivos finais do v4 e acharam problemas que tinham passado na revisão de quem editou. O custo é baixo (basicamente STT). Rode em todo vídeo.

- **Como rodar:** um subagente por foco, em paralelo, se houver subagentes. Sem subagentes, faça uma passada separada por foco, do zero, sem reaproveitar as conclusões da edição.
- **Briefing de cada revisor** (o mesmo formato para os 3 focos):
  - o foco e a lista dele (abaixo);
  - os caminhos dos 4 arquivos finais, do `index.html` e de `$QA`, e o preâmbulo do topo deste arquivo;
  - o roteiro aprovado (texto da narração), a URL do QR e os instantes dos cortes, da emenda e do CTA;
  - as seções B e C deste checklist, como roteiro de conferência;
  - o pedido: achar defeitos, não confirmar que está bom. O revisor não ouve áudio: usa STT, espectrograma e ebur128.
- **Saída de cada revisor:** uma linha por problema, com problema, instante (s) ou quadro, arquivo, severidade e correção proposta. Severidade: alta = não entrega; média = corrige antes de entregar; baixa = registra ou mostra ao cliente. Se não achar nada, o revisor diz o que conferiu.

Focos:
- **Áudio:** cortes, emendas, rampas, níveis, STT da fala e do ambiente, espectrogramas da §C.4.
- **Imagem:** tiras a 8 fps nas manipulações, boca, bordas do desfoque, legendas sobre objetos.
- **Técnico/sincronia:** palavra falada × destaque da legenda, pulsos, CTA, QR, formato dos arquivos.

O que a verificação achou no v4 do Verão Conectado, com a correção aplicada no v5 (exemplos vividos; num vídeo novo, procure os mesmos tipos de defeito):
- Estalo em 15,41 s: degrau de ganho da cama, exposto pela frase nova → rampa de 0,8 s. Problema médio.
- Celular deformando no T2 ao descer para o colo → trocar para a outra variação, que segura o celular firme. Problema médio.
- Alignment com pausa falsa antes de "internet?" (+0,25 s) e "Voltec" ~0,1 s atrasado → `START_FIX`.
- Desfoque do CTA puxando preto nas bordas → escala ≥ 1 + 6σ/largura junto com o blur.
- Pulso do "Saiba mais" encostando na palavra anterior → `inline-block` + `transform-origin` no lado fixo.
- Legenda cobrindo o celular no take 1 → posição baixa no trecho (`LOW_RANGES`).
- STT ouvindo "conectado" no lugar de "conectada" → ponto para o cliente ouvir. Se incomodar, regere só a frase com vírgula e emende.

Corrija, renderize de novo e repita a seção C nos 4 arquivos.
