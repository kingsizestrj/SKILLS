# Modo falando: a personagem fala para a câmera [não testado]

Use quando o pedido for com ela falando ("com ela falando", "ela fala para a câmera", "ela explicando", "depoimento dela"). O caminho foi escolhido pelo usuário em 15/10/2026:
1. O Veo 3.1 gera o take já com a fala, com os lábios sincronizados com a voz do próprio Veo.
2. A ElevenLabs troca essa voz pela voz da persona (speech-to-speech, `scripts/sts.py`). O tempo da fala não muda, então a boca continua batendo com a voz nova.

**[Voltec]** A voz é a Radassa 100%, `4yvYc2GSakxLWMhlsd6b`.

**Nada deste modo foi gerado ainda.** O 1º vídeo é o teste: comece com 1 take falado (A/B) e avise o cliente no portão 3 que o formato é novo.

O que já foi conferido sem gastar crédito (15/10/2026):
- O `prep.py` com `FALA` foi testado com áudio sintético: a fala cai no ponto certo da linha do tempo e os takes falados entram mudos. O modo narrado ficou igual ao entregue na v5, a ±2 LSB, o mesmo ruído entre duas execuções.
- O `stt_alinhamento.py` + `build_legendas.py` foram testados com o STT da master da v5.
- O `sts.py` foi testado com um modelo inexistente: o envio chega à API, que recusa com `model_not_found`, e nada é cobrado.

Todo o resto da skill vale igual: portões, snapshot aprovado antes do vídeo, 2 variações por take, QA e edição.

Alternativas registradas, não usadas por decisão do usuário:
- `creatify-aurora`: imagem + áudio → fala. A conta tem acesso pela API. Vai só até 720p e não aceita prompt.
- Seedance com `audios` de referência: bloqueado na conta.

## 1. O que muda em relação ao modo narrado

| Item | Modo narrado (padrão) | Modo falando |
|---|---|---|
| Boca | Lábios fechados (SKILL.md §3, regra 4) | Ela diz a fala do take |
| Olhar | No rosto de quem filma, nunca cravado na lente (regra 6) | Falando com quem assiste: na lente, ou, na selfie, na própria imagem da tela (olhos um pouco abaixo da lente), com desvios naturais |
| Voz | TTS eleven_v4 da narração inteira numa request | Voz do Veo trocada take a take (`sts.py`) |
| Texto | Roteiro da narração | Uma fala por take, até ~90 caracteres (§2) |
| negative_prompt | Com `talking, speech, lip-syncing` e o conjunto de boca | Sem esses termos (§4) |
| Som nativo do take | Entra a −30 LUFS | Take falado entra mudo, porque tem a voz original do Veo; o ambiente vem da cama de SFX |
| Legendas | Alignment do TTS | STT da mix final → `stt_alinhamento.py` (§8) |
| Custo | 19.391 por geração de vídeo | O mesmo no vídeo, mais a troca de voz (custo a medir, §6) |

Misturar os dois modos é possível: takes falados (`FALA`) e takes com narração em off por cima (`NARR`), sem uma voz por cima da outra.

## 2. Roteiro: a fala de cada take

- **O que ela diz é o anúncio:** a fala de cada take vem aprovada no portão 1, palavra por palavra. Oferta, preço e CTA vêm do cliente, como sempre (SKILL.md §1b).
- **Uma fala por take, curta.** O take tem 8 s, e a fala deve caber em ~5–6 s, com ~1 s livre antes e depois para o corte. Ritmo de referência: a Radassa no TTS fala ~17–18 caracteres/s (294 caracteres ≈ 16,6 s). O ritmo do Veo não foi medido. Por isso, no máximo ~90 caracteres por take. Mensagem maior vira mais takes, com corte seco entre eles (como em vlog), ou narração em off sobre takes sem fala.
- **Marca e números:** "Voltéc" com acento dentro das aspas do prompt, para puxar o vol-TÉC [não testado]; "Voltec" na tela. Números por extenso.
- **CTA falado:** a frase paga do SKILL.md §7.1 tem 56 caracteres e cabe num take.
- Guarde cada fala em `prompts/fala_<take>.txt`: o QA compara o STT com ela.
- Prévia para o portão 3 (opcional, ≈1 crédito/caractere): gere as falas na voz da Radassa pelo TTS normal (SKILL.md §5, Narração), só para o cliente ouvir o texto e o tom. A voz final vem do `sts.py`.

