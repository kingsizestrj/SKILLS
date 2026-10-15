# Prompts de realismo: princípios, armadilhas e moderação

Regras para escrever os prompts de qualquer vídeo realista com IA da Voltec com a personagem, em qualquer campanha, estação ou cenário. Elas saíram do caso de referência testado, o Reels "Verão Conectado" (15/10/2026). Os trechos dele aparecem como exemplo ("ex.: Verão Conectado"), não como padrão. Os moldes completos estão em `prompts-moldes.md`: molde-base com slots no §2.9 e cena interna, noturna ou com roupa nova no §2.10.

Os prompts vão em **inglês** (o Veo só garante inglês); os comentários estão em português. Todo prompt marcado como "testado" é o texto exato que foi para a API: foi conferido contra os corpos salvos em `/home/syllas/hyperframes/voltec-reels-ia/bodies/` (o `.txt` do prompt só tem a quebra de linha final a mais).

**Nível de evidência** (aparece entre colchetes):
- **[vivido]**: aconteceu na sessão e a correção foi conferida no resultado.
- **[aplicado]**: veio da pesquisa ou das críticas, entrou nos prompts finais e os takes saíram sem o problema. Não houve teste A/B sem a regra.
- **[pesquisa]**: só da pesquisa, não testado na sessão.
- **[não testado]**: derivado das regras que funcionaram e nunca gerado. Antes de mostrar ao cliente, faça o A/B do snapshot e revise com `qa-checklist.md` §A.

**Escopo**:
- **Geral**: vale para qualquer anúncio com IA.
- **Voltec**: fixo da Voltec com a personagem, em todo vídeo.
- **Grussaí**: geografia real da área atendida.
- **Verão Conectado** (ou "ex.: Verão Conectado"): valor só da campanha de referência. Numa campanha nova, vira slot (`prompts-moldes.md` §2.9).

Arquivos relacionados: `prompts-moldes.md` (os moldes completos: §0 fluxo e envio, §2 moldes), `persona-e-marca-voltec.md` (âncora de identidade, assets, voz), `locais-grussai.md` (local e sol), `api-elevenlabs.md` (endpoints e envio), `modelos-e-custos.md`, `qa-checklist.md` (revisão do snapshot e do take), `edicao-hyperframes.md`.

Sumário: 1. Princípios · 3. Armadilhas vividas · 4. Moderação. A numeração continua a dos moldes: §0 (fluxo e envio) e §2 (moldes) ficam em `prompts-moldes.md`.

---

## 1. Princípios que valeram na prática

### 1.1 Snapshot primeiro; o vídeo só anima (Geral) [vivido]
- O quadro inicial é gerado na API de imagem, aprovado pelo cliente e enviado como `start_frame`. Rosto, roupa, lugar e luz ficam travados. O prompt de vídeo descreve só movimento, câmera e som.
- O snapshot já mostra a **pose inicial** da ação: boca fechada ou sorriso leve, objeto na mão e sem motion blur congelado.
- Descreva o snapshot como frame de vídeo, não como foto: `A single frame grabbed from a casual vertical 9:16 smartphone video, not a photo shoot.` O vídeo herda o look do primeiro quadro.
- Defeito no primeiro quadro piora no vídeo: só aprove com mãos perfeitas (5 dedos, pegada coerente). [pesquisa]

