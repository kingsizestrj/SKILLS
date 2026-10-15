# Prompts de realismo: moldes completos (imagem, vídeo e narração)

Moldes para qualquer vídeo realista com IA da Voltec estrelado pela personagem da marca, em qualquer campanha, estação, tema ou cenário. Os textos testados vêm do caso de referência, o Reels "Verão Conectado" (15/10/2026), e aparecem como **exemplo testado (Verão Conectado)**. Varanda, rede, selfie na areia, roupa de crochê, sol de fim de tarde de verão e sons de praia são dessa campanha, não padrão. Para uma cena nova, comece pelo molde-base (2.9) e use os exemplos para ver como cada slot foi preenchido. Para cena interna, noturna ou roupa nova, veja 2.10.

Os prompts vão em **inglês** (o Veo só garante inglês); os comentários estão em português. Todo prompt marcado como "testado" é o texto exato que foi para a API: foi conferido contra os corpos salvos em `/home/syllas/hyperframes/voltec-reels-ia/bodies/` (o `.txt` do prompt só tem a quebra de linha final a mais).

**Nível de evidência** (aparece entre colchetes):
- **[vivido]**: aconteceu na sessão e a correção foi conferida no resultado.
- **[aplicado]**: veio da pesquisa ou das críticas, entrou nos prompts finais e os takes saíram sem o problema. Não houve teste A/B sem a regra.
- **[pesquisa]**: só da pesquisa, não testado na sessão.
- **[não testado]**: derivado das regras que funcionaram e nunca gerado. Antes de mostrar ao cliente, faça o A/B do snapshot e revise com `qa-checklist.md` §A. No portão 3, avise que a cena é nova.

**Escopo**:
- **Geral**: vale para qualquer anúncio com IA.
- **Voltec**: fixo da Voltec com a personagem, em todo vídeo: âncoras de rosto, pele e mãos, sem joias, voz, pronúncia, cidades e textos de CTA.
- **Grussaí**: geografia real da área atendida (praia plana voltada para o leste, restinga, mar cinza).
- **Verão Conectado** (ou "ex.: Verão Conectado"): valor só da campanha de referência. Numa campanha nova, vira um slot a preencher (2.9).

Arquivos relacionados: `prompts-principios.md` (§1 princípios e checklist do prompt, §3 armadilhas vividas, §4 moderação), `persona-e-marca-voltec.md` (âncora de identidade, assets, voz), `locais-grussai.md` (local e sol), `api-elevenlabs.md` (endpoints e envio), `modelos-e-custos.md`, `qa-checklist.md` (revisão do snapshot e do take), `edicao-hyperframes.md`.

Sumário (arquivo grande, acima do limite de uma leitura do Read: ache a seção com Grep, ex. `^### 2\.9`, e leia com offset/limit): 0. Fluxo e envio · 2. Moldes (2.1 snapshot com amiga filmando · 2.2 edição de pose · 2.3 selfie · 2.4 edição de identidade · 2.5 vídeo Veo · 2.6 negative_prompt · 2.7 Seedance · 2.8 narração · 2.9 molde-base de cena para qualquer campanha · 2.10 cena interna, noturna ou com roupa nova). §1 (princípios), §3 (armadilhas) e §4 (moderação) ficam em `prompts-principios.md`.

---

## 0. Fluxo e envio

1. Escreva o snapshot pelo molde-base (2.9), olhando o exemplo testado mais perto da cena (2.1 amiga filmando, 2.2 pose no mesmo lugar, 2.3 selfie). Gere **2 variações** de cada take, revise com o checklist de snapshot do `qa-checklist.md` (§A) e mostre ao cliente. **Nenhum vídeo antes da aprovação.**
   - Quantos takes, em que lugares e com que ação vêm do roteiro da campanha (slot). O Verão Conectado teve 3 takes: varanda, rede e selfie na areia.
   - Gere o T1 A/B primeiro. Escolha você a melhor pelo `qa-checklist.md` §A e use-a como **T1 base**: o take seguinte no mesmo lugar é edição dela, com a câmera no mesmo ponto (2.2); lugar novo é imagem nova com ela como Image 1 (2.3). Na sessão, T2 e T3 saíram do T1-A `5vBTv3B9FOt44Vu8jMY4` antes do storyboard.
   - No portão 3, diga ao cliente quais takes derivam do T1-X. Se ele escolher o outro T1, refaça os derivados a partir dele (2 imagens por take, ≈554 cada; ex.: Verão Conectado: T2 e T3, 4 imagens, ≈2,2 mil créditos) antes de qualquer vídeo.
2. Se a composição foi aprovada e só a semelhança da persona precisa melhorar, faça a edição de identidade (2.4) sobre o snapshot aprovado. Não regere do zero.
3. Vídeo (esqueleto com slots em 2.9, exemplos testados em 2.5, negativo em 2.6) com `start_frame` = `generation_id` do snapshot aprovado: 2 variações por take, seeds diferentes.
4. Narração (2.8) inteira numa request só. Para trocar uma frase depois, gere só ela e emende (`api-elevenlabs.md` §5.5).

Monte o corpo a partir do `.txt` do prompt com `jq` (evita erro de aspas e de escape). O preâmbulo é o mesmo da skill toda; variáveis não passam de uma chamada do Bash para a outra, então repita-o em cada chamada:

```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
jq -n --rawfile p "$PROJ/prompts/T1_snapshot.txt" --arg rosto "ID_ASSET_ROSTO" --arg local "ID_ASSET_LOCAL" \
  '{model_id:"gpt-image-2.5-sunburst", prompt:($p|rtrimstr("\n")), aspect_ratio:"9:16", resolution:"2K", quality:"high",
    images:[{type:"asset",asset_id:$rosto},{type:"asset",asset_id:$local}]}' > "$PROJ/bodies/T1_gpt25.json"
```

Envie e baixe com `scripts/el.py`, que lê a chave de `~/.config/elevenlabs/env` sem imprimir. Cada `submit` aceito gasta créditos:

```bash
# imagem não tem seed: o mesmo corpo enviado 2 vezes dá 2 variações (2 cobranças)
python3 -I "$SKILL/scripts/el.py" submit image "$PROJ/bodies/T1_gpt25.json"     # imprime o generation_id
python3 -I "$SKILL/scripts/el.py" submit image "$PROJ/bodies/T1_gpt25.json"
python3 -I "$SKILL/scripts/el.py" wait image "$PROJ/snapshots/T1_a" ID_DA_PRIMEIRA   # espera e baixa T1_a.png
python3 -I "$SKILL/scripts/el.py" wait image "$PROJ/snapshots/T1_b" ID_DA_SEGUNDA

# vídeo: dois corpos que só diferem na seed (20260115 e 20260116)
python3 -I "$SKILL/scripts/el.py" submit video "$PROJ/bodies/T1_veo_v1.json"
python3 -I "$SKILL/scripts/el.py" submit video "$PROJ/bodies/T1_veo_v2.json"
```

Para esperar e baixar uma rodada de vídeos, use `scripts/poll_round.py <ids.json> --out "$PROJ/takes"`, com `ids.json` = `{"T1_veo_v1": "<id>", ...}`. Guarde sempre o `generation_id`: o `content_url` expira em cerca de 1 h. Detalhes em `api-elevenlabs.md`.

---

## 2. Moldes completos e comentados

### 2.1 Snapshot com amiga filmando (T1): gpt-image-2.5-sunburst. Exemplo testado (Verão Conectado: varanda) [vivido: aprovado como T1-A]

Ordem dos blocos: papéis das referências → frame de vídeo e câmera → `Location` → `Subject` (identidade, roupa, objeto, expressão, mãos) → `Skin and hair` → `Light` → `Look` → frase final de restrição.

Corpo (estrutura real de `/home/syllas/hyperframes/voltec-reels-ia/bodies/T1_gpt25.json`):

```json
{
  "model_id": "gpt-image-2.5-sunburst",
  "prompt": "<texto abaixo>",
  "aspect_ratio": "9:16",
  "resolution": "2K",
  "quality": "high",
  "images": [
    {"type": "asset", "asset_id": "<ROSTO_SEM_DEDOS>"},
    {"type": "asset", "asset_id": "<FOTO_REAL_DO_LOCAL>"}
  ]
}
```

- Sai em 1152x2048 (9:16 exato) e custa ≈554 créditos. A API de imagem não tem `seed` nem `negative_prompt` (campo extra dá 422, sem custo). Para 2 variações, mande o mesmo corpo 2 vezes.
- Nos modelos de imagem, a função de cada ref vem da **ordem** em `images` e do texto `Image 1 ... Image 2 ...`. Não existe campo `role`.
- **Voltec** (`bodies/assets.json`): `<ROSTO_SEM_DEDOS>` = `na7keiYvPpGArmyghOpk`, fixo em todo vídeo (recorte 730x730 do rosto da foto do carro, sem dedos e sem colar: `/home/syllas/hyperframes/voltec-reels-ia/refs/persona_headshot_sem_dedos.jpg`).
- `<FOTO_REAL_DO_LOCAL>` muda com o cenário. Ex.: Verão Conectado: `Mf1kechhOOoqJO70sPNd` (`grussai_restinga_casuarinas_horizonte_mar_01.jpg`, CC BY 4.0, Pablo Cauã da Silva Toledo). Em outro cenário, use outra foto com licença aberta ou do cliente (`locais-grussai.md` §6–§7). Foto com licença NC nunca sobe para a API.
- Cena sem foto aberta (loja, casa, carro) e sem foto do cliente: tire a Image 2 do corpo e a frase dela do prompt, e descreva o lugar só no texto (2.10) [não testado: todo snapshot aprovado teve foto do local].
- A/B feito na sessão: o mesmo prompt com as mesmas refs no `gemini-3-pro-image` (mesmo corpo, sem `quality`) afinou o rosto e trocou a roupa. O gpt-image-2.5 manteve a identidade e seguiu o prompt, e venceu. [vivido]

Prompt testado (`/home/syllas/hyperframes/voltec-reels-ia/prompts/T1_snapshot.txt`):