## 3. Snapshot para fala

- Rosto grande no quadro: do peito para cima ou meio corpo, de frente ou 3/4. Rosto pequeno não segura a identidade (SKILL.md §8), e na fala a boca precisa aparecer bem.
- No 1º quadro: boca fechada ou sorriso leve, nada na frente da boca (mão, celular, cabelo) e as mãos paradas numa posição simples.
- Olhar: amiga filmando → na lente, ou no rosto dela logo acima da lente. Selfie → na própria imagem da tela, como no T3 testado (`prompts-moldes.md` §2.5).
- Luz suave e com direção no rosto: na fala aparecem dentes e o interior da boca, e sombra dura no rosto piora os dois.
- Use os moldes `prompts-moldes.md` §2.1–2.3 com essa pose. A edição de identidade é a mesma (persona §5). Revise com `qa-checklist.md` §A, com atenção à boca a 100%.

## 4. Prompt do Veo com fala

Mesmo esqueleto de `prompts-moldes.md` §2.5, mudando o miolo. O texto abaixo é molde [não testado]: preencha as chaves e mantenha o resto.

```text
Vertical 9:16 amateur smartphone video, one continuous real-time take with no cuts, filmed {QUEM FILMA, DISTÂNCIA, ALTURA, QUAL CÂMERA}: natural micro-shake and slow breathing sway, no zoom, no pan. The woman in the first frame, {ÂNCORA CURTA: adulta, cabelo, roupa}, {ONDE ESTÁ + POSE EXATA DO SNAPSHOT, COM AS DUAS MÃOS}.
[00:00-00:01] She looks {at the lens | at her own image on the screen}, relaxed, with a soft closed-lip smile, and takes a small breath.
[00:01-00:07] She speaks to the camera in Brazilian Portuguese, in a warm, natural, conversational tone, at an easy pace: "{FALA}" {UM GESTO PEQUENO: a small nod, eyebrows lifting on the key word; her hands stay as in the first frame}.
[00:07-00:08] She finishes with a closed-lip smile and holds still, blinking naturally.
Only she speaks, in a natural young adult woman's voice with a Brazilian accent; no one else speaks, no narrator, no voice-over. {REGRA DO OBJETO}. The {3-4 ELEMENTOS VISÍVEIS NO SNAPSHOT} stay exactly as in the first frame; {O QUE SE MEXE}. Light: {A MESMA DO SNAPSHOT}. Unedited, candid phone footage: natural skin texture with visible pores, natural teeth, crisp daylight frames with almost no motion blur, true-to-life colors.
Ambient noise: {CAMA}, quiet under her voice, recorded by the phone's built-in microphone. SFX: {RUÍDO NO MICROFONE}. No music. (no subtitles)
```

- O que sai do esqueleto: `Her lips stay closed the entire time...`, o "nunca som de boca" e o olhar só no rosto de quem filma.
- A fala vai entre aspas, na língua da fala (português), e o resto do prompt fica em inglês, como nos outros moldes.
- `Brazilian Portuguese` e `Brazilian accent` são obrigatórios: o `sts.py` troca o timbre, mas mantém o sotaque e a entonação da fonte.
- **negative_prompt:** a lista "Geral" do `prompts-moldes.md` §2.6, **tirando** `talking, speech, lip-syncing` e sem o conjunto de boca (`open mouth, pursed lips, ...`). Acrescente `second voice, other people talking, off-screen voice, crowd chatter`. Mantenha `narration, voice-over` (nenhum narrador além dela).
- O corpo é o mesmo do modo narrado (`generate_audio: true` é obrigatório: sem áudio não há fala), e a rodada é a do SKILL.md §5.

