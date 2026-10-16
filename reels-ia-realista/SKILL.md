---
name: reels-ia-realista
description: Produz e edita vídeos realistas com IA da Voltec (provedor de internet de São João da Barra-RJ) estrelados pela personagem/modelo da marca, em Reels, Stories ou anúncio 9:16 de qualquer campanha, estação ou tema (promoção, institucional, dica de Wi-Fi, suporte, inauguração), em locais reais da região (Grussaí, Atafona, Chapéu do Sol, São João da Barra) ou em cena interna, com narração em off ou com ela falando para a câmera, portões de aprovação do cliente, snapshot aprovado antes de qualquer vídeo, ElevenLabs (gpt-image-2.5, Veo 3.1, voz clonada Radassa por TTS ou troca de voz, SFX e STT) e edição HyperFrames com legendas, CTA e QR validado; use sempre que o pedido for criar ou ajustar um vídeo, Reels, Stories ou anúncio realista com IA da Voltec ou dessa personagem (inclusive com ela falando, recortar take, trocar frase ou CTA, versão com legendas, refinar a identidade), e como base para outra marca ou persona; não use em assuntos da Voltec sem vídeo, como rede, provisionamento, GenieACS ou TR-069.
---

# Vídeos realistas com IA da Voltec com a personagem da marca (ElevenLabs + HyperFrames)

Produção e edição de qualquer vídeo realista com IA da Voltec estrelado pela personagem da marca (Reels, Stories ou anúncio 9:16, em qualquer campanha, estação, tema ou cenário): persona de IA em lugar real → snapshot aprovado → Veo 3.1 image-to-video → narração com voz clonada → edição HyperFrames com legendas, CTA e QR. Aqui ficam o fluxo, as regras, os fixos da Voltec e os slots que mudam a cada vídeo. Corpos JSON, prompts completos e comandos longos estão em `references/`.

**Caso de referência testado:** o Reels "Verão Conectado" (15/10/2026; 20,5 s, 1080x1920, 24 fps; entregue na v5). Os valores dele aparecem como "ex.: Verão Conectado" e nunca são padrão: o que é da campanha é slot (§1b), e o exemplo preenchido está no §7.2.

- **[Voltec]** marca o que é fixo da Voltec com a personagem ou da área atendida (Grussaí e região). "Ex.: Verão Conectado" marca valor só da campanha de referência. O resto vale para qualquer anúncio com IA.
- Nível de evidência, o mesmo das references: **[vivido]** aconteceu na sessão e foi conferido; **[aplicado]** veio da pesquisa ou das críticas e entrou nos takes aprovados; **[pesquisa]** só da pesquisa; **[não testado]** derivado das regras, sem nenhuma geração (§8).
- `$SKILL` = pasta deste SKILL.md; `$PROJ` = pasta do projeto do vídeo. Variáveis de shell não passam de uma chamada do Bash para outra: repita o preâmbulo da seção 5 em cada chamada.
- Prompts de geração em inglês. Textos ao cliente, narração e legendas em português.
- A chave da API fica em `~/.config/elevenlabs/env` (chmod 600) e `scripts/el.py` a lê sem imprimir. Nunca use `echo`, `cat`, `env`, `curl -v` ou `set -x` com ela, nem a escreva em arquivo, prompt ou mensagem.
- Você não ouve áudio: confira com STT (texto e `audio_event`), espectrograma do trecho e ebur128, e liste na página do portão os instantes para o cliente ouvir.

## 1. Quando usar

- **[Voltec]** Qualquer vídeo **realista** com IA da Voltec estrelado pela **personagem da marca**, que precisa parecer filmada de verdade por alguém: Reels, Stories ou anúncio; qualquer campanha, estação ou tema (promoção sazonal, institucional, dica de Wi-Fi, suporte, inauguração, Black Friday); cenário real da área atendida (Grussaí, Atafona, Chapéu do Sol, São João da Barra; o que serve de cenário: §7.1) ou interno (casa, loja, carro). Cenário, roupa ou formato que nunca foi gerado: §8.
- Geração pela API da ElevenLabs: imagem (snapshot), vídeo (Veo 3.1; Seedance pela API só com liberação, ou manual no app), narração com voz clonada, SFX e STT.
- Edição no HyperFrames: cortes por quadro, mixagem, cartões, legendas sincronizadas, CTA e QR.
- Ajuste num vídeo de IA já entregue: recortar take, trocar variação, trocar uma frase ou o CTA, versão com legendas, refinar a identidade.
- **Com ela falando para a câmera** ("com ela falando", "ela fala", "ela explicando"): modo falando, em `references/modo-falando.md`. O Veo 3.1 gera o take com a fala e o `sts.py` troca a voz para a Radassa. [vivido: teste de 13 s aprovado em 15/10/2026]
- **[GERAL]** Outra marca ou persona: o que não é [Voltec] serve, com adaptação (troque o §7.1 e preencha os slots do §1b). Projeto de referência: `/home/syllas/hyperframes/voltec-reels-ia/` (Verão Conectado; só leitura).
- Não serve para motion graphics sem pessoa nem cena gerada (aí basta o HyperFrames) nem para assuntos da Voltec sem vídeo (rede, GenieACS, TR-069).

**Padrão de qualidade** (exigência da Voltec; use como padrão em todo projeto): realismo máximo; câmera crível, como alguém filmando de verdade; ambiente real, sem troca brusca; nenhuma anomalia no objeto da mão; locais reais com fotos licenciadas (ou do próprio cliente) mostradas ao cliente; **snapshot aprovado antes de qualquer vídeo**; prompts detalhados (movimento, pele, captação de áudio com ruídos reais); pesquisa de boas práticas antes de gerar.

## 1b. Começo rápido: qualquer vídeo novo da Voltec com a personagem