### 1.2 Câmera com dono (Geral) [aplicado]
Todo prompt diz **quem filma**, a que altura, a que distância, com que câmera e qual é o **único** movimento. Câmera impossível (drone, grua, gimbal, travelling perfeito na areia) denuncia IA.
- Amiga filmando (ex.: Verão Conectado, T1): `filmed handheld by a friend standing about 1.2 meters in front of her at chest height with the phone's main rear camera: natural micro-shake and slow breathing sway, no zoom, no pan.`
- Selfie (ex.: Verão Conectado, T3): `recorded by the woman herself on her phone's front camera at arm's length, slightly above eye level ... the phone is the camera and never appears; her extended right arm stays at the lower-left edge of the frame.`
- Celular apoiado num móvel, parado, na altura da cintura (`at waist height`, como está na pesquisa), olhando um pouco para cima [pesquisa; nunca gerado]: opção para cena interna (`prompts-moldes.md` §2.10).
- Imperfeição crível sem geometria impossível: incline o quadro inteiro, com duas linhas retas do lugar inclinando juntas. Ex.: Verão Conectado: `The whole frame is rolled about 2 degrees, so the top of the wall and the horizon tilt together and stay parallel.` Se o prompt inclinar só o horizonte, o modelo deixa o parapeito reto, e isso é geometria impossível. Em cena interna, as linhas podem ser o batente da porta e a borda da janela [não testado].
- A câmera não revela o que não está no primeiro quadro: nada de pan largo, órbita ou recuo. Área revelada é área inventada. [pesquisa]
- Take seguinte no mesmo lugar: **mesma posição de câmera**, só um passo e uma inclinação (T2, `prompts-moldes.md` §2.2). No Verão Conectado, a versão do plano com a amiga agachada na altura dos olhos de quem está na rede foi barrada pela crítica: com a câmera a ~1,05 m, o horizonte cai no topo do parapeito e o mar some atrás da parede, e o modelo colaria um fundo de praia com cara de cenário pintado.
- Nos takes UGC, estes vão para o negativo: `cinematic color grading`, `film look`, `drone shot`, `crane shot`, `gimbal glide`, `slow motion`, `zoom`, `shallow depth of field`, `heavy bokeh`. No prompt, não escreva "cinematic" nem peça lente de retrato (85 mm).

### 1.3 Um lugar e uma ação principal por take (Geral) [aplicado]
- Um clipe = um local, um horário e uma ação principal em 2 a 3 tempos (em 8 s). Ação que não cabe no tempo sai acelerada e deforma mão e objeto.
- Nunca "cut to..." ou "then she is at the beach" no mesmo prompt. Trocar de local exige novo snapshot.
- Cada tempo diz parte do corpo, direção, velocidade e amplitude (`slowly tilts the raised phone a little left and right`). O primeiro começa **exatamente** na pose do snapshot. Diga onde estão as duas mãos.
- Termine o take parado (`holds still, blinking naturally`): sobra folga para cortar.
- Sequência sem troca brusca de ambiente: um lugar e uma hora por vídeo, com a mesma roupa e cortes motivados. Ex.: Verão Conectado: T1 e T2 na mesma varanda (corte seco de antes e depois), T3 na areia em frente à mesma casa, na mesma tarde, com a mesma roupa e o mesmo vento.

### 1.4 Objeto já no primeiro quadro, e quieto (Geral) [vivido]
- Um único objeto de mão (no Verão Conectado, o celular), já na mão no snapshot, com a pegada descrita: `fingers wrapped around the back, thumb on the side edge`, `in a plain matte black case with no logo`.
- Tela sempre virada para ela (`only the back of the phone is visible`, `no screen is visible`): se a tela aparece, o modelo inventa interface e texto.
- `The whole phone stays inside the frame`: objeto que sai do quadro volta redesenhado (forma, cor, quantidade).
- **Não mande abaixar, guardar, girar nem trocar o objeto de mão.** Na verificação final, o celular do T2r v2 (2ª rodada) virou uma "barra" fina com dedos fundidos quando ela o abaixou para o colo, sem que o prompt pedisse isso. A correção foi trocar pela variação em que ela segura o aparelho firme o tempo todo. Se o objeto precisa se mover, descreva o caminho: `brings the phone down along her right side to chest height without passing in front of her face`.
- Na selfie, o celular é a câmera e não aparece: zero anomalia de objeto.
- Mão livre ancorada: `her left hand on her hip`, `her left hand resting in her lap`, `her left hand stays out of frame`.
- Padrões finos tremulam: use tecido liso ou de trama grande. Ex.: Verão Conectado: crochê de trama aberta e grande, rede lisa sem franjas (`plain off-white woven cotton hammock without fringes`). [aplicado]
- Objeto da cena que não vai na mão, como o roteador [não testado]: as mesmas regras. Ele fica sem logo nem texto, parado num móvel desde o 1º quadro, e ela não o pega (`prompts-moldes.md` §2.10).

