# Persona, voz e marca: Voltec

A personagem (a persona de IA da marca, guardada na conta ElevenLabs) é a estrela de todo vídeo realista da Voltec. Vale para qualquer campanha, estação ou tema (promoção sazonal, institucional, dica de Wi-Fi, suporte, inauguração, Black Friday) e para qualquer cenário: da área atendida (Grussaí, Atafona, Chapéu do Sol, São João da Barra) ou interno (casa, loja, carro). Rosto, pele, mãos, voz, pronúncia e marca são os mesmos em todo vídeo. Roupa, objeto, cenário, roteiro e os textos da campanha mudam a cada vídeo.

Como ler:
- **[VOLTEC]** = específico da Voltec; **[GERAL]** = vale para qualquer persona ou marca.
- **Fixo** = vale em todo vídeo da Voltec com a personagem: identidade e âncoras de rosto, pele e mãos (seções 2 a 3.3, fecho da 3.4 e tabela 3.5), refs (4), edição de identidade (5), voz, settings e pronúncia (6) e marca (7.1: logo, cores, fontes, cidades e os textos do CTA pago × orgânico).
- **Slot** = preencha a cada vídeo: roupa e objeto na mão (3.4), roteiro da narração (6), gancho, cartão da campanha, oferta, escolha do CTA (pago ou orgânico) e destino do QR (7.2) e cenário (10). A lista completa dos slots do vídeo (tema, takes, luz, som, duração, cama de SFX) está no `SKILL.md` §1b.
- **(Verão Conectado)** ou **ex.: Verão Conectado** = valor da campanha "Verão Conectado 2026", o caso de referência testado (Reels entregue em 15/10/2026). É exemplo preenchido, nunca padrão: oferta, destino do QR, cartão "VERÃO ☀ CONECTADO", gancho, roupa de praia, luz e vento de verão. Numa campanha nova, pergunte ao cliente ou refaça.
- **Nível de evidência** (o mesmo do `SKILL.md`), entre colchetes:
  - **[vivido]**: aconteceu na sessão e foi conferido no resultado.
  - **[aplicado]**: veio da pesquisa ou das críticas, entrou nos prompts finais e o resultado saiu sem o problema.
  - **[pesquisa]**: só da pesquisa.
  - **[não testado]**: derivado das regras que funcionaram, nunca gerado. Antes de mostrar ao cliente, faça o A/B do snapshot e revise com `qa-checklist.md` §A.
- **não pesquisado: pesquise com `locais-grussai.md` §7–§9** = fato de lugar (loja, carro, casa, outra praia) que ninguém conferiu. Não descreva no prompt antes de pesquisar.