1. **Leia nesta ordem:** este SKILL.md (com o §7) → `persona-e-marca-voltec.md` §1–4 e §6–7 → o cenário: em Grussaí, `locais-grussai.md` §1, §3 (com a tabela "Outras estações") e §4; em outro lugar ou cena interna, o §8 deste arquivo, `persona-e-marca-voltec.md` §10 e `locais-grussai.md` §7–§10 → `prompts-principios.md` §1 (com o "Checklist do prompt") → só o molde de `prompts-moldes.md` §2 mais perto da cena (2.1 amiga filmando, 2.2 pose no mesmo lugar, 2.3 selfie, 2.5–2.6 vídeo; cena nova: 2.9–2.10). O resto, só na fase em que precisar. `prompts-moldes.md` e `persona-e-marca-voltec.md` passam do limite de uma leitura do Read: ache a seção com Grep (ex.: `^### 2\.9`, `^## 10`) e leia com offset/limit.
2. **Já decidido (fixos da Voltec; não pergunte de novo):** persona da conta, com os assets `na7keiYvPpGArmyghOpk`, `pUgU1HXgmdqXfP02iR8T` e `ZY1iDcJLhPFklahPnvkM` já na conta (não suba de novo; persona §4) e as âncoras de rosto, pele e mãos (persona §3.1–3.3); voz "Radassa 100%" `4yvYc2GSakxLWMhlsd6b`, eleven_v4, 0.45/0.85, `"pt"`, e o A/B agora é entre 2 seeds dessa voz; pronúncia vol-TÉC ("Voltéc" no TTS, "Voltec" na tela); sem joias nem tatuagens; sem música; logo, cores, fontes e cidades (§7.1); as regras de realismo, prompt e QA (§3, `qa-checklist.md`) e os portões (§2). Modelo: Veo 3.1 pela API, escolhido em 15/10/2026; só volte à pergunta se o teste de acesso sem custo (`modelos-e-custos.md` §2.2) ou a revisão de catálogo da Fase 1 mudarem o quadro.
3. **Slots do vídeo:** pergunte sempre, antes de escrever a narração (no chat basta). Exemplo preenchido no §7.2.
   - **Vêm do cliente (nunca invente):** tema e formato (Reels, Stories, anúncio); narração em off (padrão) ou ela falando para a câmera (`references/modo-falando.md`), e nesse caso a fala de cada take; oferta, preço, condições e período; anúncio pago (botão "Saiba mais" + QR) ou post orgânico ("link na bio"); destino do QR (o `page_id=674` é a página "Verão Conectado 2026": não o reaproveite sem o cliente confirmar); se os créditos das fotos CC BY vão na legenda do post.
   - **Pergunte e proponha (o cliente aprova no portão 1 ou 2):** cenário, horário e luz; duração; roteiro de takes (por take: lugar, objeto na mão e som ambiente); roupa; gancho; cartão da campanha; texto da cama de SFX.
4. **Refaça por cena, estação ou cenário** (nada disso se copia do exemplo): âncora de roupa no estilo da persona §3.4 (opaca, sem estampa nem logo; tecido liso ou de trama grande, porque padrão fino tremula); luz pelo sol calculado para lugar, data e hora (`locais-grussai.md` §8; em Grussaí, a tabela "Outras estações" do §3: no inverno, sol a ~19,5° por volta de 15h40 e sol da tarde a ~293–304°; na selfie em contraluz ela caminha para o sul e o mar fica à direita); vento (só o do verão foi pesquisado: pesquise antes); som ambiente do lugar (no prompt de vídeo e na cama de SFX); trechos de lugar do negative_prompt (`prompts-moldes.md` §2.6); espaço livre no snapshot para o gancho, numa área lisa do quadro (o `#q1` do template fica no alto à direita; ex.: Verão Conectado: céu aberto no T1); textos da campanha nos tokens `__…__` do template: gancho, título do cartão em 1 ou 2 partes com ícone opcional (ex.: "VERÃO ☀ CONECTADO", com o sol) e oferta; texto da cama de SFX.
5. **Projeto e página novos:** `$HOME/hyperframes/<campanha>` e um Artifact novo. Não republique na URL do Verão Conectado (§7.2).

## 2. Fluxo em fases e portões

Cada portão é uma página (Artifact) com A/B lado a lado e perguntas numeradas. Peça resposta curta no formato "T1-A, T2-A, T3-A, voz A, modelo 1"; foi o que acelerou as decisões.
- **Página:** uma por projeto, republicada a cada portão (mesmo arquivo, mesma URL), com o portão atual no topo e as decisões já tomadas embaixo; campanha nova = página nova. Mídia vai como arquivos de suporte em `media/`: snapshots em JPG (~200 KB cada na sessão), narração em MP3 e prévia do vídeo em MP4 com poster JPG (~11 MB na sessão; limite de 15 MB por arquivo). Estrutura modelo (ex.: a página do Verão Conectado): leia https://claude.ai/artifact/MivTjGgrZ9ZyhZTftP66kh (Artifact, `action: "read"`). Por take: A/B, câmera, ação, som captado, narração, texto na tela e tempo. Depois: narração A/B com tabela de tempos, caminhos de modelo, locais com crédito e uma caixa com o formato de resposta.
- **Registro:** anote as respostas de cada portão em `$PROJ/DECISOES.md` e na seção "Decisões" da página.
- **Juntar portões:** junte 1, 2 e 3 numa página só quando oferta, CTA (pago × orgânico) e destino do QR já estiverem respondidos. Sem isso, faça antes o portão 1 (no chat basta) e não gere snapshot nem narração. A narração mostrada num storyboard antes das respostas é provisória: depois delas (pronúncia, CTA, oferta), gere a narração final com a voz escolhida (2 seeds, ~300 créditos cada), antes dos vídeos. Ex.: Verão Conectado: `narracao_radassa100` no storyboard e `narracao_v2_A_s1` depois das respostas.
- **Nunca se junta:** vídeo antes do OK do portão 3.

**Fase 1. Pesquisa e plano (0 crédito)**
- Pesquise em paralelo (4 frentes: modelos, realismo/anti-alucinação, locais e API; com subagentes em paralelo, se houver). Depois escreva o roteiro e o plano de takes no formato do storyboard: por take, lugar e hora, quem filma e câmera, ação em 2–3 tempos, objeto, som captado, frase da narração, texto na tela e tempo.
- Rode **2 críticas independentes** antes de gastar: um subagente por foco; sem subagentes, uma passada separada por foco. Técnica = campos e limites da API (`api-elevenlabs.md` §3.3), duração/1080p, custos e moderação (`prompts-principios.md` §4). Realismo = "Checklist do prompt" de `prompts-principios.md` §1 + luz e geometria (sol calculado em `locais-grussai.md` §8; cena interna ou noturna: §8 deste arquivo). Cada uma devolve problema, take, severidade e correção.
- Rankings mudam rápido: se `modelos-e-custos.md` tiver mais de ~2 meses, consulte de novo. A partir de 17/11/2026, confira se `veo-3.1-generate-001` ainda existe. Teste o acesso a cada modelo sem gastar (§2.2 do mesmo arquivo).
- **Cliente já atendido:** as references são a pesquisa. Refaça só o item acima e o que é novo na campanha: estação (o vento fora do verão não foi pesquisado), cenário fora do exemplo ou sem foto aberta (peça fotos ao cliente, `locais-grussai.md` §7; o que não foi pesquisado está no §8 e em `locais-grussai.md` §10), roupa e objeto na mão (persona §3.4). Mantenha as 2 críticas antes de gastar.
- **Portão 1, o cliente recebe:** modelo recomendado com placar datado e custo previsto; roteiro com a narração escrita; perguntas numeradas: CTA de anúncio pago ou de post orgânico, destino do QR, pronúncia da marca, oferta e preço (vêm do cliente; nunca invente), persona e refs (avise se alguma ref tiver outro rosto), voz e consentimento, música (padrão: sem), duração, tatuagens e joias, rótulo "Informações de IA", crédito das fotos. **[Voltec]** Pergunte só o que a seção 1b manda.

**Fase 2. Locais reais (0 crédito)**
- Fotos com a licença lida na página da foto e o local provado (geotag, OpenStreetMap): método em `locais-grussai.md` §7. Calcule o sol para a hora da cena (`locais-grussai.md` §8) e confira o vento do lugar. Só CC0 e CC BY vão para a API; foto NC serve só de referência para escrever o prompt. Cena interna (casa, loja, carro): fotos do próprio cliente, sem placa nem letreiro legível (§8).
- **Portão 2, o cliente recebe:** folha de contato (verde = pode ir para a API; vermelho = NC), créditos, o cenário único proposto (um lugar e um horário; ex.: Verão Conectado: a varanda e a areia em frente, numa tarde de verão) e o horário da luz.