### 1.5 Boca fechada sob narração (Geral) [vivido]
- A personagem **não fala** no vídeo gerado: a narração (TTS com a voz clonada) entra na edição. Nenhum modelo da API faz lip-sync com a voz clonada mantendo o `start_frame`, e fala no prompt puxa legenda queimada.
- Peça a boca fechada em positivo, listando os verbos que o modelo costuma inventar:
  `Her lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth, and she never speaks.`
- Mostre emoção por olhos, testa, bochechas e ombros: `a closed-mouth chuckle: her cheeks lift, her eyes crinkle and her shoulders shake gently while her lips stay together` e `her smile widens without opening her mouth`.
- Tire também o som humano do bloco de áudio. O T1 v2 trocou `her single short huff through the nose` por `a soft rustle of fabric as her arm comes down`.
- Risada de boca aberta sob a voz parece dublagem fora de sincronia.

### 1.6 Olhar para o rosto de quem filma, não para a lente (Geral) [aplicado]
- Amiga filmando: `She lifts her eyes to her friend's face just above the lens`.
- Selfie: `looking at her own image on the screen, so her eyes aim slightly below the lens`.
- Olhar cravado na lente é linguagem de apresentador e de anúncio, e é comum em vídeo gerado.

### 1.7 Luz fisicamente coerente [aplicado]
**Geral**
- Uma fonte de luz real, com horário e direção. Se estiver fora do quadro, diga onde (`the sun itself is out of frame`).
- Exposição de celular: exponha pelo rosto e deixe o que é mais claro estourar um pouco. Ex.: Verão Conectado: `The phone exposes for her face, so the sunlit background is slightly overexposed.`
- Nada de "golden" antes da hora. Quem decide é a altura do sol: a ~19° a luz é quente e clara; abaixo de ~10°, dourada (`locais-grussai.md` §8, "Como ler", item 4). Escreva `Not golden-hour orange.` quando a hora não for dourada. Ex.: Verão Conectado: segundo as críticas, às 17h de meados de janeiro o sol está a ~19° de altura (`warm late-afternoon sunlight ... Not golden-hour orange.`), e luz dourada de verdade só aparece a partir de ~17h40.
- Não peça ajuste de autoexposição sem motivo, porque o modelo responde com pulsação de brilho (flicker). A exposição só muda se algo grande e claro entra ou sai do quadro. A frase saiu dos prompts finais e `brightness flicker` entrou no negativo.
- Vento coerente com o cabelo: escolha a direção para o cabelo nunca cruzar o rosto. Ex.: Verão Conectado: na varanda, `a light breeze from behind her lifts a few strands at her shoulders, none across her face`; na areia, ela anda de frente para o vento: `sweeping her hair back off her face`.
- Cadência de celular de dia: `crisp daylight frames with almost no motion blur`, com ruído só na sombra. Para noite ou interior com pouca luz, veja o bloco abaixo.

**Outra estação, outro lugar ou cena interna: como aplicar a regra** [não testado]
1. **Externa, em qualquer lugar e data:**
   - Rode o snippet de `locais-grussai.md` §8 com as coordenadas, a data e a hora da cena.
   - Escolha a hora pela altura do sol, não pelo relógio. Para repetir a luz aprovada, mire ~19,5°. Em Grussaí, a tabela "Outras estações" de `locais-grussai.md` §3 já dá a hora: ~16h00 a 16h20 no outono e na primavera, ~15h40 no inverno.
   - Compare o azimute com a direção da fachada ou da praia (`locais-grussai.md` §8, "Como ler", itens 1 a 3). Diferença acima de 90° = fachada na sombra e rosto em sombra aberta.
   - Ponha o sol atrás dela ou de lado. Confira o vento antes de fixar o cabelo: fora do verão, não foi pesquisado.