Preâmbulo de shell (o mesmo em toda a skill). Variáveis não passam de uma chamada do Bash para a outra, por isso os blocos abaixo o repetem:
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
```
O projeto de referência (abaixo) é só para leitura: os comandos usam nomes de arquivo novos para não sobrescrever nada dele. A chave da API fica em `~/.config/elevenlabs/env` e `scripts/el.py` a lê sem imprimir. Nunca escreva a chave em arquivo, prompt, comando ou mensagem.

Projeto de referência: Reels "Verão Conectado", entregue em 15/10/2026, em `/home/syllas/hyperframes/voltec-reels-ia/`.

---

## 1. Regras rápidas

1. **[VOLTEC]** A personagem é a **persona da conta ElevenLabs** (fotos de uniforme Voltec, carro e loja). Não é o rosto dos frames do vídeo "selfie" antigo.
2. **[GERAL]** Ela **não fala em cena**. A voz dela entra como narração em off (Radassa). Durante a narração, a personagem fica com os lábios fechados ou num sorriso parado; boca abrindo sob a voz parece dublagem.
3. **[GERAL]** A identidade entra no vídeo **só pelo `start_frame`** (o snapshot aprovado). Nunca mande o rosto em `images` num corpo de vídeo: no Veo, `images` não combina com `start_frame`, e no Seedance o rosto em `images` cai no filtro de rosto real.
4. **[GERAL]** Faça os snapshots com **gpt-image-2.5-sunburst**. Se a semelhança ficou fraca mas a composição foi aprovada, **edite a identidade** (seção 5) em vez de regerar do zero.
5. **[GERAL]** O vídeo gerado **não tem texto nem logo**. Logo, nome, oferta e QR entram só na edição (HyperFrames).
6. **[VOLTEC]** No TTS escreva **"Voltéc"** (pronúncia vol-TÉC). Na tela e na legenda, escreva **"Voltec"**.
7. **[VOLTEC]** Em anúncio pago, o CTA é o botão **"Saiba mais" + QR na tela**. **"Link na bio"** é só para post orgânico. Pergunte qual é **antes** de gerar a narração.
8. **[VOLTEC]** O QR nunca leva ao WhatsApp (o usuário trocou explicitamente). **(Verão Conectado)** O destino foi **https://provedorvoltecinternet.online/?page_id=674**, a página "Verão Conectado 2026". Numa campanha nova, pergunte o destino ao cliente. Valide decodificando um quadro do vídeo final.
9. **[GERAL]** Ao publicar, ative o rótulo **"Informações de IA"** da Meta.
10. **[VOLTEC]** Roupa, objeto na mão e cenário são slots da campanha (seções 3.4 e 10). Só a varanda, a rede e a selfie na areia, numa tarde de verão, foram gerados. Loja, carro, casa, uniforme, inverno e noite são **[não testado]**: comece pelo A/B do snapshot e avise no portão 3 que a cena é nova.

---

## 2. [VOLTEC] A personagem

É a mesma mulher em todo vídeo da Voltec, de qualquer campanha. Só roupa, objeto e cenário mudam (slots).

- Mulher **adulta** brasileira. No prompt, escreva "an adult Brazilian woman, about 26 years old". O plano dizia 28, e a crítica apontou que isso podia envelhecer a personagem, cujo rosto nas referências aparenta 22 a 25 anos. Escreva sempre "adult".
- Pelas referências: rosto arredondado de bochechas cheias e queixo definido, pele morena média e quente, olhos castanho-escuros amendoados, sobrancelhas grossas, cabelo castanho-escuro quase preto, liso e longo, com risca levemente de lado. Unhas vinho-escuro.
- As refs da persona (seção 4) mostram **tatuagens finas de texto nos antebraços** e um **colar dourado** (foto do carro). Os dois saíram dos prompts aprovados ("No jewelry"; as tatuagens não são citadas), porque texto pequeno vira pseudo-texto e tremulação. Se o cliente fizer questão deles, confirme antes.
- **Lição [GERAL]:** o vídeo "selfie" que o usuário mandou no começo tinha **outro rosto** (genérico/glam). A sessão usou a persona da conta e avisou o usuário, que confirmou depois mandando mais fotos da mesma persona. Se aparecer uma referência com rosto divergente, avise e pergunte antes de gerar.

---

## 3. Âncoras de texto (copie igual em todo prompt do projeto)

**Snapshot novo da persona (campanha nova): siga o fluxo testado.**
1. Prompt com a âncora 3.1 e `images` = [`na7keiYvPpGArmyghOpk` (rosto), foto do local], como o T1 aprovado (`bodies/T1_gpt25.json` do Verão Conectado).
2. Compare o rosto lado a lado com o snapshot final do Verão Conectado, `HInXH8bxSo6aEH0mUmup` (o `start_frame` do T1 entregue na v5; PNG em `/home/syllas/hyperframes/voltec-reels-ia/snapshots/T1_id_a_HInXH8bxSo6aEH0mUmup.png`).
3. Se a semelhança ficar abaixo, faça a edição de identidade (seção 5: descritores 3.2 e as 3 refs) antes do portão 3 (SKILL.md §2).
4. Snapshot do zero com os descritores 3.2 ou com 2 rostos em `images` não foi testado. Se tentar, faça A/B contra o fluxo testado.

Os textos ficam em inglês porque os prompts são em inglês. Take que é edição de outro (no Verão Conectado, o T2 é edição do T1) não repete a âncora inteira.

### 3.1 Identidade (snapshots aprovados T1 e T3)
```text
an adult Brazilian woman, about 26 years old, round face with full cheeks, warm medium-tan skin, dark-brown almond-shaped eyes, thick dark defined eyebrows, a straight nose with a soft rounded tip, full lips, long straight dark-brown, almost black hair with a slight side part
```

### 3.2 Descritores refinados (da edição de identidade que gerou a versão final)
```text
her oval face with soft rounded cheeks and a defined chin, her dark-brown almond-shaped eyes, her thick, softly arched dark eyebrows, her straight nose with a soft rounded tip, her lips and smile, her warm medium-tan skin tone and her long straight dark-brown hair with a slight side part. Match her slim, average build and natural proportions from Image 4.
```
- O fluxo testado foi: snapshot com a âncora 3.1, depois edição de identidade com os descritores 3.2. Os descritores 3.2 nunca foram testados num snapshot novo, gerado do zero.
- "slim, average build" passou no gpt-image (edição de imagem). **Não leve descritor de corpo para o prompt de vídeo**, por causa da moderação do Veo.

### 3.3 Pele, mãos e cabelo (T1)
```text
Five natural fingers on each hand, visible knuckle creases, short dark wine-red nails slightly worn at the tips.
Skin and hair: real, unretouched skin with visible pores on the nose and cheeks, a faint natural shine on the forehead and nose bridge, slightly uneven tone around the mouth and chin, two tiny blemishes near the jawline, fine wispy hairs along the hairline, slightly darker skin under the eyes; light everyday makeup only; small natural asymmetry. Hair not salon-perfect, with slight humidity frizz
```

### 3.4 Roupa e objeto na mão (slot: uma âncora por vídeo)

Roupa e objeto mudam a cada vídeo. Rosto, pele e mãos (3.1 a 3.3) e o fecho do fim desta seção ficam. Escreva a âncora de roupa uma vez e copie-a palavra por palavra em todos os prompts do vídeo, em 3 tamanhos [vivido]:
- **longa**, no `Subject` do snapshot (`prompts-moldes.md` §2.1 e §2.3);
- **curta**, no `{OUTFIT}` da edição de identidade (seção 5);
- **curtíssima**, na âncora do prompt de vídeo (`The woman in the first frame, ..., wearing ...`; `prompts-moldes.md` §2.5).

**Regras para escrever uma âncora de roupa nova** (tiradas do que funcionou):
1. **Opaca e casual, sem transparência nem decote.** A gola testada é a redonda. Nada de `sheer`, `lace`, `low-cut` ou `tight` (lista na 3.5). Isso também reduz o risco de moderação. [aplicado]
2. **Lisa:** sem estampa, logo, bordado, número ou texto. A marca entra só no overlay. [aplicado: `plain` nas peças e `the clothes have no print` no fecho dos prompts aprovados] Escrever `without any logo, print or lettering` no prompt vem da pesquisa e nunca foi gerado [pesquisa].
3. **Sem padrão fino:** tecido liso ou de trama grande (o crochê de trama aberta passou). Padrão miúdo e franja tremulam (`prompts-principios.md` §1.4). [aplicado]
4. **Sem joias:** `No jewelry`; as tatuagens de texto das refs ficam fora do prompt (seção 2) [aplicado]. A pesquisa também tira óculos escuros, chapéu e brinco pendente, que o vento deforma [pesquisa].
5. **Peças com nome simples** (`white cotton tank top`, `light-wash denim shorts`), sem marca nem modelo de produto (moderação Third-party, 3.5). [aplicado]

**Ex.: Verão Conectado [vivido]** (roupa de praia dos 3 takes aprovados):
```text
She wears a loose, hip-length white cotton crochet beach cover-up with a large open-weave pattern and three-quarter sleeves, worn open over a plain white cotton tank top with a round neckline, and light-wash denim shorts. No jewelry.
```
- Curta (`{OUTFIT}`): `loose white crochet cover-up over a plain white tank top, light-wash denim shorts`.
- Curtíssima (vídeo): `wearing a white crochet beach cover-up over a white tank top`. No T1, que mostra as pernas, foi `... and light denim shorts`.

**Exemplos de âncora nova [não testado]** (derivados das regras acima; faça o A/B do snapshot e a revisão do `qa-checklist.md` §A antes de mostrar ao cliente):

| Cena | Âncora longa | Cuidados |
|---|---|---|
| Uniforme da Voltec liso, **sem logo** (loja, suporte, institucional) | `She wears a plain red short-sleeved cotton polo shirt with navy-blue sleeves trimmed in red at the cuffs, navy-blue side panels, a red collar and a white button placket buttoned to the top, without any logo, print, embroidery or lettering, and dark-blue jeans. No jewelry.` | Cores e corte do uniforme das refs (`persona_corpo_inteiro.jpg`). O logo bordado das refs vaza texto: a marca entra só no overlay. A gola polo abotoada é fechada, mas não é a gola redonda testada. Revise o peito a 100% (logo inventado ou remendo). |
| Inverno, lisa e casual | `She wears a plain heather-gray cotton sweatshirt with a round neckline and long sleeves, without any logo, print or lettering, and dark-blue jeans. No jewelry.` | Moletom liso ou tricô de ponto grosso (`chunky knit`); ponto miúdo e trança tremulam. Sem cachecol nem gorro (regra 4). Luz de inverno em `locais-grussai.md` §3; o vento fora do verão não foi pesquisado. |
| Loja ou escritório, casual | `She wears an open, plain navy-blue cotton blazer over a plain white cotton T-shirt with a round neckline, and dark-blue jeans, without any logo, print or lettering. No jewelry.` | Mesma estrutura da roupa testada: camada aberta sobre blusa lisa de gola redonda. |

No molde-base de cena (`prompts-moldes.md` §2.9), o `{OUTFIT}` é só a descrição da roupa: tire o `She wears` e o `No jewelry.`, que o molde já tem.

**Objeto na mão.** Um só, já na mão no 1º quadro, inteiro no quadro e sem marca. Não mande abaixar, guardar nem girar (`prompts-principios.md` §1.4). Ex.: Verão Conectado [vivido], o celular, quando aparece no quadro (no T3 em selfie ele é a câmera e não aparece):
```text
one smartphone in a plain matte black case with no logo; the whole phone is inside the frame with space above it; the screen faces down toward her, fingers wrapped around the back, thumb on the side edge, so only the back of the phone is visible.
```
Outro objeto, como roteador ou notebook, é [não testado]: valem as mesmas regras, sem tela, etiqueta ou marca à vista. A ref da loja com headset mostra o risco: o notebook dela tem a marca legível na tampa.

**Fecho fixo de todo snapshot**, em qualquer campanha:
```text
There is no text, sign, number, logo or watermark anywhere, the clothes have no print, and there are no other people in the frame.
```

### 3.5 O que evitar

| Evite | Por quê | Use |
|---|---|---|
| "28 years old", "girl", "young girl", "teen", "cute", "petite" | Envelhece o rosto ou aciona o filtro "Child" do Google | "an adult Brazilian woman, about 26 years old" |
| "baby hairs" | Gatilho evitável do filtro "Child" | "fine wispy hairs along the hairline" |
| Descritor de corpo no vídeo (body, figure, curves, slim waist, legs, hips, chest, thighs) | Moderação | "medium shot", "her left hand rests in her lap" |
| sheer, see-through, lace, low-cut, plunging, cleavage, bikini, swimsuit, tight, revealing, wet | Moderação. A selfie antiga tinha renda transparente e decote V | Roupa opaca de gola redonda (3.4; ex.: Verão Conectado, crochê opaco sobre regata de gola redonda) |
| Uniforme com logo, estampa, letreiro | O vídeo não pode ter texto nem logo | Roupa lisa "without any logo, print or lettering"; a marca entra só no overlay |
| iPhone, WhatsApp, FaceTime, Instagram, Havaianas; nome de famoso | Categorias Third-party e Celebrity | "smartphone", "video call" |
| Colar, brincos, tatuagens de texto | Pseudo-texto e tremulação | "No jewelry" |
| Headset ou acessórios presentes nas refs | Vazam para a cena | Recorte a ref ou não a use |
| Olhar cravado na lente | Linguagem de anúncio | "looks at her friend's face just above the lens"; na selfie, "her eyes aim slightly below the lens" |
| Boca abrindo sob a narração (risada aberta, bufada, sopro) | Parece dublagem. "huffs once through her nose" virou uma boca em "O" | "Her lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth" (mais em `references/prompts-principios.md` §1.5 e §3.1) |

Moderação já vista na conta: um Veo Fast foi bloqueado com o support code **15236754** ("Celebrity"). Se acontecer de novo, mude o ângulo ou a expressão e deixe o rosto maior no quadro. Não repita o mesmo pedido. Bloqueios e falhas não são cobrados.

---

## 4. Referências na conta ElevenLabs e o que funcionou

Os arquivos locais ficam em `/home/syllas/hyperframes/voltec-reels-ia/refs/`. Os IDs vêm da pesquisa e de `/home/syllas/hyperframes/voltec-reels-ia/bodies/assets.json`. A pesquisa conferiu (md5 idêntico) que `hTTaqslvmsLwuN5qwT4W`, `9snOZM2EfiYIjKtqfsW2` (e as duas duplicatas) e `bZiCdj3zIGYdX0UKyfvU` são os arquivos locais. Os assets enviados na sessão estão mapeados em `bodies/assets.json` (`headshot`, `restinga`, `rosto_loja`, `corpo_sem_logo`).

| asset_id | O que é | Arquivo local | Usar? |
|---|---|---|---|
| `na7keiYvPpGArmyghOpk` | Rosto da foto do carro, recorte 730x730 sem dedos e sem colar | `persona_headshot_sem_dedos.jpg` | **Sim**: rosto em todos os snapshots aprovados e na edição de identidade ("ignore the car interior behind her") |
| `pUgU1HXgmdqXfP02iR8T` | Rosto da foto da loja, recorte 420x420 | `novas_20261015/ref_a_rosto_crop.jpg` | **Sim**: 2º rosto na edição de identidade |
| `ZY1iDcJLhPFklahPnvkM` | Corpo inteiro com o logo do uniforme apagado | `persona_corpo_inteiro_sem_logo.jpg` | **Sim**: proporções na edição de identidade |
| `hTTaqslvmsLwuN5qwT4W` | Foto do carro inteira | `persona_carro.jpg` | Só se faltar o recorte: tem dedos no queixo, colar e alça vermelha |
| `9snOZM2EfiYIjKtqfsW2` (duplicatas `WsxbGI8G837Wl8ofKmBC`, `Ls8V07Oeh6TUw6C7E6Qm`) | Corpo inteiro de uniforme vermelho com logo VOLTEC bordado | `persona_corpo_inteiro.jpg` | **Não** direto: o logo e o vermelho vazam. Use `ZY1iDcJLhPFklahPnvkM` |
| `bZiCdj3zIGYdX0UKyfvU` | Loja com letreiro VOLTEC enorme | `persona_loja_logo.jpg` | **Não**: vaza texto |
| (sem asset) | Frames do vídeo "selfie" antigo | `persona_selfie_*.jpg` | **Não**: outro rosto (genérico/glam), renda transparente, decote V, pôr do sol no mar |
| (sem asset) | Loja com headset | `novas_20261015/ref_c_chatgpt_131820.jpg` | **Não**: o fone vaza para a cena |
| (sem asset) | Passarela de madeira, corpo inteiro | `novas_20261015/ref_d_129987.jpg` | **Não**: rosto pequeno (e a saída de praia é de renda transparente) |

A foto real do local usada no Verão Conectado (restinga de Grussaí, CC BY) também já está na conta: `Mf1kechhOOoqJO70sPNd`. Ver `references/locais-grussai.md`. Para cenas de loja, carro ou uniforme, os riscos que estas refs mostram e como enquadrar sem texto estão na seção 10.

### Snapshots aprovados do Verão Conectado (generation_id)
Os PNGs ficam em `/home/syllas/hyperframes/voltec-reels-ia/snapshots/`, e as versões 1080x1920 em `snapshots/normalizados/`.

| Take | Final aprovado (com edição de identidade) | Base, antes da edição |
|---|---|---|
| T1: varanda, celular erguido | `HInXH8bxSo6aEH0mUmup` (`T1_id_a_…png`) | `5vBTv3B9FOt44Vu8jMY4` |
| T2: rede, chamada de vídeo | `e7k1uG3FnY3q8R0oUuCG` (`T2_id_a_…png`) | `0fZysnZPt1Xmk1RaJF5H` |
| T3: selfie na areia | `O2D10yzDXIp2eu8jbhtj` (`T3_id_a_…png`) | `gXl0EPY5A3LhPnLlHbBv` |

- O snapshot aprovado vira o **start_frame** do vídeo. O T1 final usou `"start_frame": {"type": "generation", "generation_id": "HInXH8bxSo6aEH0mUmup"}`.
- Numa cena nova com a mesma roupa e o mesmo cabelo, ele vira a **Image 1** ("Image 1 is a frame from earlier the same afternoon: keep exactly the same woman, hair and outfit"). Foi assim que o T3 nasceu do T1.
- O `generation_id` precisa existir no workspace. Se a API recusar o pedido (a recusa não é cobrada), suba o PNG local como asset.

### Regras de referência [GERAL]
- O rosto vai **grande e de frente**, em boa resolução. Tire dedos e mãos do recorte, tire logo e letreiro (ffmpeg `delogo` ou recorte) e tire acessórios que possam vazar (headset). Rosto pequeno no quadro não serve.
- Nos modelos de imagem não existe campo de papel: **a ordem das imagens e uma frase no prompt** dizem o que cada uma é ("Image 1 is the woman's face: keep her exact identity, facial proportions, skin tone, eyes, eyebrows, nose, lips and hair; ignore the car interior behind her").
- O snapshot inicial que funcionou (T1) usou **1 rosto + 1 foto do local**. A pesquisa recomenda no máximo 2 refs de identidade, porque mais rostos aumentam a deriva. Na edição de identidade foram 3 refs mais a Image 1, e o resultado foi aprovado.
- **gpt-image-2.5-sunburst** (`aspect_ratio` "9:16", `resolution` "2K", que sai em 1152x2048, `quality` "high", ≈554 créditos por imagem) manteve rosto e roupa. **gemini-3-pro-image** afinou e alterou o rosto e trocou a roupa.

Preparar refs novas (as da Voltec acima já estão prontas e na conta):
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
cd "$PROJ"
# apagar logo/letreiro: a caixa x/y/w/h é a do logo NESSA foto.
# Na foto de corpo inteiro da Voltec foi x=850:y=1560:w=180:h=90 (testado: o "VOLTEC" some)
ffmpeg -i refs/ref_corpo.jpg -vf 'delogo=x=850:y=1560:w=180:h=90' refs/ref_corpo_sem_logo.jpg
# recortar o rosto sem dedos (caixa esquerda, topo, direita, base).
# Na foto do carro da Voltec foi 445,792,1175,1522 -> 730x730
python3 -I -c "from PIL import Image; Image.open('refs/ref_rosto.jpg').crop((445, 792, 1175, 1522)).save('refs/ref_rosto_sem_dedos.jpg', quality=95)"
# subir como asset (upload não gasta crédito); anote o asset_id em bodies/assets.json
python3 -I "$SKILL/scripts/el.py" upload refs/ref_rosto_sem_dedos.jpg
```