**Fase 3. Snapshots e narração (portão obrigatório)**
- Snapshot = 1º quadro de cada take, no `gpt-image-2.5-sunburst` (9:16, 2K, high), com **2 variações por take**. Revise todos com `qa-checklist.md` §A.
- Gere T1 A/B primeiro. Escolha você a melhor pelo `qa-checklist.md` §A e use-a como base: o take seguinte no mesmo lugar é edição dela, com a câmera no mesmo ponto; lugar novo é imagem nova com ela como Image 1 (ex.: Verão Conectado: T2 e T3 saíram do T1-A `5vBTv3B9FOt44Vu8jMY4` antes do storyboard). No portão 3, diga quais takes derivam do T1-X. Se o cliente escolher o outro T1, refaça os derivados a partir dele (2 imagens por take; ex.: Verão Conectado: T2 e T3, 4 imagens, ≈2,2 mil créditos) antes de qualquer vídeo.
- Narração inteira numa request, com 2 vozes ou 2 seeds. A duração medida pelo alignment define os cortes. Confira a tônica da marca e o texto falado (`stress.py` + STT).
- **Portão 3, o cliente recebe:** A/B de cada take lado a lado com a ref do rosto, players da narração A/B, as fotos dos locais e a pergunta do modelo. **Pare até a resposta** e guarde os `generation_id` aprovados.

**Fase 4. Vídeos, 2 variações por take**
- Veo 3.1, `start_frame` = generation_id do snapshot aprovado, 9:16, 1080p, 8 s, com áudio, seeds 20260115 e 20260116. O prompt descreve só movimento, câmera e som (`prompts-moldes.md` §2.5–2.6). A personagem não fala, exceto no modo falando (`references/modo-falando.md` §4).
- 19.391 créditos por geração, 2 por take (ex.: Verão Conectado, 3 takes × 2 variações = 116.346). Na sessão, 6 gerações em paralelo ficaram prontas em ~3 min (varia). O cliente não recebe nada nesta fase.

**Fase 5. Seleção e QA de cada variação (portão interno)**
- Folha de contato a 2 fps, tiras numeradas a 24 fps (boca) e a 8 fps (mãos e objeto), e STT do áudio nativo (`qa-checklist.md` §B). Anote o quadro de cada defeito (take Veo = 192 quadros; quadro = segundos × 24) e escolha in/out que o evite. Se a variação A não tem janela limpa, use a B. Se as duas falham, regere mudando UMA variável.
- Regerar além das 2 variações: dentro da reserva de 1 rodada aprovada no portão 1; acima disso, peça OK com o motivo e o custo (19.391 por take).
- O cliente só recebe algo aqui se houver dúvida real: as 2 variações em loop na página.

**Fase 6. Edição (0 crédito, fora a cama de SFX: 40 créditos/s, ~800 por 20 s)**
- `prep.py` (cortes por quadro, fim congelado sob o CTA, mix) e o `index.html` do template, com cartões ancorados no alignment. Lint, check e render a 24 fps (`edicao-hyperframes.md`).
- Antes do portão 4, rode o bloco automático da `qa-checklist.md` §C e a verificação independente §D na master. O cliente só vê o corte que passou.
- **Portão 4, o cliente recebe:** o vídeo editado na página (prévia leve) e os instantes para ele ouvir com atenção: cortes, emenda, rampa e cada vez que a marca é falada, mais os pontos em que o STT ouviu algo diferente do roteiro (ex.: Verão Conectado: "conectado" em "conectada o verão").

**Fase 7. Versões com e sem legenda**
- O mesmo index, com a variável `legendas`. `build_legendas.py` gera as legendas pelo alignment. Recodifique para Instagram. São 4 arquivos: master e Instagram, com e sem legenda. Entregue as duas versões por padrão (na sessão, a legendada foi pedida depois).

**Fase 8. QA final, verificação independente e entrega**
- Repita a `qa-checklist.md` §C nos 4 arquivos (número de quadros, −14 LUFS e ≤ −1,5 dBTP, QR decodificado, fim sem quadro preto, faststart) e a §D se algo mudou depois do portão 4: 3 revisores separados (áudio, imagem, técnico/sincronia), um subagente por foco ou, sem subagentes, uma passada separada por foco. Na sessão eles acharam 2 problemas médios que quem editou não tinha visto.
- **Entrega, o cliente recebe:** os 4 arquivos com nome de campanha e versão, a página com o vídeo, o recado "ative o rótulo Informações de IA da Meta" e os créditos das fotos CC BY. Atualize `prompts/`, `bodies/` e `audio/COMO_FOI_MONTADA_*.txt` com o que foi realmente usado, e a memória do projeto com caminhos, versão e decisões (**[Voltec]** ex.: Verão Conectado: `voltec-reels-ia-producao.md`).
- Pedido de ajuste depois da entrega: siga a tabela da seção 4, nesta ordem de preferência: recortar, trocar variação, trocar frase, editar identidade, regerar.

**Orçamento:** por rodada, 38.782 créditos de vídeo por take (2 variações de 19.391) mais ~5 a 7 mil de imagens, narração e SFX (`modelos-e-custos.md` §6). Ex.: Verão Conectado, 3 takes e ~20 s: ≈122 a 125 mil por rodada. Reserve mais uma rodada de vídeo (~120 mil para 3 takes). A sessão real, com refação de identidade e CTA novo, fechou em ≈253 mil, e o vídeo foi ~92% disso.

## 3. Regras de ouro

