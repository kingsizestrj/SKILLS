# API ElevenLabs: guia de bolso

Endpoints para qualquer vídeo da Voltec com a personagem, em qualquer campanha. Os corpos reais, os textos e os números medidos vêm do caso de referência testado, o Reels "Verão Conectado" (15/10/2026). A base é `https://api.elevenlabs.io/v1` e a autenticação vai no header `xi-api-key`.

Como ler as marcas:
- **real**: corpo idêntico ao que rodou na sessão (cópias em `/home/syllas/hyperframes/voltec-reels-ia/bodies/`).
- **validado**: conferido contra o OpenAPI oficial na pesquisa, mas não executado.
- **[Voltec]**: fixo da conta ou da personagem da Voltec, em qualquer campanha (voz, settings, assets da persona, conta).
- **ex.: Verão Conectado**: valor só da campanha de referência (prompts, texto da narração, oferta, texto da cama de SFX, número de takes). Numa campanha nova, troque.
- **[não testado]**: derivado das regras e nunca rodado.

Escolha de modelo e custos: `modelos-e-custos.md`. Texto dos prompts: `prompts-moldes.md` (moldes) e `prompts-principios.md` (como escrever).

## Mapa rápido

| O quê | Chamada | Custo |
|---|---|---|
| Subir referência | `POST /v1/assets` (multipart: `asset`, `name`) | 0 |
| Listar, obter, apagar asset | `GET /v1/assets`, `GET /v1/assets/{id}`, `DELETE /v1/assets/{id}` | 0 |
| Gerar imagem | `POST /v1/flows/image` | ~554 (gpt-image-2.5 high) |
| Gerar vídeo | `POST /v1/flows/video` | 19.391 (Veo 3.1, 8 s, 1080p) |
| Status e URL de download | `GET /v1/flows/{image\|video}/{id}` | 0 |
| Listar gerações feitas pela API | `GET /v1/flows/video?page_size=..&status=..&model_id=..&cursor=..` | 0 |
| Narração com tempos por caractere | `POST /v1/text-to-speech/{voice_id}/with-timestamps?output_format=wav_48000` | ≈1/caractere |
| Transcrição para QA | `POST /v1/speech-to-text` (multipart) | não medido |
| Efeito sonoro | `POST /v1/sound-generation?output_format=mp3_44100_192` | 40/s |
| Música (não usada) | `POST /v1/music?output_format=mp3_48000_192` | 900/min |

---

## 0. Chave, scripts e convenções

**Chave**: fica em `~/.config/elevenlabs/env` (linha `ELEVENLABS_API_KEY=...`, chmod 600). Nunca imprima a chave:
- `scripts/el.py` lê a chave do ambiente ou desse arquivo e não a imprime. Outro arquivo pode ser indicado em `ELEVENLABS_ENV_FILE`.
- No shell, carregue com `set -a; source ~/.config/elevenlabs/env; set +a` e use `"$ELEVENLABS_API_KEY"`.
- Não use `curl -v`, `set -x`, `echo`, `env` nem `cat` no arquivo: todos vazam a chave no log.

**Preâmbulo dos exemplos** (o mesmo da skill toda). Variáveis não passam de uma chamada do Bash para a outra: rode-o na mesma chamada de cada bloco. Use um projeto novo: os exemplos gravam em `bodies/`, `audio/` etc. e sobrescreveriam arquivos do projeto da Voltec.

```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$PROJ"/{prompts,bodies,refs,snapshots,takes,audio,qa} && cd "$PROJ"
```

Nos blocos Python: `import os, sys, json; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el`.

**`scripts/el.py`** (detalhes no cabeçalho do script):

| Uso | Faz |
|---|---|
| `el.req(method, path, body=None, headers=None, raw=False)` | Chamada genérica. Devolve `(status, json)`, ou `(status, bytes)` com `raw=True`. Erro HTTP volta como `(código, json ou texto)`, sem exceção. |
| `el.upload_asset(path, name=None)` | `POST /assets` multipart. |
| `el.submit(kind, body)` | `POST /flows/{image\|video}`. **Gasta créditos** se for aceito. |
| `el.get(kind, gid)` / `el.fetch(kind, gid, outbase)` | Status / baixa para `<outbase>.<ext>` se estiver `completed`. |
| `el.wait(kind, ids, interval=None, maxwait=900)` | Polling de vários ids: 3 s para imagem, 15 s para vídeo, e dobra o intervalo ao receber 429. Devolve `{id: resposta_final}`; quem estoura o prazo volta com `status: timeout_local`. |
| `el.tts(voice_id, body, outbase, output_format="wav_48000")` | TTS with-timestamps. Grava `<outbase>.wav` e `<outbase>_alignment.json`. |
| CLI: `python3 -I "$SKILL/scripts/el.py" upload\|submit\|get\|wait\|tts ...` | Os mesmos comandos pela linha de comando. O print nunca mostra o `content_url`. |

Outros scripts:
- `scripts/poll_round.py <ids.json> [--kind video|image] [--out PASTA]`: espera e baixa uma rodada salva como `{nome: generation_id}`.
- `scripts/stt.py <arquivo> [--ss S --t D] [--out x.json]`: transcrição para QA (seção 6).
- `scripts/stress.py`: confere a tônica da marca pelo alignment (seção 5.4).

**Respostas**:

| Código | Significado | Cobra? |
|---|---|---|
| 200 no create | aceito: `{"id": "...", "status": "pending"}` | sim, se completar |
| 403 `model_access_denied` | modelo bloqueado para a conta | não |
| 422 | corpo inválido: campo desconhecido ou valor fora do enum | não |
| 429 | limite de taxa: faça backoff exponencial | não |
| `status: failed` no GET | a geração falhou (seção 4) | não |

---

## 1. Assets: subir referências

`POST /v1/assets`, multipart com dois campos obrigatórios: `asset` (o arquivo) e `name` (texto). A resposta é `{"asset_id", "name", "mime_type", "created_at_unix", "content_url"}`. O `content_url` é assinado, vale ~1 h e vem `null` enquanto o upload processa.

