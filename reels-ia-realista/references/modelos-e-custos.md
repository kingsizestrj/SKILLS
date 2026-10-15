# Modelos de vídeo e imagem e custos (ElevenLabs)

Base: pesquisa e produção do Reels "Verão Conectado" da Voltec, o caso de referência testado, em **15/10/2026**. Os rankings foram consultados nesse dia: Artificial Analysis (AA, refresh de set/2026) e LMArena (snapshot de 22/09/2026). Ranking e catálogo de modelos mudam rápido. Se esta página tiver mais de uns 2 meses, consulte de novo antes de recomendar um modelo ao cliente.

Os custos por unidade valem para qualquer vídeo. Os totais são de um vídeo de ~20 s com 3 takes, como o do exemplo. Para outro roteiro, use a conta por take do §6.

- **[Voltec]**: vale para a conta da Voltec, em qualquer campanha.
- **ex.: Verão Conectado**: número ou valor só da campanha de referência.
- O resto vale para qualquer anúncio com IA.

Relacionados: `api-elevenlabs.md` (corpos e chamadas), `prompts-principios.md` (como escrever os prompts), `prompts-moldes.md` (moldes completos), `qa-checklist.md` (revisão dos takes).

## Resumo

| Decisão | Escolha | Por quê |
|---|---|---|
| Vídeo, padrão (tudo pela API) | `veo-3.1-generate-001`, 9:16, 1080p, 8 s, com áudio, image-to-video a partir do snapshot aprovado, **2 variações por take** | É o melhor modelo de vídeo liberado na API da conta e entregou o Reels (12 gerações). 19.391 créditos por take (medido). |
| Vídeo, máximo realismo | Seedance 2.5 (`bytedance-seedance-v2.5`) | Fica no topo dos rankings, bem à frente do Veo. **[Voltec]** Na API devolve 403 `model_access_denied`, então só roda no app web (manual) e corre risco com o filtro de rosto. |
| Imagem com a personagem (snapshot) | `gpt-image-2.5-sunburst`, 9:16, 2K, `quality: "high"` | Manteve a identidade e seguiu o prompt (~554 créditos). O `gemini-3-pro-image` afinou o rosto e trocou a roupa. |
| Orçamento | Por rodada: 38.782 por take (2 variações Veo) + ~5 a 7 mil de imagens, narração e SFX. Ex.: Verão Conectado, ~20 s com 3 takes: ≈125 mil por rodada, com reserva para mais uma | O vídeo é ~92% do custo. A produção real do Verão Conectado, com uma rodada de refação, fechou em ≈253 mil. |

---

## 1. Vídeo: ranking e evidências

### 1.1 Placar geral (Elo de votos cegos; maior é melhor)