2. **Cena interna (casa, loja, carro):**
   - A fonte é a janela, a porta, o para-brisa ou uma luminária. Diga qual, de que lado e se fica fora do quadro.
   - Luz do dia pela janela segue o sol real. Calcule com `locais-grussai.md` §8 e compare o azimute com a direção da janela ("Como ler", passo 5): com diferença acima de 90°, não entra sol direto, só a luz suave do céu.
   - A direção da janela de um lugar real não foi pesquisada: pergunte ao cliente ou use foto dele (`locais-grussai.md` §7).
   - Luz de lâmpada é `warm`, nunca `golden-hour`.
3. **Noite:**
   - Use uma fonte prática no quadro ou logo fora dele (luz da varanda, abajur). A tela do celular, virada para ela, só como luz secundária.
   - Troque `crisp daylight frames` por quadros nítidos com ruído fino de celular nas áreas escuras.
   - Como a orla de Grussaí é iluminada à noite não foi pesquisado: pesquise com `locais-grussai.md` §7–§9 antes de descrever.

Textos de exemplo e o resto da adaptação: `prompts-moldes.md` §2.10.

**Grussaí** (detalhes em `locais-grussai.md`). Luz e vento abaixo são da cena de verão do Verão Conectado (~17h); fora do verão, use a tabela "Outras estações" de `locais-grussai.md` §3 e pesquise o vento antes.
- A praia é plana e voltada para o leste: o sol se põe atrás das casas, **nunca no mar**. Às 17h no verão, a varanda de frente para o mar fica em sombra aberta, com o fundo ensolarado.
- Na areia: sol baixo atrás dela e à direita do quadro, fora de cena, fazendo contraluz na borda do rosto; rosto em sombra aberta rebatida pela areia; vento nordeste de frente jogando o cabelo para trás. Às 17h sol e vento vêm de lados quase opostos, então sol de frente obrigaria o cabelo a voar na cara.
- Vista do 2º andar: areia e mar são uma faixa fina (~2 a 4° do quadro): `a thin band of pale sand and a thin band of flat gray-blue sea`. Pedir "praia larga" faz o modelo subir a câmera ou pôr a casa em cima da areia.

### 1.8 Nada de texto, logo ou marca gerados (Geral) [aplicado]
- Feche todo prompt de imagem com `There is no text, sign, number, logo or watermark anywhere, the clothes have no print, and there are no other people in the frame.`
- No vídeo Veo, `(no subtitles)` no fim, mais o negativo com `subtitles, captions, on-screen text, text overlay, watermark, logo, brand name, readable signs, phone screen interface`. No Seedance, as frases oficiais (`prompts-moldes.md` §2.7).
- Nenhum nome de marca no prompt (`iPhone`, `WhatsApp`, `Instagram`, `FaceTime`). Use `smartphone` e `video call`.
- Referências sem logo nem letreiro (recorte ou `ffmpeg delogo`), porque o modelo transfere texto das refs para a cena.
- Cenário ou roupa da própria marca (loja da Voltec, uniforme): nada de letreiro nem de logo bordado na cena, nem no prompt (`prompts-moldes.md` §2.10) [não testado].
- Logo, QR, legendas e preço entram só na edição (HyperFrames).
- Antes da sessão, a conta já tinha tido legenda em português queimada num Veo Fast com fala no prompt (geração QgxroTk1FNOGUAuXpk0o). A pesquisa recomenda nunca pôr falas entre aspas.