## 5. Escolha da variação (antes de trocar a voz)

Faça o `qa-checklist.md` §B normal e mais isto, em cada variação:
```bash
python3 -I "$SKILL/scripts/stt.py" "takes/T1_veo_v1_<id>.mp4" --out qa/T1_veo_v1_veo_stt.json | jq -r .text   # tem de bater com prompts/fala_T1.txt
```
- Palavra trocada, faltando ou sobrando: use a outra variação. Se as duas falham, regere mudando uma variável (fala mais curta ou palavra mais simples).
- Marca: o STT costuma escrever "Voltec", "Voltech" ou parecido. A tônica certa (vol-TÉC) não se mede com segurança aqui: liste o instante para o cliente ouvir no portão. Se o Veo insistir em "VÓL-tec", tire a marca da fala; ela fica nos cartões.
- Escolha in/out em pausas, nunca no meio de palavra: in ≥ 0,1 s antes da 1ª palavra e out ≥ 0,15 s depois da última (tempos do STT × 24 = quadro).

## 6. Troca de voz para a persona (`sts.py`)

```bash
python3 -I "$SKILL/scripts/sts.py" 4yvYc2GSakxLWMhlsd6b "takes/T1_veo_v1_<id>.mp4" audio/fala_T1_veo_v1_radassa.wav --seed 20261015
python3 -I "$SKILL/scripts/stt.py" audio/fala_T1_veo_v1_radassa.wav --out qa/T1_veo_v1_radassa_stt.json | jq -r .text
```
- **O que o script faz:**
  - extrai o áudio do take e envia com `eleven_multilingual_sts_v2`, o único modelo de STS com português na conta (GET /v1/models, 15/10/2026);
  - usa `wav_48000`, `remove_background_noise=true` (o ambiente do Veo sai e volta pela cama de SFX) e os settings 0.45/0.85 da voz [não testado no STS];
  - avisa se a duração mudar mais de 1 quadro.
- Use a mesma seed e os mesmos settings em todos os takes, para a voz não mudar entre cortes. Se o timbre não parecer a Radassa, suba `--similarity` ou troque a seed. Mude uma coisa por vez.
- **Custo:** ainda não medido. Na 1ª vez, compare o saldo antes e depois (só leitura):
```bash
python3 -I - <<'EOF'
import os, sys; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
st, r = el.req("GET", "/user/subscription"); print(st, r.get("character_count"), "de", r.get("character_limit"))
EOF
```
Anote o valor neste arquivo e em `modelos-e-custos.md`.

## 7. QA do take falado (além do §B)

1. **Texto:** o STT da voz trocada tem de dizer as mesmas palavras do STT do Veo (§5).
2. **Deriva de tempo:** a mesma palavra tem de começar no mesmo instante nas duas versões. Até 0,08 s (2 quadros) está ok. Acima disso, a boca sai de sincronia: troque a seed do `sts.py` ou use a outra variação.
```bash
python3 -I - qa/T1_veo_v1_veo_stt.json qa/T1_veo_v1_radassa_stt.json <<'EOF'
import json, re, sys
a, b = ([w for w in json.load(open(p))["words"] if w.get("type") == "word"] for p in sys.argv[1:])
norm = lambda w: re.sub(r"[^\wÀ-ÿ]", "", w["text"]).lower()
print("palavras:", len(a), len(b), "| mesmas palavras:", [norm(w) for w in a] == [norm(w) for w in b])
for x, y in zip(a, b): print(f'{x["text"]:>14} {x["start"]:6.2f} {y["start"]:6.2f} {y["start"] - x["start"]:+.3f}')
print("deriva máxima (s):", round(max(abs(y["start"] - x["start"]) for x, y in zip(a, b)), 3))
EOF
```
3. **Boca:** faça tiras numeradas a 24 fps (comando 3 do `qa-checklist.md` §B, com o recorte na boca), centradas nas palavras com p, b ou m, em que os lábios têm de fechar. Use os instantes do STT.
4. **Dentes e boca:** procure dentes que se fundem, somem ou tremem, e língua estranha, nas mesmas tiras.
5. **Olhar e identidade durante a fala:** folha de contato a 2 fps. A fala puxa o rosto: compare com o snapshot e a ref.
6. **Para o cliente ouvir:** liste na página a fala de cada take, cada vez que ela diz a marca e os cortes.