1. **Snapshot aprovado antes de qualquer vídeo.** O vídeo só anima (`start_frame`), então rosto, roupa, lugar e luz ficam travados. [vivido]
2. **2 variações por take** (imagem: 2 requests; Veo: seeds diferentes; narração ou frase trocada: 2 ou 3 seeds). Em toda rodada da sessão, pelo menos uma variação teve defeito. [vivido]
3. **Recorte antes de regerar.** Escolher in/out em quadros de 24 fps custa zero; o "O" da boca no T1 sumiu assim. Numa refação, mude uma variável só. [vivido]
4. **A personagem não fala.** Sob narração: `Her lips stay closed the entire time: she does not blow air, sigh, purse her lips or open her mouth, and she never speaks.` A emoção vem de olhos, testa e ombros. Nada de huff, sigh ou risada de boca aberta. [vivido] Exceção: modo falando (`references/modo-falando.md`). [vivido]
5. **Um lugar, uma ação e um objeto**, já no 1º quadro, com a tela (se houver) virada para ela. Não mande abaixar, guardar nem girar o objeto: manipulação é onde o Veo mais erra, então revise esses trechos a 8 fps. [vivido]
6. **Câmera com dono**: quem filma, altura, distância e um movimento só, sem zoom, pan, drone ou gimbal. **Olhar no rosto de quem filma** (na selfie, na própria imagem da tela), nunca cravado na lente. [aplicado] No modo falando, ela fala com quem assiste: olhar na lente ou na tela da selfie. [vivido na selfie]
7. **Nenhum texto, logo, marca ou nome de lugar** no prompt nem nas refs: descreva o lugar fisicamente. Logo, oferta, legenda e QR entram só na edição. [aplicado]
8. **Moderação**: `an adult ... about 26 years old`, `fine wispy hairs` (nunca `baby hairs`), roupa opaca, nenhum descritor de corpo no vídeo, nenhuma palavra sensível nem para negar. Geração moderada não é cobrada: mude uma coisa e tente de novo. [aplicado]
9. **Luz e vento coerentes com a geografia e a hora reais** (calcule o sol). Escreva `Not golden-hour orange` quando a hora não for dourada. [aplicado] Em cena interna ou à noite, uma fonte de luz real, com direção (§8). [não testado]
10. **Veo na API**: sempre `9:16`, `1080p` e 8 s (1080p só sai com 8 s). Não mande `enhance_prompt` (com `false` a geração falha) nem `webhook`. Feche o prompt com `(no subtitles)` e use negative_prompt longo. [vivido]
11. **Persona no `gpt-image-2.5-sunburst`.** Composição aprovada com rosto pouco parecido pede edição de identidade, não snapshot do zero. Refs: rosto grande e de frente, sem dedos, sem logo, sem acessório que possa vazar. [vivido]
12. **Narração inteira numa request.** Para trocar uma frase, gere só ela com `previous_text` e emende num silêncio. **Registre como a narração foi montada** (`COMO_FOI_MONTADA_*.txt`); sem isso, uma regeração traz o texto antigo de volta. [vivido]
13. **Marca com grafia fonética no TTS e grafia certa na tela.** Confira a tônica com `stress.py` e o texto com STT. [vivido]
14. **Áudio sem degrau de ganho** (use rampa ou fade) e sem música. Narração a −16 LUFS, ambiente nativo a −30 LUFS com ducking, cama de SFX a −36 LUFS e master a −14 LUFS / −1,5 dBTP. [vivido]
15. **CTA e QR**: pergunte se é anúncio pago ou post orgânico no portão do roteiro. Valide o QR decodificando um quadro do vídeo final (master e Instagram) e rode a verificação independente antes de entregar. [vivido]

## 4. Decisões rápidas

| Situação | Decisão | Por quê / custo |
|---|---|---|
| Modelo de vídeo | `veo-3.1-generate-001` pela API, image-to-video a partir do snapshot | Testado em 12 gerações e automatizável; 19.391 créditos por take |
| A conta tem Seedance na API, ou o cliente quer o topo do ranking | Seedance 2.5 (720p, sem seed; no app, manual); antes, 1 teste barato com a persona como start_frame | Topo dos rankings de set/2026, bem à frente do Veo, mas nunca foi gerado nesta skill; tem filtro de rosto real; falha não é cobrada |
| Ensaiar ação e câmera barato | Veo 3.1 Fast (7.272 por 8 s, histórico) e versão final no Veo padrão | Não usado na sessão; o mesmo seed não reproduz em outro modelo |
| Modelo de imagem com a persona | `gpt-image-2.5-sunburst`, 9:16, 2K (1152x2048), high, ≈554 | Manteve a identidade; o `gemini-3-pro-image` afinou o rosto |
| Duração do vídeo | Medir pelo alignment: última palavra no vídeo + ~1 s. Ex.: Verão Conectado v5: narração de 326 caracteres = 19,06 s, última palavra em 19,44 s no vídeo (NARR_OFFSET 0,30) + ~1 s = 20,5 s | Medido; ritmo de referência: 294 caracteres ≈ 16,6 s (v2) |
| Cenário, roupa ou formato nunca gerado (loja, carro, casa, uniforme, inverno, noite, Stories) | Seguir o §8, fazer A/B no snapshot e avisar no portão 3 que a cena é nova | [não testado]; errar no snapshot custa ≈554, no vídeo 19.391 por geração |
| Composição aprovada, rosto pouco parecido ou refs novas | Edição de identidade (Image 1 = snapshot aprovado + 2 ou 3 refs) | Mantém o quadro aprovado; depois refaça os vídeos do take, porque o start_frame mudou |
| Snapshot reprovado por lugar, luz ou câmera | Regerar o snapshot mudando uma variável do prompt | A edição foi feita para manter o quadro; trocar cenário ou câmera nela reinventa tudo |
| Mesma cena com pose nova | Editar o snapshot aprovado, com a câmera no mesmo ponto | Mudar o ponto de vista numa edição reinventa o cenário |
| Defeito no take, mas sobra janela limpa | Recortar in/out | Zero crédito |
| Defeito sem janela limpa | Usar a outra variação; se as duas falham, regerar mudando 1 variável | 19.391 por take |
| Trocar uma frase ou o CTA | Gerar só a frase com `previous_text`, emendar e juntar os alignments (`api-elevenlabs.md` §5.5) | ≈1 crédito por caractere |
| O roteiro todo mudou | Regerar a narração inteira e refazer os tempos | Prosódia contínua |
| Música | Sem música (padrão); se pedirem, de −18 a −24 dB sob a voz | Sem música parece vídeo real; o nível com música não foi testado |
| Ela precisa falar na câmera | Modo falando: Veo 3.1 com a fala no prompt, troca de voz para a Radassa (`sts.py`), takes falados mudos no `prep.py` (`FALA`) e legendas pelo STT (`references/modo-falando.md`) | [vivido: teste de 13 s aprovado em 15/10/2026, 38.892 créditos]; até ~75 caracteres de fala por take; troca de voz e STT ~110 créditos |

## 5. Comandos essenciais

Rode de cima para baixo; cada bloco começa depois do preâmbulo. Todo `submit` aceito gasta créditos; recusas 403/422 e gerações que falham ou são moderadas não são cobradas.

**Preâmbulo** (repita em cada chamada do Bash: variáveis não passam de uma chamada para a outra):
```bash
export SKILL="$HOME/.claude/skills/reels-ia-realista"   # ou a "Base directory" que o Claude Code mostra ao carregar a skill; nunca "~" entre aspas
export PROJ="$HOME/hyperframes/<campanha>"               # pasta do projeto da campanha; nunca a do Verão Conectado (§7.2: só leitura; os exemplos gravam arquivos)
export HF="$PROJ/reels-final" QA="$PROJ/qa"
export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
mkdir -p "$PROJ"/{prompts,bodies,refs,locais,snapshots,takes,audio,qa} && cd "$PROJ"
```
- **Comandos demorados:** rode `poll_round.py`, `el.py wait` (vídeo) e `hyperframes render`/`check` com `timeout: 600000` na ferramenta Bash ou com `run_in_background` (6 Veo levaram ~3 min; cada render, ~2 min). Se o polling for interrompido, rode de novo: ele só faz GET e baixa o que já terminou.
- **Nomes da narração:** `bodies/tts_<vN>_s<seed>.json` → `audio/narracao_<vN>_s<seed>.wav` + `audio/narracao_<vN>_s<seed>_alignment.json`.