```text
Reference roles: Image 1 is the woman's face: keep her exact identity, facial proportions, skin tone, eyes, eyebrows, nose, lips and hair; ignore the car interior behind her. Image 2 is a real photo of the coastal restinga where this scene takes place: use it only for the shape of the wind-bent casuarina trees with wispy gray-green needles, the dry yellowish dune grass, the flat gray-blue sea and the perfectly straight, empty horizon; ignore its midday light and deep-blue sky.

A single frame grabbed from a casual vertical 9:16 smartphone video, not a photo shoot. Filmed handheld by a friend standing about 1.2 meters in front of her, holding the phone level at chest height (main rear camera, about 26 mm equivalent). The whole frame is rolled about 2 degrees, so the top of the wall and the horizon tilt together and stay parallel. Medium-wide shot framed from just above her knees, her slightly right of center, open sky in the upper right of the frame.

Location: the shaded upstairs balcony of a simple two-story beach house facing the sea, in a quiet, flat beach town of low houses. Directly behind her legs hangs an empty, plain off-white woven cotton hammock without fringes, parallel to the balcony wall; only its fabric shows at the bottom edge of the frame, and its ropes rise toward hooks outside the frame. Behind it, a white-painted masonry balcony wall with a flat top, which appears behind her at about the height of her lower ribs. Beyond the wall, seen from upstairs (the coastal road is hidden below the wall): scattered wind-bent casuarina trees whose crowns rise against the sky beside her shoulders, low dunes with dry yellowish grass, a thin band of pale sand and a thin band of flat gray-blue sea, with the straight, empty horizon passing just below her shoulders. Flat coastal land only: no hills, rocks, islands, high-rise buildings, poles, cars or signs.

Subject: an adult Brazilian woman, about 26 years old, round face with full cheeks, warm medium-tan skin, dark-brown almond-shaped eyes, thick dark defined eyebrows, a straight nose with a soft rounded tip, full lips, long straight dark-brown, almost black hair with a slight side part, most of it falling behind her shoulders. She wears a loose, hip-length white cotton crochet beach cover-up with a large open-weave pattern and three-quarter sleeves, worn open over a plain white cotton tank top with a round neckline, and light-wash denim shorts. No jewelry. She holds her right hand up just above her head, elbow slightly bent, with one smartphone in a plain matte black case with no logo; the whole phone is inside the frame with space above it; the screen faces down toward her, fingers wrapped around the back, thumb on the side edge, so only the back of the phone is visible. She squints up at it with a frustrated half-frown, eyebrows drawn together, lips closed and pulled slightly to one side. Her left hand rests on her hip. Five natural fingers on each hand, visible knuckle creases, short dark wine-red nails slightly worn at the tips.

Skin and hair: real, unretouched skin with visible pores on the nose and cheeks, a faint natural shine on the forehead and nose bridge, slightly uneven tone around the mouth and chin, two tiny blemishes near the jawline, fine wispy hairs along the hairline, slightly darker skin under the eyes; light everyday makeup only; small natural asymmetry. Hair not salon-perfect, with slight humidity frizz; a light breeze from behind her lifts a few strands at her shoulders, none across her face.

Light: about 5 pm in summer. The sun is low behind the house, so the balcony and her face are in soft, even open shade, with a faint bright edge of skylight on her hair and shoulders. The casuarinas, dunes, sand and sea beyond the wall are in warm late-afternoon sunlight under a clear pale-blue sky with a few small white clouds low over the sea. Not golden-hour orange. The phone exposes for her face, so the sunlit background is slightly overexposed.

Look: a real smartphone video frame: wide lens, deep focus with the background clearly recognizable, phone HDR tone mapping, slight over-sharpening and video-compression softness, faint noise only in the shadows, true-to-life colors, no color grade, no filter, no bokeh, no retouching.

There is no text, sign, number, logo or watermark anywhere, the clothes have no print, and there are no other people in the frame.
```

Por que cada trecho existe:

| Trecho | Função | Escopo | Slot (2.9) |
|---|---|---|---|
| `Reference roles: Image 1 is the woman's face ... ignore the car interior behind her.` | Cada ref recebe um papel explícito e o que deve ser ignorado (fundo, uniforme, logo). | Geral; o texto da Image 1 é o da ref fixa da Voltec | fixo |
| `Image 2 is a real photo ... use it only for the shape of ... ignore its midday light and deep-blue sky.` | A foto real do local serve para formas e vegetação; a luz vem do texto (as fotos de licença aberta são de meio-dia). | Geral (conteúdo: Grussaí) | `{PLACE}` |
| `A single frame grabbed from a casual vertical 9:16 smartphone video, not a photo shoot.` | O look de frame de vídeo passa para o vídeo. | Geral | fixo |
| `Filmed handheld by a friend standing about 1.2 meters ... chest height (main rear camera, about 26 mm equivalent).` | Câmera com dono. | Geral | `{CAMERA_OWNER}` |
| `The whole frame is rolled about 2 degrees, so the top of the wall and the horizon tilt together...` | Imperfeição de celular sem geometria impossível. | Geral | `{CAMERA_OWNER}` |
| `Medium-wide shot ... open sky in the upper right of the frame.` | Reserva o espaço onde o texto da edição vai entrar. | Geral | `{CAMERA_OWNER}` |
| `Directly behind her legs hangs an empty ... hammock ... only its fabric shows at the bottom edge` | Planta no T1 o objeto que o T2 vai usar: a edição de pose não precisa inventar a rede. | Geral (técnica); a rede é do Verão Conectado | `{PLACE}` |
| `seen from upstairs (the coastal road is hidden below the wall) ... a thin band of pale sand and a thin band of flat gray-blue sea` | Geometria coerente com a altura da câmera. | Grussaí (varanda do Verão Conectado) | `{PLACE}` |
| `Flat coastal land only: no hills, rocks, islands, high-rise buildings, poles, cars or signs.` | Corta os clichês de "praia com morro" e os postes e placas que viram texto. | Grussaí | `{PLACE}` |
| `Subject: an adult Brazilian woman, about 26 years old, ...` | Âncora de identidade, com idade adulta explícita. | Voltec (fixo) | `{IDENTITY_ANCHOR}` |
| `loose, hip-length white cotton crochet beach cover-up with a large open-weave pattern ... plain white cotton tank top with a round neckline` | Roupa opaca, sem decote e de trama grande (não tremula). | Verão Conectado (roupa de praia) | `{OUTFIT}` |
| `the whole phone is inside the frame with space above it; the screen faces down toward her ... only the back of the phone is visible` | Objeto inteiro no quadro, sem tela. | Geral | `{OBJECT}` |
| `lips closed and pulled slightly to one side. Her left hand rests on her hip.` | Boca fechada e mão livre ancorada desde o primeiro quadro. | Geral | `{EXPRESSION}` e `{OBJECT}` |
| `Skin and hair: ... fine wispy hairs ... a light breeze from behind her lifts a few strands at her shoulders, none across her face.` | Pele real e cabelo que não cruza o rosto. | Voltec (pele, fixa); a brisa é do Verão Conectado | fixo + `{TIME_AND_LIGHT}` |
| `Light: about 5 pm in summer. The sun is low behind the house ... Not golden-hour orange.` | Luz coerente com a geografia (praia para o leste). | Grussaí, verão (Verão Conectado) | `{TIME_AND_LIGHT}` |
| `Look: a real smartphone video frame ...` | Look de celular. | Geral | fixo |
| `There is no text, sign, number, logo or watermark anywhere ...` | Zero texto gerado. | Geral | `{CLOSING_NO_TEXT}` |

Para outro cenário ou outra campanha, use o molde-base (2.9), que dá nome a cada slot desta tabela.
- Fixos: a frase de frame de vídeo, a âncora de identidade, a pele, as mãos, `No jewelry`, o look e a frase final.
- Da cena: `{CAMERA_OWNER}` (quem filma muda; a regra da câmera com dono, não), `{PLACE}` (a foto de referência e `Location`), `{TIME_AND_LIGHT}` (sol calculado para o lugar, a data e a hora: `locais-grussai.md` §8), `{OUTFIT}`, `{OBJECT}` e `{EXPRESSION}`.

### 2.2 Edição de pose no mesmo lugar (T2). Exemplo testado (Verão Conectado: rede) [vivido: aprovado como T2-A]

É uma **edição** do T1 base (§0, item 1), não uma imagem nova: assim o lugar, a luz e a roupa continuam os mesmos.

```json
{
  "model_id": "gpt-image-2.5-sunburst",
  "prompt": "<texto abaixo>",
  "aspect_ratio": "9:16",
  "resolution": "2K",
  "quality": "high",
  "images": [
    {"type": "generation", "generation_id": "<ID_DO_T1_BASE>"},
    {"type": "asset", "asset_id": "<ROSTO_SEM_DEDOS>"}
  ]
}
```

Snapshot gerado pela API não precisa de upload: entra como `{"type": "generation", ...}`. Na Voltec, o T1 base foi o T1-A `5vBTv3B9FOt44Vu8jMY4` (`bodies/T2_gpt25_a.json`), escolhido antes do storyboard e depois aprovado pelo cliente. O T1 base ainda não passou pelo portão 3: diga ao cliente de qual T1 o T2 deriva e, se ele escolher o outro, refaça o T2 a partir dele antes de qualquer vídeo.

Prompt testado (`/home/syllas/hyperframes/voltec-reels-ia/prompts/T2_snapshot.txt`):

```text
Edit Image 1, a frame from the same smartphone video a few minutes later. Image 2 shows the woman's face for extra fidelity (ignore the car interior behind her). Keep exactly the same woman, outfit, phone, balcony wall, hammock, view, late-afternoon light and phone-camera look. The friend filming is in the same spot, still holding the phone at chest height and facing the sea in the same direction; the friend has only taken a small step closer and tilted the phone slightly down to frame her in the hammock. Change only her pose and this small reframing; do not add, remove or move any object.

Pose: she now sits sideways in the same off-white hammock that hung behind her, her back toward the wall, both feet on the floor out of frame, her body turned slightly toward the camera. Her right hand holds the same phone in the matte black case at chin height, about 40 cm in front of her and a little to her right so it does not cover her face, screen toward her as if on a video call; only the back of the phone is seen, at an angle. She looks at the screen with a closed-lip smile, cheeks lifted and eyes slightly crinkled, as if about to chuckle. Her left hand rests in her lap.

Framing: medium shot from her lap up, her face a little above the center of the frame. Because the camera is higher than her and tilted slightly down, the top of the white wall runs just behind the top of her head; above it, the same casuarina crowns, the thin band of pale sand and the flat gray-blue sea, with the straight horizon about a third of the way down the frame and open pale-blue sky above. The view keeps exactly the perspective, trees and horizon of Image 1, only slightly larger; the whole frame is still rolled about 2 degrees.

Keep real, unretouched skin: visible pores, a faint shine on the forehead and nose, tiny blemishes near the jaw, fine wispy hairs at the hairline, small creases at the outer corners of her eyes; natural hands with five fingers each, short dark wine-red nails; no jewelry. There is no text, sign, logo or watermark anywhere, and no other people.
```