```bash
python3 -I "$SKILL/scripts/el.py" upload refs/rosto_frente.jpg        # -> 200 {"asset_id": "...", ...}
# sem Python:
set -a; source ~/.config/elevenlabs/env; set +a
curl -sS -X POST https://api.elevenlabs.io/v1/assets -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "asset=@refs/rosto_frente.jpg;type=image/jpeg" -F "name=rosto_frente.jpg"
```

Gerência:
- `GET /v1/assets?page_size=1..100&search=<texto no nome>&cursor=<next_cursor>` lista.
- `GET /v1/assets/{id}` devolve uma URL nova.
- `DELETE /v1/assets/{id}` apaga, sem afetar as gerações que já usaram o asset.

**Referência de mídia**. O formato é o mesmo em `images[]`, `start_frame`, `end_frame`, `videos[]` e `audios[]`:
- `{"type": "asset", "asset_id": "..."}`: arquivo enviado com `/v1/assets`.
- `{"type": "generation", "generation_id": "..."}`: saída de outra geração da API, sem upload. Pode até estar pendente.
- `{"type": "inline_base64", "content_base64": "...", "mime_type": "image/jpeg"}`: até 25 MB decodificado. É efêmero (pode sumir depois da geração), então ref reutilizada deve virar asset.

Regras:
- MIME aceitos: imagem jpeg, png, webp, heic, heif; áudio mpeg, wav; vídeo mp4, quicktime, webm.
- O upload não gasta crédito, mas ocupa cota: Pro 11 GB, Scale 33 GB, Business 111 GB. Acima disso, o erro é `asset_storage_limit_exceeded`. É preciso plano Pro ou superior e chave com permissão de Image & Video.
- Coisa feita no app web precisa ser baixada e subida como asset. Coisa feita pela API vai como `generation`.
- Prepare a referência antes de subir: rosto grande e de frente, sem dedos no recorte, sem logo nem letreiro (ffmpeg `delogo` ou recorte). Detalhes em `persona-e-marca-voltec.md`.
- **[Voltec]** Os IDs das refs da persona já estão na conta, listados em `/home/syllas/hyperframes/voltec-reels-ia/bodies/assets.json`: headshot, rosto_loja e corpo_sem_logo são fixos da persona; restinga é a foto do local do Verão Conectado.

Para normalizar uma imagem em 9:16 exato (1080x1920, RGB), faça isto quando o modelo herdar o formato do frame (Seedance 2.5) e com as saídas 1536x2752 do Gemini, depois suba como asset:

```bash
ffmpeg -i in.png -vf "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920:flags=lanczos" -pix_fmt rgb24 -frames:v 1 out.png
```

---

## 2. Imagem: `POST /v1/flows/image`

**Snapshot, real** (ex.: Verão Conectado, `/home/syllas/hyperframes/voltec-reels-ia/bodies/T1_gpt25.json`):

```json
{"model_id": "gpt-image-2.5-sunburst",
 "prompt": "<texto de prompts/T1_snapshot.txt (inglês, ~4.400 caracteres)>",
 "aspect_ratio": "9:16", "resolution": "2K", "quality": "high",
 "images": [{"type": "asset", "asset_id": "<rosto da persona>"},
            {"type": "asset", "asset_id": "<foto real do local>"}]}
```

**Edição de identidade, real** (`T1_id_a.json`). A Image 1 é o snapshot aprovado, passado como `generation`. As Images 2 a 4 são o rosto do carro, o rosto da loja recortado e o corpo inteiro sem logo:

```json
{"model_id": "gpt-image-2.5-sunburst",
 "prompt": "Edit Image 1, a frame from a casual smartphone video. Keep everything in Image 1 exactly as it is: ... Change only the woman's likeness so she is unmistakably the same person shown in Images 2, 3 and 4 ...",
 "aspect_ratio": "9:16", "resolution": "2K", "quality": "high",
 "images": [{"type": "generation", "generation_id": "<snapshot aprovado>"},
            {"type": "asset", "asset_id": "<rosto 1>"},
            {"type": "asset", "asset_id": "<rosto 2>"},
            {"type": "asset", "asset_id": "<corpo sem logo>"}]}
```

A edição de pose no mesmo lugar (T2) usa o mesmo formato. O Gemini (`T1_gemini_a.json`, real) é igual, com `"model_id": "gemini-3-pro-image"` e sem `quality`. Os textos completos, exemplos testados do Verão Conectado, estão em `prompts-moldes.md` §2.1 a §2.4 (o da identidade é um molde com `{OBJECT}`, `{OUTFIT}`, `{SETTING}` e `{EXPRESSION}`). Para outra cena, use o molde-base com slots de `prompts-moldes.md` §2.9.

**Campos por modelo**:

| Campo | gpt-image-2.5-sunburst (também gpt-image-2 e -2.5-flare) | gemini-3-pro-image | gemini-3.1-flash-image |
|---|---|---|---|
| `aspect_ratio` | `"9:16"` | `"9:16"` | `"9:16"` |
| `resolution` | `"2K"` (sai 1152x2048, 9:16 exato) | `"1K"`, `"2K"`, `"4K"` (2K sai 1536x2752) | 1K usado no histórico |
| `quality` | `high` (usado), `xhigh`, `max` | – | – |
| `images` (máximo) | 10 | 10 | 14 |
| `mask` | sim: PNG do tamanho da Image 1, onde a área 100% transparente é a editável; exige `images` | – | – |
| `seed`, `negative_prompt` | não (422) | não (422) | não |

Outros limites de refs: gemini-2.5-flash-image até 5; gpt-image-1 e 1.5 até 5 (e sem 9:16); seedream-5 até 10, com seed (ByteDance, bloqueado).

**Pegadinhas**:
- Cada request gera 1 imagem; não há parâmetro de quantidade. Para A/B, mande 2 requests (2 cobranças).
- Não há seed, então não dá para regerar a mesma imagem. Guarde o `generation_id` aprovado: ele vira o `start_frame` do vídeo.
- Nos modelos de imagem não existe `role`. A função de cada ref vem da ORDEM e do texto ("Image 1 is ..., Image 2 is ...").
- Use 2 refs de identidade e 1 do local (no máximo 2). Rostos divergentes aumentam a deriva.
- Existe encadeamento automático (mandar o vídeo apontando para uma imagem ainda pendente), mas ele dispara o vídeo sem a aprovação do cliente. Não use quando o snapshot precisa de OK.

