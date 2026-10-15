# Locais reais: Grussaí (São João da Barra-RJ) e método para qualquer lugar

**Grussaí é o lugar pesquisado a fundo:** traços visuais, mapa, 12 fotos com licença, vento do verão e sol no verão (pesquisa) e nas outras estações (cálculo). O vento fora do verão não foi pesquisado. É o cenário do caso de referência, o Reels "Verão Conectado" (tarde de verão, ~17h). **O método das §7 a §9 vale para qualquer lugar:** achar fotos com licença e provar o local (§7), calcular o sol (§8) e pôr o lugar no prompt (§9). Atafona, Chapéu do Sol, o centro de São João da Barra, a loja da Voltec, casas e carro não foram pesquisados; o que checar em cada um está na §10.

Como ler:
- **[GRUSSAÍ]** = específico de Grussaí e região; **[GERAL]** = vale para qualquer anúncio com lugar real.
- Nível de evidência (o mesmo do `SKILL.md`): **[vivido]** aconteceu na sessão e foi conferido; **[aplicado]** veio da pesquisa ou das críticas e entrou nos takes aprovados; **[pesquisa]** só da pesquisa; **[não testado]** derivado das regras, nunca gerado.
- **não pesquisado: pesquise com `locais-grussai.md` §7–§9** = fato de lugar que ninguém conferiu. Não o escreva no prompt antes de pesquisar.
- **(Verão Conectado)** = valor da campanha de referência: exemplo testado, não padrão.