---

## 5. Fluxo de edição de identidade

A mecânica é **[GERAL]**; os IDs são da Voltec.

**Quando usar:** o cliente aprovou a composição, a pose e o lugar, mas o rosto não está igual o bastante, ou chegaram refs novas. A edição preserva o quadro aprovado; regerar do zero perde a composição. No projeto, o feedback 2 (refs novas) foi resolvido assim, numa única rodada a/b aprovada, e os 3 vídeos foram refeitos a partir das versões editadas.

**Passos**
1. Image 1 = o snapshot aprovado (`{"type": "generation", ...}`). Images 2 a 4 = rosto do carro sem dedos, rosto da loja recortado e corpo sem logo.
2. Preencha `{OBJECT}`, `{OUTFIT}`, `{SETTING}` e `{EXPRESSION}` com o que está na Image 1; não mude o resto do texto. Numa campanha nova, `{OUTFIT}` é a versão curta da âncora de roupa da campanha (3.4) e `{OBJECT}` é o objeto que ela segura: nunca deixe no prompt uma roupa ou um objeto que não está na imagem. Com o uniforme liso na Image 1 [não testado], o `ignore ... the red uniform, the logo` do molde fala das refs, não da Image 1: revise o peito a 100% (logo inventado ou remendo).
3. Gere **2 variações** (a/b). O gpt-image não tem seed, e cada request gera 1 imagem (≈554 créditos).
4. Revise a 100%: 5 dedos por mão, pegada coerente, unhas, dentes, olhos, padrão da roupa (no Verão Conectado, o crochê), horizonte, nenhum texto. Compare lado a lado com as refs.
5. Mostre ao cliente lado a lado (antes e depois, a e b). Com a aprovação, o resultado vira o `start_frame` do vídeo. Na sessão, a variante "a" venceu nos 3 takes.