**Rodada de imagens** (2 variações do T1 com o mesmo corpo):

```bash
python3 -I - <<'EOF'
import os, sys, json; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
IDS, ids = "snapshots/T1_ids.json", {}                 # um arquivo de ids novo por rodada
for nome in ("T1_gpt25_a", "T1_gpt25_b"):
    st, r = el.submit("image", json.load(open("bodies/T1_gpt25.json")))
    print(nome, st, r.get("id") if st == 200 else r)   # 4xx: nada criado, nada cobrado
    if st == 200:
        ids[nome] = r["id"]
        json.dump(ids, open(IDS, "w"), indent=1)       # grava a cada envio
EOF
python3 -I "$SKILL/scripts/poll_round.py" snapshots/T1_ids.json --kind image --out snapshots
# -> snapshots/T1_gpt25_a_<id>.png ... o <id> no nome é o que vai no start_frame
```

Na sessão, as imagens ficaram prontas em ~1 min.

---

## 3. Vídeo: `POST /v1/flows/video`

### 3.1 Veo 3.1: corpo real da sessão

Ex.: Verão Conectado, `/home/syllas/hyperframes/voltec-reels-ia/bodies/T1r_veo_v1.json`. O formato vale para qualquer take; o prompt e o snapshot mudam:

```json
{"model_id": "veo-3.1-generate-001",
 "prompt": "<texto de prompts/T1_video_veo_v2.txt>",
 "negative_prompt": "<texto de prompts/T1_negative_veo_v2.txt>",
 "start_frame": {"type": "generation", "generation_id": "<snapshot aprovado>"},
 "aspect_ratio": "9:16", "resolution": "1080p", "duration_secs": 8,
 "generate_audio": true, "seed": 20260115}
```

A 2ª variação é o mesmo corpo com `"seed": 20260116`. O corpo não leva `enhance_prompt` nem `webhook`.

### 3.2 Campos aceitos (Veo 3.1 e Veo 3.1 Fast)

- Obrigatórios: `model_id`, `prompt`.
- `negative_prompt`, `seed`, `enhance_prompt` (não mande; ver 3.3).
- `duration_secs`: 4, 6 ou 8 (padrão 8).
- `aspect_ratio`: `16:9` ou `9:16` (padrão 16:9).
- `resolution`: `720p`, `1080p` ou `4K` (padrão 720p).
- `generate_audio`: padrão true.
- `start_frame`, e `end_frame`, que exige `start_frame`.
- `images`: até 3 itens `{"image": <referência>, "role": "subject" | "style"}`.
- `webhook`.

### 3.3 Pegadinhas do Veo (vividas ou documentadas)

1. **Nunca mande `enhance_prompt: false`**: a geração falha com "Veo 3 prompt enhancement cannot be disabled". O Google sempre reescreve o prompt, então deixe explícito "amateur smartphone video" e ponha "cinematic color grading, film look" no negative.
2. **`webhook`** só funciona com webhook inscrito no workspace. **[Voltec]** Não há nenhum (`GET /v1/workspace/webhooks` → `[]`), e com o campo o create é recusado. Use polling.
3. **Padrões ruins**: sem `aspect_ratio` o vídeo sai 16:9; sem `resolution`, 720p. Mande sempre `"9:16"` e `"1080p"`.
4. **1080p só com 8 s.** A doc da Gemini API diz "1080p only supports 8s duration". O schema da ElevenLabs não valida a combinação, então 6 s com 1080p pode falhar ou cair para 720p. Gere 8 s e corte na edição.
5. **`start_frame` × `images`**: `images` (ingredients) não combina com `start_frame`/`end_frame` e exige 8 s. Para fidelidade ao snapshot aprovado, use `start_frame`.
6. Vídeo não serve de `start_frame`, só imagem. `end_frame` só quando a câmera e a luz forem as mesmas e só a pose mudar; senão sai morph.
7. `negative_prompt` é uma lista de termos, sem "no" nem "don't". Lista longa funciona: os da sessão tinham ~1.000 caracteres.
8. O prompt vai em inglês (o Vertex lista só inglês), com marcações `[00:00-00:03]`. O limite é de ~1.024 tokens; os prompts da sessão tinham de 1.750 a 1.970 caracteres.
9. Não ponha fala no vídeo: fala entre aspas puxa legenda queimada (já aconteceu no Fast). Termine o prompt com "(no subtitles)" e ponha "subtitles, captions, on-screen text" no negative.
10. Use seeds diferentes por variação (20260115 e 20260116 na sessão). O mesmo seed não reproduz o resultado em outro modelo.
11. Moderação do Google: `failure_reason: moderated`, com o código no `error_message` (15236754 = Celebrity; 58061214 e 17301594 = Child). Não é cobrado. Mude UMA coisa (ângulo ou expressão do snapshot, tirar "baby" do texto) e tente de novo.
12. A saída medida é 1080x1920, 24 fps, H.264 + AAC 48 kHz estéreo, com exatamente 8,000 s.

### 3.4 Rodada de vídeo: takes × 2 variações (ex.: Verão Conectado, 3 takes)

Custa takes × 2 × 19.391 créditos. Com 3 takes, como no Verão Conectado: **6 × 19.391 = 116.346 créditos**. Só rode depois de os snapshots estarem aprovados. O `SNAP` abaixo tem os 3 takes do exemplo: ponha os takes do roteiro.