Comentários:
- `Keep exactly the same woman, outfit, phone, balcony wall, hammock, view, late-afternoon light and phone-camera look.` Liste tudo o que fica.
- `The friend filming is in the same spot ... only taken a small step closer and tilted the phone slightly down` mantém a câmera no mesmo lugar (`prompts-principios.md` §1.2). Mudar o ponto de vista numa edição obriga o modelo a redesenhar a varanda.
- `Change only her pose and this small reframing; do not add, remove or move any object.`
- `Pose:` ela começa **já sentada** (nunca peça a ação de entrar na rede). O celular fica na altura do queixo, um pouco à direita, para não cobrir o rosto, com a tela virada para ela. A expressão de partida é `closed-lip smile ... as if about to chuckle`, e o vídeo começa dela. Use `left hand rests in her lap` em vez de "thigh" (moderação).
- `Framing:` explica a geometria: com a câmera mais alta que ela e inclinada para baixo, o topo do parapeito passa atrás da cabeça e o horizonte fica a ~1/3 do quadro. `The view keeps exactly the perspective, trees and horizon of Image 1, only slightly larger`.
- O bloco final repete a pele e a restrição de texto de forma curta.
- Em outra cena, a estrutura é geral e fica: `Edit Image 1` → lista do que fica → quem filma continua no mesmo ponto → `Change only her pose and this small reframing` → `Pose:` → `Framing:` → pele e restrição de texto. Troque só a lista do que fica, a pose e o enquadramento. A rede, a videochamada e o horizonte a ~1/3 são do Verão Conectado.

### 2.3 Selfie (T3). Exemplo testado (Verão Conectado: selfie andando na areia) [vivido: aprovado como T3-A]

Imagem nova (o local muda), com o T1 base (§0, item 1) como referência de identidade, cabelo e roupa. Na Voltec, a Image 1 foi o mesmo T1-A `5vBTv3B9FOt44Vu8jMY4` (`bodies/T3_gpt25_a.json`); se o cliente escolher o outro T1, refaça o T3 também.

```json
{
  "model_id": "gpt-image-2.5-sunburst",
  "prompt": "<texto abaixo>",
  "aspect_ratio": "9:16",
  "resolution": "2K",
  "quality": "high",
  "images": [
    {"type": "generation", "generation_id": "<ID_DO_T1_BASE>"},
    {"type": "asset", "asset_id": "<ROSTO_SEM_DEDOS>"},
    {"type": "asset", "asset_id": "<FOTO_REAL_DO_LOCAL>"}
  ]
}
```

Prompt testado (`/home/syllas/hyperframes/voltec-reels-ia/prompts/T3_snapshot.txt`):

```text
Reference roles: Image 1 is a frame from earlier the same afternoon: keep exactly the same woman, hair and outfit. Image 2 shows her face for extra fidelity (ignore the car interior behind her). Image 3 is a real photo of the restinga behind this beach: use it only for the shape of the wind-bent casuarinas with wispy gray-green needles, the dry yellowish dune grass, the flat sea and the straight, empty horizon; ignore its midday light and deep-blue sky.

A single frame grabbed from a selfie video recorded on a smartphone's front camera, not a photo shoot. She holds the phone herself at arm's length, slightly above eye level and angled a little down; the phone is the camera and never appears; her extended right arm enters from the lower-left corner, slightly stretched by the wide front lens (about 24 mm equivalent). Framed from mid-chest up, her face in the upper-middle of the frame, slightly right of center; the whole frame is rolled about 3 degrees; open sea and sky on the left side. She is looking at her own image on the phone screen, so her eyes aim slightly below the lens.

Scene, about 5 pm in summer: she walks slowly along the firm, damp sand of a very wide, flat beach. Behind her the beach recedes far into the distance. On the left side of the frame, the sea: olive-gray near the shore and gray-blue farther out, with several parallel lines of white surf and a straight, empty horizon. On the right side, low dunes with dry yellowish grass and a line of wind-bent casuarinas, with a few terracotta roofs barely visible behind them. Two tiny people stand far down the beach near the water. Flat coastline only: no hills, rocks, islands, piers, kiosks, umbrellas or high-rise buildings.

Subject: an adult Brazilian woman, about 26 years old, round face with full cheeks, warm medium-tan skin, dark-brown almond-shaped eyes, thick dark defined eyebrows, a straight nose with a soft rounded tip, full lips, long straight dark-brown, almost black hair with a slight side part. She wears the same loose, hip-length white cotton crochet beach cover-up with a large open-weave pattern and three-quarter sleeves, worn open over the plain white cotton tank top with a round neckline, and light-wash denim shorts. No jewelry. Shoulders relaxed, a soft closed-lip smile. The steady sea breeze blows from in front of her, sweeping her hair back off her face over her left shoulder (frame right), a few loose strands lifting; the front edges of the cover-up flutter slightly.

Light: warm late-afternoon sun, low behind her and off to the right of the frame (the sun itself is out of frame). It puts a warm bright edge of light on her left cheek, her shoulder and her windblown hair, while the rest of her face is in soft open shade lifted by light bouncing off the pale sand, with catchlights from the bright sky in her eyes. The casuarinas on the right are partly backlit; the sky is clear pale blue, brighter and slightly clipped toward the right, a little hazy over the sea. Not golden-hour orange.

Skin: real, unretouched skin with visible pores on the nose and cheeks, fine wispy hairs at the hairline, a faint sheen at her temples, slightly uneven tone around the mouth, two tiny blemishes near the jawline, cheeks and nose a little sun-flushed; light everyday makeup only; natural lip texture; small natural asymmetry.

Look: a front-camera phone video frame: wide-angle perspective, deep focus with the background recognizable, phone HDR tone mapping, slight over-sharpening and compression softness, true-to-life colors, no filter, no bokeh, no retouching.

There is no text, sign, logo or watermark anywhere, and the clothes have no print.
```

Comentários:
- Câmera de selfie: frontal, com o braço estendido, um pouco acima dos olhos e inclinada para baixo. `the phone is the camera and never appears` e o braço entra pelo canto inferior esquerdo, levemente esticado pela grande-angular (~24 mm).
- `her eyes aim slightly below the lens`: ela se olha na tela (`prompts-principios.md` §1.6).
- `rolled about 3 degrees`: a selfie andando inclina um pouco mais que o T1 (2°).
- `Two tiny people stand far down the beach`: gente pequena, distante e **parada** (figura andando tende a derreter). Sem gente, ou com 1 a 2 adultos ao longe.
- `Flat coastline only: no hills, rocks, islands, piers, kiosks, umbrellas or high-rise buildings.` Os quiosques e guarda-sóis de Grussaí têm marca de cerveja e viram texto.
- Vento de frente (`sweeping her hair back off her face over her left shoulder (frame right)`) e sol atrás, à direita, fora do quadro: contraluz na borda do rosto e sombra aberta rebatida pela areia (`prompts-principios.md` §1.7).
- `cheeks and nose a little sun-flushed`: pele de quem está na praia, sem filtro (Verão Conectado; tire em cena interna ou sem sol).
- Selfie em outro lugar: a câmera frontal, o braço fixo no canto e o olhar na própria imagem da tela são gerais. Mar à esquerda, vento de frente e sol atrás à direita valem para o verão em Grussaí. No inverno, para manter o contraluz, ela caminha para o sul e o mar fica à direita (`locais-grussai.md` §3, "Outras estações"); o vento de inverno não foi pesquisado.

### 2.4 Edição de identidade com novas referências [vivido: aprovada; os 6 vídeos foram refeitos]

**Quando usar**: o cliente aprovou a composição, mas a persona não está parecida o bastante (ou mandou fotos novas). A edição mantém a composição aprovada e muda só a semelhança. Depois, todos os vídeos precisam ser refeitos, porque o `start_frame` muda. Na sessão foram mais 6 gerações Veo.

**Preparar as refs** [vivido]:
- Rosto grande e de frente funciona melhor. Recorte só a cabeça, **sem dedos ou mãos** no recorte.
- Tire logo e letreiro com recorte ou `ffmpeg delogo`. Comando testado pela crítica técnica (as coordenadas valem para esse arquivo; o "VOLTEC" some):
  `ffmpeg -i /home/syllas/hyperframes/voltec-reels-ia/refs/persona_corpo_inteiro.jpg -vf 'delogo=x=850:y=1560:w=180:h=90' /home/syllas/hyperframes/voltec-reels-ia/refs/persona_corpo_inteiro_sem_logo.jpg`
- Descarte refs com acessório que pode vazar para a cena (a foto com headset) e refs de rosto pequeno (a da passarela).
- Suba as refs como asset com `python3 -I "$SKILL/scripts/el.py" upload <arquivo>`, que imprime o `asset_id`. Upload não gasta crédito.

```json
{
  "model_id": "gpt-image-2.5-sunburst",
  "prompt": "<molde abaixo, com {OBJECT}, {OUTFIT}, {SETTING} e {EXPRESSION} preenchidos>",
  "aspect_ratio": "9:16",
  "resolution": "2K",
  "quality": "high",
  "images": [
    {"type": "generation", "generation_id": "<ID_DO_SNAPSHOT_APROVADO>"},
    {"type": "asset", "asset_id": "<ROSTO_1>"},
    {"type": "asset", "asset_id": "<ROSTO_2>"},
    {"type": "asset", "asset_id": "<CORPO_INTEIRO_SEM_LOGO>"}
  ]
}
```

**Voltec** (`bodies/T1_id_a.json`, `T2_id_a.json`, `T3_id_a.json`): `<ROSTO_1>` = `na7keiYvPpGArmyghOpk` (rosto do carro, sem dedos), `<ROSTO_2>` = `pUgU1HXgmdqXfP02iR8T` (rosto da loja recortado, sem o letreiro: `refs/novas_20261015/ref_a_rosto_crop.jpg`), `<CORPO_INTEIRO_SEM_LOGO>` = `ZY1iDcJLhPFklahPnvkM` (`refs/persona_corpo_inteiro_sem_logo.jpg`). As variações a e b usaram corpos idênticos.

Molde. O texto testado é `/home/syllas/hyperframes/voltec-reels-ia/prompts/identidade_edit.txt`, que já traz `{OBJECT}` e `{OUTFIT}` preenchidos com os valores da tabela abaixo:

```text
Edit Image 1, a frame from a casual smartphone video. Keep everything in Image 1 exactly as it is: the framing and camera angle, her pose and the position of her hands and arms, {OBJECT}, the outfit ({OUTFIT}), {SETTING}, the light and the phone-camera look. Change only the woman's likeness so she is unmistakably the same person shown in Images 2, 3 and 4: her oval face with soft rounded cheeks and a defined chin, her dark-brown almond-shaped eyes, her thick, softly arched dark eyebrows, her straight nose with a soft rounded tip, her lips and smile, her warm medium-tan skin tone and her long straight dark-brown hair with a slight side part. Match her slim, average build and natural proportions from Image 4. Keep her expression from Image 1: {EXPRESSION}. Use the references only for her identity and build: ignore their backgrounds, the car, the red uniform, the logo and the signs. Real, unretouched skin with visible pores, a faint natural shine and small natural asymmetry; natural hands with five fingers each and short dark wine-red nails. There is no text, logo or watermark anywhere.
```

Valores usados no Verão Conectado (os prompts finais são exatamente o molde com estes trechos; com esses valores, o texto é idêntico ao testado):