Preâmbulo de shell (o mesmo em toda a skill). Variáveis não passam de uma chamada do Bash para a outra, por isso os blocos abaixo o repetem:
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
```
O projeto de referência (`/home/syllas/hyperframes/voltec-reels-ia`, com as fotos em `locais/`) é só para leitura.

Fontes: pesquisa de locais de 15/10/2026 (fotos georreferenciadas + OpenStreetMap), críticas técnica e de realismo, prompts aprovados do Reels "Verão Conectado". Os números de sol do **verão** vêm da pesquisa. Os das **outras estações** foram calculados com o snippet da seção 8; não estavam na pesquisa.

---

## 1. [GRUSSAÍ] O essencial em 10 linhas

1. É **100% plana**: nenhum morro, serra, costão, pedra, ilha, píer ou prédio alto. O horizonte do mar é uma linha reta e vazia.
2. A praia olha para o **leste (~95°)**. O sol nasce no mar e se põe **atrás das casas e da restinga**. Em nenhuma época do ano existe pôr do sol no mar.
3. O mar é aberto e levemente turvo: oliva/cinza-esverdeado perto da arrebentação, azul-acinzentado ao longe, com várias linhas paralelas de espuma. **Nunca turquesa.**
4. A areia é dourada/mel e a faixa é muito larga e plana. Entre a avenida e a areia corre uma faixa de **restinga com casuarinas tortas pelo vento**.
5. As casas são baixas (1 a 2 pavimentos), de reboco pintado e telha cerâmica laranja. Os postes de concreto têm fiação aérea.
6. No verão, o **vento nordeste** é constante: cabelo, roupa e copas se mexem, e o vento bate no microfone do celular. Fora do verão, o vento não foi pesquisado.
7. À tarde, numa varanda de frente para o mar, o rosto fica em **sombra aberta** e o fundo ensolarado sai um pouco estourado.
8. Às **17h no verão a luz é quente e clara, não dourada** (sol a ~19,5°). Luz dourada de verdade só a partir de ~17h40. Nas outras estações, a mesma luz chega mais cedo (§3).
9. Nos prompts **não escreva "Avenida Atlântica", "RJ", "Brazil" nem "Grussaí"**: com "RJ", "Avenida Atlântica" puxa Copacabana. Descreva o lugar fisicamente.
10. Foto com licença **NC (não comercial)** serve só para você escrever o prompt. Ela nunca vai como imagem para a API nem aparece no vídeo.

---

## 2. [GRUSSAÍ] Como o lugar é (traços visuais reais)

| Elemento | Como é de verdade |
|---|---|
| Relevo | Planície costeira e restinga do delta do Paraíba do Sul, completamente plana. Do lado da terra só aparecem casas baixas, copas de casuarinas, amendoeiras e coqueiros, e a planície com brejos e lagoas até perder de vista. |
| Areia | Dourada a amarelo-mel, de grão médio a grosso, com grãos translúcidos de quartzo e pedacinhos brancos de concha. A seca é clara e fofa, cheia de pegadas e marcas de pneu. A molhada é marrom-acinzentada e espelhada. A faixa tem dezenas de metros de largura (passa de 100 m na maré baixa), é plana e tem declive suave. |
| Mar | Oceano aberto, sem recife, levemente turvo pelo sedimento do Paraíba do Sul. Oliva/cinza-esverdeado perto da arrebentação (mais amarronzado em Atafona) e azul-acinzentado/aço ao longe. Várias linhas paralelas de espuma branca, com ondas quebrando espalhadas. Nunca turquesa nem transparente. |
| Restinga | Faixa de 50 a 150 m sobre dunas baixas entre a avenida e a areia, cortada por trilhas de areia. Casuarinas (*Casuarina equisetifolia*) de tronco escuro e copa rala de "agulhas" verde-acinzentadas, todas tortas para o mesmo lado. No chão: capim de duna dourado/seco misturado a verde, tapetes de salsa-da-praia (*Ipomoea pes-caprae*, folhas carnudas bilobadas e flores lilás), algodão-de-seda (*Calotropis procera*), aroeira e cactos colunares (*Cereus fernambucensis*). Coqueiros esparsos e amendoeiras ficam perto das casas. Um roteiro do Sesc cita passarelas de madeira de acessibilidade até a areia em Grussaí e em Chapéu do Sol. |
| Casas da orla | Casas de veraneio de 1 a 2 pavimentos, de alvenaria rebocada pintada de branco, creme, salmão, rosa, amarelo ou vermelho, com telha cerâmica laranja (algumas têm laje). Muros baixos com portão, varandas, piscininhas, terrenos vagos com grama e fileiras de coqueiros. As ruas laterais são de areia branca-bege, sem asfalto. |
| Av. Atlântica (orla) | Asfalto de 2 faixas com calçada/ciclovia pintada em blocos alternados vermelho/laranja e azul. Postes de concreto com fiação aérea e postes de luz finos do lado do mar. |
| Calçadão e quiosques | Polo Gastronômico de Grussaí, a ~600 m da orla: pórtico de toras de eucalipto sem casca com placa de madeira escura, quiosques de telhado de 4 águas em telha cerâmica bege/terracota, mesas e cadeiras plásticas, guarda-sóis amarelos e vermelhos de marca de cerveja e piso de bloquete. Calçadão de pedra portuguesa em desenho de ondas (claro azulado com faixas escuras) e coqueiros curvados pelo vento. Um estudo do IFF cita ~10 quiosques na própria areia (não há foto aberta deles). |
| Céu (verão) | Azul profundo e saturado, com cúmulos ou altocúmulos esparsos. Sol duro e quente no meio do dia. |
| Gente | Mesmo no verão a praia é ampla e pouco adensada: pessoas pequenas e espalhadas, alguns guarda-sóis e cadeiras. |

**Arredores**
- **Atafona** fica ao norte, na foz do Paraíba do Sul. A areia é bege e o mar, cinza-oliva a amarronzado. É conhecida pela erosão (ruínas e árvores mortas na areia), o que tem conotação negativa: **não use como cenário de anúncio**. Serve como referência de cor do mar e de arrebentação para toda a costa de São João da Barra.
- A **lagoa** da foto do Commons é provavelmente o espelho d'água junto ao SESC Grussaí, não a Lagoa de Grussaí principal (~8 km). Tem água escura e parada, casuarinas, amendoeiras e uma mureta de treliça branca. Trocar praia por lagoa quebra a continuidade.
- **Chapéu do Sol**: não há foto aberta.
- O que checar antes de usar Atafona, Chapéu do Sol ou outro lugar da área como cenário: §10.

**Mapa (OSM, conferido na pesquisa)**, de norte para sul: Atafona (-21,62) → Chapéu do Sol (-21,66) → Grussaí (vila em -21,70; praia de -21,6875 a -21,71; ponto OSM "Praia de Grussaí" em -21,6948 / -41,0239) → Iquipari (-21,737). O SESC Grussaí fica em -21,689 / -41,037. O trecho das fotos georreferenciadas da orla (~-21,694 / -41,025) é o lugar usado no Verão Conectado.

**Denuncia que NÃO é Grussaí** (use como negativo ou como motivo para reprovar o snapshot): morro, serra, costão ou pedra; ilha no horizonte; prédios altos; água turquesa ou transparente; coqueiral de resort; areia branca "pó"; pôr do sol no mar; calçadão com prédios ao estilo Copacabana.

---

## 3. [GRUSSAÍ] Sol: geometria e horários

### Verão (pesquisa; verão 2026/27, horário de Brasília, sem horário de verão)

| Momento | Hora | Azimute / altura | Onde está o sol |
|---|---|---|---|
| Nascer | 04h58 a 05h45 | 95° a 115° | sobre o mar |
| 17h (meados de janeiro) | 17h00 | azimute ~254°, altura ~19,5° | atrás das casas: luz quente e clara, **ainda não dourada** |
| Começo do dourado de verdade | ~17h40 | sol abaixo de ~10° | baixo, atrás das casas |
| Pôr | 18h05 a 18h32 | 245° a 265° | sobre a terra, atrás das casas e da restinga |

Consequências práticas:
- **Nunca** escreva "sunset over the sea". Se quiser o sol no quadro, enquadre para a terra, com as casuarinas em contraluz (como na foto do fusca). O único sol sobre o mar é o **nascer**.
- À tarde, quem olha para o mar está de costas para o sol, então não há reflexo de sol na água. "Apertar os olhos com o brilho do mar" à tarde está errado.
- Ao entardecer, o céu sobre o mar fica azul-claro em tons pastel, às vezes com uma faixa rosada no horizonte leste.
- À tarde, a varanda de frente para o mar fica em **sombra aberta**: luz suave no rosto e fundo mais claro, como o HDR do celular faz.
- Em meados de janeiro, ao meio-dia, o sol fica quase a pino (calculado: ~89° em 15/01). A luz é dura e as sombras, curtas. É a luz da maioria das fotos de referência, então peça ao modelo para ignorá-la.

### Outras estações (calculado com o snippet da seção 8 para o ponto -21,695 / -41,025; confira se mudar de lugar)

| Dia (2027) | Nascer (azimute) | Sol a ~19,5° à tarde, a mesma altura do T1/T3 aprovados | Sol a ~10° (começo do dourado) | Pôr (azimute) | Altura máx. |
|---|---|---|---|---|---|
| 15/01 | 05h15 (113°) | 17h00 (254°) | 17h43 (251°) | 18h33 (247°) | ~89° |
| 15/04 | 05h57 (80°) | 16h02 (290°) | 16h45 (285°) | 17h32 (280°) | ~58° |
| 15/07 | 06h23 (67°) | 15h39 (304°) | 16h27 (298°) | 17h19 (293°) | ~47° |
| 15/10 | 05h13 (99°) | 16h20 (268°) | 17h01 (265°) | 17h48 (260°) | ~77° |

Na linha de 15/01, o cálculo bate com a pesquisa com ~1 min de diferença (arredondamento).

- O ano todo, o nascer fica sobre o mar (azimute de ~65° no inverno a ~116° no verão) e o pôr fica sobre a terra (~244° a ~295°). A regra "sem pôr do sol no mar" vale sempre.
- **Inverno:** o sol da tarde vem de oeste-noroeste (~293° a 304°). Para repetir o contraluz da selfie do T3, ela caminha para o **sul** e o mar fica à **direita** do quadro. No verão é o contrário: caminha para o norte, com o mar à esquerda.
- Para a mesma luz das "17h de verão" aprovadas, mire o sol a ~19,5° de altura: ~16h00 a 16h20 no outono e na primavera, ~15h40 no inverno.
- **O vento fora do verão não foi pesquisado.** Pesquise antes de fixar a direção do cabelo numa campanha de inverno.

---

## 4. [GRUSSAÍ] Vento (só o do verão foi pesquisado)

- No verão sopra **nordeste constante**. As fotos mostram isso: todas as casuarinas tortas para o mesmo lado e o coqueiro dobrado.
- Efeitos para pedir: cabelo e roupa leve esvoaçando, copas balançando, areia fina correndo rente ao chão e vento batendo no microfone do celular em "bumps" graves (vale incluir no prompt de áudio).
- Mantenha a intensidade coerente entre os takes: **brisa leve na varanda** (protegida pela casa e pelas casuarinas) e **vento constante com rajadas na areia aberta** ("steady, gusty wind on the open beach").
- Às 17h de verão, o sol (oeste-sudoeste) e o vento (nordeste) vêm de lados quase opostos. Se o rosto recebe sol de frente, o vento vem pelas costas e joga o cabelo na cara, que é justamente a anomalia a evitar. Por isso a selfie aprovada tem o sol atrás dela e o vento de frente.
- Na varanda, o vento vem do mar, por trás dela. Peça: *"a light breeze from behind her lifts a few strands at her shoulders, none across her face"*, com a maior parte do cabelo caída atrás dos ombros.
- Fora do verão: **não pesquisado: pesquise com `locais-grussai.md` §7–§9**. Ache direção e força na estação e na hora da cena, com fonte datada, antes de fixar a direção do cabelo. As árvores tortas das fotos mostram o vento dominante, não o do dia. A regra que vale sempre: o cabelo nunca cruza o rosto (sol e vento escolhidos juntos, como no verão).

---

## 5. [GRUSSAÍ] Receitas de cena aprovadas no verão (luz, câmera e vento)

**Exemplos testados no verão.** Tudo nesta seção é do Verão Conectado (tarde de verão, ~17h): 5.1, 5.2 e 5.5 saíram dos takes aprovados pelo cliente [vivido], 5.4 é a regra de continuidade que funcionou [aplicado], e 5.3 são alternativas da pesquisa [pesquisa]. Numa campanha nova, use como molde e refaça o que é da campanha:
- a luz: fora do verão, pela tabela "Outras estações" da seção 3 (inverno: sol a ~19,5° por volta de 15h40, vindo de ~304°; a selfie do T3 inverte de lado);
- o vento: fora do verão, pesquise antes de fixar a direção do cabelo (§4);
- a roupa: âncora da campanha (`persona-e-marca-voltec.md` §3.4); os blocos da 5.5 citam a saída de praia (`cover-up`);
- em outro lugar, a geometria e as fotos (§8 e §10).

### 5.1 Varanda do 2º andar de frente para o mar, ~17h no verão (T1 e T2 do Verão Conectado)
- **Casa:** sobrado simples de 2 andares, de frente para o mar. Parapeito de alvenaria branca de topo reto, que no plano do T1 aparece atrás dela na altura das costelas. Piso cerâmico bege. Rede de algodão off-white lisa e **sem franjas**, paralela ao parapeito, já "plantada" no T1 (só o tecido na borda de baixo do quadro) para o T2 acontecer nela.
- **Vista acima do parapeito:** copas de casuarinas tortas ao lado dos ombros dela, dunas baixas de capim seco amarelado, uma **faixa fina** de areia clara e uma **faixa fina** de mar cinza-azulado, com o horizonte reto passando logo abaixo dos ombros. A avenida fica escondida abaixo do parapeito.
- **Geometria:** do 2º andar, areia e mar ocupam só ~2° a 4° do quadro (60 a 90 px de 1920). Nunca peça "wide beach" a partir da varanda, senão o modelo inventa uma câmera alta ou põe a casa em cima da areia.
- **Câmera:** uma amiga a ~1,2 m, celular nivelado na altura do peito, câmera traseira (~26 mm eq.), apontada para o mar (leste). O quadro inteiro fica girado ~2°: parapeito e horizonte inclinam juntos.
- **Luz:** o sol baixo está atrás da casa, então varanda e rosto ficam em sombra aberta, com uma borda clara de céu no cabelo e nos ombros. Casuarinas, dunas, areia e mar recebem sol quente de fim de tarde, sob céu azul-claro com nuvenzinhas baixas sobre o mar. O celular expõe para o rosto, e o fundo sai um pouco estourado. *"Not golden-hour orange."*
- **T2 (rede):** mesma câmera, mesmo lugar e mesma direção. A amiga só dá um passo curto à frente e inclina o celular para baixo. Como a câmera fica mais alta que ela sentada, o topo do parapeito passa logo atrás da cabeça e o horizonte fica a ~1/3 do topo do quadro, que é o espaço do logo. Não abaixe a câmera até a altura dela sentada: com a câmera nessa altura, o horizonte cai no topo do parapeito e a praia some atrás da parede.

### 5.2 Selfie andando na areia, ~17h no verão (T3)
- Ela caminha devagar para o **norte**, na areia firme e úmida em frente à mesma quadra. A câmera frontal (~24 mm eq.) está no braço direito esticado, que entra pelo canto inferior esquerdo. A câmera olha para o sul.
- **Quadro:** o mar fica à **esquerda** (oliva-acinzentado perto, cinza-azulado longe, várias linhas de espuma, horizonte reto). À **direita**, dunas baixas de capim amarelado e uma fila de casuarinas tortas, com alguns telhados terracota quase escondidos. A praia se perde ao fundo. Duas pessoas minúsculas **paradas** ("stand") longe, perto da água; figuras andando tendem a derreter.
- **Luz:** o sol baixo fica atrás dela, à direita do quadro e fora dele. Ele faz uma borda quente na bochecha esquerda, no ombro e no cabelo. O resto do rosto fica em sombra aberta rebatida pela areia clara. As casuarinas ficam em contraluz parcial. O céu é azul-claro, mais claro e um pouco estourado à direita, com leve névoa sobre o mar. Sem disco solar e sem flare.
- **Vento:** de frente para ela. Joga o cabelo para trás, sobre o ombro esquerdo (direita do quadro), e as bordas da saída de praia tremulam.
- **Olhar:** para a própria imagem na tela, com os olhos um pouco abaixo da lente.

### 5.3 Alternativas [pesquisa] (vindas da pesquisa; não geradas na sessão)
- **Selfie de frente para a terra, com sol no rosto:** rosto dourado e mar pastel atrás. Risco: no verão, o vento nordeste vem pelas costas e joga o cabelo no rosto.
- **Luz dourada de verdade:** mude a hora para ~17h50 em **todos** os takes (sombras mais longas, céu sobre o mar mais pálido). Nunca mude a hora de um take só.
- **Nascer do sol sobre o mar:** 04h58 a 05h45 no verão. É o único "sol no mar" coerente.
- **Tarde nublada clara:** luz difusa e sombras suaves. É mais gentil com a pele e mais segura para a continuidade.
- **Quiosque ou calçadão:** serve como B-roll, mas fica a ~600 m da orla (quebra o "um lugar só") e as fotos de referência são NC e cheias de texto e marcas. Peça "no readable signs, text or logos".
- **Lagoa:** só como cenário alternativo calmo. Não mistura com praia no mesmo Reels.

### 5.4 Continuidade (o que evitou "troca brusca de ambiente")
- **Um lugar e uma tarde:** a mesma quadra, com a mesma hora, o mesmo céu, o mesmo vento e a mesma roupa em todos os takes. T1 e T2 se passam na mesma varanda; o T3 se passa na areia logo em frente.
- O snapshot do take seguinte no mesmo lugar é uma **edição** do snapshot aprovado, que muda só a pose e um reenquadramento pequeno.
- Da varanda para a areia, use um corte motivado (olhar com olhar) ou gere um take de transição. Nunca escreva "cut to" dentro de um prompt.

### 5.5 Blocos prontos para prompt (inglês, sem nome de lugar, tirados dos prompts aprovados)

Ex.: Verão Conectado [vivido]. Os blocos trazem `about 5 pm in summer`, o vento de verão e a saída de praia (`cover-up`): numa campanha nova, troque hora, estação, vento e roupa e mantenha a estrutura.

Fundo da varanda (snapshot T1):
```text
Location: the shaded upstairs balcony of a simple two-story beach house facing the sea, in a quiet, flat beach town of low houses. [...] Behind it, a white-painted masonry balcony wall with a flat top, which appears behind her at about the height of her lower ribs. Beyond the wall, seen from upstairs (the coastal road is hidden below the wall): scattered wind-bent casuarina trees whose crowns rise against the sky beside her shoulders, low dunes with dry yellowish grass, a thin band of pale sand and a thin band of flat gray-blue sea, with the straight, empty horizon passing just below her shoulders. Flat coastal land only: no hills, rocks, islands, high-rise buildings, poles, cars or signs.
```

Luz da varanda:
```text
Light: about 5 pm in summer. The sun is low behind the house, so the balcony and her face are in soft, even open shade, with a faint bright edge of skylight on her hair and shoulders. The casuarinas, dunes, sand and sea beyond the wall are in warm late-afternoon sunlight under a clear pale-blue sky with a few small white clouds low over the sea. Not golden-hour orange. The phone exposes for her face, so the sunlit background is slightly overexposed.
```

Cena da areia (snapshot T3):
```text
Scene, about 5 pm in summer: she walks slowly along the firm, damp sand of a very wide, flat beach. Behind her the beach recedes far into the distance. On the left side of the frame, the sea: olive-gray near the shore and gray-blue farther out, with several parallel lines of white surf and a straight, empty horizon. On the right side, low dunes with dry yellowish grass and a line of wind-bent casuarinas, with a few terracotta roofs barely visible behind them. Two tiny people stand far down the beach near the water. Flat coastline only: no hills, rocks, islands, piers, kiosks, umbrellas or high-rise buildings.
```

Luz e vento da areia:
```text
The steady sea breeze blows from in front of her, sweeping her hair back off her face over her left shoulder (frame right), a few loose strands lifting; the front edges of the cover-up flutter slightly.
Light: warm late-afternoon sun, low behind her and off to the right of the frame (the sun itself is out of frame). It puts a warm bright edge of light on her left cheek, her shoulder and her windblown hair, while the rest of her face is in soft open shade lifted by light bouncing off the pale sand, with catchlights from the bright sky in her eyes. The casuarinas on the right are partly backlit; the sky is clear pale blue, brighter and slightly clipped toward the right, a little hazy over the sea. Not golden-hour orange.
```

Papel da foto real do local, quando ela vai como imagem de referência:
```text
Image 2 is a real photo of the coastal restinga where this scene takes place: use it only for the shape of the wind-bent casuarina trees with wispy gray-green needles, the dry yellowish dune grass, the flat gray-blue sea and the perfectly straight, empty horizon; ignore its midday light and deep-blue sky.
```

Linha de ambiente no prompt de vídeo (só o que já está no snapshot):
```text
The white wall, the hammock, the casuarinas and the sea horizon stay exactly as in the first frame
The surf on the left, the dunes and casuarinas on the right and the straight, empty horizon stay exactly as in the first frame
```

Trechos de lugar do `negative_prompt` do Veo:
```text
warped background, melting walls, bending horizon, mountains, hills, rocky coast, islands, high-rise buildings, turquoise water, palm-lined resort, sunset over the sea, golden-hour orange glow
```
No T3, acrescente `sun disk in frame`. Não ponha `cars` no negativo se o áudio pedir carro passando: o Veo gera imagem e som juntos, e o negativo pode suprimir o som.

---

## 6. [GRUSSAÍ] Fotos reais com licença

As 12 fotos estão em `/home/syllas/hyperframes/voltec-reels-ia/locais/`. Os créditos completos estão em `/home/syllas/hyperframes/voltec-reels-ia/locais/creditos.json` (página, URL da imagem, data, coordenadas, como o local foi verificado e observações). Todas tiveram o local confirmado pela página de origem.

| # | Arquivo | O que mostra | Autor | Licença | Uso comercial | Para que serve |
|---|---|---|---|---|---|---|
| 1 | `grussai_orla_aerea_av_atlantica_01.jpg` | Drone ao longo da Av. Atlântica: casas, ciclovia colorida, casuarinas, praia e mar (jul/2022) | EBN DIGI (frame de vídeo do YouTube) | CC0 1.0 (conforme o Commons) | sim | Mapa e layout da orla. Não serve como ângulo de câmera. Por segurança, credite EBN DIGI |
| 2 | `grussai_orla_av_atlantica_casas_restinga_01.jpg` | Da restinga olhando para a terra: algodão-de-seda, avenida, casas de veraneio (dez/2023) | Gabriel Jovêncio Ribeiro (iNaturalist) | CC BY 4.0 | sim, com crédito | Padrão das casas, postes e fiação da orla |
| 3 | `grussai_orla_casuarinas_praia_01.jpg` | Casuarinas inclinadas (uma quebrada) contra o céu, praia ao fundo; vertical (dez/2023) | Gabriel Jovêncio Ribeiro (iNaturalist) | CC BY 4.0 | sim, com crédito | Forma das casuarinas. Tem uma plaquinha branca no canto, que pode virar texto: evite como imagem de entrada |
| 4 | `grussai_restinga_casuarinas_horizonte_mar_01.jpg` | Três casuarinas tortas, duna de capim seco, horizonte reto do mar (out/2025) | Pablo Cauã da Silva Toledo (iNaturalist) | CC BY 4.0 | sim, com crédito | **A referência de local dos snapshots aprovados.** Já está na conta como asset `Mf1kechhOOoqJO70sPNd` ("restinga" em `/home/syllas/hyperframes/voltec-reels-ia/bodies/assets.json`; conferido em 15/10/2026 que é esta foto) |
| 5 | `grussai_casuarina_dunas_fim_de_tarde_01.jpg` | Casuarina sobre duna, luz dourada rasante, praia larga, fusca azul (jan/2014) | Gil Alves (Unsplash) | CC0 1.0 (Unsplash pré-2017, conforme o Commons) | sim | Composição e contraluz de fim de tarde. Tem filtro forte: não use a cor |
| 6 | `grussai_praia_faixa_areia_ampla_01.jpg` | Faixa de areia larguíssima, mar como uma linha, banhistas minúsculos (fev/2012, 16h45) | Julio César Mulatinho (Flickr) | CC BY-NC 2.0 | **NÃO** | Só referência interna da escala da praia. A areia sai alaranjada (iPhone 4) e há crianças identificáveis |
| 7 | `grussai_polo_gastronomico_quiosques_01.jpg` | Pórtico de eucalipto, quiosques, guarda-sóis (jan/2014, 17h51) | Julio César Mulatinho (Flickr) | CC BY-NC 2.0 | **NÃO** | Só referência interna de quiosque. Tem placa, marcas de cerveja e placas de carro legíveis |
| 8 | `grussai_calcadao_pedra_portuguesa_noite_01.jpg` | Calçadão em ondas, coqueiro e lua (mar/2008, noite, tremida) | Aline** (Flickr) | CC BY-NC 2.0 | **NÃO** | Só o padrão do calçadão, como referência interna |
| 9 | `grussai_lagoa_01.jpg` | Lagoa escura e parada, casuarinas, amendoeiras, céu nublado (jan/2009) | Andrevruas (Wikimedia Commons) | CC BY 3.0 (dupla com GFDL) | sim, com crédito | Vegetação ou cenário calmo. É provavelmente o lago do SESC, não a lagoa principal |
| 10 | `grussai_restinga_salsa_da_praia_duna_01.jpg` | Tapete de salsa-da-praia com flores lilás sobre a duna (dez/2023) | Gabriel Jovêncio Ribeiro (iNaturalist) | CC BY 4.0 | sim, com crédito | Chão e primeiro plano |
| 11 | `grussai_areia_textura_macro_01.jpg` | Macro da areia: grãos dourados, quartzo e conchas (jan/2025) | Pablo Cauã da Silva Toledo (iNaturalist) | CC BY 4.0 | sim, com crédito | Textura e cor da areia para closes (pés, pegadas) |
| 12 | `atafona_praia_ondas_01.jpg` | Atafona: arrebentação e mar cinza-oliva (dez/2006, 10h21) | carminha (Flickr) | CC BY-NC-SA 2.0 | **NÃO** | Só referência interna da cor do mar. Tem carimbo de data laranja e só 1024x768 |

**Regras de uso na geração**
- Como imagem de entrada para a API, só entram fotos de uso comercial (CC0 ou CC BY). Prefira a nº 4. Depois vêm a 2, a 10, a 11 e a 3 (esta com cuidado por causa da plaquinha). A nº 1 serve só para layout.
- Use **no máximo 1 a 2 fotos de local por snapshot**, cada uma com papel explícito no prompt (bloco da seção 5.5). Os snapshots aprovados usaram só a nº 4.
- Quase todas são de meio-dia, então escreva sempre *"ignore its midday light and deep-blue sky"*.
- Suba a foto uma vez como asset e reaproveite o `asset_id`. O upload não gasta crédito:
  ```bash
  export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
  export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
  export HF="$PROJ/reels-final" QA="$PROJ/qa"
  export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
  python3 -I "$SKILL/scripts/el.py" upload /home/syllas/hyperframes/voltec-reels-ia/locais/grussai_areia_textura_macro_01.jpg
  ```
  Anote o id em `bodies/assets.json` do projeto. Detalhes da API em `references/api-elevenlabs.md`.
- **CC BY:** crédito ao autor. A sugestão do plano é pôr o crédito na legenda do post, se o cliente aprovar. **CC BY-SA:** derivados vão sob a mesma licença. **NC:** nunca vai para a API (nem como imagem de referência) e nunca aparece no vídeo; serve só para você olhar e escrever o prompt.

Créditos prontos (das fotos de uso comercial):
```text
Fotos de referência de Grussaí: Pablo Cauã da Silva Toledo e Gabriel Jovêncio Ribeiro (iNaturalist, CC BY 4.0); Andrevruas (Wikimedia Commons, CC BY 3.0); EBN DIGI e Gil Alves (CC0).
```
Use só os nomes das fotos que de fato entraram na geração. No Verão Conectado foi só a de Pablo Cauã da Silva Toledo (iNaturalist, CC BY 4.0).

---

## 7. [GERAL] Achar mais fotos com licença aberta e provar o local

**Onde procurar** (o que rendeu em Grussaí)
1. **Fotos do próprio cliente (a melhor fonte):** a equipe fotografa ou filma no celular os pontos reais. O direito de uso é garantido e a luz e o ângulo são reais. Peça sem pessoas identificáveis e sem placas legíveis. Faltou foto aberta de varanda de casa de praia, de Chapéu do Sol, da Lagoa de Grussaí principal e dos quiosques da areia: **para essas cenas, e para toda cena interna (casa, loja, carro; §10), peça ao cliente**.
2. **iNaturalist:** observações de plantas e bichos com paisagem ao fundo, georreferenciadas. Rendeu 5 das 8 fotos de uso comercial. A licença é **por foto** (página `https://www.inaturalist.org/photos/<id>`). O original fica em `https://inaturalist-open-data.s3.amazonaws.com/photos/<id>/original.jpg` (às vezes `.jpeg`).
3. **Wikimedia Commons:** procure pela categoria do lugar (aqui, "Grussaí"), pela descrição e pelo GPS no EXIF. Às vezes o `upload.wikimedia.org` devolve 429 (limite de requisições). Na sessão, o contorno foi baixar as miniaturas de tamanho padrão primeiro e os originais depois.
4. **Flickr com filtro Creative Commons:** confira geotag e título. Muitas fotos são NC, ou seja, só referência interna.
5. **Unsplash:** só tinha a foto do fusca, que já estava no Commons como CC0 por ser anterior a 2017.
6. Procure com as grafias variantes: "Grussaí", "Grussai" e "Gruçaí" (a foto do fusca tinha o título "Gruçaí, São João da Barra").
7. O site da Prefeitura (sjb.rj.gov.br) é uma SPA e não informa licença de uso, por isso **não foi usado**.