**Refs e snapshots** (texto do prompt: o molde de `prompts-moldes.md` §2.1–2.4 mais perto da cena; **[Voltec]** pule o upload: os asset_id estão no §7.1):
```bash
cp /home/syllas/hyperframes/voltec-reels-ia/refs/persona_headshot_sem_dedos.jpg refs/rosto_sem_dedos.jpg   # [Voltec] o rosto na7keiYvPpGArmyghOpk, para o A/B; outra persona: ponha a foto do rosto aqui
python3 -I "$SKILL/scripts/el.py" upload refs/rosto_sem_dedos.jpg          # imprime o asset_id (0 crédito); [Voltec] pule
jq -n --rawfile p prompts/T1_snapshot.txt --arg rosto "<asset_rosto>" --arg local "<asset_local>" \
  '{model_id:"gpt-image-2.5-sunburst", prompt:($p|rtrimstr("\n")), aspect_ratio:"9:16", resolution:"2K", quality:"high",
    images:[{type:"asset",asset_id:$rosto},{type:"asset",asset_id:$local}]}' > bodies/T1_gpt25.json
python3 -I - T1 <<'EOF'   # envio A/B (api-elevenlabs.md §2): o mesmo corpo 2 vezes (sem seed, varia; ≈554 cada)
import os, sys, json; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
T = sys.argv[1]; IDS, ids, body = f"snapshots/{T}_ids.json", {}, json.load(open(f"bodies/{T}_gpt25.json"))
for nome in (f"{T}_gpt25_a", f"{T}_gpt25_b"):
    st, r = el.submit("image", body); print(nome, st, r.get("id") if st == 200 else r)
    if st == 200:
        ids[nome] = r["id"]; json.dump(ids, open(IDS, "w"), indent=1)
EOF
python3 -I "$SKILL/scripts/poll_round.py" snapshots/T1_ids.json --kind image --out snapshots   # -> snapshots/T1_gpt25_a_<id>.png ...
ffmpeg -loglevel error -y -i "snapshots/T1_gpt25_a_<ID_A>.png" -i "snapshots/T1_gpt25_b_<ID_B>.png" -i refs/rosto_sem_dedos.jpg -filter_complex \
  "[0]scale=-2:960[a];[1]scale=-2:960[b];[2]scale=-2:960[c];[a][b][c]hstack=inputs=3" qa/T1_ab_ref.jpg   # A/B + ref para a página
# Escolhido o T1 base (qa-checklist.md §A), monte cada take seguinte e repita o envio A/B e o poll com o nome dele.
# Mesmo lugar = edição do T1 base (abaixo; ex.: Verão Conectado: T2). Lugar novo = + foto do local como 3ª imagem (ex.: T3).
jq -n --rawfile p prompts/T2_snapshot.txt --arg t1 "<gen_id do T1 base>" --arg rosto "<asset_rosto>" \
  '{model_id:"gpt-image-2.5-sunburst", prompt:($p|rtrimstr("\n")), aspect_ratio:"9:16", resolution:"2K", quality:"high",
    images:[{type:"generation",generation_id:$t1},{type:"asset",asset_id:$rosto}]}' > bodies/T2_gpt25.json
```

**Narração** (Fase 3, junto com os snapshots; settings e tags em `api-elevenlabs.md` §5; troca de frase e junção de alignments em §5.5):
```bash
VOZ="<voice_id>"; N=v1           # [Voltec] VOZ=4yvYc2GSakxLWMhlsd6b ("Radassa 100%"); roteiro em prompts/narracao_v1.txt
for S in 20261015 20261016; do   # A/B entre 2 seeds; ≈1 crédito/caractere cada
  jq -n --rawfile t prompts/narracao_$N.txt --argjson seed $S \
    '{text: ($t|rtrimstr("\n")), model_id: "eleven_v4", language_code: "pt",
      voice_settings: {stability: 0.45, similarity_boost: 0.85}, apply_text_normalization: "auto", seed: $seed}' > bodies/tts_${N}_s$S.json
  python3 -I "$SKILL/scripts/el.py" tts "$VOZ" bodies/tts_${N}_s$S.json audio/narracao_${N}_s$S          # .wav + _alignment.json
  python3 -I "$SKILL/scripts/stress.py" audio/narracao_${N}_s$S.wav audio/narracao_${N}_s${S}_alignment.json  # outra marca: --palavra REGEX --corte N
  python3 -I "$SKILL/scripts/stt.py" audio/narracao_${N}_s$S.wav | jq -r .text                          # tem de bater com o roteiro sem as tags
done
```

**Rodada de vídeo** (só depois do portão 3; 19.391 por take aceito):
```bash
python3 -I - <<'EOF'
import os, sys, json; sys.path.insert(0, os.environ["SKILL"] + "/scripts"); import el
R = ""   # 2ª rodada: R = "r" (vira T1r_veo_v1..., como na sessão) e SNAP só com os takes refeitos; os corpos da 1ª ficam intactos
SNAP = {"T1": "<gen_id T1 aprovado>", "T2": "<gen_id T2>", "T3": "<gen_id T3>"}   # um item por take aprovado (ex.: Verão Conectado: T1, T2 e T3)
IDS, ids = f"takes/veo{R}_ids.json", {}
for take, snap in SNAP.items():
    prompt = open(f"prompts/{take}_video_veo.txt").read().strip()
    neg = open(f"prompts/{take}_negative_veo.txt").read().strip()
    for v, seed in (("v1", 20260115), ("v2", 20260116)):
        body = {"model_id": "veo-3.1-generate-001", "prompt": prompt, "negative_prompt": neg,
                "start_frame": {"type": "generation", "generation_id": snap},
                "aspect_ratio": "9:16", "resolution": "1080p", "duration_secs": 8, "generate_audio": True, "seed": seed}
        json.dump(body, open(f"bodies/{take}{R}_veo_{v}.json", "w"), ensure_ascii=False, indent=1)
        st, r = el.submit("video", body); print(take + R, v, st, r.get("id") if st == 200 else r)
        if st == 200:
            ids[f"{take}{R}_veo_{v}"] = r["id"]; json.dump(ids, open(IDS, "w"), indent=1)
EOF
python3 -I "$SKILL/scripts/poll_round.py" takes/veo_ids.json --out takes   # 2ª rodada: takes/veor_ids.json; -> takes/<nome>_<id>.mp4 + status
```

**QA de cada take:** comandos e checklist em `qa-checklist.md` §B.

**Modo falando:** a voz sai dos takes. Rode `sts.py` em cada take escolhido e preencha `FALA` no `prep.py`. A narração em off acima só entra nos takes sem fala, e as legendas vêm do STT da mix (`references/modo-falando.md` §5–8).

Cama de SFX: `api-elevenlabs.md` §7 → `audio/ambiente_sfx.mp3`, com `duration_seconds` ≥ TOTAL/24 (máximo 30; 40 créditos/s) e o texto reescrito para a `<cena>` da campanha (ex.: Verão Conectado: casa de praia no fim de tarde).