**Molde** (o `prompts/identidade_edit.txt` testado, com o objeto e a roupa como campos)
```text
Edit Image 1, a frame from a casual smartphone video. Keep everything in Image 1 exactly as it is: the framing and camera angle, her pose and the position of her hands and arms, {OBJECT}, the outfit ({OUTFIT}), {SETTING}, the light and the phone-camera look. Change only the woman's likeness so she is unmistakably the same person shown in Images 2, 3 and 4: her oval face with soft rounded cheeks and a defined chin, her dark-brown almond-shaped eyes, her thick, softly arched dark eyebrows, her straight nose with a soft rounded tip, her lips and smile, her warm medium-tan skin tone and her long straight dark-brown hair with a slight side part. Match her slim, average build and natural proportions from Image 4. Keep her expression from Image 1: {EXPRESSION}. Use the references only for her identity and build: ignore their backgrounds, the car, the red uniform, the logo and the signs. Real, unretouched skin with visible pores, a faint natural shine and small natural asymmetry; natural hands with five fingers each and short dark wine-red nails. There is no text, logo or watermark anywhere.
```

Valores usados no Verão Conectado. Com esses valores, o texto é idêntico ao testado (`bodies/T1_id_a.json`, `T2_id_a.json` e `T3_id_a.json`):

| Take | `{OBJECT}` | `{OUTFIT}` | `{SETTING}` | `{EXPRESSION}` |
|---|---|---|---|---|
| T1 | the phone | loose white crochet cover-up over a plain white tank top, light-wash denim shorts | the shaded balcony with the white wall, the hammock behind her, the casuarinas and the sea | squinting up at the phone with a frustrated half-frown, lips closed |
| T2 | the phone | loose white crochet cover-up over a plain white tank top, light-wash denim shorts | the same balcony with the off-white hammock, the white wall, the casuarinas and the sea | a closed-lip smile while looking at the phone screen |
| T3 | the phone | loose white crochet cover-up over a plain white tank top, light-wash denim shorts | the wide flat beach with the sea on the left, the dunes and casuarinas on the right and the low sun behind her | a soft closed-lip smile while looking at her own image on the phone screen |

Corpo (igual ao `bodies/T1_id_a.json` do Verão Conectado; num projeto novo, salve como `bodies/T1_id.json` com o seu snapshot na Image 1):
```json
{
  "model_id": "gpt-image-2.5-sunburst",
  "prompt": "<molde preenchido>",
  "aspect_ratio": "9:16",
  "resolution": "2K",
  "quality": "high",
  "images": [
    {"type": "generation", "generation_id": "5vBTv3B9FOt44Vu8jMY4"},
    {"type": "asset", "asset_id": "na7keiYvPpGArmyghOpk"},
    {"type": "asset", "asset_id": "pUgU1HXgmdqXfP02iR8T"},
    {"type": "asset", "asset_id": "ZY1iDcJLhPFklahPnvkM"}
  ]
}
```

Enviar as 2 variações, esperar e baixar (cada POST aceito gasta ≈554 créditos):
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
export TAKE=T1
mkdir -p "$PROJ/snapshots" && cd "$PROJ"
python3 -I - <<'EOF'
import json, os, sys; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
TAKE = os.environ["TAKE"]
body = json.load(open(f"bodies/{TAKE}_id.json"))
os.makedirs("snapshots", exist_ok=True)
ids = {}
for v in ("a", "b"):
    st, r = el.submit("image", body)          # só o aceite (200 com id) é cobrado; recusa 422/429 não
    print(v, st, r.get("id") if st == 200 else r)
    if st == 200:                             # grava a cada aceite: se o "b" for recusado, o id do "a" não se perde
        ids[f"{TAKE}_id_{v}"] = r["id"]
        json.dump(ids, open(f"snapshots/{TAKE}_id_ids.json", "w"), indent=1)