```bash
python3 -I - <<'EOF'
import os, sys, json; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
R = ""   # 2ª rodada: R = "r" (como no SKILL.md §5) e SNAP só com os takes refeitos; os arquivos da 1ª ficam intactos
SNAP = {"T1": "<gen_id do snapshot T1 aprovado>", "T2": "<gen_id T2>", "T3": "<gen_id T3>"}
IDS, ids = f"takes/veo{R}_ids.json", {}   # no Verão Conectado eram takes/veo_round1_ids.json e veo_round2_ids.json
for take, snap in SNAP.items():
    prompt = open(f"prompts/{take}_video_veo.txt").read().strip()
    neg = open(f"prompts/{take}_negative_veo.txt").read().strip()
    for v, seed in (("v1", 20260115), ("v2", 20260116)):
        body = {"model_id": "veo-3.1-generate-001", "prompt": prompt, "negative_prompt": neg,
                "start_frame": {"type": "generation", "generation_id": snap},
                "aspect_ratio": "9:16", "resolution": "1080p", "duration_secs": 8,
                "generate_audio": True, "seed": seed}
        json.dump(body, open(f"bodies/{take}{R}_veo_{v}.json", "w"), ensure_ascii=False, indent=1)
        st, r = el.submit("video", body)
        print(take + R, v, st, r.get("id") if st == 200 else r)
        if st == 200:
            ids[f"{take}{R}_veo_{v}"] = r["id"]
            json.dump(ids, open(IDS, "w"), indent=1)
EOF
python3 -I "$SKILL/scripts/poll_round.py" takes/veo_ids.json --out takes   # 2ª rodada: takes/veor_ids.json
# -> takes/T1_veo_v1_<id>.mp4 ...; imprime status, failure_reason e error_message de cada um
```

Para um envio avulso: `python3 -I "$SKILL/scripts/el.py" submit video bodies/T1_veo_v1.json` e depois `python3 -I "$SKILL/scripts/el.py" wait video takes/T1_veo_v1_<ID> <ID>`.

### 3.5 Seedance (validado, NÃO executado: 403 na conta Voltec)

Teste de acesso sem custo: `modelos-e-custos.md`, seção 2.2. Prompt próprio (sem segundos, sons entre `<...>`): `prompts-moldes.md`, seção 2.7.

**A) Seedance 2.5, take único de até 30 s:**

```json
{"model_id": "bytedance-seedance-v2.5", "prompt": "<prompt Seedance>",
 "start_frame": {"type": "asset", "asset_id": "<snapshot normalizado 9:16>"},
 "aspect_ratio": "auto", "resolution": "720p", "duration_secs": 12, "generate_audio": true}
```

- `duration_secs` é inteiro de 4 a 30, com padrão 5, então informe sempre.
- `resolution`: use 720p. A doc lista 480p e 720p; o schema aceita 1080p, mas a Civitai diz que é rejeitado, e se for aceito é cobrado.
- Com `start_frame`, `aspect_ratio` é `auto` e herda o formato do frame, que precisa ser 9:16 exato.
- Sem `seed` e sem `negative_prompt` (dão 422).
- As refs (até 30 images, 10 videos, 10 audios) não combinam com `start_frame`/`end_frame`.

**B) Seedance 2.0, 1080p com seed:**

```json
{"model_id": "bytedance-seedance-v2", "prompt": "<prompt Seedance>",
 "start_frame": {"type": "asset", "asset_id": "<snapshot 9:16>"},
 "aspect_ratio": "9:16", "resolution": "1080p", "duration_secs": 10, "generate_audio": true, "seed": 4242}
```

- Duração de 4 a 15 s. `resolution`: 480p, 720p, 1080p ou 4k (minúsculo). `aspect_ratio`: auto, 21:9, 16:9, 4:3, 1:1, 3:4 ou 9:16. Aceita seed.
- As variantes `-fast` e `-mini` têm os mesmos campos, mas só fazem 480p e 720p.
- Refs: até 9 images, 3 videos (15 s somados) e 3 audios (15 s somados), com no máximo 12 no total; áudio exige pelo menos 1 image ou video.
- Nunca mande o rosto da persona em `images`/`videos` (filtro de rosto real da BytePlus).

### 3.6 Continuidade entre takes (pesquisa; não usado na sessão)

Na sessão, cada take teve o seu snapshot aprovado e os cortes foram motivados. Para emendar um take no outro:

```bash
ffmpeg -sseof -0.3 -i takes/T1.mp4 -update 1 refs/T1_last.png   # último quadro do take N
```

Suba o PNG como asset e use-o como `start_frame` do take N+1. Opcional: o snapshot do take seguinte como `end_frame`. Não há "extend" na API; o Seedance 2.5 Extend e o Omni Extend existem só no app.

---

## 4. Polling e download (imagem e vídeo)

- Consulte `GET /v1/flows/{image|video}/{generation_id}` com o header `xi-api-key`.
- O status vai de `pending` para `generating` e termina em `completed` ou `failed`.
  - `completed`: `{id, status, content_url, content_mime_type}`.
  - `failed`: `{id, status, failure_reason, error_message}`. O `failure_reason` é um destes: `timeout`, `model_error`, `moderated`, `invalid_parameters`, `dependency_failed`, `charging_failed`, `internal_error`. Falha não é cobrada.
- Ritmo: imagem com 2 s ou mais entre GETs. Vídeo com 10 s ou mais, subindo até ~60 s, e teto local de ~30 min. Com 429, backoff exponencial. Na sessão, 6 Veo em paralelo ficaram prontos em ~3 min, mas isso varia.
- O `content_url` é uma URL assinada (storage.googleapis.com) que vale ~1 h e baixa sem header. Se expirar, faça o GET de novo. Guarde o id, não a URL.
- `timeout_local` no `el.wait` só quer dizer que o prazo local acabou: a geração continua no servidor. Consulte depois com `python3 -I "$SKILL/scripts/el.py" get video <ID>`.
- Para recuperar ids: `GET /v1/flows/video?page_size=1..100&status=completed&model_id=veo-3.1-generate-001&cursor=...`. Só lista o que foi gerado pela API; o que foi feito no app não aparece.

Sem Python, com curl (o POST gasta créditos):

```bash
set -a; source ~/.config/elevenlabs/env; set +a
curl -sS -X POST https://api.elevenlabs.io/v1/flows/video -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" --data-binary @bodies/T1_veo_v1.json        # -> {"id":"<ID>","status":"pending"}
curl -sS https://api.elevenlabs.io/v1/flows/video/<ID> -H "xi-api-key: $ELEVENLABS_API_KEY" \
  | jq '{status, failure_reason, error_message}'
curl -sSL "$(curl -sS https://api.elevenlabs.io/v1/flows/video/<ID> -H "xi-api-key: $ELEVENLABS_API_KEY" | jq -r .content_url)" \
  -o takes/T1_veo_v1_<ID>.mp4
```

---