**Edição, bloco 1: preparar** (HyperFrames testado na 0.8.161). O QR sai aqui, ANTES do `prep.py` e do render:
```bash
mkdir -p "$HF"/{assets,media,renders} && cd "$HF"
cp "$SKILL/scripts/index_template.html" index.html; cp "$SKILL/scripts/prep.py" "$SKILL/scripts/build_legendas.py" .
cp /home/syllas/hyperframes/verao-conectado/assets/logo-voltec.png assets/logo.png; cp assets/logo.png assets/logo-cta.png   # [Voltec] logo oficial, fixa (§7.1)
[ -d "$FERR/qr/node_modules/jsqr" ] || (mkdir -p "$FERR/qr" && cd "$FERR/qr" && npm i qrcode@1.5.4 jsqr@1.4.0 pngjs@7.0.0)   # 1ª vez: precisa de rede
node -e 'require("qrcode").toString(process.argv[1], {type: "svg", errorCorrectionLevel: "M", margin: 0,
  color: {dark: "#111111", light: "#ffffff"}}, (e, s) => { if (e) throw e; require("fs").writeFileSync("assets/qr.svg", s); });' "<URL>"   # URL respondida no portão 1
```

**Pare e edite** antes do bloco 2 (detalhes em `edicao-hyperframes.md` §4–8 e na tabela de tokens e campos `PREENCHA` do §13; conferência antes do render em `qa-checklist.md` §C.0):
- `prep.py`: `SEGMENTS`, `TOTAL`, `NARR`, `NARR_OFFSET` e `BED`.
- `build_legendas.py`: `ALIGN`, `PHRASES` e `CTA_START` (= `T.cta` do index). Num projeto novo, `START_FIX` e `LOW_RANGES` começam vazios e só são preenchidos depois de medir com `stt.py --ss/--t`.
- Os tokens `__…__` e os `EDITAR` do `index.html`: gancho, título do cartão da campanha e ícone opcional, oferta, CTA (pago × orgânico), tempos `T` e duração em 5 lugares (`TOTAL/24`). Depois, `grep -nE '__[A-Z0-9_]+__' index.html` não pode imprimir nada.

**Edição, bloco 2: render e versões.** O render da 0.8.161 é best-effort: sem `assets/qr.svg`, sairia sem QR e sem erro. Por isso o `--no-best-effort` (falha em vez de sair sem a mídia) e o decode no fim.
```bash
cd "$HF"; V="<campanha>_vN"; T_QR="<instante com o QR na tela, em s>"   # Verão Conectado v5: V=verao-conectado-reels-ia_v5, T_QR=18.6
python3 prep.py                  # media/base.mp4 + media/mix.wav; "python3 prep.py audio" refaz só o áudio
python3 build_legendas.py        # injeta as legendas no index.html
npx --no-install hyperframes lint
npx --no-install hyperframes check
npx --no-install hyperframes render -o "renders/$V.mp4" --fps 24 --quality delivery --no-best-effort
npx --no-install hyperframes render -o "renders/${V}_legendas.mp4" --fps 24 --quality delivery --no-best-effort --variables '{"legendas":true}'
for v in "$V" "${V}_legendas"; do ffmpeg -loglevel error -y -i "renders/$v.mp4" -c:v libx264 -preset slow -crf 19 -maxrate 20M \
  -bufsize 40M -profile:v high -level 4.2 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart "renders/${v}_instagram.mp4"; done
ffmpeg -loglevel error -y -ss "$T_QR" -i "renders/${V}_instagram.mp4" -frames:v 1 "$QA/qr.png"
node "$SKILL/scripts/decode.cjs" "$QA/qr.png"   # tem de imprimir a URL do QR
```
Receita completa do QR: `edicao-hyperframes.md` §11.1 (gerar e conferir se a página está no ar) e §11.2 (decodificar na master e no Instagram). O bloco automático de QA final, que roda nos 4 arquivos, está em `qa-checklist.md` §C.

## 6. Mapa dos arquivos

| Arquivo | Para que serve |
|---|---|
| `references/modelos-e-custos.md` | Placar de vídeo datado, Veo na prática, status da conta, teste de acesso sem custo, modelos de imagem, custos (medido/histórico/doc/estimado) e orçamento |
| `references/api-elevenlabs.md` | Endpoints, corpos JSON reais, pegadinhas do Veo, polling, TTS e emenda de frase, STT, SFX, música e tabela de erros |
| `references/prompts-principios.md` | Como escrever: 12 princípios e "Checklist do prompt" (§1), armadilhas vividas (§3) e moderação (§4) |
| `references/prompts-moldes.md` | Fluxo e envio (§0) e moldes completos (§2: snapshot, pose, selfie, identidade, Veo, negativos, Seedance, narração; 2.9 molde-base de cena; 2.10 cena interna, noturna ou com roupa nova). Arquivo grande: leia por seção (Grep `^### 2\.` + Read com offset/limit) |
| `references/locais-grussai.md` | Grussaí real (sol por estação, vento do verão, receitas de cena do exemplo, fotos licenciadas) e método para qualquer lugar: fotos (§7), sol (§8) e lugar no prompt (§9) |
| `references/persona-e-marca-voltec.md` | Persona, âncoras de texto, assets, edição de identidade, voz Radassa, marca, QR, CTA, publicação e a personagem em cada cenário (§10). Arquivo grande: leia por seção (Grep `^##` + Read com offset/limit) |
| `references/edicao-hyperframes.md` | Pastas, in/out em quadros, `prep.py` e mixagem, index, legendas, lint/render, Instagram e ajustes rápidos |
| `references/qa-checklist.md` | Portões A (snapshot), B (take), C (vídeo final) e D (verificação independente), com comandos |
| `references/modo-falando.md` | Ela falando para a câmera: fala por take, snapshot, prompt do Veo com fala, troca de voz, QA de sincronia, edição e legendas; testado e aprovado em 15/10/2026 |
| `scripts/el.py` | Biblioteca e CLI da API (upload, submit, get, wait, tts); lê a chave sem imprimir |
| `scripts/poll_round.py` | Espera e baixa uma rodada salva como `{nome: generation_id}` (só GET) |
| `scripts/stt.py` | Transcrição scribe_v1 para QA, com `--ss`, `--t` e `--out` |
| `scripts/stress.py` | Tônica da marca medida pelo alignment do TTS (`--palavra`, `--corte`) |
| `scripts/sts.py` | Troca de voz (speech-to-speech) de um take para a voz da persona, com o mesmo tempo; confere a duração |
| `scripts/stt_alinhamento.py` | STT (`stt.py`) → alignment por caractere, para as legendas do modo falando |
| `scripts/decode.cjs` | Lê o QR de quadros PNG (jsQR); sai com 1 se não ler |
| `scripts/prep.py` | Molde: cortes por quadro, fim congelado, grão e mix a −14 LUFS; `FALA` para takes falados |
| `scripts/build_legendas.py` | Molde: legendas pelo alignment, injetadas no index |
| `scripts/index_template.html` | Molde da composição HyperFrames 9:16: tokens da campanha (gancho, cartão, oferta), cidades, CTA, QR e legendas por variável |
| `scripts/flows_submit_poll.sh` | Alternativa em curl + jq: envia, faz polling com backoff e baixa |

## 7. [Voltec] Dados da Voltec (troque em outro cliente)