| Take | `{OBJECT}` | `{OUTFIT}` | `{SETTING}` | `{EXPRESSION}` |
|---|---|---|---|---|
| T1 | `the phone` | `loose white crochet cover-up over a plain white tank top, light-wash denim shorts` | `the shaded balcony with the white wall, the hammock behind her, the casuarinas and the sea` | `squinting up at the phone with a frustrated half-frown, lips closed` |
| T2 | `the phone` | `loose white crochet cover-up over a plain white tank top, light-wash denim shorts` | `the same balcony with the off-white hammock, the white wall, the casuarinas and the sea` | `a closed-lip smile while looking at the phone screen` |
| T3 | `the phone` | `loose white crochet cover-up over a plain white tank top, light-wash denim shorts` | `the wide flat beach with the sea on the left, the dunes and casuarinas on the right and the low sun behind her` | `a soft closed-lip smile while looking at her own image on the phone screen` |

Comentários:
- Preencha `{OBJECT}`, `{OUTFIT}`, `{SETTING}` e `{EXPRESSION}` com o que está na Image 1 e não mude o resto do texto. A roupa da tabela é a de praia do Verão Conectado: numa campanha com outra roupa, mandar "manter" o crochê, que não está na Image 1, arrisca repintar a roupa.
- `Keep everything in Image 1 exactly as it is: ...` enumera enquadramento, pose, mãos, objeto, roupa, cenário, luz e look. Quanto mais completa a lista, menos o modelo mexe.
- `Change only the woman's likeness so she is unmistakably the same person shown in Images 2, 3 and 4: ...` descreve os traços **olhando as refs novas**. A âncora mudou de `round face with full cheeks` (snapshots originais) para `oval face with soft rounded cheeks and a defined chin`. Para snapshots novos da persona, veja a regra em `persona-e-marca-voltec.md` §3.
- `Keep her expression from Image 1: ...` impede que a edição troque a expressão aprovada.
- `Use the references only for her identity and build: ignore their backgrounds, the car, the red uniform, the logo and the signs.`
- [não testado] Cena com o uniforme da Voltec (polo vermelha lisa, 2.10): a roupa da Image 1 se parece com a das refs, e o molde manda ignorar `the red uniform` delas. Descreva no `{OUTFIT}` a polo que está na Image 1 (a versão curta da âncora de uniforme liso, `persona-e-marca-voltec.md` §3.4) e mantenha o resto do texto. Confira o peito a 100% (logo inventado ou remendo): o logo bordado é o risco que a ref de uniforme já mostrou (`prompts-principios.md` §3.8).
- `Match her slim, average build ... from Image 4` passou na edição de imagem. No prompt de **vídeo**, não use descritor de corpo (`prompts-principios.md` §4).

### 2.5 Vídeo Veo 3.1 com timestamps: esqueleto e exemplos testados (Verão Conectado) [vivido]

Esqueleto (geral). Os mesmos campos, com nome de slot em inglês e o que escrever em cada um, estão no molde-base (2.9). Os prompts reais têm 295 a 331 palavras (~1.750 a 1.970 caracteres); a crítica técnica cita um limite de 1.024 tokens no Veo.

```text
Vertical 9:16 amateur smartphone video, one continuous real-time take with no cuts, filmed {QUEM FILMA, DISTÂNCIA, ALTURA, QUAL CÂMERA}: natural micro-shake and slow breathing sway, no zoom, no pan. The woman in the first frame, {ÂNCORA CURTA: adulta, cabelo, roupa}, {ONDE ESTÁ + POSE EXATA DO SNAPSHOT, COM AS DUAS MÃOS}.
[00:00-00:03] {TEMPO 1: parte do corpo, direção, velocidade, amplitude; parte da pose do snapshot}.
[00:03-00:05] {TEMPO 2: caminho do objeto, se ele se mexer; emoção por olhos, testa e ombros}.
[00:05-00:08] {TEMPO 3: olhar para o rosto de quem filma ou para a tela; termina parada, piscando}.
Her lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth, and she never speaks. {REGRA DO OBJETO}. The {3-4 ELEMENTOS VISÍVEIS NO SNAPSHOT} stay exactly as in the first frame; {O QUE SE MEXE}. Light: {A MESMA DO SNAPSHOT}. Unedited, candid phone footage: natural skin texture with visible pores, crisp daylight frames with almost no motion blur, true-to-life colors.
Ambient noise: {CAMA}, recorded by the phone's built-in microphone. SFX: {RUÍDO NO MICROFONE}; {UM SOM DE AÇÃO, NUNCA SOM DE BOCA}. No music. (no subtitles)
```

Corpo (estrutura real de `bodies/T1r_veo_v1.json`; a v2 só troca a seed para 20260116):

```json
{
  "model_id": "veo-3.1-generate-001",
  "prompt": "<texto do take>",
  "negative_prompt": "<lista da seção 2.6>",
  "start_frame": {"type": "generation", "generation_id": "<ID_DO_SNAPSHOT_APROVADO>"},
  "aspect_ratio": "9:16",
  "resolution": "1080p",
  "duration_secs": 8,
  "generate_audio": true,
  "seed": 20260115
}
```

```bash
jq -n --rawfile p "$PROJ/prompts/T1_video_veo_v2.txt" --rawfile n "$PROJ/prompts/T1_negative_veo_v2.txt" \
  --arg snap "ID_DO_SNAPSHOT_APROVADO" --argjson seed 20260115 \
  '{model_id:"veo-3.1-generate-001", prompt:($p|rtrimstr("\n")), negative_prompt:($n|rtrimstr("\n")),
    start_frame:{type:"generation",generation_id:$snap}, aspect_ratio:"9:16", resolution:"1080p",
    duration_secs:8, generate_audio:true, seed:$seed}' > "$PROJ/bodies/T1_veo_v1.json"
```

Regras do Veo na API (sessão):
- 1080p só com `duration_secs: 8`. Gere 8 s mesmo que vá usar 4 s e corte na edição. Saída: 1080x1920, 24 fps, 8,000 s. Custo medido: 19.391 créditos por take com áudio.
- **Nunca** envie `enhance_prompt: false`: falha com "Veo 3 prompt enhancement cannot be disabled". O Google sempre reescreve o prompt, por isso ele precisa ser completo e reforçar "amateur smartphone".
- Não envie `webhook` (a conta não tem webhook inscrito, e o create é rejeitado). `images` não combina com `start_frame`.
- Timestamps `[00:00-00:03]` são o formato documentado do Veo. No Seedance, não use (2.7).

**Exemplos testados (Verão Conectado).** Os três textos abaixo são da campanha de referência: varanda, rede, areia, luz de fim de tarde de verão e sons de praia. Em outra cena, preencha o esqueleto (2.9) e use estes textos como modelo de nível de detalhe, não como texto pronto.

**T1 v2: celular erguido, sob narração.** Texto testado (`prompts/T1_video_veo_v2.txt`; take escolhido T1r v1):

```text
Vertical 9:16 amateur smartphone video, one continuous real-time take with no cuts, filmed handheld by a friend standing about 1.2 meters in front of her at chest height with the phone's main rear camera: natural micro-shake and slow breathing sway, no zoom, no pan. The woman in the first frame, an adult Brazilian woman with long straight dark-brown hair, wearing a white crochet beach cover-up over a white tank top and light denim shorts, stands on a shaded beach-house balcony, her phone raised just above her head in her right hand, her left hand on her hip.
[00:00-00:03] She slowly tilts the raised phone a little left and right, squinting up at the screen with her eyebrows drawn together.
[00:03-00:05] In one slow, continuous movement she brings the phone down along her right side to chest height without passing in front of her face and looks at the screen with a disappointed frown, lips pressed together; her shoulders drop.
[00:05-00:08] She lifts her eyes to her friend's face just above the lens with a tired, embarrassed closed-lip half-smile, gives one slow small shake of her head and holds still, blinking naturally.
Her lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth, and she never speaks. The whole phone stays inside the frame, only its back toward the camera. The white wall, the hammock, the casuarinas and the sea horizon stay exactly as in the first frame; a light breeze stirs a few strands of hair at her shoulders. Light: late-afternoon sun behind the house; her face in soft open shade; the sunlit background slightly overexposed. Unedited, candid phone footage: natural skin texture with visible pores, crisp daylight frames with almost no motion blur, true-to-life colors.
Ambient noise: steady sea breeze and distant surf, recorded by the phone's built-in microphone. SFX: wind bumping the microphone now and then; a soft rustle of fabric as her arm comes down. No music. (no subtitles)
```

- A primeira linha traz formato, câmera com dono e imperfeições, e fecha com `no zoom, no pan`.
- `The woman in the first frame, ...` é uma âncora curta que não contradiz a imagem, e a frase seguinte repete a pose **exata** do snapshot.
- `[00:03-00:05]` descreve o caminho do celular (`along her right side ... without passing in front of her face`). A emoção é `a disappointed frown, lips pressed together`: a v1 dizia `huffs once through her nose` e gerou o sopro em "O" (`prompts-principios.md` §3.1).
- `[00:05-00:08]` traz o olhar no rosto da amiga e o take termina parado.
- `Her lips stay closed the entire time: ...` é a correção definitiva do sopro.
- `The white wall, the hammock, the casuarinas and the sea horizon stay exactly as in the first frame` cita só o que está no snapshot.
- O SFX virou `a soft rustle of fabric as her arm comes down`: nenhum som de boca.

**T2: rede, risada de boca fechada.** Texto testado (`prompts/T2_video_veo.txt`; take escolhido T2r v1):

```text
Vertical 9:16 amateur smartphone video, one continuous real-time take with no cuts, filmed handheld by a friend standing about one meter in front of her, phone at chest height angled slightly down: natural micro-shake and breathing sway, no zoom, no pan. The woman in the first frame, an adult Brazilian woman with long straight dark-brown hair, wearing a white crochet beach cover-up over a white tank top, sits sideways in a plain off-white hammock on a shaded beach-house balcony, on a video call, holding her phone at chin height in her right hand with the screen toward her, her left hand resting in her lap.
[00:00-00:03] Looking at the screen, she breaks into a closed-mouth chuckle: her cheeks lift, her eyes crinkle and her shoulders shake gently while her lips stay together.
[00:03-00:05] She nods twice, smiling at the screen, blinking naturally.
[00:05-00:08] She lifts her eyes to her friend's face just above the lens and holds a wide, relaxed closed-lip smile.
She never speaks and her mouth never moves as if talking. Only the back of the phone faces the camera and no screen is visible; the hammock gives only a slight wobble. The white wall, the casuarinas and the sea horizon stay exactly as in the first frame; a light breeze stirs loose strands of hair at her shoulders. Light: soft open shade on her face; the sunlit background slightly overexposed. Unedited, candid phone footage: natural skin texture with visible pores, small creases at the corners of her eyes when she smiles, crisp daylight frames, true-to-life colors.
Ambient noise: soft sea breeze and distant surf, recorded by the phone's built-in microphone. SFX: a faint creak of the hammock ropes as she shifts; a light wind bump on the microphone. No music. (no subtitles)
```