EOF
# espera e baixa (só GET): snapshots/<nome>_<id>.<ext>, com a extensão tirada do content_mime_type
python3 -I "$SKILL/scripts/poll_round.py" "snapshots/${TAKE}_id_ids.json" --kind image --out snapshots
```
Corpos, polling e normalização para 1080x1920 estão detalhados em `references/api-elevenlabs.md` e `references/edicao-hyperframes.md`.

---

## 6. [VOLTEC] Voz Radassa (narração)

| voice_id | Nome | O que é | Usar? |
|---|---|---|---|
| `4yvYc2GSakxLWMhlsd6b` | Radassa 100% | Clone instantâneo (IVC) com 3 amostras somando ~81 s. Limpa: as pausas ficam em silêncio digital | **Principal**: é a "Voz A", aprovada pelo cliente |
| `eHs9HKeucCzJ3ChAjmII` | Radassa | IVC com 8 amostras de 8 a 10 s extraídas de vídeos de IA, com ruído de fundo (−40 a −90 dB) | Só para A/B. O eleven_v4 copia o ruído do treino |

**Settings aprovados:** `model_id` "eleven_v4", `stability` 0.45, `similarity_boost` 0.85, `language_code` "pt", `apply_text_normalization` "auto", seed fixo e saída `wav_48000` (PCM 16 bits, mono, 48 kHz).
- **Sempre sobrescreva** os settings salvos na voz (0.2/0.3), que são baixos demais para o v4.
- O v4 não tem `style`, `speed`, `speaker_boost` nem `<break>`. A duração se ajusta pelo tamanho do texto.
- Ajustes da pesquisa, **não testados**: entrega teatral ou instável → stability 0.55; monótona → 0.38.
- A voz A já foi aprovada. Daqui em diante, o A/B é entre seeds da mesma voz (o projeto gerou `narracao_v2_A_s1` e `_s2`; ficou a s1, seed 20261015).

Gerar com timestamps. Gera a narração inteira **numa request só**, para a prosódia ficar contínua, e salva o alignment usado pelas legendas. Nomes: `bodies/tts_<vN>_s<seed>.json` → `audio/narracao_<vN>_s<seed>.wav` + `audio/narracao_<vN>_s<seed>_alignment.json`:
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$PROJ"/{bodies,audio} && cd "$PROJ"
python3 -I - <<'EOF'
import json, os, sys; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
V, SEED = "v1", 20261015
body = {
    "text": open(f"prompts/narracao_{V}.txt").read().strip(),   # roteiro com tags e "Voltéc"; sem o "\n" final (o alignment da sessão não o tem)
    "model_id": "eleven_v4",
    "language_code": "pt",
    "voice_settings": {"stability": 0.45, "similarity_boost": 0.85},
    "apply_text_normalization": "auto",
    "seed": SEED,
}
json.dump(body, open(f"bodies/tts_{V}_s{SEED}.json", "w"), ensure_ascii=False, indent=1)
# POST /v1/text-to-speech/<voz>/with-timestamps?output_format=wav_48000  (GASTA CRÉDITOS)
# -> audio/narracao_v1_s20261015.wav + audio/narracao_v1_s20261015_alignment.json (characters / start / end por caractere)
print(el.tts("4yvYc2GSakxLWMhlsd6b", body, f"audio/narracao_{V}_s{SEED}"))
EOF
```
Pela linha de comando é a mesma coisa: `python3 -I "$SKILL/scripts/el.py" tts 4yvYc2GSakxLWMhlsd6b bodies/tts_v1_s20261015.json audio/narracao_v1_s20261015`.
Custo: ≈1 crédito por caractere. Para o A/B de seeds, rode de novo com outro `SEED` (ex.: 20261016).

**Roteiro: slot da campanha.** O texto sai do portão 1: gancho, oferta e CTA mudam a cada vídeo. A forma é fixa: primeira pessoa, coloquial, "Voltéc" no TTS, números por extenso, no máximo 1 tag a cada 1 ou 2 frases, o CTA do modo escolhido (7.1) e a narração inteira numa request. A duração do vídeo sai do alignment (`SKILL.md` §4).

**Ex.: Verão Conectado [vivido]**, roteiro aprovado (`prompts/narracao_v3.txt`; ordem gancho → virada → cidades → oferta → CTA; use como molde de tom):
```text
[frustrated] Casa de praia sem internet? Ninguém merece...
[relieved, smiling] Agora sim! Com a Voltéc eu fico conectada o verão inteiro.
Tem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra.
[upbeat] Sem fidelidade: planos de dois a cinco meses.
[excited] Clica no botão Saiba Mais ou escaneia o QR code na tela!
```
- As tags `[frustrated]`, `[relieved, smiling]`, `[upbeat]` e `[excited]` não são lidas em voz alta (duram ~0,1 s no alignment). A pesquisa recomenda no máximo 1 tag a cada 1 ou 2 frases.
- Escreva números por extenso no TTS ("dois a cinco"). Na legenda e na tela, use dígitos ("2 a 5").

**Pronúncia**
- **"Voltec" = vol-TÉC** (confirmado pelo cliente). No TTS escreva **"Voltéc"**; na tela e na legenda, "Voltec". O `build_legendas.py` faz a troca pelo `FIX`, que já vem com `{"Voltéc": "Voltec"}`; os números falados por extenso entram no mesmo `FIX` a cada vídeo (Verão Conectado: `"dois": "2"`, `"cinco": "5"`; nunca "um", que também é artigo).
- Você não ouve áudio: confira a tônica medindo, e o texto com STT.
  ```bash
  export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
  export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
  export HF="$PROJ/reels-final" QA="$PROJ/qa"
  export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
  cd "$PROJ"
  python3 -I "$SKILL/scripts/stress.py" audio/narracao_v1_s20261015.wav audio/narracao_v1_s20261015_alignment.json
  python3 -I "$SKILL/scripts/stt.py" audio/narracao_v1_s20261015.wav | jq -r .text   # tem de bater com o roteiro sem as tags
  ```
  A saída esperada do `stress.py`, para cada "Voltéc", é "tônica no fim". É uma heurística: a parte "téc" sai mais longa que a "Vol" e com energia de pelo menos 80% da dela. Use o WAV cru do TTS, sem corte nem atraso. Liste na página do portão o instante de cada "Voltec" (o `@` da saída) e peça ao cliente para confirmar ouvindo no portão.
- "Grussaí" é oxítona. Escrita normal, saiu certa no Verão Conectado. Se errar, a pesquisa sugere "Grussa-í" ou o IPA "/ɡɾusaˈi/" (não foi preciso testar).
- STT da narração (o comando acima). Em toda campanha, liste no portão as palavras em que o STT ouviu algo diferente do roteiro. Ex.: Verão Conectado [vivido]: o STT ouve "conectado" em "conectada o verão" por causa da ligação entre as palavras. Mostre ao cliente; se incomodar, regere só a frase com vírgula ("conectada, o verão inteiro") e emende. É uma frase do meio: veja o limite em `api-elevenlabs.md` §5.5 (não testado).
- O alignment às vezes erra: marcou uma pausa inexistente antes de "internet?" e atrasou "Voltec" em ~0,1 s. Corrija os inícios à mão (`START_FIX` no `build_legendas.py`), medindo com STT ou com o envelope do áudio.

**Trocar uma frase sem refazer a narração** (como o CTA virou "Saiba Mais")

Passo 1. Gere **só a frase nova**, com a mesma voz e os mesmos settings, seed novo e `previous_text` = as frases anteriores. Gere 2 ou 3 seeds (o projeto gerou `cta_v3_20261015`, `…16` e `…17`; ficou a 20261017). Você não ouve áudio: descarte por medida (STT de cada seed tem de bater com o texto, sem `audio_event`; `stress.py` se a frase tiver "Voltéc") e ponha as que passarem na página do portão, com player, para o cliente escolher ouvindo. Corpo:
```json
{"text": "[excited] Clica no botão Saiba Mais ou escaneia o QR code na tela!",
 "model_id": "eleven_v4", "language_code": "pt",
 "voice_settings": {"stability": 0.45, "similarity_boost": 0.85},
 "apply_text_normalization": "auto", "seed": 20261017,
 "previous_text": "Tem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra. Sem fidelidade: planos de dois a cinco meses."}
```