### 7.1 Fixos da Voltec com a personagem (valem em todo vídeo)

- **Persona:** a da conta ElevenLabs (fotos de uniforme, carro e loja), "an adult Brazilian woman, about 26 years old", sem joias nem tatuagens no prompt, com as âncoras de rosto, pele e mãos copiadas igual (persona §3.1–3.3). Assets na conta (não suba de novo): rosto sem dedos `na7keiYvPpGArmyghOpk`, rosto da loja `pUgU1HXgmdqXfP02iR8T`, corpo sem logo `ZY1iDcJLhPFklahPnvkM`. Não use os frames da selfie antiga (outro rosto), a foto com headset, a da passarela (rosto pequeno), a da loja com o letreiro VOLTEC (`bZiCdj3zIGYdX0UKyfvU`) nem o uniforme com o logo bordado (`9snOZM2EfiYIjKtqfsW2`; use o corpo sem logo).
- **Voz:** "Radassa 100%" `4yvYc2GSakxLWMhlsd6b` (principal; `eHs9HKeucCzJ3ChAjmII` só para A/B), eleven_v4, 0.45/0.85, `"pt"`, `wav_48000`. No TTS, "Voltéc" (vol-TÉC) e números por extenso; na tela, "Voltec" e algarismos.
- **Textos fixos:** cidades Grussaí, Atafona, Chapéu do Sol e São João da Barra, nesta ordem (cartão "Tem Voltec em" e linha do CTA); CTA pago "Clica no botão Saiba Mais ou escaneia o QR code na tela!"; CTA orgânico "Assina pelo link na bio!". Qual dos dois vai é slot (§1b).
- **QR:** nunca o WhatsApp (o usuário trocou explicitamente). O destino é slot: pergunte e confira se a página está no ar com curl e headers de navegador (o site devolve 406 ao curl simples; `edicao-hyperframes.md` §11.1).
- **Marca:** logo para fundo claro em `/home/syllas/hyperframes/verao-conectado/assets/logo-voltec.png` (a pasta é do projeto HyperFrames anterior; a logo é a oficial, de toda campanha), sempre sobre cartão branco; **nunca redesenhe a logo** nem a mande ao gerador. Cores `#d7262f` e `#2f2f33`; fontes Montserrat 800/900 e Barlow 600/700. Sem música.
- **Área atendida:** Grussaí é plana, com a praia voltada para o leste (~95°): o sol nasce no mar e **nunca se põe no mar**, em nenhuma estação. Mar cinza-azulado ou oliva, nunca turquesa; casuarinas tortas; casas baixas. Nunca escreva "Avenida Atlântica", "RJ", "Brazil" ou "Grussaí" no prompt. A orla de Atafona não é recomendada como cenário (erosão, conotação negativa; `locais-grussai.md` §2 e §10); Chapéu do Sol não tem foto aberta. Sol por data e hora: `locais-grussai.md` §3 e §8. Foto da restinga já na conta: `Mf1kechhOOoqJO70sPNd` (CC BY 4.0, Pablo Cauã da Silva Toledo).
- **Conta (15/10/2026):** Veo liberado; modelos ByteDance com 403 `model_access_denied` na API; nenhum webhook inscrito; plano growing_business com 5,22 milhões de créditos por ciclo.

### 7.2 Exemplo preenchido: Verão Conectado (15/10/2026)

O caso de referência testado, com os slots do §1b preenchidos. É molde de preenchimento, nunca padrão.

| Slot | Verão Conectado |
|---|---|
| Tema e formato | Promoção sazonal de verão (casa de praia sem internet); Reels 9:16 para anúncio pago, com botão; 3 takes |
| Cenário, horário e luz | Orla de Grussaí: varanda do 2º andar de uma casa de frente para o mar e a areia em frente; ~17h de meados de janeiro, sol a ~19,5° atrás das casas (luz quente, ainda não dourada; dourado só a partir de ~17h40); vento nordeste (`locais-grussai.md` §3–§5) |
| Roteiro de takes | T1 varanda, celular erguido sem sinal, frustrada (amiga filmando); T2 rede, chamada de vídeo, risada de boca fechada; T3 selfie andando na areia |
| Roupa | Saída de praia de crochê branca de trama grande sobre regata branca e short jeans claro (persona §3.4) |
| Objeto na mão | Celular de capa preta fosca sem logo, com a tela virada para ela (no T3 ele é a câmera) |
| Som ambiente | Brisa do mar e mar distante (T1, T2) ou ondas na areia (T3); vento no microfone; tecido (T1) e rangido da rede (T2) |
| Gancho | "Casa de praia / sem internet?", no céu do T1 |
| Oferta | "Planos sem fidelidade" + "de 2 a 5 meses" (na voz, "dois a cinco") |
| CTA | Anúncio pago: a frase paga do §7.1 e o cartão "clique em Saiba mais" + QR. Até a v3 era "link na bio" (resposta inicial), trocado quando o cliente avisou que o anúncio teria botão |
| Destino do QR | `https://provedorvoltecinternet.online/?page_id=674`, página "Verão Conectado 2026" (no projeto, `assets/qr-checkout.svg`) |
| Duração | 20,5 s = 492 quadros (última palavra em 19,44 s) |
| Cartão da campanha | "VERÃO ☀ CONECTADO" (sol como ícone) |
| Cama de SFX | `audio/ambiente_praia_sfx.mp3`, 20 s, casa de praia no fim de tarde (texto em `api-elevenlabs.md` §7) |
| Legendas | `START_FIX` [("internet?", 1, 1.38), ("Voltec", 1, 5.32), ("Voltec", 2, 8.03)], `LOW_RANGES` [(0.0, 3.70)], `CTA_START` 15.40; `FIX` com `"dois": "2"` e `"cinco": "5"` além do `"Voltéc": "Voltec"` |

- **Projeto (só leitura):** `/home/syllas/hyperframes/voltec-reels-ia/` (prompts/, bodies/ com `assets.json`, snapshots/, takes/, audio/, refs/, locais/, reels-final/). Memória: `voltec-reels-ia-producao.md`.
- **Página:** https://claude.ai/artifact/MivTjGgrZ9ZyhZTftP66kh (storyboard + vídeo); serve de modelo, mas campanha nova vai numa página nova.
- **IDs:** snapshots finais (`start_frame`) T1 `HInXH8bxSo6aEH0mUmup`, T2 `e7k1uG3FnY3q8R0oUuCG` e T3 `O2D10yzDXIp2eu8jbhtj`, editados (identidade) a partir de T1-A `5vBTv3B9FOt44Vu8jMY4`, T2-A `0fZysnZPt1Xmk1RaJF5H` e T3-A `gXl0EPY5A3LhPnLlHbBv`. Takes da v5: `T1r_veo_v1_bICA18jbanp0KfqE3fgS` (in 19, 89 quadros), `T2r_veo_v1_RvTRU6nLzVKOEUqVWUh5` (62, 101) e `T3r_veo_v2_R41wQEvLdexHBvaXIRsl` (5, 187), mais 115 quadros congelados.
- **Narração:** `audio/narracao_v3.wav` + `_alignment.json` = `narracao_v2_A_s1` (seed 20261015) + CTA `cta_v3_20261017` emendado em 15,05 s (+0,17 s, −3 dB); roteiro em `prompts/narracao_v3.txt` (persona §6) e montagem em `audio/COMO_FOI_MONTADA_narracao_v3.txt`; `NARR_OFFSET` 0,30.
- **Entrega v5:** `/home/syllas/hyperframes/voltec-reels-ia/reels-final/renders/verao-conectado-reels-ia_v5{,_instagram,_legendas,_legendas_instagram}.mp4` (enviados ao cliente como `Verao_Conectado_REELS_IA_v5_{master,instagram}.mp4` e `..._v5_legendas_{master,instagram}.mp4`). A v3 e a v4 são antigas (a v3 ainda tem o "link na bio").