- `breaks into a closed-mouth chuckle: her cheeks lift, her eyes crinkle and her shoulders shake gently while her lips stay together` é risada sem boca aberta, porque a frase "Agora sim! ..." da narração cai em cima.
- `She never speaks and her mouth never moves as if talking.` A videochamada puxaria fala, por isso a restrição dupla.
- `the hammock gives only a slight wobble` evita física estranha da rede.
- O prompt não manda abaixar o celular, e mesmo assim a T2r v2 o abaixou e deformou (`prompts-principios.md` §3.9). Revise os momentos de manipulação.

**T3: selfie andando na areia.** Texto testado (`prompts/T3_video_veo.txt`; take escolhido T3r v2):

```text
Vertical 9:16 selfie video recorded by the woman herself on her phone's front camera at arm's length, slightly above eye level, one continuous real-time take with no cuts; the phone is the camera and never appears; her extended right arm stays at the lower-left edge of the frame. The frame bobs gently with each step and the horizon tilts a few degrees and corrects itself, with slight residual stabilization wobble and mild wide-angle stretch near the edges; no zoom. The woman in the first frame, an adult Brazilian woman with long straight dark-brown hair, wearing a white crochet beach cover-up over a white tank top, walks slowly along the firm sand of a wide, flat beach in the late afternoon, looking at her own image on the screen, so her eyes aim slightly below the lens.
[00:00-00:03] She walks at an unhurried pace with a soft closed-lip smile.
[00:03-00:05] A gust of wind hits: she narrows her eyes and her smile widens without opening her mouth.
[00:05-00:08] She turns her head toward the sea on the left of the frame for a moment, then looks back at the screen, blinking slowly, still walking.
Her lips stay together; she never speaks; her left hand stays out of frame. The surf on the left, the dunes and casuarinas on the right and the straight, empty horizon stay exactly as in the first frame; the low warm sun behind her on the right of the frame outlines her cheek and windblown hair; the wind keeps her hair swept back off her face. Unedited, candid phone footage: natural skin texture with visible pores, flyaway hairs catching the light, crisp daylight frames, true-to-life colors.
Ambient noise: waves washing up the sand nearby, recorded by the phone's front microphone close to her face. SFX: gusty wind buffeting the microphone in low rumbles. No music. (no subtitles)
```

- A câmera de selfie se descreve pelo balanço do passo, pelo horizonte que inclina e corrige e pelo wobble de estabilização. O braço fica fixo no canto.
- `A gust of wind hits: she narrows her eyes and her smile widens without opening her mouth.` O vento motiva o gesto e o som no microfone.
- `her left hand stays out of frame` ancora a mão livre.
- No áudio, o microfone frontal fica perto do rosto, então o vento entra em `low rumbles`.

### 2.6 negative_prompt (só Veo)

É uma lista de termos separados por vírgula, sem "no" nem "don't". Pode suprimir sons também (`prompts-principios.md` §1.11).

**Base dos três takes do Verão Conectado** (testada; está em T1 v2, T2 e T3). A parte "Geral" e a de persona valem para qualquer vídeo da Voltec; a parte de lugar muda com o cenário.

Geral:
```text
subtitles, captions, on-screen text, text overlay, watermark, logo, brand name, readable signs, phone screen interface, background music, soundtrack, singing, narration, voice-over, talking, speech, lip-syncing, duplicate person, objects appearing or disappearing, extra fingers, fused fingers, malformed hands, distorted face, face morphing, identity change, changing outfit, flickering fabric pattern, brightness flicker, warped background, bending horizon, scene cut, transition, slow motion, time-lapse, zoom, drone shot, crane shot, gimbal glide, cinematic color grading, film look, teal and orange grade, studio lighting, lens flare, shallow depth of field, heavy bokeh, airbrushed skin, plastic skin, beauty filter, doll face, CGI, 3D render, cartoon
```

Local (ex.: Verão Conectado, Grussaí: costa plana, mar cinza, sol atrás das casas; troque em outro lugar; cena interna: 2.10):
```text
mountains, hills, rocky coast, islands, high-rise buildings, turquoise water, palm-lined resort, sunset over the sea, golden-hour orange glow
```

Persona (decisão da Voltec: sem joias):
```text
jewelry
```

**Acréscimos por take** (testados; ex.: Verão Conectado):

| Take | Acrescentar |
|---|---|
| T1, celular erguido, sob narração (v2) | `open mouth, pursed lips, blowing air, whistling, yawning, hand over mouth, extra people, second phone, phone leaving the frame, melting walls` |
| T2, rede | `extra people, second phone, fringed hammock, mesh hammock, tangled ropes, big hammock swing, phone covering the face, melting walls` |
| T3, selfie | `phone visible in frame, crowd, people near the camera, deformed arm, hair covering the face, sun disk in frame` |

- O conjunto de boca (`open mouth, pursed lips, blowing air, whistling, yawning, hand over mouth`) foi aplicado e verificado só no T1 v2. Recomendação: use-o em todo take que fica sob narração.
- Listas completas por take: `prompts/T1_negative_veo_v2.txt`, `T2_negative_veo.txt` e `T3_negative_veo.txt`.
- Não escreva palavras sensíveis nem para negar (`prompts-principios.md` §4).

### 2.7 Versão Seedance (sem segundos, sons entre `<...>`) [pesquisa: não rodou na sessão]

**Status**: nesta conta, os modelos ByteDance dão `403 model_access_denied` na API e só funcionam no app web da ElevenLabs. O acesso foi testado **sem custo**, mandando um `start_frame` com `generation_id` inexistente: o 403 vem antes da validação do ID. O Seedance também tem filtro de rosto real nas imagens de entrada (`prompts-principios.md` §4). Os moldes abaixo vêm das críticas, com a correção do sopro aplicada, e **nunca foram gerados**.

Corpo (pesquisa, validado só contra o schema):

```json
{
  "model_id": "bytedance-seedance-v2.5",
  "prompt": "<texto>",
  "start_frame": {"type": "generation", "generation_id": "<ID_DO_SNAPSHOT_APROVADO>"},
  "aspect_ratio": "auto",
  "resolution": "720p",
  "duration_secs": 5,
  "generate_audio": true
}
```
- 2.5: `duration_secs` inteiro de 4 a 30 (o padrão é 5; informe sempre). O plano previa 5 s para o T1 no Seedance, o que cabe nos 2 tempos do molde abaixo. Com `start_frame`, o aspect é sempre `auto` e herda o formato do frame, então o snapshot precisa ser 9:16 exato (o gpt-image-2.5 2K já sai 1152x2048). Não tem `seed` nem `negative_prompt` (campo extra dá 422). O 1080p aparece no schema, mas a documentação lista 480p e 720p.
- `bytedance-seedance-v2` (2.0): 4 a 15 s, 1080p (o schema lista até 4k), aceita `seed`, `aspect_ratio` "9:16" explícito.
- No app: Start Frame = snapshot baixado, mesmo prompt, 9:16.

Como converter um prompt Veo em Seedance:
1. Tire os timestamps: o guia oficial diz que tempo exato é instável e gera resultado anormal. Use "She ... Then ... Finally ...".
2. Corte redescrições e mantenha o texto curto. A crítica de realismo recomenda um núcleo de 120 a 170 palavras; as versões dela ficaram com ~170 a ~230 palavras antes da linha de sons. Em take curto, use 2 tempos.
3. Um movimento de câmera só.
4. Sons entre `<...>`, sem os rótulos `Ambient noise:` e `SFX:`.
5. Escreva `There is no background music. Nobody speaks.` (o modelo cria trilha por padrão).
6. Feche com as frases oficiais de restrição. **Sem `(no subtitles)`**: no Seedance, parênteses marcam música.
7. Em vídeo vertical, a chance de legenda espontânea é maior: mantenha "Nobody speaks" e revise. Fala, se um dia for inevitável, vai entre `{...}` com o idioma (`says in Brazilian Portuguese {...}`). Não testado.

T1 em versão Seedance (ex.: Verão Conectado): adaptação do texto da crítica, com a correção da v2, em 2 tempos para ~5 s (**não testado**):

```text
Vertical amateur smartphone video, one continuous real-time take, filmed handheld by a friend about 1.2 meters in front of her at chest height. The woman in the first frame stands on a shaded beach-house balcony, phone raised just above her head in her right hand, left hand on her hip.
She slowly sways the raised phone a little left and right, squinting up at it. Then, in one slow continuous movement, she brings it down along her right side to chest height without passing in front of her face and looks at the screen with a disappointed frown, lips pressed together; her shoulders drop. Her lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth, and she never speaks. The whole phone stays in frame, only its back toward the camera.
Natural handheld micro-shake and breathing sway, one small reframing as her arm comes down; no zoom, no pan.
The white wall, the hammock, the casuarinas and the sea horizon stay exactly as in the first frame; a light breeze stirs a few strands of hair at her shoulders.
<steady sea breeze and distant surf> <wind bumping the phone microphone> <a soft rustle of fabric as her arm comes down>
There is no background music. Nobody speaks.
Real skin texture with pores, natural blinking, true-to-life phone colors, crisp daylight frames.
The woman's face and body proportions remain stable without deformation; her fingers stay natural around the single phone; movements are natural and smooth, with no stutter or flicker. Keep it subtitle-free. Avoid generating any text or subtitles. Do not generate a logo. Do not generate a watermark.
```

### 2.8 Narração eleven_v4 com tags [vivido]

**Estrutura do roteiro.** É a do Verão Conectado, a única testada: primeira pessoa, coloquial, uma ideia por linha.

| Bloco | O que diz | Fixo ou slot | Ex.: Verão Conectado |
|---|---|---|---|
| 1. Gancho | o problema, numa pergunta curta, com a emoção na tag | slot (tema da campanha) | `[frustrated] Casa de praia sem internet? Ninguém merece...` |
| 2. Voltec resolve | a virada, com "Voltéc" no texto do TTS | slot; a grafia "Voltéc" é fixa | `[relieved, smiling] Agora sim! Com a Voltéc` |
| 3. Benefício | o que muda para ela | slot | `eu fico conectada o verão inteiro.` |
| 4. Cidades | onde tem Voltec | fixo da Voltec | `Tem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra.` |
| 5. Oferta | o que o cliente mandou, com números por extenso | slot (vem do cliente; nunca invente) | `[upbeat] Sem fidelidade: planos de dois a cinco meses.` |
| 6. CTA | anúncio pago: botão + QR; post orgânico: link na bio | os 2 textos são fixos da Voltec; a escolha é slot | pago: `[excited] Clica no botão Saiba Mais ou escaneia o QR code na tela!`; orgânico: `[excited] Assina pelo link na bio!` |