## 5. TTS: eleven_v4 com timestamps

### 5.1 Chamada

`POST /v1/text-to-speech/{voice_id}/with-timestamps?output_format=wav_48000` devolve um JSON: `{audio_base64, alignment: {characters[], character_start_times_seconds[], character_end_times_seconds[]}, normalized_alignment}`. Sem `/with-timestamps`, a resposta é o próprio áudio.

O `wav_48000` sai em WAV PCM 16 bits, mono, 48 kHz, a mesma taxa do áudio do Veo (conferido com ffprobe). WAV/PCM de 44,1 kHz para cima exige plano Pro ou superior; a alternativa é `mp3_44100_192`.

Nomes (convenção da skill): `prompts/narracao_<vN>.txt` → `bodies/tts_<vN>_s<seed>.json` → `audio/narracao_<vN>_s<seed>.wav` + `audio/narracao_<vN>_s<seed>_alignment.json`. No Verão Conectado os nomes eram outros, e continuam valendo lá: a narração aprovada é `audio/narracao_v2_A_s1.wav` (seed 20261015).

Corpo com a voz e os settings fixos da Voltec. O seed 20261015 é o da narração aprovada do Verão Conectado; para o A/B, gere também outro seed (ex.: 20261016):

```bash
VOZ=4yvYc2GSakxLWMhlsd6b      # [Voltec] "Radassa 100%"
jq -n --rawfile t prompts/narracao_v1.txt --argjson seed 20261015 \
  '{text: ($t|rtrimstr("\n")), model_id: "eleven_v4", language_code: "pt",
    voice_settings: {stability: 0.45, similarity_boost: 0.85},
    apply_text_normalization: "auto", seed: $seed}' > bodies/tts_v1_s20261015.json
python3 -I "$SKILL/scripts/el.py" tts "$VOZ" bodies/tts_v1_s20261015.json audio/narracao_v1_s20261015
# -> audio/narracao_v1_s20261015.wav + audio/narracao_v1_s20261015_alignment.json (formato lido por build_legendas.py e stress.py)
```

Em Python: `st, r = el.tts(VOZ, body, "audio/narracao_v1_s20261015")`.

### 5.2 Settings do eleven_v4

| Parâmetro | Valor | Nota |
|---|---|---|
| `model_id` | `eleven_v4` | até 10.000 caracteres por request; multiplicador 1,0 |
| `voice_settings.stability` | `0.45` | faixa de 0,40 a 0,50. Saiu teatral ou instável, suba para 0,55; saiu monótona, desça para 0,38 (sugestão do plano, não testada na sessão) |
| `voice_settings.similarity_boost` | `0.85` | faixa de 0,80 a 0,90 |
| `language_code` | `"pt"` | força português e a normalização correspondente |
| `seed` | fixo (0 a 4294967295) | reprodutível. Para outra leitura, troque o seed (a sessão gerou 2 a 3 seeds por texto e escolheu a melhor) |
| `apply_text_normalization` | `"auto"` | escreva números por extenso ("dois a cinco meses"). Recomendação da pesquisa; o registro da sessão não diz se foi enviado |
| `style`, `speed`, `use_speaker_boost` | não existem no v4 | – |
| SSML `<break>` | não funciona no v4 nem no v3 | use pontuação |

- Os settings salvos na voz (ex.: stability 0,2 e similarity 0,3) são baixos demais para o v4. Sobrescreva em toda request.
- Fallback para A/B: `eleven_multilingual_v2` com `{"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": true, "speed": 1.0}` e SEM `language_code`, que esse modelo não suporta.

### 5.3 Texto: tags, pausas e ênfase

- As tags vão em inglês, entre colchetes, no ponto em que a entrega muda. As da sessão foram `[frustrated]`, `[relieved, smiling]`, `[upbeat]` e `[excited]`. Elas não são lidas em voz alta e ocupam ~0,1 s no alignment (o `build_legendas.py` as ignora).
- Use no máximo 1 tag a cada 1 ou 2 frases, e prefira tags descritivas: o v4 às vezes lê uma tag ambígua como efeito sonoro.
- Pausa: reticências, travessão ou quebra de linha. Ênfase: CAIXA ALTA (ex.: "o verão INTEIRO"; da pesquisa, não testada). Vírgula e interrogação mudam a entonação.
- Escreva texto falado, não escrito: frases curtas e marcas de fala ("tá", "olha só", "gente").
- O v4 não tem `speed`, então a duração se ajusta pelo tamanho do texto. Na sessão, 294 caracteres (com tags) deram 16,6 s de áudio, a frase de 66 caracteres deu 3,8 s e a narração montada da v3, com 326 caracteres, deu 19,06 s: ~17 a 18 caracteres por segundo. A estrutura do roteiro e a conta para planejar estão em `prompts-moldes.md` §2.8.
- Gere a narração INTEIRA numa request, para a prosódia ficar contínua, e corte ou posicione pelos timestamps.

**Ex.: Verão Conectado**, texto final (`/home/syllas/hyperframes/voltec-reels-ia/prompts/narracao_v3.txt`).
- Fixos da Voltec: "Voltéc" no TTS, a frase das cidades e os dois textos de CTA (pago, abaixo; orgânico: "Assina pelo link na bio!").
- Da campanha: o gancho, o benefício e a oferta. A oferta vem sempre do cliente.

```text
[frustrated] Casa de praia sem internet? Ninguém merece...
[relieved, smiling] Agora sim! Com a Voltéc eu fico conectada o verão inteiro.
Tem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra.
[upbeat] Sem fidelidade: planos de dois a cinco meses.
[excited] Clica no botão Saiba Mais ou escaneia o QR code na tela!
```

### 5.4 Pronúncia

- O que funcionou: grafia fonética no texto do TTS, "Voltéc" para vol-TÉC. Na legenda vai a grafia certa, "Voltec" (mapa `FIX` do `build_legendas.py`).
- Alternativas da pesquisa, não testadas na sessão: IPA entre barras, dentro de aspas no texto (ex.: "/ɡɾusaˈi/"), ou `pronunciation_dictionary_locators` (até 3 por request).
- Para conferir a tônica, rode `python3 -I "$SKILL/scripts/stress.py" audio/narracao_v1_s20261015.wav audio/narracao_v1_s20261015_alignment.json`. Ele mede a duração e a energia de "Vol" e "téc" e dá um veredito. Para outra marca, use `--palavra REGEX --corte N`. O WAV tem de ser a saída crua do TTS. É heurística, e você não ouve áudio: liste na página do portão o instante de cada "Voltec" para o cliente confirmar ouvindo.
- No TTS, números e siglas vão por extenso; na legenda, em algarismos.