### 1.9 Look de celular e pele real (Geral) [aplicado]
- Look: `wide lens, deep focus with the background clearly recognizable, phone HDR tone mapping, slight over-sharpening and video-compression softness, faint noise only in the shadows, true-to-life colors, no color grade, no filter, no bokeh, no retouching.`
- Pele (rosto e mãos): `visible pores on the nose and cheeks, a faint natural shine on the forehead and nose bridge, slightly uneven tone around the mouth and chin, two tiny blemishes near the jawline, fine wispy hairs along the hairline`. **Nunca `baby hairs`** (ver 3.4).
- Mãos: `Five natural fingers on each hand, visible knuckle creases, short dark wine-red nails slightly worn at the tips.` (As unhas vinho-escuro são fixas da persona da Voltec.)
- Palavras que puxam look de IA e não entram: `cinematic`, `8K`, `ultra realistic`, `masterpiece`, `stunning`, `flawless`, `perfect skin`, `porcelain`, `glass skin`, `airbrushed`. [pesquisa]

### 1.10 Âncoras iguais e ambiente só com o que está no quadro (Geral) [aplicado]
- Use o mesmo texto de identidade e de roupa, palavra por palavra, em todos os prompts do vídeo. A identidade é fixa da Voltec (`persona-e-marca-voltec.md` §3.1); a roupa é da campanha, no estilo do §3.4.
- No vídeo: `The woman in the first frame, <âncora curta>`. A âncora nunca contradiz a imagem.
- A linha de ambiente lista 3 a 4 elementos que **aparecem de fato** no snapshot, mais `stay exactly as in the first frame`. Elemento citado que não está no quadro tende a surgir durante o clipe, com morph.
- Nomes de lugar ficam fora do prompt: descreva o lugar fisicamente (3.3).

### 1.11 Áudio de captação: 3 camadas, sem música (Geral) [aplicado]
- Formato Veo: `Ambient noise: <cama>, recorded by the phone's built-in microphone. SFX: <ruído no microfone>; <um som ligado a uma ação>. No music.`
- No máximo 3 camadas: a cama do lugar (com o mesmo texto nos takes do mesmo lugar), um ruído no microfone e um som de ação. Ex.: Verão Conectado: brisa e mar ao longe, o vento batendo no microfone, o rangido da rede ou o tecido. Nada de passos que o microfone não captaria, gaivota de banco de sons ou risadas.
- Cena interna: room tone, ventilador e a rua lá fora, e o manuseio do celular no lugar do vento no microfone (`prompts-moldes.md` §2.10) [não testado].
- O Veo gera áudio e vídeo juntos, então o negativo pode suprimir sons: não negue algo que o áudio pede (ex.: `cars` no negativo contra `a car passing` no áudio).
- O áudio nativo vira só ambiente na mixagem (`edicao-hyperframes.md`). Use STT para provar que ele não tem fala nem música (`qa-checklist.md`).

### 1.12 Duas variações por take e revisão quadro a quadro (Geral) [vivido]
- Em toda rodada, pelo menos uma das variações teve problema: celular de quem filma aparecendo, mão na boca, celular deformando. No Veo, envie o mesmo corpo com seeds diferentes (na sessão, 20260115 e 20260116).
- Muita falha se resolve escolhendo o trecho do take (in/out em quadros de 24 fps), o que custa zero. Gerar de novo custa 19.391 créditos por take Veo de 8 s em 1080p.
- Para refazer, mude **uma** variável por vez. Prefira regerar ou simplificar a ação a empilhar adjetivos. [pesquisa]