- Os blocos 2 e 3 podem ir na mesma frase, como no exemplo.
- Tema sem oferta (institucional, dica de Wi-Fi, suporte): o bloco 5 sai, e o CTA continua pago ou orgânico; pergunte no portão 1 [não testado].
- **Ritmo medido** (voz Radassa 100%, eleven_v4; tags e quebras de linha contam): 294 caracteres ≈ 16,6 s na v2 (`narracao_v2_A_s1.wav`, 16,64 s) e 326 caracteres = 19,06 s na v3 (`narracao_v3.wav`, montada com a emenda e 0,17 s de silêncio). Dá ~17 a 18 caracteres por segundo.
- Para planejar: caracteres ≈ 17 × segundos de narração. É uma conta derivada dessas 2 medidas; o tempo certo sai sempre do alignment. A duração do vídeo é a última palavra no vídeo + ~1 s (`SKILL.md` §4).

Texto final do Verão Conectado (exemplo; `/home/syllas/hyperframes/voltec-reels-ia/prompts/narracao_v3.txt`). A oferta e o CTA são dessa campanha; numa campanha nova, vêm do cliente:

```text
[frustrated] Casa de praia sem internet? Ninguém merece...
[relieved, smiling] Agora sim! Com a Voltéc eu fico conectada o verão inteiro.
Tem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra.
[upbeat] Sem fidelidade: planos de dois a cinco meses.
[excited] Clica no botão Saiba Mais ou escaneia o QR code na tela!
```

Regras:
- **Tags** de emoção em inglês, entre colchetes, no começo da frase em que a entrega muda (`[frustrated]`, `[relieved, smiling]`, `[upbeat]`, `[excited]`). Elas não são lidas em voz alta e ocupam ~0,1 s ou menos no alignment. No máximo uma por frase. Tags de reação (`[laughs]`, `[sighs]`) não foram usadas nem testadas; a pesquisa avisa que o v4 às vezes interpreta uma tag ambígua como efeito sonoro.
- **Pronúncia da marca**: grafia fonética só no texto do TTS (`Voltéc` para vol-TÉC); a legenda e a tela mostram a grafia correta, "Voltec". Confira a tônica com `scripts/stress.py` (duração e energia das sílabas pelo alignment).
- **Números por extenso** no TTS (`dois a cinco meses`); a legenda pode mostrar "2 a 5".
- **Pausas**: reticências para hesitação, interrogação muda a entonação, quebra de linha cria pausa. O v4 não aceita SSML `<break>`. CAIXA ALTA para ênfase vem da pesquisa e não foi testada.
- **Settings** (sessão): `stability` 0.45, `similarity_boost` 0.85, `language_code` "pt", `seed` fixo. O v4 não tem `style`, `speed` nem speaker boost. Os valores salvos na voz (0.2/0.3) são baixos demais para o v4: sobrescreva sempre. Se a entrega sair teatral ou instável, a pesquisa sugere stability 0.55; se sair monótona, 0.38 (não testado).
- **Gere a narração inteira numa request** (prosódia contínua) e corte pelos timestamps. Na sessão, a v2 saiu em 2 versões (`narracao_v2_A_s1` e `_s2`) e a s1 foi a usada.
- **Roteiro de anúncio pago** (Voltec): o CTA é o botão "Saiba mais" mais o QR na tela. "Link na bio" é só para post orgânico.

Ex.: Verão Conectado. Corpo reconstruído a partir de `audio/COMO_FOI_MONTADA_narracao_v3.txt` (o JSON não foi salvo): texto de `narracao_v2.txt`, seed 20261015; a v3 é essa narração com o CTA emendado (ver abaixo). Endpoint: `POST https://api.elevenlabs.io/v1/text-to-speech/4yvYc2GSakxLWMhlsd6b/with-timestamps?output_format=wav_48000`, voz "Radassa 100%" da Voltec. Saída: WAV 48 kHz mono. O `apply_text_normalization: "auto"` vai como nos outros arquivos da skill: é recomendação da pesquisa, e o registro não diz se foi enviado.

```json
{
  "text": "[frustrated] Casa de praia sem internet? Ninguém merece...\n[relieved, smiling] Agora sim! Com a Voltéc eu fico conectada o verão inteiro.\nTem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra.\n[upbeat] Sem fidelidade: planos de dois a cinco meses.\n[excited] Assina pelo link na bio!",
  "model_id": "eleven_v4",
  "language_code": "pt",
  "voice_settings": {"stability": 0.45, "similarity_boost": 0.85},
  "apply_text_normalization": "auto",
  "seed": 20261015
}
```

Numa produção nova, gere de uma vez o roteiro final completo, com os nomes da convenção (`bodies/tts_<vN>_s<seed>.json` → `audio/narracao_<vN>_s<seed>.wav` + `_alignment.json`; corpo com `jq` em `api-elevenlabs.md` §5.1). Para gerar, salvar o áudio e o alignment e conferir:

```bash
# POST .../with-timestamps?output_format=wav_48000 -> .wav + _alignment.json (GASTA CRÉDITOS, ~1 por caractere)
python3 -I "$SKILL/scripts/el.py" tts 4yvYc2GSakxLWMhlsd6b "$PROJ/bodies/tts_v1_s20261015.json" "$PROJ/audio/narracao_v1_s20261015"
python3 -I "$SKILL/scripts/stt.py" "$PROJ/audio/narracao_v1_s20261015.wav"                     # o texto falado está certo?
python3 -I "$SKILL/scripts/stress.py" "$PROJ/audio/narracao_v1_s20261015.wav" \
  "$PROJ/audio/narracao_v1_s20261015_alignment.json"                                            # tônica de "Voltéc"
```

**Trocar uma frase sem regravar tudo** (como o CTA virou "Saiba Mais"). O procedimento completo, com o código que junta os alignments, está em `api-elevenlabs.md` §5.5; aqui fica o registro do que a sessão fez. A frase nova foi gerada sozinha, com a mesma voz e os mesmos settings e `previous_text` com as frases anteriores. Corpo reconstruído do mesmo registro (com `apply_text_normalization` pelo mesmo motivo):

```json
{
  "text": "[excited] Clica no botão Saiba Mais ou escaneia o QR code na tela!",
  "model_id": "eleven_v4",
  "language_code": "pt",
  "voice_settings": {"stability": 0.45, "similarity_boost": 0.85},
  "apply_text_normalization": "auto",
  "previous_text": "Tem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra. Sem fidelidade: planos de dois a cinco meses.",
  "seed": 20261017
}
```
- O `previous_text` levou as frases 3 e 4. O registro não diz se as tags foram junto.
- A frase foi gerada com 3 seeds (arquivos `cta_v3_20261015/16/17.wav`) e a escolhida foi a 20261017.
- A emenda foi feita num silêncio: o corte em 15,05 s (depois de "meses"), fade de 20 ms, 0,17 s de silêncio e a frase nova com −3,0 dB para casar com a anterior. Comando real:
  `ffmpeg -i narracao_v2_A_s1.wav -i cta_v3_20261017.wav -filter_complex "[0:a]atrim=end=15.05,asetpts=N/SR/TB,afade=t=out:st=15.03:d=0.02[a];anullsrc=r=48000:cl=mono,atrim=duration=0.17[g];[1:a]aresample=48000,aformat=channel_layouts=mono,volume=-3.0dB,asetpts=N/SR/TB[b];[a][g][b]concat=n=3:v=0:a=1[out]" -map "[out]" -ar 48000 -ac 1 narracao_v3.wav`
- O alignment da frase nova é deslocado pelo ponto da emenda (+15,22 s) e juntado ao anterior. O código está em `api-elevenlabs.md` §5.5 (a única versão na skill).
- **Registre sempre** como a narração final foi montada (texto final em `prompts/narracao_vN.txt` e um `audio/COMO_FOI_MONTADA_*.txt`). Sem isso, uma regeração futura traz o CTA antigo de volta.

### 2.9 Molde-base de cena para qualquer campanha [não testado como texto único; montado a partir dos moldes testados]

Cada bloco saiu de um prompt testado (2.1, 2.3 e 2.5), mas o conjunto, como texto único com slots, nunca foi enviado.
- Conferido na revisão da skill (15/10/2026): preenchidos com os trechos do T1 do Verão Conectado, os dois moldes reproduzem exatamente `prompts/T1_snapshot.txt` e `prompts/T1_video_veo_v2.txt`. No snapshot, a frase da mão livre (`Her left hand rests on her hip.`) vai logo depois da expressão, como no original. Isso confere o texto, não uma geração nova.
- Tudo entre chaves é slot: o nome em inglês diz qual é, e o texto depois dos dois-pontos diz que parte escrever ali. Um slot pode aparecer em mais de um lugar.
- O texto fora das chaves é fixo. As únicas exceções previstas estão nas notas abaixo de cada molde: sem foto do local, na selfie e com pouca luz.
- Escreva os slots em inglês, com o mesmo texto em todos os prompts do mesmo lugar (`prompts-principios.md` §1.10).
- Compare com o exemplo testado mais perto da cena.

**Snapshot** (gpt-image-2.5-sunburst; corpo como em 2.1, com `images` = [rosto, foto do local]):

```text
Reference roles: Image 1 is the woman's face: keep her exact identity, facial proportions, skin tone, eyes, eyebrows, nose, lips and hair; ignore the car interior behind her. Image 2 is a real photo of {PLACE: o lugar, em poucas palavras}: use it only for {PLACE: as formas que valem}; ignore its {PLACE: a luz da foto e o que ela tem e a cena não}.

A single frame grabbed from a casual vertical 9:16 smartphone video, not a photo shoot. {CAMERA_OWNER}

Location: {PLACE}

Subject: {IDENTITY_ANCHOR} She wears {OUTFIT}. No jewelry. {OBJECT} {EXPRESSION} Five natural fingers on each hand, visible knuckle creases, short dark wine-red nails slightly worn at the tips.

Skin and hair: real, unretouched skin with visible pores on the nose and cheeks, a faint natural shine on the forehead and nose bridge, slightly uneven tone around the mouth and chin, two tiny blemishes near the jawline, fine wispy hairs along the hairline, slightly darker skin under the eyes; light everyday makeup only; small natural asymmetry. Hair not salon-perfect, with slight humidity frizz; {TIME_AND_LIGHT: o ar e o cabelo, nunca no rosto}.

Light: {TIME_AND_LIGHT}

Look: a real smartphone video frame: wide lens, deep focus with the background clearly recognizable, phone HDR tone mapping, slight over-sharpening and video-compression softness, faint noise only in the shadows, true-to-life colors, no color grade, no filter, no bokeh, no retouching.

{CLOSING_NO_TEXT}
```

- Sem foto do local: tire a frase da Image 2 e o item dela em `images` (2.1).
- Take seguinte no mesmo lugar: não use este molde; faça a edição de pose (2.2).
- Lugar novo no mesmo vídeo: o T1 base entra como Image 1 e o rosto como Image 2, como no T3 (2.3).
- Selfie: o 2º parágrafo inteiro muda, inclusive a frase de frame de vídeo. Copie a estrutura do T3 (2.3).