### 5.5 Trocar uma frase sem mexer no resto aprovado

Foi assim que a sessão trocou o CTA "link na bio" por "Saiba Mais / QR code". Esta é a única versão do procedimento (e do código que junta os alignments) na skill; `persona-e-marca-voltec.md` §6 e `edicao-hyperframes.md` §6.3 apontam para cá.

- Vale para trocar a **última** frase, como o CTA. Numa frase do meio, seria preciso cortar nos dois silêncios em volta dela e deslocar também o resto da narração: não foi feito na sessão (não testado).
- Os exemplos usam os valores do Verão Conectado com os nomes da convenção (§5.1): narração aprovada `audio/narracao_v1_s20261015`, frase nova `audio/cta_v2_s<seed>` e montagem `audio/narracao_v2` (sem seed no nome, porque junta duas gerações). Os arquivos reais da sessão estão em `/home/syllas/hyperframes/voltec-reels-ia/audio/`: `narracao_v2_A_s1` + `cta_v3_20261017` → `narracao_v3`.

**1.** Gere só a frase nova, com a mesma voz, os mesmos settings e `previous_text` com as frases anteriores. Faça 2 ou 3 seeds. O texto e o `previous_text` abaixo são do Verão Conectado: troque pelos da campanha.

```bash
VOZ=4yvYc2GSakxLWMhlsd6b
for s in 20261015 20261016 20261017; do
  jq -n --arg t "[excited] Clica no botão Saiba Mais ou escaneia o QR code na tela!" \
        --arg prev "Tem Voltéc em Grussaí, Atafona, Chapéu do Sol e São João da Barra. Sem fidelidade: planos de dois a cinco meses." \
        --argjson seed "$s" \
    '{text: $t, previous_text: $prev, model_id: "eleven_v4", language_code: "pt",
      voice_settings: {stability: 0.45, similarity_boost: 0.85}, apply_text_normalization: "auto", seed: $seed}' \
    > "bodies/tts_cta_v2_s$s.json"
  python3 -I "$SKILL/scripts/el.py" tts "$VOZ" "bodies/tts_cta_v2_s$s.json" "audio/cta_v2_s$s"
done
```

- O registro da sessão diz só "previous_text = frases 3 e 4"; não diz se a tag `[upbeat]` foi junto. Aqui vai sem ela.
- Confira cada seed com STT (seção 6). Você não ouve áudio: ponha as versões na página do portão para o cliente escolher. Na sessão ficou a 20261017.

**2.** Escolha o corte num silêncio entre o fim da última palavra mantida e o começo da frase trocada. No alignment do Verão Conectado, "meses" termina em 14,96 s e o `[excited]` começa em 15,154 s; a sessão cortou em 15,05. Confirme o silêncio no próprio áudio. No arquivo real (`narracao_v2_A_s1.wav`), este comando acha silêncio de 14,99 a 15,12 s (conferido na revisão da skill, não na sessão):

```bash
ffmpeg -hide_banner -nostats -i audio/narracao_v1_s20261015.wav -af silencedetect=n=-45dB:d=0.05 -f null - 2>&1 | grep silence_
```

Emende com fade curto, um silêncio e o ganho casado com a frase anterior. Na sessão: corte em 15,05 s, fade de 20 ms, 0,17 s de silêncio e a frase nova a −3 dB. Num projeto novo, troque os nomes, o corte (`15.05`), o início do fade (`15.03` = corte − 0,02), o silêncio (`0.17`) e o ganho. Rodado com os arquivos do Verão Conectado, o comando reproduz o `narracao_v3.wav` byte a byte (conferido na revisão da skill):

```bash
ffmpeg -i audio/narracao_v1_s20261015.wav -i audio/cta_v2_s20261017.wav -filter_complex "[0:a]atrim=end=15.05,asetpts=N/SR/TB,afade=t=out:st=15.03:d=0.02[a];anullsrc=r=48000:cl=mono,atrim=duration=0.17[g];[1:a]aresample=48000,aformat=channel_layouts=mono,volume=-3.0dB,asetpts=N/SR/TB[b];[a][g][b]concat=n=3:v=0:a=1[out]" -map "[out]" -ar 48000 -ac 1 audio/narracao_v2.wav
```

**3.** Junte os alignments: a frase nova entra deslocada em corte + silêncio (15,05 + 0,17 = 15,22 s). Se o corte cair fora do silêncio, o script para sem gravar nada. Rodado com os arquivos do Verão Conectado, ele reproduz as palavras e os tempos usados nas legendas, os mesmos do `narracao_v3_alignment.json`. Só o fim da quebra de linha antes da frase nova sai diferente, e o `build_legendas.py` ignora espaços e quebras.

```bash
python3 -I - <<'EOF'
import json
# Verão Conectado: narracao_v2_A_s1 + cta_v3_20261017 -> narracao_v3, com os mesmos CORTE, SILENCIO e TROCADA
APROVADA = "audio/narracao_v1_s20261015"   # narração aprovada (nome sem .wav)
NOVA = "audio/cta_v2_s20261017"            # só a frase nova, na seed escolhida
SAIDA = "audio/narracao_v2"                # o mesmo nome do WAV montado no passo 2
CORTE, SILENCIO = 15.05, 0.17              # os mesmos valores do ffmpeg do passo 2
TROCADA = "[excited]"                      # começo da frase trocada, como está no texto do TTS aprovado
a = json.load(open(f"{APROVADA}_alignment.json"))
b = json.load(open(f"{NOVA}_alignment.json"))
texto = "".join(a["characters"])
assert texto.count(TROCADA) == 1, "TROCADA precisa aparecer uma vez só no texto aprovado"
k = texto.index(TROCADA)
fim_fala = max(e for c, e in zip(a["characters"][:k], a["character_end_times_seconds"]) if c.isalnum())
ini_trocada = a["character_start_times_seconds"][k]
assert fim_fala <= CORTE <= ini_trocada, f"CORTE fora do silêncio entre {fim_fala:.3f} e {ini_trocada:.3f} s"
OFF = CORTE + SILENCIO                     # onde a frase nova começa na montagem
TEMPOS = ("character_start_times_seconds", "character_end_times_seconds")
out = {key: a[key][:k] for key in ("characters",) + TEMPOS}
out["characters"] += b["characters"]
for key in TEMPOS:
    out[key] += [t + OFF for t in b[key]]
json.dump(out, open(f"{SAIDA}_alignment.json", "w"), ensure_ascii=False)
print(f"{SAIDA}_alignment.json: {len(out['characters'])} caracteres; frase nova a partir de {OFF:.2f} s")
EOF
```