Passo 2. Corte a narração aprovada num silêncio, aplique um fade de 20 ms, acrescente um silêncio curto e a frase nova com o ganho casado (−3 dB casou com a frase anterior). Para casar o ganho sem ouvir, compare o loudness integrado (filtro `ebur128`) da frase anterior, recortada com `atrim` pelos tempos do alignment, com o da frase nova, e use a diferença no `volume=` (medido depois nos arquivos do projeto: −18,2 LUFS × −15,2 LUFS = −3,0 dB, o valor usado). Comando usado no projeto, rodado dentro de `audio/` (sem `-y`, o ffmpeg pergunta antes de sobrescrever). Num projeto novo, troque os nomes (convenção `narracao_<vN>_s<seed>.wav`) e o ponto de corte:
```bash
ffmpeg -i narracao_v2_A_s1.wav -i cta_v3_20261017.wav -filter_complex "[0:a]atrim=end=15.05,asetpts=N/SR/TB,afade=t=out:st=15.03:d=0.02[a];anullsrc=r=48000:cl=mono,atrim=duration=0.17[g];[1:a]aresample=48000,aformat=channel_layouts=mono,volume=-3.0dB,asetpts=N/SR/TB[b];[a][g][b]concat=n=3:v=0:a=1[out]" -map "[out]" -ar 48000 -ac 1 narracao_v3.wav
```
Confira a emenda sem ouvir, como em `references/qa-checklist.md` §C.4 (espectrograma do trecho: clique ou degrau = linha vertical fina), e liste o instante dela na página do portão para o cliente ouvir (no projeto, 15,05–15,22 s da narração; no vídeo, some o `NARR_OFFSET` do `prep.py`, que foi 0,30 s).

Passo 3. Junte os alignments, deslocando a frase nova pelo corte mais o silêncio (+15,22 s no projeto). O código único fica em `references/api-elevenlabs.md` §5.5 (variáveis `APROVADA`, `NOVA`, `SAIDA`, `CORTE`, `SILENCIO` e `TROCADA`). Use o mesmo corte e o mesmo silêncio do ffmpeg do passo 2 e grave a saída com nome novo (no projeto, ela foi `narracao_v3_alignment.json`). Com os valores do Verão Conectado, o código reproduz as palavras e os tempos usados nas legendas.

Passo 4. **Registre a montagem** em `prompts/narracao_vN.txt` e em `audio/COMO_FOI_MONTADA_narracao_vN.txt`. Sem esse registro, uma regeração futura traz o CTA antigo de volta.

**Consentimento [GERAL]:** se "Radassa 100%" for a voz de uma pessoa real, mantenha o consentimento dela documentado. É exigência da ElevenLabs para clonagem.

---

## 7. [VOLTEC] Marca

Duas partes: **7.1 Fixos**, iguais em todo vídeo da Voltec, e **7.2 Slots da campanha**, preenchidos a cada vídeo, com o Verão Conectado como exemplo.

### 7.1 Fixos (todo vídeo da Voltec)

#### Logo
- **Oficial:** vem do site voltecautomacao.com.br, no caminho `wp-content/uploads/2026/06/LOGOMARCA-VOLTEC-branco-1.png` (1920x710, branca, para fundo escuro).
- **Versão para fundo claro**, já pronta, com letras pretas e o raio e as ondas de wi-fi em vermelho: `/home/syllas/hyperframes/verao-conectado/assets/logo-voltec.png` (1920x710, PNG com transparência). Há cópias idênticas em `/home/syllas/hyperframes/voltec-reels-ia/reels-final/assets/logo-voltec.png` e `logo-voltec-cta.png`.
- **Nunca redesenhe a logo à mão**: o usuário rejeitou a versão recriada. A versão clara vai sempre sobre cartão ou pílula branca.
- A logo nunca vai como referência para o gerador de imagem ou vídeo; ela só entra no overlay.

#### Cores e fontes
O template base é `/home/syllas/hyperframes/reels/template.html`. A composição do Verão Conectado é `/home/syllas/hyperframes/voltec-reels-ia/reels-final/index.html`; a versão generalizada fica em `scripts/index_template.html`.

| Token | Valor | Onde (exemplos do Verão Conectado) |
|---|---|---|
| `--red` | `#d7262f` | "VERÃO", faixa "Planos sem fidelidade", pinos das cidades, "ASSINE AGORA", "Saiba mais" |
| `--dark` | `#2f2f33` | "CONECTADO", faixa "de 2 a 5 meses" |
| `--ink` | `#1f1f22` | Texto sobre cartão branco |
| `--panel` | `#ffd6a1` | Painel claro do template (opcional) |
| cinza | `#6a6a70` | Textos secundários ("TEM VOLTEC EM", "aqui na tela", linha de cidades) |
| sol | `#f39a1e` (raios), `#f6a623` (disco) | Ícone de sol entre "VERÃO" e "CONECTADO" (cor só do cartão dessa campanha, não da marca) |
| legenda | fundo `rgba(18,18,20,0.68)`, texto `#fff`, palavra falada `#ffd36b` | Versão com legendas |
| véu do CTA | `rgba(24,14,6,0.38)` | Escurece o vídeo desfocado sob o cartão final |

- **Montserrat 800/900:** títulos, pergunta do gancho, oferta, CTA e legendas.
- **Barlow 600/700:** textos de apoio (cidades, texto do QR). O template também carrega o peso 500.
- `<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Barlow:wght@600;700&display=block" rel="stylesheet" />`
- Elementos fixos: cartão branco (raio de 26 px, sombra suave); pergunta do gancho em caixa branca no estilo do texto nativo do Instagram; pinos vermelhos nas cidades, que acendem quando a narração fala cada nome; oferta em faixa vermelha com subfaixa escura. O texto do gancho, o cartão da campanha e a oferta são slots (7.2).
- Texto nunca vai sobre o rosto ou o corpo dela. Zona segura do Reels: x 64–930, y 220–1480 (mais em `references/edicao-hyperframes.md`).

#### QR: gerar, conferir e validar
- **Nunca o WhatsApp**: o usuário trocou explicitamente. O destino é slot da campanha (7.2): pergunte ao cliente e confira se a página está no ar (curl abaixo).
- **Gerar, antes do `prep.py` e do render.** O template da skill (`scripts/index_template.html`) carrega `assets/qr.svg`. Sem esse arquivo, o render do HyperFrames 0.8.161 sai sem QR e não falha. Com a URL do Verão Conectado, o comando abaixo gera um SVG idêntico, byte a byte, ao `qr-checkout.svg` do projeto de 15/10 (nível M, margem 0; conferido com qrcode 1.5.4). No projeto do Verão Conectado o arquivo se chamava `assets/qr-checkout.svg`; o template espera `assets/qr.svg`. Os pacotes ficam em `$FERR/qr`, fora do projeto, e servem também ao `scripts/decode.cjs` (ver `references/qa-checklist.md`):
  ```bash
  export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
  export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
  export HF="$PROJ/reels-final" QA="$PROJ/qa"
  export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
  [ -d "$FERR/qr/node_modules/jsqr" ] || (mkdir -p "$FERR/qr" && cd "$FERR/qr" && npm i qrcode@1.5.4 jsqr@1.4.0 pngjs@7.0.0)   # só na 1ª vez; precisa de rede
  URL="https://provedorvoltecinternet.online/?page_id=674"   # (Verão Conectado) campanha nova: a URL que o cliente indicar
  mkdir -p "$HF/assets" && cd "$HF"
  node -e 'require("qrcode").toString(process.argv[1], {type: "svg", errorCorrectionLevel: "M", margin: 0, color: {dark: "#111111", light: "#ffffff"}}, (e, s) => { if (e) throw e; require("fs").writeFileSync("assets/qr.svg", s) })' "$URL"
  ```