| Modelo (`model_id`) | AA imagem→vídeo, com áudio | AA texto→vídeo, com áudio | LMArena imagem→vídeo (22/09/2026) | Onde roda |
|---|---|---|---|---|
| Seedance 2.5 (`bytedance-seedance-v2.5`) | 1139 ±17 (#2–4) | 1160 ±15 (#3 de 28) | 1477 (#3) | API só com liberação da ByteDance; app |
| Seedance 2.0 (`bytedance-seedance-v2`) | 1121 ±18 | 1136 (#7) | 1475 | API só com liberação; app |
| MiniMax H3 | 1141 (#1) | – | – | só no app (nativo em 768p) |
| Gemini Omni Flash 1.1 | 1134 | – | – | só no app |
| Veo 3.1 (`veo-3.1-generate-001`) | 1031 ±17 (#11–15) | 967 ±18 (#19) | 1398 (#10) | API liberada |
| Veo 3.1 Fast (`veo-3.1-fast-generate-001`) | 1017 ±16 | 965 | 1385 | API liberada |

Como ler a tabela:
- A vantagem do Seedance sobre o Veo é robusta: cerca de 65% de preferência em imagem→vídeo (o fluxo que usamos, a partir do snapshot) e de 75 a 86% nas categorias de texto→vídeo.
- Seedance 2.5 e 2.0 estão em empate técnico (a diferença cabe no intervalo de confiança). Veo 3.1 e Fast estão em empate estatístico.
- MiniMax H3 e Omni Flash 1.1 empatam com o Seedance 2.5 em imagem→vídeo, mas só existem no app.
- Os blogs pró-Veo para UGC (ex.: ugccopilot, "For most UGC, Veo") são de fornecedores e comparam com o Seedance 2.0, não com o 2.5.

### 1.2 Categorias que mais pesam num Reels realista

As categorias são do board texto→vídeo do AA. O board imagem→vídeo não tem categorias.

| Categoria | Seedance 2.5 | Seedance 2.0 | Omni Flash 1.1 | Veo 3.1 |
|---|---|---|---|---|
| Human Anatomy | 1182 (#1) | 1154 (#3) | 1096 | 900 (#20) |
| Social Media & Creator | 1186 | – | 1090 | 926 |
| Camera Control | 1119 | 1089 | 1072 | 934 (#24) |
| Spatio-Temporal Consistency | 1140 | 1093 | 1088 | 990 |
| Live-Action Film | 1099 | – | 1051 | 820 (#25) |
| Audio Synchronization | 1118 | 1152 (#3) | 1175 | 996 |
| Dialogue & Lip Sync | 1203 (#1) | – | – | 893 |

O Veo Fast tem Human Anatomy 879 (#23) e Social Media & Creator 982. O Seedance 2.5 tem Physics 1121 (#2).

### 1.3 Outras evidências, com data

- **31/07/2026**: a ByteDance lança o Seedance 2.5 (TechNode). A página oficial diz "visuals are more realistic" e a ElevenLabs o descreve como "sharper realism".
- **05/09/2026**: no teste lado a lado da Krea (Seedance 2.5 × Veo 3.1), nenhum dos dois resolve manipulação complexa de objeto. No Veo a ação ficou mais natural, mas também falhou. Regra: o mínimo de objetos na mão.
- **Aposentadoria do Veo**: o Google lista `veo-3.1-generate-001` e o Fast com aposentadoria "November 17, 2026 or later" (Vertex, model lifecycle). O desligamento de 22/10/2026 citado em blogs é dos endpoints preview da Gemini API, não destes IDs. **A partir de 17/11/2026, confira na doc "Create Video Generation" da ElevenLabs se o `model_id` ainda existe antes de planejar.**
- **[Voltec]** Antes da sessão, a conta já tinha 14 vídeos Veo gerados pela API (6 Veo 3.1 e 8 Fast). Todos saíram em 1080x1920, 24 fps, 8,0 s, AAC 48 kHz estéreo, com a persona consistente a partir do start_frame. Na inspeção da pesquisa, a pele saía lisa, "com cara de filtro".

### 1.4 Veo 3.1 na prática (12 gerações na sessão)

O que funcionou:
- Segura rosto, roupa e lugar do start_frame pelos 8 s.
- O áudio nativo serve de "captação do celular" (vento, mar) e vai baixo na mixagem, sob a narração.
- Aceita negative_prompt longo e marcações `[00:00-00:03]` no prompt. Seeds diferentes dão variações diferentes.

O que falhou (em toda rodada, pelo menos 1 das 2 variações teve problema):
- O pedido "bufa pelo nariz" virou sopro de boca em "O". Risadas abrem a boca, e sob narração em off isso parece dublagem.
- O celular deformou quando ela o abaixou para o colo: virou uma barra fina, com dedos fundidos. Objeto que gira ou fica de perfil é onde o Veo mais erra.
- O celular de quem filma apareceu no topo do quadro aos 4,5 s.
- A mão foi à boca, como num bocejo.

As correções de prompt estão em `prompts-principios.md` (seção 3). Muitas vezes basta escolher outro trecho do take (in/out em quadros de 24 fps), sem custo nenhum.

### 1.5 Ficha técnica na API da ElevenLabs

| | Veo 3.1 / Veo 3.1 Fast | Seedance 2.5 | Seedance 2.0 (e -fast, -mini) |
|---|---|---|---|
| Duração | 4, 6 ou 8 s | 4 a 30 s, take único | 4 a 15 s |
| Resolução | 720p, 1080p, 4K (o Vertex não oferece 4K no Fast). **1080p só com 8 s** | 480p ou 720p na prática. O schema aceita 1080p, mas a Civitai diz que é rejeitado | 480p, 720p, 1080p, 4k (-fast e -mini: até 720p) |
| Aspecto | 16:9 ou 9:16 (padrão 16:9) | com start_frame é forçado para `auto` (herda o formato do frame) | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 |
| seed | sim | não | sim |
| negative_prompt | sim | não | não |
| Áudio | gera áudio nativo; não aceita áudio de entrada | gera áudio nativo | gera áudio nativo |
| Referências | `images` até 3 (role subject/style), só com 8 s e sem start/end frame | até 30 images, 10 videos, 10 audios, sem start/end frame | até 9 images, 3 videos, 3 audios (máximo 12; áudio exige image ou video), sem start/end frame |
| Saída | 1080x1920, 24 fps, H.264 + AAC 48 kHz estéreo, 8,000 s (medido) | 720x1280 (escalar para 1080x1920 na edição) | – |

Só existem no app, fora da API: Gemini Omni Flash 1.1 (start/end frame, 9:16, 1080p nativo, 3 a 10 s, áudio nativo, Extend até 40 s), MiniMax H3, Wan 3.0, FLUX 3, Kling 3.0/O3, Kling 3.0 Motion Control, Seedance 2.5 Video Edit e Extend, e lip-sync com Sync 3 ou OmniHuman.

---

## 2. Status real na conta e teste sem custo

### 2.1 [Voltec] Situação em 15/10/2026

| Modelo | API | App web | Observação |
|---|---|---|---|
| Veo 3.1 e Veo 3.1 Fast | liberado | sim | 14 vídeos pela API antes da sessão e mais 12 na sessão |
| Modelos ByteDance: Seedance 2.5, 2.0, -fast e -mini (e o Seedream 5) | **403 `model_access_denied`**: verificado na sessão; pela doc, todos os ByteDance vêm bloqueados | Seedance 2.0 e 2.5 usados no app entre 28/09 e 03/10 | 2 de 4 tentativas de Seedance 2.5 no app, em 28/09, saíram com 0 crédito: falharam, com causa não confirmada (a suspeita é o filtro de rosto) |
| Omni Flash 1.1, MiniMax H3, Kling etc. | não existem na API | sim | – |
| Webhooks de Flows | nenhum configurado (`GET /v1/workspace/webhooks` → `[]`) | – | não mande o campo `webhook` |

Falhas registradas na conta, todas sem custo:
- 4 vídeos Veo falharam por causa de `enhance_prompt: false` ("Veo 3 prompt enhancement cannot be disabled").
- 1 Veo Fast foi barrado pela moderação do Google com o support code 15236754, que é a categoria "Celebrity" (rosto fotorrealista parecido com o de alguém famoso).

Defeito numa geração que foi cobrada: 1 Veo Fast (geração `QgxroTk1FNOGUAuXpk0o`) saiu com legendas em português queimadas no vídeo.

### 2.2 Testar o acesso a um modelo sem gastar

O create faz as checagens nesta ordem:
1. validação do schema (erro 422);
2. acesso ao modelo (erro 403);
3. existência das referências.

Então um corpo **válido no schema**, com `start_frame` apontando para um `generation_id` que não existe, nunca vira geração. Foi assim que a sessão provou o bloqueio sem gastar nada:

```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
python3 -I - "$SKILL/scripts" <<'EOF'
import sys; sys.path.insert(0, sys.argv[1]); import el
for m in ["bytedance-seedance-v2.5", "bytedance-seedance-v2", "bytedance-seedance-v2-fast", "bytedance-seedance-v2-mini"]:
    st, r = el.submit("video", {"model_id": m, "prompt": "A woman smiles at the camera.",
        "start_frame": {"type": "generation", "generation_id": "teste00naoexiste0000"},
        "aspect_ratio": "auto", "resolution": "720p", "duration_secs": 5, "generate_audio": True})
    print(m, st, r.get("detail", r) if isinstance(r, dict) else r)
EOF
```

| Resposta | O que significa |
|---|---|
| 403, `detail.type: authorization_error`, `detail.code: model_access_denied` ("You do not have access to this model") | Bloqueado na API. Nada foi criado nem cobrado. **[Voltec]** Foi o resultado em 15/10/2026. |
| Outra recusa, falando da referência inexistente | O acesso existe, e nada foi criado. |
| 422 | O corpo está inválido no schema. Corrija: o 422 vem antes da checagem de acesso e não revela nada. |
| 200 com `id` (não deveria acontecer) | Acompanhe com `el.get("video", id)`. Geração que falha não é cobrada. |

Não existe endpoint de permissões. O `GET /v1/user` não traz flags de acesso, e a tela Model Approvals (elevenlabs.io/app/workspace/model-approvals) é só para Enterprise e controla o app, não a liberação ByteDance na API.

### 2.3 Pedir a liberação ByteDance

Mande e-mail para support@elevenlabs.io a partir do e-mail dono da conta, com:
- o workspace_id;
- os model_ids desejados (`bytedance-seedance-v2.5`, `bytedance-seedance-v2`, `-v2-fast`, `-v2-mini`);
- o uso (ex.: anúncios próprios, com persona criada por IA pela própria empresa);
- a região (Brasil; o Seedance 2.x não está disponível nos EUA);
- o endpoint que será usado (`POST /v1/flows/video`).

A doc diz "Enterprise customers can contact support to request access", então a resposta pode ser negativa ou exigir upgrade. Não planeje contando com a liberação.

**[Voltec]** workspace_id `c2a4559701e24248aa43df1791a9bf8c`, plano growing_business (fatura de US$299/mês, equivalente ao Scale). O seat do dono é workspace_admin.

### 2.4 Mesmo com acesso: o filtro de rosto da BytePlus

- A doc da BytePlus diz que o Seedance 2.0 e o 2.5 não aceitam upload direto de imagem ou vídeo de referência com rosto humano real. Só confiam em saídas "trusted" da própria plataforma, como últimos quadros de vídeos Seedance ou imagens do Seedream 5 feitas só de texto, da mesma conta e com até 30 dias. O start_frame também é imagem de entrada, então uma persona fotorrealista pode ser barrada. Erro típico: "The request failed because the input image may contain real person".
- A ElevenLabs não documenta como trata isso.
- Nunca mande o rosto da persona em `images`; use start_frame.
- Faça um teste barato antes de planejar: 1 geração `bytedance-seedance-v2-mini` (480p, 4 s) pela API, se liberada, ou Seedance 2.5 no app, com a persona como start_frame. Falha e moderação não são cobradas. Se voltar `moderated`, faça os takes com rosto no Veo.

---

## 3. Quando usar cada modelo de vídeo

| Situação | Modelo e configuração | Observação |
|---|---|---|
| Padrão: Claude gera tudo pela API, com aprovação do cliente em cada portão | `veo-3.1-generate-001`, 9:16, 1080p, 8 s, `generate_audio: true`, start_frame = snapshot aprovado, 2 seeds por take | Testado na sessão. Gere sempre 8 s e corte na edição. |
| Testar ação e câmera barato antes da versão final | `veo-3.1-fast-generate-001` (7.272 créditos por 8 s) | Empata com o padrão nos rankings e custa cerca de 1/3. Faça a final no padrão: o mesmo seed não reproduz o resultado em outro modelo. Não foi usado na sessão. |
| Plano-sequência longo (até 30 s, sem cortes), realismo máximo, e alguém para operar o app | Seedance 2.5 no app, 720p, start frame = snapshot 9:16 exato | Topo dos rankings. Riscos: filtro de rosto, sem seed, 720p (escalar com lanczos e grão leve, sem unsharp). Operação manual: subir o frame, colar o prompt, baixar o MP4. |
| Precisa de 1080p nativo ou de seed na família ByteDance | Seedance 2.0 (app; na API só com liberação) | 4 a 15 s. |
| A/B no app com um modelo do Google | Gemini Omni Flash 1.1, 1080p, 3 a 10 s | Empata com o Seedance 2.5 em imagem→vídeo, custa ~7,3 mil créditos por geração no histórico e não passa pelo filtro da BytePlus (passa pelo "Celebrity" do Google). Não foi testado na sessão. |
| A personagem precisa falar com lip-sync na voz clonada | Nenhum modelo da API faz isso mantendo o start_frame. Use narração em off, mixada na edição. | No Seedance, `audios` não combina com start_frame; o Veo não aceita áudio de entrada. |
| Cabeça falante a partir de uma imagem e um áudio | `creatify-aurora` (API) | 480p/720p, sem controle de câmera nem de ambiente. Fora do estilo UGC. |
| O mais real possível: filmagem real com troca de pessoa | Seedance 2.5 Video Edit ou Kling 3.0 Motion Control (app) | Alguém filma a ação real no celular, no local, e o modelo troca a pessoa. Não foi testado. |

Regras que valem para qualquer modelo:
- Sempre image-to-video, com o snapshot aprovado como start_frame. O modelo só anima e não inventa rosto, roupa nem lugar.
- 2 variações por take. Quando o modelo aceita seed, use seeds diferentes.
- Um lugar e uma ação principal por take, com o mínimo de objetos na mão (ver `prompts-principios.md` §1.3 e §1.4).
- Mude UMA variável por refação, e prefira recortar o take a gerar de novo.

---

## 4. Imagem: snapshot é o primeiro quadro do vídeo

| Modelo | Evidência | Na sessão | Use para |
|---|---|---|---|
| `gpt-image-2.5-sunburst` | 1º do AA em texto→imagem (Elo 1217) e em edição (1198). OpenAI, lançado em 08/09/2026; na API da ElevenLabs desde o changelog de 21/09/2026 (Flare e Sunburst). Aceita `mask`. | **Venceu.** Manteve a identidade e seguiu o prompt. 2K 9:16 sai em 1152x2048 (9:16 exato) e serve direto como start_frame. ~554 créditos (high). | Snapshots com a personagem, edição de pose no mesmo lugar e edição de identidade (Image 1 = snapshot aprovado). |
| `gemini-3-pro-image` (Nano Banana Pro) | A doc diz que "planeja a cena antes de renderizar", mantém semelhança de até 5 pessoas, aceita até 10 refs e faz 1K/2K/4K. | Bonito, mas afinou e alterou o rosto e trocou a roupa. 2K 9:16 sai em 1536x2752, que não é 9:16 exato e precisa ser normalizado. | Cenas sem personagem ou A/B de cenário. |
| `gemini-3.1-flash-image` (Nano Banana 2) | Até 14 refs. | Não usado. | Rascunhos baratos (609 créditos em 1K, no histórico). |
| `gpt-image-1` e `gpt-image-1.5` | Só fazem 1:1, 3:2 e 2:3. | – | Evitar: não fazem 9:16. |
| `seedream-5` | ByteDance. | – | Evitar: bloqueado na API e indisponível nos EUA. |

Observações:
- Não existe teste independente de identidade comparando o GPT 2.5 com o Nano Banana Pro (o 2.5 saiu sem validação independente). O critério é o A/B com as suas referências reais.
- A sessão usou `quality: "high"` em tudo, inclusive nos snapshots aprovados. Existem `xhigh` e `max` (a pesquisa sugeria deixá-los para a versão final), mas o custo deles não foi medido.
- GPT e Gemini não têm seed nem negative_prompt, e cada request gera 1 imagem. Para A/B, mande 2 requests (2 cobranças) e guarde o `generation_id` da aprovada, porque não dá para regerar igual.
- Existe também a variante `gpt-image-2.5-flare` (até 10 refs e `mask`). Não há dados dela na sessão.

---

## 5. Custos

Como ler a coluna "Tipo":
- **MEDIDO**: medido na sessão de 15/10/2026.
- **HISTÓRICO**: consumo real da conta antes da sessão, por modelo, obtido com `GET /v1/usage/character-stats`.
- **DOC**: preço publicado pela ElevenLabs.
- **ESTIMADO**: não verificado. Confira no app, que mostra o preço antes de gerar e cobra o mesmo valor da API. A API não tem endpoint de estimativa.

| Item | Créditos | Tipo |
|---|---|---|
| Veo 3.1, 1080p, 8 s, com áudio | **19.391** por take (~2.424/s) | MEDIDO + HISTÓRICO (valor exato em 7 gerações) |
| gpt-image-2.5-sunburst, 2K, quality high | **≈554** por imagem | MEDIDO + HISTÓRICO |
| TTS eleven_v4 | **≈1 por caractere** | MEDIDO |
| SFX com `duration_seconds: 20` | **≈800** | MEDIDO (bate com a doc: 40 créditos/s) |
| Projeto inteiro, 3 rodadas de entrega (ex.: Verão Conectado) | **≈253 mil** (≈4,9% de um ciclo de 5,22 milhões) | MEDIDO **[Voltec]** |
| Veo 3.1 Fast, 1080p, 8 s, com áudio | 7.272 (~909/s) | HISTÓRICO (valor exato em 8 gerações) |
| Seedance 2.5, 720p, 9:16 (app) | 22.406 e 84.022 em 2 gerações, coerente com 8 s e 30 s a ~2.800/s | HISTÓRICO (duração inferida) |
| Seedance 2.0, 720p, 9:16 (app) | 17.552 por geração (duração não registrada) | HISTÓRICO |
| Gemini Omni Flash 1.1, 1080p (app) | ~7.339 por geração | HISTÓRICO |
| Kling 3 Pro com áudio (app) | 8.144 | HISTÓRICO |
| Kling 3 Pro Motion Control (app) | 10.338 a 29.122 | HISTÓRICO |
| Seedance 2.5 Extend (app) | 30 a 43 mil | HISTÓRICO |
| Sync lipsync v3 (app) | ~5.500 por clipe curto | HISTÓRICO |
| gemini-3.1-flash-image, 1K | 609 | HISTÓRICO |
| Voice changer (speech-to-speech) | 1.000/min (8 s ≈ 133) | DOC + HISTÓRICO |
| SFX com duração automática | 200 por geração | DOC |
| Música (Eleven Music) | 900/min (20 s ≈ 300) | DOC (não foi usada) |
| TTS flash/turbo v2.5, v4_turbo, v3_conversational | 0,5 por caractere | DOC (multiplicador do `GET /v1/models`) |
| Upload de assets, GETs de status, `POST /v1/music/plan` | 0 | DOC + vivido |
| Geração `failed` ou `moderated`, erro 422, recusa 403 | 0 | DOC + vivido |
| gemini-3-pro-image, 1K/2K | ~800 (4K: ~1.450) | ESTIMADO (foi gerado na sessão, mas o custo não foi registrado) |
| Veo sem áudio | ~9.700 (padrão) e ~4.850 (Fast) por 8 s | ESTIMADO (cerca de metade, pela tabela do Google) |
| Seedance 2.5 de 15 s / 20 s | ~42 mil / ~56 mil | ESTIMADO (a ~2.800/s) |
| Seedance 2.0 em 1080p | cerca do dobro do 720p | ESTIMADO |
| STT scribe_v1 | não medido; na sessão foi tratado como barato | – |

Regra prática (derivada): créditos ≈ 6.060 × preço de tabela do provedor em US$. Bate exato no Veo (US$3,20 vira 19.391; US$1,20 vira 7.272). Nos outros modelos é aproximação: no Seedance 2.5, a regra dá ~2.485/s e o histórico deu ~2.800/s.

Preço de criador de referência (AA, imagem→vídeo, US$/min): Seedance 2.5 24,60; Seedance 2.0 22,45; Veo 3.1 24,00; Veo Fast 9,00; Omni Flash 1.1 9,12.

Outros pontos:
- 4K custa mais e não serve para Reels (1080x1920).
- O histórico da conta tem requests eleven_v4 de 30/09 e 03/10 registradas com 0 crédito (talvez promoção de lançamento). Orce 1 crédito por caractere, que foi o medido.
- **[Voltec]** O plano growing_business dá 5,22 milhões de créditos por ciclo mensal. Para medir o custo real de uma etapa, compare o saldo antes e depois, ou consulte `GET /v1/usage/character-stats`, que foi o que a pesquisa usou (por modelo, em blocos de 10 min). O openapi.json baixado na pesquisa (15/10/2026) marca o endpoint como deprecated.

---

## 6. Orçamento de um vídeo de ~20 s com 3 takes (ex.: Verão Conectado)

A tabela vale para um vídeo de ~20 s com 3 takes, a receita do Verão Conectado: 3 takes de 8 s no Veo 3.1, cortados para 19 a 20,5 s, com narração em off e sem música. Para outro número de takes ou outra duração, use a conta por take logo abaixo da tabela.

| Etapa | Quantidade | Créditos |
|---|---|---|
| Snapshots com A/B | 6 a 9 imagens gpt-image-2.5 high | 3.300 a 5.000 |
| Refazer T2 e T3 se o cliente escolher o outro T1 (`prompts-moldes.md` §0) | 4 imagens | ~2.200 |
| A/B opcional no gemini-3-pro-image | 2 imagens | ~1.600 (estimado) |
| Edição de identidade (se o cliente mandar refs novas) | 6 imagens | ~3.300 |
| Narração | 4 leituras de ~300 caracteres (na sessão: 2 vozes no storyboard + 2 seeds da final) | ~1.200 |
| Troca de uma frase da narração | 3 seeds × ~66 caracteres | ~200 |
| Cama de SFX | ≥ duração do vídeo (ex.: 21 s para 20,5 s; `api-elevenlabs.md` §7) | ~800 a 840 |
| STT para QA | vários arquivos | pequeno (não medido) |
| **Vídeo** | 3 takes × 2 variações = 6 Veo 3.1 | **116.346** |
| **Uma rodada completa** | | **≈122 a 125 mil** (~2,4% de 5,22 milhões) |

**Conta por take, para outro roteiro** (derivada dos custos medidos):
- Vídeo: takes × 2 × 19.391 = 38.782 por take.
- Snapshots: takes × 2 × ≈554 = ≈1.108 por take, mais as refações.
- Narração: ≈1 crédito por caractere em cada leitura, a ~17 caracteres por segundo de fala (`prompts-moldes.md` §2.8).
- Cama de SFX: 40 × segundos.
- Conferência: com 3 takes, a conta dá ≈122 mil, o piso da tabela. Com 4 takes, ≈162 mil (só o vídeo dá 155.128).
- Cada take Veo tem 8 s. No Verão Conectado, os 3 takes cortados deram 19 a 20,5 s.

Real da sessão (Verão Conectado): ≈253 mil. Só as 12 gerações Veo somam 232.692 (≈92%); o resto foram 14 imagens (2 Gemini e 12 GPT), TTS, SFX, STT e testes. As rodadas foram:
1. v1: 6 Veo (≈116 mil).
2. Refinamento da identidade: 6 edições de imagem e mais 6 Veo.
3. CTA novo e legendas: só TTS de uma frase e edição.

Como planejar:
- Orce 1 rodada e reserve mais 1 rodada de vídeo (com 3 takes: ~125 mil + ~120 mil). O cliente quase sempre pede ajuste.
- Alternativa estimada: take único de 20 s no Seedance 2.5 (app), com 3 tentativas, fica em ~170 mil.
- Rascunho de ação no Veo Fast: 7.272 por take (3 takes ≈ 22 mil). A final vai no padrão.

Como economizar (lições da sessão):
- Rode as 2 críticas independentes (técnica e realismo) antes de gastar; elas não custam crédito. Na sessão, antes de qualquer geração, elas pegaram: risada de boca aberta sob a narração (`prompts-principios.md` §3.2), câmera impossível no T2 (§1.2), nome de lugar puxando Copacabana (§3.3), "baby hairs", que aciona o filtro "Child" do Google (§3.4), e o 1080p que só sai com 8 s (`api-elevenlabs.md` §3.3).
- Aprove o snapshot antes de qualquer vídeo, porque o vídeo é ~92% do custo.
- Recorte antes de gerar de novo. O "O" da boca no take 1 saiu de graça, cortando o take antes do quadro em que a boca abre (24 fps).
- Para mudar o texto da narração, gere só a frase nova com `previous_text` e emende (ver `api-elevenlabs.md` §5.5).
- Teste de acesso e erros de validação não custam nada (403 e 422), e falha e moderação também não.
- 2 variações por take parecem caras, mas evitam uma rodada extra: em toda rodada, uma das duas teve defeito.