**4.** Registre a montagem: o texto final em `prompts/narracao_v2.txt` e um `audio/COMO_FOI_MONTADA_narracao_v2.txt` com voz, settings, seeds, `previous_text`, corte, silêncio, ganho e o comando do passo 2. Sem esse registro, uma regeração futura traz o texto antigo de volta. **[Voltec]** Exemplo: `/home/syllas/hyperframes/voltec-reels-ia/audio/COMO_FOI_MONTADA_narracao_v3.txt`.

**5.** Aponte a edição para a montagem: `NARR` = `audio/narracao_v2.wav` no `prep.py` e `ALIGN` = `audio/narracao_v2_alignment.json` no `build_legendas.py`. O resto (duração, `PHRASES`, `CTA_START`, tempos do index e render) está em `edicao-hyperframes.md` §6.3.

O alignment às vezes erra. Na sessão, ele marcou uma pausa que não existia antes de "internet?" (+0,25 s) e atrasou "Voltec" em ~0,1 s. Meça com STT (seção 6) ou pelo envelope do áudio e corrija à mão os inícios na legenda (`START_FIX` em `build_legendas.py`).

### 5.6 [Voltec] Vozes

- `4yvYc2GSakxLWMhlsd6b`, "Radassa 100%": clone instantâneo (IVC), pt-BR, com amostras limpas. É a voz principal, a "voz A" aprovada.
- `eHs9HKeucCzJ3ChAjmII`, "Radassa": IVC com amostras extraídas de vídeos de IA, com ruído de fundo. Serve só para A/B, porque o v4 copia o timbre E o ruído das amostras.
- Se a voz clonada for de uma pessoa real, mantenha o consentimento documentado (regra da ElevenLabs).
- Consultas de leitura: `GET /v1/voices/{id}` (dados e settings salvos) e `GET /v1/models` (limites e multiplicadores).

### 5.7 Efeitos no TTS (não usados)

O campo `audio_effects` no corpo aplica filtro de telefone, ambiente ou ruído (catálogo em `GET /v1/audio-effects/catalog`) e não muda o custo. Na sessão, a narração ficou seca e próxima, como voz em off de creator, sem efeito.

---

## 6. Speech-to-text (scribe_v1) para QA

`POST /v1/speech-to-text`, multipart com `model_id=scribe_v1`, `language_code=por`, `tag_audio_events=true`, `timestamps_granularity=word` e `file`. A resposta traz `text` e `words[]`. O `type` de cada item é `word` (fala), `spacing` ou `audio_event` (sons sem fala, como risada ou passos).

O `scripts/stt.py` faz tudo: converte qualquer áudio ou vídeo para WAV 16 kHz mono com ffmpeg, envia, remove os `spacing` e imprime `{"text", "words": [{"text", "start", "end", "type"}]}`:

```bash
python3 -I "$SKILL/scripts/stt.py" takes/T1_veo_v1_<ID>.mp4 --out qa/stt_T1_veo_v1.json | jq -r .text
jq -r '.words[] | select(.type=="word") | "\(.start)\t\(.end)\t\(.text)"' qa/stt_T1_veo_v1.json   # qualquer linha aqui = fala no take
python3 -I "$SKILL/scripts/stt.py" audio/narracao_v1_s20261015.wav | jq -r .text                  # compare com o roteiro sem tags
python3 -I "$SKILL/scripts/stt.py" renders/final.mp4 --ss 15.0 --t 5.5 | jq -r .text              # só a janela do CTA (ex.: Verão Conectado, a partir de 15 s)
```

| Checagem | Arquivo | Esperado |
|---|---|---|
| O áudio nativo do take não tem fala nem música | cada take gerado | nenhuma `word` (só `audio_event`, ou texto vazio) |
| A narração diz o texto certo | WAV da narração e mix final | texto igual ao roteiro sem as tags |
| Inícios de palavra para a legenda | narração ou mix | comparar com o alignment e corrigir o `START_FIX` |
| Frase emendada | narração montada | frase completa, sem corte nem estalo |

- Ligação entre palavras confunde o STT. Ex.: Verão Conectado: o STT ouviu "conectado" no lugar de "conectada", por causa da ligação "conectada‿o verão". Leve ao cliente. Se incomodar, regere só a frase com vírgula ("conectada, o verão inteiro") e emende; é uma frase do meio, então veja o limite do 5.5.
- Os tempos são relativos ao arquivo transcrito (com `--ss`, o script já devolve na linha do tempo do arquivo). No mix, lembre do atraso da narração.
- O custo não foi medido; na sessão foi tratado como barato e rodado em todos os arquivos finais.

---

## 7. Efeitos sonoros: `POST /v1/sound-generation`

O formato de saída vai na query (`output_format=mp3_44100_192` ou `pcm_48000`). A resposta é o próprio arquivo de áudio.

| Campo | Valor |
|---|---|
| `text` (obrigatório) | descrição em inglês |
| `duration_seconds` | de 0,5 a 30; `null` deixa o modelo escolher |
| `prompt_influence` | de 0 a 1 (padrão 0,3); quanto maior, mais literal |
| `loop` | true ou false; só no `eleven_text_to_sound_v2`. Bom para cama |
| `model_id` | `"eleven_text_to_sound_v2"` |

Custo: 40 créditos/s com duração informada (20 s ≈ 800, medido), ou 200 por geração com duração automática. O texto não muda o preço.