- **Conferir se a página está no ar.** Na sessão, o curl simples já tomou 406 do site. Com headers de navegador, deu 200 em 15/10/2026 (campanha nova: troque a URL):
  ```bash
  curl -sS -o /dev/null -w '%{http_code}\n' -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" -H "Accept: text/html" "https://provedorvoltecinternet.online/?page_id=674"
  ```
- **Validar sempre:** extraia um quadro do CTA do vídeo final e decodifique com `scripts/decode.cjs`. Faça isso na master e na versão do Instagram (passo a passo em `references/qa-checklist.md`).

#### CTA: pago × orgânico
Os textos de cada modo são fixos. Qual dos dois o vídeo usa é slot (7.2), perguntado no portão do roteiro.

| | Anúncio pago (tem botão) | Post orgânico (sem botão) |
|---|---|---|
| Narração | "Clica no botão Saiba Mais ou escaneia o QR code na tela!" | "Assina pelo link na bio!" (a bio do Instagram tem link de contato) |
| Cartão final | "ASSINE AGORA" / "clique em **Saiba mais**" / QR + "ou escaneie o QR code / aqui na tela" / linha das cidades | Logo + "ASSINE AGORA" + "link na bio" + QR |
| Animação | Pulso no "Saiba mais" e no QR, cada um no instante em que a voz fala a palavra | — |

Lição [vivido]: a v3 saiu com "link na bio", mas o anúncio teria botão. Corrigir custou gerar a frase de novo e emendar (seção 6) e mexer no cartão. **Pergunte no portão do roteiro.**

#### Cidades e pronúncia
- **Cidades atendidas:** Grussaí, Atafona, Chapéu do Sol e São João da Barra, nesta ordem na narração e no cartão "Tem Voltec em". No CTA aparecem como "Grussaí · Atafona · Chapéu do Sol · São João da Barra".
- **Pronúncia:** vol-TÉC. "Voltéc" no TTS; "Voltec" na tela e na legenda (seção 6).

### 7.2 Slots da campanha (preencha a cada vídeo)

Pergunte no portão 1 (`SKILL.md` §1b e §2). O que vem do cliente **não se inventa**: as fontes desta skill não têm preço, prazo nem condição de oferta.

| Slot | Quem define | Regra | Ex.: Verão Conectado [vivido] |
|---|---|---|---|
| Gancho | Você propõe; o cliente aprova no portão 1 ou 2 | Pergunta curta na caixa branca (7.1), fora do rosto, no espaço que o prompt do snapshot já reservou | "Casa de praia sem internet?" (1ª frase da narração), no céu à direita do T1, reservado com `open sky in the upper right of the frame`; o celular fica à esquerda |
| Cartão da campanha | Você propõe; o cliente aprova | Logo para fundo claro + nome da campanha: preencha `__TITULO_1__` (vermelho) e `__TITULO_2__` (grafite) e troque ou apague o ícone opcional `#icone` (comentários EDITAR do `scripts/index_template.html`; tabela em `edicao-hyperframes.md` §13.1–13.2) | Lockup "VERÃO" vermelho + sol + "CONECTADO" escuro (no molde: `__TITULO_1__` = VERÃO, `__TITULO_2__` = CONECTADO e o sol no `#icone`; no index entregue eram `.verao`, `.conectado`, `#sun` e `#sun-rays`) |
| Oferta | Cliente: oferta, prazos e preços | Na tela em dígitos; na voz por extenso | "Planos sem fidelidade de 2 a 5 meses". Na tela: "Planos sem fidelidade" + "de 2 a 5 meses". Na voz: "Sem fidelidade: planos de dois a cinco meses." |
| CTA | Cliente: anúncio pago ou post orgânico | Textos fixos da 7.1 | Anúncio pago: "Clica no botão Saiba Mais ou escaneia o QR code na tela!" |
| Destino do QR | Cliente | Nunca o WhatsApp; confira se está no ar e decodifique no vídeo final (7.1) | https://provedorvoltecinternet.online/?page_id=674 = página "Verão Conectado 2026 – Voltec Internet Banda Larga" (título conferido em 15/10/2026). Não reaproveite numa campanha nova sem o cliente confirmar |

---

## 8. Publicação

- **Rótulo "Informações de IA" da Meta:** ative ao publicar. A Meta pede o rótulo em vídeo ou áudio realista feito com IA. Pela pesquisa, o Veo marca SynthID e o GPT Image grava C2PA, então a plataforma pode detectar sozinha.
- **Créditos das fotos CC BY** usadas como referência de local: na legenda do post, se o cliente aprovar (texto pronto em `references/locais-grussai.md` §6; num lugar novo, monte com o `creditos.json` do projeto).
- **Consentimento da voz clonada** documentado (seção 6).
- Nomes de lugar ("Grussaí", "Av. Atlântica") podem ir na legenda do post. Nos prompts de geração, não.

---

## 9. Arquivos do projeto de referência (Verão Conectado)

| O quê | Onde |
|---|---|
| Refs da persona | `/home/syllas/hyperframes/voltec-reels-ia/refs/` (refs novas em `refs/novas_20261015/`) |
| Asset IDs | `/home/syllas/hyperframes/voltec-reels-ia/bodies/assets.json` |
| Corpos enviados (snapshots, identidade, Veo) | `/home/syllas/hyperframes/voltec-reels-ia/bodies/` |
| Prompts finais e narração | `/home/syllas/hyperframes/voltec-reels-ia/prompts/` (`identidade_edit.txt`, `narracao_v3.txt`) |
| Snapshots e IDs | `/home/syllas/hyperframes/voltec-reels-ia/snapshots/` (`identidade_ids.json`, `normalizados/`) |
| Narração, alignment e registro da montagem | `/home/syllas/hyperframes/voltec-reels-ia/audio/` (`narracao_v3.wav`, `narracao_v3_alignment.json`, `COMO_FOI_MONTADA_narracao_v3.txt`) |
| Logo e QR | `/home/syllas/hyperframes/voltec-reels-ia/reels-final/assets/` (`logo-voltec.png`, `logo-voltec-cta.png`, `qr-checkout.svg`) |
| Template de Reels da marca | `/home/syllas/hyperframes/reels/template.html` |
| Fotos de Grussaí e créditos | `/home/syllas/hyperframes/voltec-reels-ia/locais/` (`creditos.json`) |

---

## 10. [VOLTEC] Cenários com a personagem

O cenário é slot do vídeo: um lugar e um horário por vídeo (`locais-grussai.md` §9). Só 3 cenas foram geradas, todas no Verão Conectado. Em qualquer cenário se reaproveitam a câmera com dono, o look de celular, a pele, as mãos, a boca fechada e o fecho sem texto. Lugar, luz, vento, roupa, objeto e som se refazem (molde-base com cada slot em `prompts-moldes.md` §2.9).

### 10.1 Testados [vivido] (ex.: Verão Conectado, tarde de verão em Grussaí)