**Vídeo** (Veo 3.1; corpo como em 2.5, negative_prompt como em 2.6):

```text
Vertical 9:16 amateur smartphone video, one continuous real-time take with no cuts, filmed {CAMERA_OWNER: quem filma, distância, altura e câmera}: natural micro-shake and slow breathing sway, no zoom, no pan. The woman in the first frame, {IDENTITY_ANCHOR: versão curta}, wearing {OUTFIT: versão curta}, {PLACE: onde ela está}, {OBJECT: a pose exata do snapshot, com o objeto e as duas mãos}.
[00:00-00:03] {ACTION_BEATS: tempo 1, começando na pose do snapshot}.
[00:03-00:05] {ACTION_BEATS: tempo 2}, {EXPRESSION}.
[00:05-00:08] {ACTION_BEATS: tempo 3, olhar no rosto de quem filma; termina parada, piscando}.
Her lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth, and she never speaks. {OBJECT: a regra do objeto}. The {PLACE: 3 a 4 elementos que estão no snapshot} stay exactly as in the first frame; {TIME_AND_LIGHT: o que o ar mexe}. Light: {TIME_AND_LIGHT: a mesma do snapshot}. Unedited, candid phone footage: natural skin texture with visible pores, crisp daylight frames with almost no motion blur, true-to-life colors.
Ambient noise: {AMBIENT_SOUND: a cama do lugar}, recorded by the phone's built-in microphone. SFX: {AMBIENT_SOUND: o ruído no microfone}; {AMBIENT_SOUND: um som ligado à ação, nunca de boca}. No music. {CLOSING_NO_TEXT}
```

- Na selfie, a primeira frase inteira muda: copie a estrutura do T3 (2.5).
- `crisp daylight frames` vale de dia. Com pouca luz ou à noite, veja 2.10.

**Os slots**

1. **`{CAMERA_OWNER}`**
   - O que escrever: quem filma (a amiga ou ela mesma, na selfie), a distância, a altura e a câmera (traseira, ~26 mm eq.; frontal, ~24 mm eq.). Depois, um movimento só e o quadro inteiro inclinado, com duas linhas retas do lugar inclinando juntas. Feche com o enquadramento, do joelho para cima ou mais perto, e o lugar do espaço livre para o texto da edição.
   - Ex.: Verão Conectado (T1): `Filmed handheld by a friend standing about 1.2 meters in front of her, holding the phone level at chest height (main rear camera, about 26 mm equivalent). The whole frame is rolled about 2 degrees, so the top of the wall and the horizon tilt together and stay parallel. Medium-wide shot framed from just above her knees, her slightly right of center, open sky in the upper right of the frame.` Selfie: o 2º parágrafo do T3 (2.3).
   - Opções: amiga filmando [vivido]; selfie [vivido]; celular apoiado num móvel, parado, na altura da cintura (`at waist height`, como está na pesquisa), olhando um pouco para cima [pesquisa; nunca gerado].
   - Armadilhas:
     - drone, grua, gimbal, zoom, pan, `cinematic` ou lente de retrato (`prompts-principios.md` §1.2);
     - câmera que revela o que não está no 1º quadro;
     - inclinar só o horizonte;
     - no take seguinte no mesmo lugar, a câmera em outro ponto (2.2);
     - rosto pequeno no quadro. O mais aberto aprovado foi o T1, do joelho para cima. A ref da passarela foi descartada por ter o rosto pequeno, e a pesquisa diz que rosto pequeno no quadro faz a identidade derivar no vídeo [pesquisa].
2. **`{PLACE}`**
   - O que escrever:
     - o lugar descrito fisicamente, sem nome;
     - 3 a 5 elementos fixos do fundo, com as mesmas palavras em todos os takes do mesmo lugar;
     - a geometria que essa câmera veria;
     - uma frase "only … no …" com o que não existe ali;
     - se houver foto do local, o papel dela (Image 2): só as formas, ignorando a luz da foto.
   - Ex.: Verão Conectado (T1): `the shaded upstairs balcony of a simple two-story beach house facing the sea, in a quiet, flat beach town of low houses.` (...) `Flat coastal land only: no hills, rocks, islands, high-rise buildings, poles, cars or signs.` Image 2: `a real photo of the coastal restinga where this scene takes place: use it only for the shape of the wind-bent casuarina trees with wispy gray-green needles, the dry yellowish dune grass, the flat gray-blue sea and the perfectly straight, empty horizon; ignore its midday light and deep-blue sky.`
   - Armadilhas:
     - nome de lugar no prompt: "Avenida Atlântica" com "RJ" puxa Copacabana (`prompts-principios.md` §3.3);
     - placa, letreiro, fachada com nome, número de casa ou guarda-sol de marca viram texto;
     - pedir praia larga vista do 2º andar (`prompts-principios.md` §1.7);
     - citar no vídeo o que não está no snapshot (`prompts-principios.md` §1.10);
     - trocar de lugar dentro do take (`prompts-principios.md` §1.3);
     - espelho ou vidro grande no quadro: o reflexo mostra "câmeras fantasmas" [pesquisa].
   - Fato do lugar que não está em `locais-grussai.md` não entra no prompt. Marque "não pesquisado: pesquise com `locais-grussai.md` §7–§9" ou peça foto ao cliente (`locais-grussai.md` §7, item 1).
3. **`{TIME_AND_LIGHT}`**
   - O que escrever:
     - a hora;
     - a fonte de luz real e a direção dela; se estiver fora do quadro, diga onde;
     - onde fica o rosto (sombra aberta, luz lateral ou contraluz);
     - a exposição do celular pelo rosto e o céu;
     - o ar (vento ou ar parado) e o que ele faz com o cabelo, que nunca cruza o rosto.
   - Como preencher: calcule o sol para o lugar, a data e a hora (`locais-grussai.md` §8; em Grussaí, a tabela "Outras estações" do §3). Cena interna ou noite: `prompts-principios.md` §1.7 e 2.10.
   - Ex.: Verão Conectado (T1): `about 5 pm in summer. The sun is low behind the house, so the balcony and her face are in soft, even open shade, with a faint bright edge of skylight on her hair and shoulders.` (...) `Not golden-hour orange. The phone exposes for her face, so the sunlit background is slightly overexposed.` O ar: `a light breeze from behind her lifts a few strands at her shoulders, none across her face`.
   - Armadilhas:
     - "golden" fora da hora dourada;
     - sol se pondo no mar, que em Grussaí não acontece (`locais-grussai.md` §3);
     - ajuste de autoexposição sem motivo, que vira pulsação de brilho;
     - vento jogando o cabelo no rosto, ou direção de vento fora do verão (não pesquisada);
     - hora diferente entre takes do mesmo vídeo.
4. **`{IDENTITY_ANCHOR}`** (fixo da Voltec)
   - O que escrever: no snapshot, a âncora 3.1 de `persona-e-marca-voltec.md`, palavra por palavra; no vídeo, a versão curta, que não contradiz a imagem. Para snapshot novo da persona, siga a regra de `persona-e-marca-voltec.md` §3.
   - Ex.: Verão Conectado: no snapshot do T1, a âncora 3.1 seguida de `most of it falling behind her shoulders`; no vídeo, `an adult Brazilian woman with long straight dark-brown hair`.
   - Armadilhas: `girl`, `young`, `cute`, `baby hairs` ou idade sem `adult`, que acionam o filtro "Child" (`prompts-principios.md` §3.4 e §4); descritor de corpo no vídeo; texto diferente entre os takes.
5. **`{OUTFIT}`** (slot da campanha)
   - O que escrever: roupa opaca e sem decote, sem estampa, logo ou letreiro, em tecido liso ou de trama grande. Use a âncora de roupa da campanha (regras e exemplos em `persona-e-marca-voltec.md` §3.4), palavra por palavra em todos os takes do vídeo: a versão longa no snapshot, a curta no `{OUTFIT}` da edição de identidade (2.4) e a curtíssima no vídeo. Aqui vai só a descrição da roupa: o `She wears` e o `No jewelry.` já estão no molde.
   - Ex.: Verão Conectado: `a loose, hip-length white cotton crochet beach cover-up with a large open-weave pattern and three-quarter sleeves, worn open over a plain white cotton tank top with a round neckline, and light-wash denim shorts`; no vídeo, `a white crochet beach cover-up over a white tank top and light denim shorts`.
   - Armadilhas:
     - padrão fino (renda miúda, malha, listra fina) tremula;
     - transparência e palavras de moderação, como `sheer`, `low-cut`, `bikini` e `tight` (`prompts-principios.md` §4);
     - logo bordado de uniforme vaza texto: o uniforme vai sempre liso (2.10);
     - joias e tatuagens: `No jewelry` é fixo.
6. **`{OBJECT}`**
   - O que escrever: um único objeto de mão, já na mão no snapshot, com a mão que segura e a pegada. A tela, se houver, fica virada para ela, e o objeto inteiro fica no quadro. Diga onde fica a mão livre. No vídeo, escreva a regra do objeto e, se ele se mexer, o caminho que ele faz.
   - Ex.: Verão Conectado (T1): `She holds her right hand up just above her head, elbow slightly bent, with one smartphone in a plain matte black case with no logo; the whole phone is inside the frame with space above it; the screen faces down toward her, fingers wrapped around the back, thumb on the side edge, so only the back of the phone is visible.` e `Her left hand rests on her hip.` No vídeo: `The whole phone stays inside the frame, only its back toward the camera.`
   - Armadilhas:
     - abaixar, guardar, girar ou trocar o objeto de mão: o celular do T2r v2 virou uma "barra" com dedos fundidos (`prompts-principios.md` §1.4);
     - dois objetos na mão;
     - tela à vista, que vira interface e texto;
     - objeto saindo do quadro;
     - marca no objeto;
     - roteador na mão (2.10).
7. **`{ACTION_BEATS}`** (só no vídeo)
   - O que escrever: 2 a 3 tempos em 8 s, cada um com parte do corpo, direção, velocidade e amplitude. O 1º começa exatamente na pose do snapshot. O último termina parada, piscando, com o olhar no rosto de quem filma (na selfie, na própria imagem da tela).
   - Ex.: Verão Conectado (T1 v2): `[00:00-00:03] She slowly tilts the raised phone a little left and right, squinting up at the screen with her eyebrows drawn together.` (...) `[00:05-00:08] She lifts her eyes to her friend's face just above the lens with a tired, embarrassed closed-lip half-smile, gives one slow small shake of her head and holds still, blinking naturally.`
   - Armadilhas:
     - ação que não cabe em 8 s, que sai acelerada e deforma;
     - `cut to` ou troca de lugar;
     - huff, sigh, exhale ou risada aberta sob a narração (`prompts-principios.md` §3.1–3.2);
     - olhar cravado na lente;
     - mão perto da boca (`prompts-principios.md` §3.6).
