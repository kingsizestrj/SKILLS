# SKILLS

Skills do Claude Code criadas nas nossas sessões.

| Skill | Para que serve |
|---|---|
| [reels-ia-realista](reels-ia-realista/SKILL.md) | Vídeos realistas com IA da Voltec estrelados pela personagem da marca, em qualquer campanha. O fluxo cobre pesquisa de locais reais, snapshots aprovados antes do vídeo, Veo 3.1 e narração com a voz Radassa pela ElevenLabs, e edição no HyperFrames com legendas, CTA e QR. |

## Como instalar uma skill

1. Clone este repositório.
2. Copie a pasta da skill para `~/.claude/skills/`. Exemplo:

```bash
cp -r reels-ia-realista ~/.claude/skills/
```

O Claude Code carrega a skill sozinho quando o pedido combina com a descrição dela. Também dá para chamar pelo nome, por exemplo `/reels-ia-realista`.

Nenhuma skill daqui guarda chave de API ou senha. As chaves ficam só na máquina, por exemplo em `~/.config/elevenlabs/env`.