| Cena | Câmera e ação | Snapshot | Vídeo | Luz, vento e geometria |
|---|---|---|---|---|
| Varanda (T1) | Amiga a ~1,2 m, celular na altura do peito (câmera traseira, ~26 mm); ela ergue o celular, frustrada | `prompts-moldes.md` §2.1 | `prompts-moldes.md` §2.5 (T1 v2) | `locais-grussai.md` §5.1 e §5.5 |
| Rede na mesma varanda (T2) | Edição de pose do T1: a amiga dá um passo e inclina o celular; videochamada com risada de boca fechada | `prompts-moldes.md` §2.2 | `prompts-moldes.md` §2.5 (T2) | `locais-grussai.md` §5.1 (T2) |
| Selfie na areia (T3) | Câmera frontal no braço estendido (~24 mm); ela caminha devagar olhando a própria imagem | `prompts-moldes.md` §2.3 | `prompts-moldes.md` §2.5 (T3) | `locais-grussai.md` §5.2 e §5.5 |

- Um lugar, uma tarde e a mesma roupa: o T2 é edição do T1, e o T3 é imagem nova com o T1 como Image 1 (`prompts-moldes.md` §0).
- Enquadramentos que seguraram a identidade: do joelho, do colo e do meio do peito para cima.

### 10.2 Loja, carro e uniforme: o que as refs da conta mostram

As refs da persona mostram loja, carro e uniforme, mas nenhuma cena nesses contextos foi gerada. Os riscos abaixo já aparecem nas refs; a coluna do meio diz o que a sessão fez com eles.

| Contexto | O que as refs mostram | Risco já visto e o que a sessão fez | Como enquadrar sem texto [não testado] |
|---|---|---|---|
| Loja | Letreiro VOLTEC luminoso enorme numa parede ripada (`persona_loja_logo.jpg`); balcão com notebook e headset (`novas_20261015/ref_c_chatgpt_131820.jpg`) | O letreiro vaza texto: a ref só entrou recortada no rosto (`ref_a_rosto_crop.jpg`) [aplicado]. O headset vazaria para a cena: ref descartada [aplicado]. Na mesma ref, a marca do notebook está legível na tampa | Câmera de costas para o letreiro e a fachada; fundo de parede lisa, sem letras, cartaz, tela ou vitrine; balcão vazio; notebook fechado ou fora do quadro. A marca entra só no overlay. Como é a loja real: **não pesquisado: pesquise com `locais-grussai.md` §7–§9** (peça fotos ao cliente; `locais-grussai.md` §10) |
| Carro | Banco da frente, com dedos no queixo, colar, alça vermelha e tatuagens de texto no antebraço (`persona_carro.jpg`) | Os dedos puxam a mão para perto do rosto e o colar tremula: recorte do rosto sem dedos nem colar (`persona_headshot_sem_dedos.jpg`) [aplicado]. Tatuagens fora do prompt [aplicado] | Carro parado; nunca ela dirigindo com o celular na mão (é infração de trânsito e imagem ruim para a marca). Selfie ou amiga no banco do lado (não cabem 1,2 m); do peito para cima; emblema do volante, painel e placas de outros carros fora do quadro; retrovisor e vidros sem o reflexo de quem filma ([pesquisa]: espelho e vidro grande mostram "câmera fantasma"). O que aparece pelas janelas: **não pesquisado: pesquise com `locais-grussai.md` §7–§9** |
| Uniforme | Polo vermelha com mangas e laterais azul-marinho e logo VOLTEC bordado no peito (`persona_corpo_inteiro.jpg`, asset `9snOZM2EfiYIjKtqfsW2`) | O logo e o vermelho vazam para a roupa: a ref entrou sem logo (`ffmpeg delogo`, asset `ZY1iDcJLhPFklahPnvkM`) e o prompt manda ignorar o uniforme e o logo [aplicado]. O delogo deixou uma mancha borrada no peito, que não vazou porque a ref só deu as proporções | Âncora de uniforme liso da 3.4, com `without any logo, print, embroidery or lettering`, e o peito revisado a 100%. A marca entra no overlay, fora do corpo dela (7.1) |
| Rosto pequeno | Corpo inteiro, longe, na passarela de madeira (`novas_20261015/ref_d_129987.jpg`) | Rosto pequeno não segura a identidade: ref descartada [aplicado] | Plano médio, como nos testados (10.1). Plano aberto de corpo inteiro só com A/B e revisão do rosto (`qa-checklist.md` §A) |

Pelo menos parte das refs é imagem gerada: a pesquisa achou os nomes `Gemini_Generated_Image_…` (corpo inteiro) e `Generate_car_interior_image_2K` (carro), e duas das refs novas têm "chatgpt" no nome. Elas servem para a persona, não como prova de como são a loja ou o carro reais.

### 10.3 Cenas internas: casa, loja e carro [não testado]

São as regras de luz e de objeto que funcionaram ao ar livre, aplicadas a cenas internas. Nada aqui foi gerado. As notas de adaptação para casa, loja, carro, noite, inverno e uniforme estão em `prompts-moldes.md` §2.10: lá há frases prontas de luz, som, roteador, carro e negative_prompt; casa e loja só têm regras (a loja real não foi pesquisada), e as âncoras de roupa ficam na §3.4 deste arquivo.
- **Luz:** uma fonte real, com direção escrita no prompt (`prompts-principios.md` §1.7): janela de lado, de dia; luminária da sala; luz do teto. O celular expõe para o rosto, então a janela sai um pouco estourada, como o fundo ensolarado testado. O sol só entra pela janela voltada para o lado dele: calcule com `locais-grussai.md` §8. A luz não muda no clipe, e nada de luz de estúdio nem de contorno sem fonte ([pesquisa]).
- **Noite:** nunca gerada. Escreva uma fonte real (luminária, poste visto pela janela), troque o `crisp daylight frames` dos moldes de vídeo pela frase de pouca luz de `prompts-moldes.md` §2.10 e revise mãos e boca a 8 e 24 fps (`qa-checklist.md` §B).
- **Objeto na mão:** as regras da 3.4 (um só, tela virada para ela, inteiro no quadro, parado). TV, monitor e notebook no fundo ficam desligados, de costas ou fora do quadro, porque tela à vista vira interface com texto (`prompts-principios.md` §1.4). Num vídeo de dica de Wi-Fi, o roteador fica liso, sem marca nem etiqueta, parado num móvel; ela não o manipula.
- **Câmera:** amiga a ~1,2 m na altura do peito (casa, loja) ou selfie (carro, espaço apertado). A pesquisa também sugere o celular apoiado num móvel, parado (`Phone propped against a glass on a side table at waist height`) [pesquisa].
- **Espelhos e vidros grandes** ficam fora do quadro: o reflexo mostra quem filma [pesquisa].
- **Som:** o ambiente do lugar, em 3 camadas e com `No music` (`prompts-principios.md` §1.11), com o mesmo texto da cama no prompt de vídeo e na cama de SFX (`api-elevenlabs.md` §7). Nada de mar, vento ou rua que não se ouviria ali.

### 10.4 Cenário novo, passo a passo
1. Lugar e horário: o que checar está em `locais-grussai.md` §10 (fotos com licença, local provado, sol, vento, texto que vaza). Para cena interna, peça fotos ao cliente.
2. Âncora de roupa e objeto (3.4).
3. Molde mais perto: amiga filmando (`prompts-moldes.md` §2.1), selfie (§2.3) ou o molde-base de cena (§2.9). Troque `Location`, `Light` e a roupa do `Subject`; mantenha câmera, look, pele, mãos e fecho.
4. Snapshot em A/B (2 × ≈554 créditos), revisão pelo `qa-checklist.md` §A e portão 3 avisando que a cena é nova. Só depois vem o vídeo.