## 8. Edição

- **`prep.py`:**
  - `SEGMENTS` como sempre, com in/out em pausas.
  - `FALA = {"T1_veo_v1_<id>.mp4": PROJ / "audio" / "fala_T1_veo_v1_radassa.wav", ...}`.
  - `NARR = None` (só fala na câmera) ou a narração em off dos takes sem fala.
  - Os takes de `FALA` entram mudos e a fala é cortada no mesmo in/out do vídeo.
  - Gere a cama de SFX com `duration_seconds` ≥ TOTAL/24: nos takes falados, ela é o único ambiente.
- **`TOTAL`:** última palavra na linha do tempo + ~1 s, como no modo narrado.
- **Legendas:** depois do `python3 prep.py`, faça o STT da mix e converta para alignment:
  ```bash
  cd "$HF" && python3 -I "$SKILL/scripts/stt.py" media/mix.wav --out "$QA/mix_stt.json" | jq -r .text
  python3 -I "$SKILL/scripts/stt_alinhamento.py" "$QA/mix_stt.json" "$PROJ/audio/mix_alignment.json"   # imprime o texto
  ```
- **No `build_legendas.py`:**
  - `ALIGN = PROJ / "audio" / "mix_alignment.json"` e `NARR_OFFSET = 0.0`, porque a mix já está no tempo do vídeo.
  - `PHRASES` escritos a partir do texto que o conversor imprime: mesmas palavras, já com a grafia de tela do `FIX`.
  - No `FIX`, as grafias que o STT erra. Nos STT da v5 apareceram "Voltech" e "Voltek" (→ "Voltec") e "Grossaí" (→ "Grussaí").
  - `START_FIX` e `LOW_RANGES`: como sempre (edicao §8).
- **Cartões do `index.html`:** os tempos `T` ficam ancorados nas palavras do mesmo STT. Confira se legenda e cartões não cobrem a boca: no modo falando o rosto é o centro do quadro.

## 9. Riscos conhecidos [não testado]

- **Fala errada:** o Veo pode errar ou pular palavras, ou falar com sotaque de Portugal. O STT pega na escolha da variação (§5).
- **Marca:** a tônica de "Voltec" pode sair errada, e o `sts.py` não corrige pronúncia, só o timbre.
- **Sincronia:** o STS pode mexer no tempo; confira com a deriva do §7.
- **Ruídos:** respiração e estalos da voz do Veo passam para a voz trocada (`remove_background_noise` tira o ambiente, não a respiração).
- **Rosto:** fala puxa deformação de boca e dentes e deriva de identidade. Rosto grande, boa luz e tiras a 24 fps.
- **Duração:** take de 8 s limita a fala. Frase longa demais sai corrida ou cortada.

## 10. Registro

- `audio/COMO_FOI_MONTADA_fala.txt`: por take, o take do Veo, a fala, a seed e os settings do `sts.py`, in/out e a deriva medida.
- Depois do 1º vídeo real neste modo, atualize este arquivo: o que funcionou vira [vivido], e entram o custo medido do STS e o ritmo de fala do Veo.