### Checklist do prompt (antes de gastar crédito)
- [ ] Quem filma, altura, distância, câmera; um movimento só; sem zoom nem pan.
- [ ] Pose inicial = snapshot; 2 a 3 tempos; termina parada.
- [ ] Um objeto, já no quadro, com a tela virada para ela; sem abaixar, guardar ou girar.
- [ ] Frase de lábios fechados (todo take sob narração) e nenhum som de boca no áudio.
- [ ] Olhar no rosto de quem filma ou na própria imagem da tela.
- [ ] Ambiente só com o que está no quadro, mais `stay exactly as in the first frame`.
- [ ] Luz: fonte real e direção, com a hora calculada para o lugar e a data (`locais-grussai.md` §8); `Not golden-hour orange` se a hora não for dourada; nenhum ajuste de exposição.
- [ ] Áudio com 3 camadas e `No music.`
- [ ] Sem nomes de lugar nem de marca; `fine wispy hairs`; adulta explícita.
- [ ] Fecho: `(no subtitles)` + negative_prompt (Veo) ou frases oficiais (Seedance).
- [ ] Slots da campanha preenchidos (`prompts-moldes.md` §2.9) e nada do exemplo sobrando por engano: praia, crochê, rede, `5 pm in summer`, brisa do mar e sons de praia só ficam se a cena for essa.

---

## 3. Armadilhas vividas e a correção de cada uma

### 3.1 Boca abrindo em "O" (sopro) [vivido]
- **Sintoma**: no T1 ela abre a boca como se falasse um "O". O cliente notou.
- **Causa**: o prompt pedia `presses her lips together and huffs once through her nose` e o áudio pedia `her single short huff through the nose`. O Veo fez um sopro de boca.
- **Na hora, sem custo**: recortar o take antes do quadro em que a boca abre, achado quadro a quadro a 24 fps. O T1 v1 entrou a partir do quadro 12, com 89 quadros.
- **No prompt**: a v2 (`prompts-moldes.md` §2.5) troca a bufada por `a disappointed frown, lips pressed together`, acrescenta `Her lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth`, troca o SFX de bufada por um de tecido e soma ao negativo `open mouth, pursed lips, blowing air, whistling, yawning, hand over mouth`. Regra: nada de huff, exhale ou sigh em take sob narração.

### 3.2 Risada de boca aberta sob a voz [aplicado: barrado pela crítica antes de gerar]
- **Sintoma esperado**: a boca abre e fecha enquanto a narração na voz dela fala, e o take parece dublagem fora de sincronia.
- **Causa**: o plano pedia `a short, natural laugh` no T2 e `smile showing her teeth ... one short, happy laugh` no T3, justamente sob as frases da narração.
- **Correção**: `closed-mouth chuckle` no T2, `smile widens without opening her mouth` no T3 e nenhuma risada no bloco de áudio. Nas notas da sessão: o Veo tende a abrir a boca em risadas e bufadas.

### 3.3 Nomes de lugar que puxam Copacabana [aplicado]
- **Causa**: "Avenida Atlântica" junto com "RJ" é Copacabana para qualquer modelo (calçadão de ondas, prédios, morros). Grussaí também tem calçadão de pedra portuguesa em ondas com coqueiro, o que reforça a associação. E "Grussaí" ou "Brazil" não ajudam o modelo, que não sabe como o lugar é.
- **Correção**: nenhum nome de lugar nos prompts de geração. Descreva fisicamente: `a quiet, flat beach town of low houses`, `wind-bent casuarina trees with wispy gray-green needles`, `the flat gray-blue sea`, `the straight, empty horizon`, `Flat coastal land only: no hills, rocks, islands, high-rise buildings`. Os nomes ficam nos documentos internos e na legenda do post. A fidelidade ao lugar vem da foto real (ref) e da descrição.

### 3.4 "baby hairs" [aplicado]
- **Causa**: "baby" junto de descrição de pele aciona o filtro "Child" do Google (códigos 58061214 e 17301594). No Veo, imagem para vídeo só aceita adultos.
- **Correção**: `fine wispy hairs along the hairline` em todos os prompts.

### 3.5 Celular de quem filma aparecendo [vivido]
- **Sintoma**: no T1r v2, o celular de quem filma apareceu no topo do quadro aos 4,5 s.
- **Correção usada**: a outra variação (T1r v1), que é o motivo de gerar 2 por take. Se o trecho bom terminar antes do defeito, dá para usar só ele.
- **Prevenção**: nenhuma confirmada. `second phone` já estava no negativo e não impediu. Revise sempre o take inteiro.