## 8. Cenas, roupas e formatos nunca gerados [não testado]

Nada desta seção foi gerado: são as regras do §3 e das references aplicadas a cenas novas. Em toda cena nova, faça A/B no snapshot (≈554 cada), revise com `qa-checklist.md` §A e avise no portão 3 que a cena é nova; vídeo só depois do OK. Fato de lugar sem fonte nas references fica marcado "não pesquisado: pesquise com `locais-grussai.md` §7–§9" e nunca é inventado no prompt. Detalhes: `persona-e-marca-voltec.md` §10 (a personagem em cada cenário) e §3.4 (âncoras de roupa e objeto), `locais-grussai.md` §10 (lugar por lugar) e `prompts-moldes.md` §2.9–2.10 (molde-base de cena e adaptação de luz, som e objeto).

- **Vale em qualquer cena** (§3): um lugar, uma hora e uma ação por take; câmera com dono, um movimento só e nada que revele área nova; uma fonte de luz real, com direção, igual em todos os takes; um objeto já no 1º quadro, inteiro e sem tela à mostra; lábios fechados sob a narração; nenhum texto, placa, tela legível ou logo no quadro (a marca entra só nos cartões); 3 a 5 elementos fixos do fundo, com as mesmas palavras em todos os prompts (`locais-grussai.md` §9).
- **Riscos que as refs da conta já mostraram** [vivido], válidos em todo cenário: o letreiro VOLTEC da loja e o logo bordado do uniforme vazam texto e vermelho para a cena; o headset vaza; rosto pequeno no quadro não segura a identidade. Parte das refs é imagem gerada [pesquisa]: não prova como são a loja ou o carro reais. Use só os assets do §7.1 e escreva o cenário em texto (ou com fotos do cliente sem texto).

| Cena | Como derivar [não testado] | Riscos e o que falta |
|---|---|---|
| Loja da Voltec | Fotos da loja real feitas pelo cliente, sem letreiro, cartaz, placa ou tela legível (ou recortadas); câmera de costas para o letreiro e a fachada, fundo liso; uma fonte de luz que apareça nas fotos, com direção; objeto liso, sem logo nem etiqueta; nada de "Voltec" no prompt | A foto da conta com o letreiro VOLTEC enorme vaza texto e não serve de foto do local; o notebook da ref com headset tem a marca legível. Interior, luz e móveis da loja real: não pesquisado: pesquise com `locais-grussai.md` §7–§9 |
| Carro | Carro parado (nunca ela dirigindo com o celular na mão); selfie a um braço (`prompts-moldes.md` §2.3) ou amiga no banco ao lado; do peito para cima; luz do dia por uma janela, com direção; emblema do volante, painel e placas fora do quadro; som só do que o microfone captaria ali (`prompts-principios.md` §1.11) | Carro andando: a janela revela paisagem nova a cada quadro (área revelada é área inventada, `prompts-principios.md` §1.2). Retrovisor e vidros podem refletir quem filma [pesquisa]. O rosto `na7keiYvPpGArmyghOpk` vem de uma foto no carro: mantenha "ignore the car interior behind her" e descreva o carro da cena no texto |
| Casa (sala, quarto, home office) | Fotos do cliente ou só descrição física; luz de uma janela ou luminária, com direção e hora; celular com a tela virada para ela, ou roteador liso parado num móvel (ela não o manipula); TV e telas desligadas ou fora do quadro | Sem foto do lugar, o snapshot vai só com o rosto em `images` (o T1 testado tinha rosto + foto do local). Espelhos refletem quem filma [pesquisa] |
| Uniforme liso sem logo | Âncora de uniforme liso da persona §3.4 (`without any logo, print, embroidery or lettering`), com o peito revisado a 100% | O uniforme real tem logo bordado. Na edição de identidade com o uniforme na Image 1, mantenha o texto do molde (o "ignore ... the red uniform" fala das refs, não da Image 1), descreva a polo no `{OUTFIT}` com a versão curta da âncora e confira o peito a 100% (persona §5; `prompts-moldes.md` §2.4). A marca nunca vai na roupa, só nos cartões |
| Outro ponto da região (Atafona, Chapéu do Sol, lagoa, calçadão, centro de São João da Barra) | Fotos do cliente ou achadas e provadas pelo método de `locais-grussai.md` §7; sol pelo §8 com as coordenadas do ponto; um lugar só por vídeo | Atafona: erosão, só se o cliente insistir e sem ruína no quadro; Chapéu do Sol não tem foto aberta; a lagoa não se mistura com praia no mesmo vídeo; quiosques e calçadão só têm fotos NC, cheias de texto e marcas (`locais-grussai.md` §2 e §5.3), e o calçadão em ondas puxa Copacabana (`prompts-principios.md` §3.3). O resto: não pesquisado: pesquise com `locais-grussai.md` §7–§9 |
| Outra estação em Grussaí | Sol pela tabela "Outras estações" de `locais-grussai.md` §3 (a luz do exemplo, sol a ~19,5°, cai por volta de 16h00–16h20 no outono e na primavera e de 15h40 no inverno; no inverno, a selfie em contraluz caminha para o sul, com o mar à direita); roupa nova no estilo da persona §3.4 (lá há um exemplo de inverno); tire do prompt os trechos de verão do exemplo (`about 5 pm in summer`, `sun-flushed`, a brisa do mar) | Vento, céu, clima e movimento da praia fora do verão: não pesquisado: pesquise com `locais-grussai.md` §7–§9 |
| Noite | Uma fonte real e com direção (poste, luminária, janela acesa), a mesma em todos os takes; troque "crisp daylight frames" por ruído de celular no escuro; nada de ajuste de exposição; rosto iluminado, em plano médio; mãos e boca revisadas a 8 e 24 fps | Tela acesa vira interface: continua virada para ela. A orla tem postes de luz finos do lado do mar (`locais-grussai.md` §2), mas como ela fica à noite: não pesquisado: pesquise com `locais-grussai.md` §7–§9 (a foto noturna do calçadão é NC: só referência) |
| Stories ou outra duração | 9:16 igual; vídeo mais longo = mais takes (uma ação cada, no mesmo lugar e na mesma hora), não take mais longo: na API, 1080p só sai com 8 s; cada take a mais custa 38.782 (2 variações) | Zona segura do Stories não pesquisada (a do template é a do Reels): confirme antes de posicionar texto |