Para Grussaí, Commons, Flickr CC e iNaturalist foram esgotados em 15/10/2026. Foto nova virá do cliente ou de uploads posteriores a essa data.

**Checklist para aceitar uma foto**
- [ ] A licença foi lida **na página da foto** (não na do autor nem na do site). Anote em `creditos.json`: arquivo, página, URL da imagem, autor, licença, data, coordenadas, como verificou e observações.
- [ ] O local foi provado por pelo menos um destes: observação georreferenciada com precisão em metros e `place_guess` do lugar (iNaturalist; as de Grussaí tinham precisão de 2 a 18 m); geotag do Flickr; GPS no EXIF; título ou categoria inequívocos.
- [ ] As coordenadas batem com o mapa. Na pesquisa, a conferência foi feita no OpenStreetMap, por exemplo com `https://nominatim.openstreetmap.org/search?q=Praia+de+Grussai,+Sao+Joao+da+Barra&format=json`.
- [ ] A paisagem bate com o lugar (em Grussaí: plano, sem morro). Desconfie de homônimos. Foram descartadas uma "Atafona" do Flickr que era um moinho de pedra e uma foto com placa "altitude 941 m".
- [ ] Sem pessoas identificáveis em primeiro plano, sem texto legível (placa, marca, placa de carro) e sem carimbo de data. Se tiver, use só como referência interna ou recorte.
- [ ] Filtro forte ou saturação de celular antigo foram anotados ("usar para composição, não para cor").
- [ ] A imagem abre (`PIL verify`) e tem resolução útil (as de Grussaí têm de 1024 a 3264 px no lado maior; prefira mais de 1500 px).
- [ ] Sabe-se para que a foto serve: imagem de entrada da API (só CC0/CC BY) ou só referência para escrever o prompt (NC).