Cama de ambiente. O texto é o do plano do Verão Conectado (cena de verão numa casa de praia, fim de tarde): reescreva para a cena da campanha.

```bash
python3 -I - <<'EOF'
import os, sys; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
DUR = 21   # >= duração final do vídeo (TOTAL/24 do prep.py), no máximo 30; ex.: Verão Conectado, vídeo de 20,5 s
body = {"text": "Smartphone built-in microphone recording outdoors at a beach house facing the sea in the late afternoon: "
                "steady breeze with irregular gusts buffeting the mic, distant surf, cicadas in the trees, "
                "a car passing far away, no music, no voices",
        "duration_seconds": DUR, "prompt_influence": 0.45, "loop": True, "model_id": "eleven_text_to_sound_v2"}
st, audio = el.req("POST", "/sound-generation?output_format=mp3_44100_192", body, raw=True)
if st != 200:
    raise SystemExit(f"SFX recusado ({st}): {str(audio)[:300]}")
open("audio/ambiente_sfx.mp3", "wb").write(audio)
EOF
```

- `audio/ambiente_sfx.mp3` é o nome que o `BED` do `scripts/prep.py` espera; se mudar o nome, ajuste o `BED`. No Verão Conectado o arquivo era `audio/ambiente_praia_sfx.mp3`.
- `duration_seconds` ≥ duração final (TOTAL/24), no máximo 30: o `prep.py` corta o que sobra e completa com silêncio o que falta. Na sessão, a cama tinha 20 s e o vídeo 20,5 s, então ela acabou (com fade) antes do fim.
- Descreva a CAPTAÇÃO ("recorded on a smartphone built-in mic, wind buffeting the mic") e não peça música nem voz.
- Cena interna [não testado]: descreva a captação no cômodo (room tone, ventilador, a rua lá fora, longe), sem vento no microfone e sem TV, rádio ou conversa, porque o STT acusaria fala. Exemplo e regras em `prompts-moldes.md` §2.10.
- Use SFX para reforçar e colar o áudio nativo dos takes, que já vem sincronizado com a ação, não para substituí-lo. Na sessão, uma cama contínua de 20 s ficou bem baixa sob o vídeo inteiro (mixagem em `edicao-hyperframes.md`).
- Camadas separadas (vento no mic, ondas, rangido, notificação) mixam melhor que um prompt com tudo.

---

## 8. Música (só referência; a sessão não usou)

`POST /v1/music?output_format=mp3_48000_192`, com estes campos:
- `prompt` OU `composition_plan`, nunca os dois;
- `music_length_ms`, de 3000 a 600000;
- `model_id`: o padrão da API ainda é `music_v1`, então mande `"music_v2_5"`;
- `force_instrumental: true` (só com `prompt`);
- `seed` (só com `composition_plan`).

Exemplo da pesquisa (validado, nunca gerado; trilha pensada para o Verão Conectado). **[Voltec]** O padrão é sem música; só gere se o cliente pedir.

```json
{"prompt": "Laid-back Brazilian summer acoustic pop instrumental, 100 BPM, nylon-string guitar, shaker and light pandeiro, warm round bass, sunny carefree beach-house mood, intimate lo-fi production that sits quietly under a voiceover, clean ending",
 "music_length_ms": 20000, "model_id": "music_v2_5", "force_instrumental": true}
```

- Custo: 900 créditos/min (20 s ≈ 300). `POST /v1/music/plan` cria o composition plan sem custo. `POST /v1/music/video-to-music` (multipart com o corte final) gera trilha casada com o vídeo.
- A licença dos planos pagos cobre anúncio em rede social.
- Para parecer vídeo real, não use música (escolha da sessão) ou deixe-a bem baixa (−18 a −24 dB sob a voz). "Trilha de comercial" denuncia o anúncio.

---

## 9. Outros endpoints (pesquisados, não usados)

- `POST /v1/speech-to-speech/{voice_id}`: multipart com `audio`, `model_id=eleven_multilingual_sts_v2`, `voice_settings` e `remove_background_noise=true`. Troca o timbre e mantém o ritmo (ex.: passar uma risada nativa do take para o timbre da narradora). Custa 1.000 créditos/min.
- `POST /v1/audio-isolation`: isola a voz.
- `GET /v1/usage/character-stats`: consumo por modelo. Foi assim que a pesquisa mediu os custos reais; o openapi.json baixado na pesquisa (15/10/2026) marca o endpoint como deprecated.

---

## 10. Erros e o que fazer

| Sintoma | Causa | O que fazer |
|---|---|---|
| create devolve 403 `model_access_denied` | modelo bloqueado para a conta (ByteDance) | app manual ou Veo; pedir liberação (`modelos-e-custos.md`, seção 2) |
| create devolve 422 | campo desconhecido ou valor fora do enum (ex.: `seed` no GPT, `negative_prompt` no Seedance) | corrigir o corpo; nada é cobrado |
| create recusado com `webhook` no corpo | não há webhook inscrito no workspace | tirar o campo e fazer polling |
| `failed` com "Veo 3 prompt enhancement cannot be disabled" | `enhance_prompt: false` no corpo | tirar o campo |
| `failed` com `moderated` | filtro de conteúdo (Google: 15236754 Celebrity, 58061214/17301594 Child; BytePlus: rosto real) | mudar UMA coisa (snapshot, ângulo, expressão, texto) e não repetir igual |
| `failed` com `dependency_failed` | a imagem referenciada falhou | regerar a imagem |
| vídeo com legenda queimada | fala ou aspas no prompt (mais comum em vertical) | "(no subtitles)" e negative; sem fala; regerar |
| 429 | limite de taxa | backoff exponencial (o `el.wait` já dobra o intervalo) |
| o download falha depois de um tempo | o `content_url` expirou (~1 h) | GET de novo (`el.fetch` / `poll_round.py` já fazem isso) |
| `timeout_local` | o prazo local do polling acabou | consultar depois com `el.py get` |
| `asset_storage_limit_exceeded` | cota de armazenamento cheia | apagar assets antigos |
| Veo com 6 s em 1080p falha ou sai em 720p | 1080p só com 8 s | gerar 8 s e cortar na edição |