### 3.6 Mão na boca, como bocejo [vivido]
- **Sintoma**: numa variação, ela levou a mão à boca como num bocejo.
- **Correção**: a outra variação, mais `yawning, hand over mouth` no negativo (entrou no T1 v2) e a mão livre sempre ancorada no prompt (`left hand on her hip`, `in her lap`, `out of frame`).

### 3.7 Rosto que deriva no Gemini [vivido]
- **Sintoma**: o `gemini-3-pro-image` afinou e alterou o rosto da persona e trocou a roupa. A pesquisa tinha recomendado esse modelo; a sessão desmentiu.
- **Correção**: snapshots de persona no `gpt-image-2.5-sunburst` (9:16, 2K, quality high). Faça A/B no primeiro snapshot com o mesmo prompt e as mesmas refs. Para melhorar a semelhança depois, use a edição de identidade (`prompts-moldes.md` §2.4).

### 3.8 Referências que vazam para a cena [vivido + crítica]
| Ref | Problema | O que fazer |
|---|---|---|
| Foto com headset | O fone vazaria para a cena. | Não usar. |
| Foto na passarela | Rosto pequeno não segura a identidade. | Não usar. |
| Loja com letreiro VOLTEC enorme | O modelo transfere texto. | Recortar só o rosto (`ref_a_rosto_crop.jpg`). |
| Corpo inteiro com logo bordado no uniforme | Logo e vermelho vazam para a roupa. | `ffmpeg delogo` (`prompts-moldes.md` §2.4) e `ignore ... the red uniform, the logo` no prompt. |
| Foto do carro com dedos no queixo e colar | Puxa mão perto do rosto e colar tremulando. | Recorte do rosto sem dedos e sem colar (`persona_headshot_sem_dedos.jpg`). |
| Frames antigos de selfie (rosto genérico/glam, 640x1080) | Rosto diferente da persona, e o look de IA (pele lisa, céu saturado) passa para o snapshot. | Não usar como identidade. |
| Foto do local com plaquinha ou carimbo de data | Vira texto na cena. | Escolher outra ou recortar. |

Os mesmos riscos valem para os cenários que nunca foram gerados (loja, uniforme, tema de suporte): o letreiro e o logo bordado vazam texto, o headset vaza e o rosto pequeno não segura a identidade. Como aplicar: `prompts-moldes.md` §2.10 [não testado].

### 3.9 Outras armadilhas

| Sintoma | Causa | Correção | Nível |
|---|---|---|---|
| Celular vira "barra" fina com dedos fundidos (T2r v2) | Ela abaixou o aparelho para o colo; objeto que gira ou fica de perfil é onde o Veo mais erra. | Usar a variação em que ela segura firme; não mandar abaixar, guardar ou girar; revisar a manipulação em tiras de 8 fps. | vivido |
| Fundo de praia com cara de cenário pintado | Câmera na altura dos olhos de quem está sentada: o horizonte cai no parapeito. | Mesma posição de câmera do take anterior (`prompts-moldes.md` §2.2). | crítica |
| Coisas surgindo no meio do clipe | O prompt de vídeo cita elementos que não estão no snapshot. | Linha de ambiente só com o que está no quadro (1.10). | crítica |
| Pulsação de brilho | `auto-exposure adjusts` sem causa. | Remover; `brightness flicker` no negativo. | crítica |
| Pôr do sol no mar, laranja geral | Geografia ignorada; "golden" às 17h. | Sol coerente com o lugar; `Not golden-hour orange.` | crítica |
| Horizonte torto com parapeito reto | "horizon tilted" inclina só o mar. | `The whole frame is rolled about 2 degrees, so ... tilt together and stay parallel.` | crítica |
| Legenda queimada ou fala inventada | Fala no prompt de vídeo. | Personagem não fala; narração na edição; `(no subtitles)` e negativo. | conta |
| STT ouve "conectado" em vez de "conectada" | A ligação "conectada‿o verão". | Se incomodar, gerar só a frase com vírgula ("conectada, o verão inteiro") e emendar (não aplicado; é frase do meio, veja o limite em `api-elevenlabs.md` §5.5). | vivido |
| Marca com a tônica errada (VÓL-tec) | Grafia normal no TTS. | `Voltéc` no texto do TTS + `scripts/stress.py`; "Voltec" na legenda. | vivido |
| CTA errado ("link na bio" num anúncio pago) | Roteiro de post orgânico. | Gerar só a frase nova e emendar (`api-elevenlabs.md` §5.5; registro da sessão em `prompts-moldes.md` §2.8). | vivido |