**Mostrar ao cliente** (exigência: o cliente vê as fotos reais antes dos snapshots)
Faça uma folha de contato com a cor da licença e ponha as fotos com créditos na página de aprovação:
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$QA" && cd "$PROJ"
python3 -I - <<'EOF'
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps
pasta = "/home/syllas/hyperframes/voltec-reels-ia/locais/"   # só leitura; num projeto novo, "locais/" (a pasta com as fotos e o creditos.json)
fotos = json.load(open(pasta + "creditos.json"))["fotos"]    # mesmo formato do creditos.json da Voltec
W, H, COLS = 420, 420, 4
rows = (len(fotos) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * W, rows * (H + 60)), "white")
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 15)
except OSError:
    font = ImageFont.load_default()
dr = ImageDraw.Draw(sheet)
for i, f in enumerate(fotos):
    x, y = (i % COLS) * W, (i // COLS) * (H + 60)
    sheet.paste(ImageOps.fit(Image.open(pasta + f["arquivo"]).convert("RGB"), (W - 10, H - 10)), (x + 5, y + 5))
    ok = not f["uso_comercial"].upper().startswith("NÃO")
    dr.rectangle([x + 5, y + H - 5, x + W - 5, y + H + 55], fill=(30, 140, 60) if ok else (200, 40, 40))
    dr.text((x + 10, y + H), f"{i + 1}. {f['arquivo'][:44]}", fill="white", font=font)
    dr.text((x + 10, y + H + 20), f"{f['licenca'][:24]} | {'comercial OK' if ok else 'NC: só referência'}", fill="white", font=font)
sheet.save("qa/folha_contato_locais.jpg", quality=85)   # rode a partir de $PROJ; nunca grave na pasta de referência
EOF
```
(Verde: pode ir para a API. Vermelho: NC, só referência.)

---

## 8. [GERAL] Calcular o sol para qualquer lugar e data

São as fórmulas da NOAA, em Python puro, sem numpy. Conferido contra a pesquisa: 15/01/2027 às 17h em Grussaí dá altura 19,5° e azimute 254°. O azimute é contado a partir do norte, no sentido horário (90° = leste, 270° = oeste). Use antes de escrever a luz de qualquer cena.

```bash
python3 - <<'EOF'
import math
from datetime import datetime, timedelta, timezone

def sol(lat, lon, quando):
    """Altura e azimute do sol em graus (azimute a partir do norte, sentido horário). Fórmulas NOAA, sem refração."""
    u = quando.astimezone(timezone.utc)
    t = (u.timestamp() / 86400 + 2440587.5 - 2451545) / 36525
    r = math.radians
    l0 = (280.46646 + t * (36000.76983 + 0.0003032 * t)) % 360
    m = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    c = (math.sin(r(m)) * (1.914602 - t * (0.004817 + 0.000014 * t))
         + math.sin(r(2 * m)) * (0.019993 - 0.000101 * t) + math.sin(r(3 * m)) * 0.000289)
    om = 125.04 - 1934.136 * t
    lam = l0 + c - 0.00569 - 0.00478 * math.sin(r(om))
    eps = 23 + (26 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60) / 60 + 0.00256 * math.cos(r(om))
    dec = math.asin(math.sin(r(eps)) * math.sin(r(lam)))
    y = math.tan(r(eps / 2)) ** 2
    eqt = 4 * math.degrees(y * math.sin(2 * r(l0)) - 2 * e * math.sin(r(m))
                           + 4 * e * y * math.sin(r(m)) * math.cos(2 * r(l0))
                           - 0.5 * y * y * math.sin(4 * r(l0)) - 1.25 * e * e * math.sin(2 * r(m)))
    ha = r(((u.hour * 60 + u.minute + u.second / 60 + eqt + 4 * lon) % 1440) / 4 - 180)
    la = r(lat)
    alt = math.degrees(math.asin(math.sin(la) * math.sin(dec) + math.cos(la) * math.cos(dec) * math.cos(ha)))
    az = (math.degrees(math.atan2(math.sin(ha), math.cos(ha) * math.sin(la) - math.tan(dec) * math.cos(la))) + 180) % 360
    return alt, az

def cruzamentos(lat, lon, dia, fuso=-3, alturas=(-0.833, 10, 19.5)):
    """Minuto em que o sol cruza cada altura (-0.833 = nascer/pôr), com o azimute."""
    t0 = datetime(dia.year, dia.month, dia.day, tzinfo=timezone(timedelta(hours=fuso)))
    out, ant = [], None
    for i in range(24 * 60):
        t = t0 + timedelta(minutes=i)
        alt, az = sol(lat, lon, t)
        if ant is not None:
            out += [(t.strftime("%H:%M"), h, round(az)) for h in alturas if (ant < h) != (alt < h)]
        ant = alt
    return out

LAT, LON = -21.695, -41.025                      # orla de Grussaí (Av. Atlântica); em outro lugar, a coordenada dele (OSM, §7)
BRT = timezone(timedelta(hours=-3))
print("15/01/2027 17h00 -> altura %.1f°, azimute %.0f°" % sol(LAT, LON, datetime(2027, 1, 15, 17, 0, tzinfo=BRT)))
for hora, h, az in cruzamentos(LAT, LON, datetime(2027, 7, 15)):
    print(hora, "nascer/pôr" if h < 0 else f"sol a {h}°", f"azimute {az}°")
EOF
```
Como ler o resultado na cena:
1. Ache a direção para onde a praia, a fachada ou a janela olha. Em Grussaí, ~95°.
2. Se a diferença entre o azimute do sol e a direção da fachada passar de 90°, a fachada está na sombra: rosto em sombra aberta e fundo iluminado. Em Grussaí, à tarde, a diferença fica em ~160° (sol a ~254°, fachada a ~95°).
3. Escolha a direção da câmera e da caminhada para o sol ficar atrás da pessoa (contraluz) ou de lado. O vento não pode jogar o cabelo no rosto.
4. Escreva a altura como qualidade de luz: ~19° dá luz quente e clara; abaixo de ~10°, dourada. O prompt só pede "golden" se a hora for dourada.
5. Cena interna [não testado]: a janela faz o papel da fachada. Se a diferença do passo 2 passar de 90°, não entra sol direto pela janela, e a luz dela é de céu, suave.

---

## 9. [GERAL] Lugar real dentro do prompt: regras que valeram

1. **Não nomeie o lugar.** Nome famoso ou homônimo puxa outro lugar ("Avenida Atlântica" com "RJ" vira Copacabana), e o modelo não sabe como é um lugar pequeno. Quem garante a fidelidade são a foto e a descrição física. O nome fica nos documentos internos e na legenda do post.
2. **A foto do local entra com papel explícito:** "use it only for the shape of …; ignore its midday light and deep-blue sky". A foto de referência quase nunca tem a luz da cena.
3. **O horizonte fica na altura da câmera.** Do 2º andar, areia e mar viram uma faixa fina. Com a câmera baixa, o parapeito esconde a praia. Descreva só o que aquela câmera veria de verdade.
4. **Incline o quadro inteiro**, nunca só o horizonte: *"the whole frame is rolled about 2 degrees, so the top of the wall and the horizon tilt together and stay parallel"*.
5. **Um lugar e uma hora por Reels.** O snapshot seguinte é uma edição do aprovado. Os cortes são motivados.
6. **Escolha 3 a 5 elementos fixos do fundo** e repita-os com as mesmas palavras em todos os prompts do mesmo lugar. No prompt de vídeo, cite só o que está no snapshot, seguido de *"stay exactly as in the first frame"*. O que está no texto mas não no quadro tende a aparecer no meio do clipe, com morph.
7. **Luz e vento fisicamente coerentes** com a hora e a direção (seção 8). Escreva *"Not golden-hour orange"* quando a hora não for dourada. A luz fica igual no clipe inteiro: sem nuvem passando e sem mudar a hora.
8. **A exposição só muda** se algo grande e claro entrar ou sair do quadro. Pedir "auto-exposure shifts" sem motivo vira flicker.
9. **Nenhum texto no cenário:** placas, fachadas, camisetas, números de casa. Tire já no snapshot.
10. **Gente ao fundo:** ninguém, ou 1 a 2 adultos pequenos, longe e parados. Descreva em positivo ("the beach is nearly empty") em vez de negar.

---

## 10. [GERAL] Outros lugares da área atendida e cenários internos (não pesquisados)

Nenhum destes lugares foi pesquisado a fundo nem gerado. O que já se sabe vem com a fonte; o resto é **não pesquisado: pesquise com `locais-grussai.md` §7–§9** antes de escrever o prompt. Mostre as fotos ao cliente antes dos snapshots (folha de contato da §7), faça o A/B do snapshot e avise no portão 3 que a cena é nova [não testado]. Como pôr a personagem nesses cenários sem texto, e a luz de cena interna: `persona-e-marca-voltec.md` §10.

### 10.1 O que checar em qualquer lugar novo
1. **Fotos com licença:** primeiro as do cliente (§7, item 1). Foto aberta, só com a licença lida na página da foto. CC0 e CC BY podem ir para a API; NC serve só para escrever o prompt.
2. **Local provado:** geotag, GPS no EXIF ou observação georreferenciada, conferidos no OpenStreetMap (checklist da §7).
3. **Sol:** a direção para onde olham a praia, a rua, a fachada ou a janela, e o sol da data e da hora pelo snippet da §8, com a coordenada do lugar. Não reaproveite os números de Grussaí.
4. **Vento:** direção e força na estação e na hora, com fonte datada. Só o de Grussaí no verão foi pesquisado (§4).
5. **Texto que vaza:** letreiros, fachadas, placas de rua e de carro, números de casa, cartazes, telas, embalagens e camisetas. Enquadre para fora deles já no snapshot (§9, regra 9).
6. **Gente:** ninguém, ou 1 a 2 adultos pequenos, longe e parados (§9, regra 10).
7. **Som:** o que se ouve ali de verdade, para o prompt de vídeo e a cama de SFX.

### 10.2 Lugar por lugar

Em cada lugar valem todos os itens da 10.1 (fotos, local provado, sol, vento, texto, gente e som); a última coluna diz o que é próprio dele.

| Lugar | O que já se sabe (fonte) | O que pesquisar e checar, além da 10.1 |
|---|---|---|
| Atafona | Fica ao norte, na foz do Paraíba do Sul (~-21,62 no OSM). Areia bege e mar cinza-oliva a amarronzado (foto nº 12, NC). É conhecida pela erosão, com ruínas e árvores mortas na areia, e a pesquisa recomendou não usá-la como cenário de anúncio (§2) | Se o cliente quiser mesmo assim: um trecho sem ruína no quadro e fotos de uso comercial (a única achada é NC). Direção da praia, sol, vento e placas: **não pesquisado: pesquise com `locais-grussai.md` §7–§9** |
| Chapéu do Sol | Fica entre Atafona e Grussaí (~-21,66 no OSM). Um roteiro do Sesc cita passarelas de madeira de acessibilidade até a areia. Não há foto aberta (§2) | Fotos do cliente, direção da praia, sol, vento, placas e letreiros: **não pesquisado: pesquise com `locais-grussai.md` §7–§9** |
| Centro de São João da Barra | Nada: a pesquisa não tem foto nem coordenada | Fotos com licença e local provado, direção da rua ou da fachada, sol, vento, fachadas, letreiros, placas de rua e de carro, trânsito: **não pesquisado: pesquise com `locais-grussai.md` §7–§9** |
| Loja da Voltec | Só as refs da persona, com letreiro VOLTEC luminoso numa parede ripada e balcão com notebook. Parte das refs é imagem gerada (`persona-e-marca-voltec.md` §10.2): elas não provam como é a loja real | Fotos da loja real feitas pelo cliente, sem clientes identificáveis; janelas e vidros (sol pela §8 e reflexo); luz interna; o que vaza texto: letreiro, fachada, cartazes de preço, telas, notebook com marca, uniforme com logo: **não pesquisado: pesquise com `locais-grussai.md` §7–§9** |
| Casas (interior) | Só o exterior das casas da orla de Grussaí foi pesquisado (§2) | Fotos do cliente; lado da janela e sol (§8, passo 5); TV e telas, quadros com letras, embalagens, roteador com marca, espelhos: **não pesquisado: pesquise com `locais-grussai.md` §7–§9** |
| Carro | Só a ref da persona no banco da frente, uma imagem gerada (`persona-e-marca-voltec.md` §10.2) | Carro parado; emblema do volante, painel, placas de outros carros, retrovisor e vidros (reflexo); o que se vê pelas janelas; o sol pela direção do carro (§8): **não pesquisado: pesquise com `locais-grussai.md` §7–§9** |

- **Grussaí fora do verão:** o sol está calculado (§3, "Outras estações"). Vento, céu e movimento da praia fora do verão: **não pesquisado: pesquise com `locais-grussai.md` §7–§9**.
