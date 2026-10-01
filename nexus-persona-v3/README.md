# NEXUS PERSONA — FASE 3 AUDIOVISUAL
## O que foi implementado
- Interface V3 construída sobre a V2 (perguntas institucionais, TTS, microfone, backend opcional privado).
- Estúdio local: carregamento de vídeo aprovado MP4/WEBM **que já contenha voz e sincronização labial**.
- Player com pausa, retomada, tela cheia; upload de legendas revisadas WEBVTT.
- Opção para áudio aprovado em MP3/WAV/M4A acompanhado de fotografia estática.
- Teleprompter editável; modo de alto contraste.
- O usuário seleciona vídeos/áudios e foto localmente; a interface NÃO envia esses arquivos a nenhum servidor.
- Quando o público faz uma pergunta inédita, para o vídeo de apresentação e usa resposta por síntese do navegador ou backend autorizado. A foto permanece estática: nenhum falso lip sync.

## Testar
Abra `index.html` no Chrome ou Edge; para microfone, prefira publicar em HTTPS.
1. Carregue a fotografia original. Veja o enquadramento.
2. Carregue um clipe **autorizado e já dublado/sincronizado** e clique "Reproduzir clipe aprovado".
3. Opcional: carregue `.vtt` com os tempos efetivamente revisados. Teste legenda e tela cheia.
4. Pressione "Apresentar projeto", depois escreva uma pergunta. Confira que o vídeo para e a resposta vem da base.
5. Carregue um áudio aprovado, sem vídeo, e confirme que a foto permanece estática.
6. Teste "Parar", contraste, exportação e microfone (com consentimento).
**Atenção:** vozes pt-BR, en-US etc. disponíveis variam por navegador/sistema; selecionar idioma NÃO traduz automaticamente o texto.

## Produção no Blender
`blender_nexus_stage.py` é um estágio gratuito **2.5D** com fotografia original:
```bash
blender -b -P blender_nexus_stage.py -- "/caminho/foto-autorizada.png"
```
Gera `NEXUS_PERSONA_2_5D_SEM_AUDIO.mp4`, plano cinematográfico de 12s. **Não gera boca, expressões nem sincronização labial.** A versão final mantém o áudio previamente aprovado:
```bash
ffmpeg -i NEXUS_PERSONA_2_5D_SEM_AUDIO.mp4 -i narracao_aprovada.mp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -shortest NEXUS_PERSONA_APRESENTACAO.mp4
```
Esse comando apenas sincroniza faixas por início e recorta na menor duração; não sincroniza o movimento da boca.

## Para lip sync facial REAL (próximo marco técnico)
1. Aprovar modelo facial 3D fiel à fotografia; obter referência de frente e laterais quando possível.
2. Desenvolver malha, rig, olhos, pálpebras, boca e shape keys de visemas.
3. Gerar visemas temporizados com base em **áudio aprovado**, revisar manualmente boca/dentes e microexpressões.
4. Renderizar um vídeo MP4/WEBM de apresentação. Descartar áudio temporário de qualquer gerador; reinserir áudio limpo autorizado.
5. Subir esse MP4 já sincronizado na interface V3. Respostas ao vivo só terão lip sync real com um pipeline **de geração/visemas em tempo real** adicional, que não está implementado.
6. Exibir sempre identificação do personagem como avatar digital.
Não use referência frontal isolada para inventar anatomia exata de perfis/orelha/mandíbula.

## Critérios de aprovação
Sem substituição genérica do rosto; nenhuma alteração artificial da idade. Testar o clipe após mux, verificar duração, início de voz, sincronia labial por pontos de checagem, legendas, status dos controles, fundo institucional convencional, acessibilidade e privacidade.