---

## 4. Moderação

- **Falhas não custam**: geração bloqueada volta com `failure_reason: "moderated"` e não é cobrada. Não reenvie o mesmo prompt; mude uma coisa por vez. A ordem sugerida pela pesquisa: adjetivos da roupa, depois um snapshot mais coberto, por último tirar "young" e "beach outfit".
- **Adulta explícita**: `an adult Brazilian woman, about 26 years old` (prompts finais). Nunca `girl`, `teen`, `young girl`, `cute`, `petite`. No Veo, imagem para vídeo só aceita adultos.
- **`fine wispy hairs`**, nunca `baby hairs` (3.4).
- **Roupa opaca e casual**, com o mesmo texto da âncora. Evite `sheer`, `see-through`, `lace bralette`, `low-cut`, `plunging`, `cleavage`, `bikini`, `swimsuit`, `tight`, `revealing`, `wet`. Ex.: Verão Conectado: a regata de gola redonda foi escolhida também por isso.
- **Sem descritor de corpo no vídeo** (`body`, `figure`, `curves`, `slim waist`, `legs`, `hips`, `chest`, `sweaty body`). Enquadre com `medium shot` e `from her lap up`, e diga `in her lap` em vez de "thigh". Textura de pele só no rosto.
- **Não escreva palavras sensíveis nem para negar** (`children`, `nudity`, `nsfw`, `sexy` no negativo). Descreva em positivo, como no Verão Conectado: `two tiny people stand far down the beach`, `there are no other people in the frame`.
- **Câmera respeitosa**: planos médios, nada de câmera baixa olhando o corpo, tilt percorrendo o corpo, `camera lingers on`, `posing`, `model pose`, `seductive`, `flirty`, `biting lip`.
- **Sem marcas nem terceiros** (categoria Third-party, códigos 35561574/35561575): use `smartphone` e `video call`, nunca `iPhone`, `WhatsApp`, `Instagram`, `FaceTime`, `Havaianas`.
- **Sem celebridades** (categoria Celebrity, códigos 29310472/15236754). Antes da sessão, a conta levou 1 bloqueio 15236754 num Veo Fast com essa persona. Se acontecer: mude o ângulo ou a expressão no snapshot, deixe o rosto maior no quadro e não repita o mesmo pedido.
- **Áudio também é moderado no Veo**: evite gemidos, suspiros longos e risinhos "flirty". Sob narração, nenhum som de boca (1.5).
- **Verbos neutros**: `film` e `record` em vez de "shoot". Nada de violência, nem figurada ("killer view", "dying for wifi").
- **Seedance/BytePlus**: filtro anti-deepfake nas imagens de entrada (mensagem típica: "The request failed because the input image may contain real person."). A identidade entra só pelo `start_frame`, nunca em `images`. Na API desta conta, os ByteDance dão 403 (`prompts-moldes.md` §2.7).
- **Prompts sempre em inglês.**
- **O que passou**: com os textos deste arquivo, os 14 snapshots e os 12 vídeos Veo da sessão foram concluídos (há um arquivo de saída para cada corpo em `bodies/`).