8. **`{EXPRESSION}`**
   - O que escrever: a emoção do momento do roteiro, com a boca fechada, mostrada por olhos, testa, bochechas e ombros. No snapshot, é a expressão de partida do take; o vídeo começa nela.
   - Ex.: Verão Conectado: no T1, `She squints up at it with a frustrated half-frown, eyebrows drawn together, lips closed and pulled slightly to one side.`; no T2, `She looks at the screen with a closed-lip smile, cheeks lifted and eyes slightly crinkled, as if about to chuckle.`
   - Armadilhas: boca aberta, dentes ou risada sob a voz, que parecem dublagem (`prompts-principios.md` §1.5); expressão do 1º tempo do vídeo diferente da do snapshot.
9. **`{AMBIENT_SOUND}`** (só no vídeo)
   - O que escrever: até 3 camadas captadas pelo microfone do celular: a cama do lugar (o mesmo texto nos takes do mesmo lugar), um ruído no microfone e um som ligado a uma ação. Reescreva também o texto da cama de SFX da edição (`api-elevenlabs.md` §7).
   - Ex.: Verão Conectado (T1 v2): `Ambient noise: steady sea breeze and distant surf, recorded by the phone's built-in microphone. SFX: wind bumping the microphone now and then; a soft rustle of fabric as her arm comes down. No music.`
   - Armadilhas:
     - som de boca (bufada, risada);
     - música;
     - TV, rádio ou conversa: o STT acusa fala (`qa-checklist.md` §B);
     - um som que o negativo suprime, como `cars` no negativo contra carro no áudio (`prompts-principios.md` §1.11);
     - passos que o microfone não captaria ou som de banco (ex.: gaivota).
10. **`{CLOSING_NO_TEXT}`**
    - O que escrever: no snapshot, a frase final de zero texto. No vídeo Veo, `(no subtitles)` depois de `No music.`, mais o negative_prompt (2.6). No Seedance, as frases oficiais (2.7).
    - Ex.: Verão Conectado: no T1, `There is no text, sign, number, logo or watermark anywhere, the clothes have no print, and there are no other people in the frame.`; no T3, que tem 2 pessoas ao longe, `There is no text, sign, logo or watermark anywhere, and the clothes have no print.`
    - Armadilhas: palavra sensível, mesmo para negar (`prompts-principios.md` §4); negar gente quando a cena tem gente ao fundo (descreva em positivo); nome da marca no prompt (a marca entra só na edição).

Depois de preencher:
- Passe o "Checklist do prompt" (`prompts-principios.md` §1).
- Confira que nada do exemplo sobrou por engano: praia, crochê, rede, `5 pm in summer`, brisa do mar.
- Monte o corpo como em 2.1 (snapshot) ou 2.5 (vídeo) e gere 2 variações.

### 2.10 Cena interna, noturna ou com roupa nova: notas de adaptação [não testado]

Nenhuma cena desta seção foi gerada. São as regras que funcionaram (`prompts-principios.md` §1) aplicadas a cenários que o Verão Conectado não teve: casa, loja, carro, noite, inverno e uniforme.
- Em todos: faça o A/B do snapshot e revise com `qa-checklist.md` §A. No portão 3, avise o cliente de que a cena é nova.
- Os riscos que as refs da conta já mostraram (`persona-e-marca-voltec.md` §4; `prompts-principios.md` §3.8) valem aqui:
  - o letreiro VOLTEC da loja e o logo bordado do uniforme vazam texto;
  - o headset vaza;
  - o rosto pequeno não segura a identidade.

**Luz coerente** (`{TIME_AND_LIGHT}`; regra geral em `prompts-principios.md` §1.7)
- Uma fonte real e dominante, com direção, dita no prompt:
  - a janela: `soft daylight from a window out of frame on her left`;
  - uma luminária: `a warm ceiling lamp`;
  - à noite, uma luz prática no quadro ou logo fora dele, como a luz da varanda ou um abajur.
- A tela do celular, virada para ela, ilumina pouco e de baixo: use-a só como luz secundária.
- Luz do dia pela janela segue o sol real. Calcule com `locais-grussai.md` §8 e compare o azimute com a direção da janela ("Como ler", passos 1 a 3 e 5). A direção da janela de um lugar real não foi pesquisada: pergunte ao cliente ou use foto dele.
- Exponha pelo rosto (`the phone exposes for her face, so the window is slightly overexposed`), com as sombras numa direção só e nenhum ajuste de exposição sem causa.
- Com pouca luz ou à noite, troque `crisp daylight frames` por `crisp frames with almost no motion blur and fine phone noise in the darker areas`.
- Luz de lâmpada é `warm`, nunca `golden-hour`. A pesquisa manda evitar `studio lighting`, `rim light without a source`, `volumetric light rays` e `lens flare` [pesquisa].
- Rua à noite: como a orla de Grussaí é iluminada à noite não foi pesquisado. A única foto noturna de `locais-grussai.md` §6 (nº 8) é NC e serve só de referência interna. Não pesquisado: pesquise com `locais-grussai.md` §7–§9 antes de descrever.

**Som de ambiente interno** (`{AMBIENT_SOUND}` e a cama de SFX, `api-elevenlabs.md` §7)
- Cama: o room tone do cômodo, uma fonte contínua (ventilador de teto) e a rua lá fora, baixa e longe. `a motorbike passing far away on a sandy street` é da lista de camadas distantes da pesquisa [pesquisa].
- Ruído no microfone: dentro de casa não há vento batendo no microfone. Use o manuseio do celular: `faint handling noise when she shifts her grip on the phone`, da pesquisa [pesquisa].
- Som de ação: um só, ligado ao que ela faz (o sofá, o tecido).
- Nada de TV, rádio, música ou conversa: viram fala ou música no áudio nativo, e o STT acusa (`qa-checklist.md` §B).
- Exemplo: `Ambient noise: the quiet room tone of a small house, a ceiling fan humming and a motorbike passing far away on the street outside, recorded by the phone's built-in microphone. SFX: faint handling noise on the phone; a soft creak of the sofa as she shifts. No music. (no subtitles)`

**Roteador ou outro objeto da cena** (`{OBJECT}` e `{PLACE}`)
- Sem logo, texto ou etiqueta, com LEDs simples e fixos: `a plain white wifi router with no logo, text or labels, two short antennas and a row of small steady green status lights`. LED piscando pode virar pulsação de brilho (`brightness flicker` já está no negativo).
- O roteador fica parado num móvel e está no quadro desde o 1º quadro. Ela não o pega, não o gira e não mexe nos cabos: manipulação é onde o Veo mais erra. O objeto de mão continua sendo um só (o celular).
- Poucos cabos, escondidos atrás do aparelho. Nada de caixa com marca nem de notebook ou TV com a tela à vista: viram interface e texto.

**Casa**
- Use fotos do cliente, sem pessoas identificáveis e sem placas (`locais-grussai.md` §7, item 1).
- Evite espelho e vidro grande no quadro: o reflexo mostra "câmeras fantasmas" [pesquisa].
- Escolha 3 a 5 elementos fixos do fundo, sem nada escrito (quadro com frase, calendário, embalagem).
- Opção de câmera: o celular apoiado num móvel (`{CAMERA_OWNER}`, 2.9) [pesquisa].

**Loja da Voltec**
- Nunca use a ref com o letreiro (`bZiCdj3zIGYdX0UKyfvU`) e nunca escreva o letreiro no prompt: o letreiro VOLTEC vaza texto. A marca entra só na edição.
- Como é a loja real (fachada, balcão, janela) não foi pesquisado. Não pesquisado: pesquise com `locais-grussai.md` §7–§9 ou peça foto ao cliente.
- Enquadre sem letreiro, fachada ou material de campanha à vista, em plano médio: um plano aberto da loja deixa o rosto pequeno.
- Roupa: o uniforme liso (abaixo) ou a âncora casual de loja de `persona-e-marca-voltec.md` §3.4.

**Carro**
- Parado, com o motor desligado: `a parked car with the engine off`. Carro andando põe paisagem correndo nas janelas (área revelada é área inventada), vibração e celular na mão de quem dirige.
- Som: `the quiet inside of a parked car, muffled street sounds outside`, sem motor.
- Volante, painel e chave sem logo; tela do painel desligada; placas dos outros carros fora do quadro. Retrovisor e vidros refletem: cuidado com câmera fantasma [pesquisa].
- O rosto da ref fixa (`na7keiYvPpGArmyghOpk`) foi recortado da foto do carro. Mantenha `ignore the car interior behind her` na Image 1, descreva o carro da cena só no `{PLACE}` e confira se o interior da ref não foi copiado.

**Inverno e outras estações** (`{OUTFIT}` e `{TIME_AND_LIGHT}`)
- Roupa: use a âncora de inverno de `persona-e-marca-voltec.md` §3.4 (moletom liso ou tricô de ponto grosso), nos 3 tamanhos, palavra por palavra em todos os prompts do vídeo.
- O clima e a roupa de inverno em Grussaí não foram pesquisados (não pesquisado: pesquise com `locais-grussai.md` §7–§9).
- Luz pela tabela "Outras estações" de `locais-grussai.md` §3: no inverno, sol a ~19,5° por volta de 15h40, e a selfie em contraluz caminha para o sul, com o mar à direita.
- Vento fora do verão: não pesquisado (`locais-grussai.md` §3); pesquise antes de fixar o cabelo.
- Tire os trechos de verão que sobram do exemplo: `about 5 pm in summer`, `sun-flushed`, a brisa do mar.

**Uniforme da Voltec, sempre liso**
- Pelas refs da conta (`persona_corpo_inteiro.jpg` e `persona_loja_logo.jpg`), o uniforme é uma polo vermelha com mangas e laterais azul-marinho, gola vermelha e carcela branca, e o logo VOLTEC bordado no peito.
- Use a âncora de uniforme liso de `persona-e-marca-voltec.md` §3.4. Ela já traz `without any logo, print, embroidery or lettering`; o "without any logo, print or lettering" é da pesquisa.
- Confira o peito a 100% no snapshot (logo inventado ou remendo): o logo bordado é o que vaza. A marca entra só no overlay.
- Edição de identidade com o uniforme na Image 1: veja a nota em 2.4.
- Sem headset, mesmo num tema de suporte: a ref com headset foi descartada porque o fone vazaria para a cena.

**Rosto grande no quadro**
- Do joelho para cima ou mais perto: o mais aberto aprovado foi o T1. Plano aberto de loja, rua ou praia deixa o rosto pequeno.
- A ref da passarela foi descartada por ter o rosto pequeno, e a pesquisa diz que rosto pequeno no quadro faz a identidade derivar [pesquisa].

**negative_prompt de cena interna**
- Troque a parte de lugar da praia (2.6) por `melting walls, warped furniture, bending door frames, mirror reflections, TV screen, laptop screen, extra people`.
- Mantenha a base geral e `jewelry`.

---
