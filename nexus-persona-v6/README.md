# NEXUS PERSONA V6 — dois filmes integrados à interação ao vivo

## O que foi realizado
Foram pré-configurados os dois arquivos entregues pelo usuário:
- **1Conhecimento Deve Circular.mp4** → [abrir vídeo 1](https://cdn.creativeclaw.co/u/5dd90fe8/videos/0228548f-b112-414c-9815-7cbff820e3ce.mp4)
- **2Conhecimento Deve Circular.mp4** → [abrir vídeo 2](https://cdn.creativeclaw.co/u/5dd90fe8/videos/11cead6e-fce2-4fe3-a730-552bcea8d253.mp4)

O novo `index.html` reaproveita a interface V4 (foto automática, respostas, voz, microfone, teleprompter, vídeo autorizado) e acrescenta:
- **Filme 1**, **Filme 2** e **Apresentação completa (1 + 2)**, com reprodução dos áudios **originais**, sem custo de geração;
- Encerrada a apresentação, continua no **modo de perguntas**, com respostas da base institucional e síntese de voz do navegador;
- A pergunta interrompe o clipe em execução e desativa a sequência para que a gravação não concorra com a resposta;
- Controle de volume, seleção de 25/50/75% de cada filme para inspeção, checklist humano de identidade/voz/lábios;
- Upload local alternativo caso a CDN não esteja disponível. Os vídeos ficam na nuvem do acervo existente; **o ZIP não contém os MP4 fisicamente**.

## Testar em 2 minutos
1. Baixe o ZIP deste ramo, abra `nexus-persona-v6/index.html` no Chrome/Edge **com internet**.
2. Confirme a imagem de referência do apresentador.
3. Pressione **Apresentação completa (1 + 2)**. Se o navegador impedir reprodução, clique Play no próprio vídeo.
4. Escute atentamente os dois áudios originais. O modo de perguntas funciona ao fim da sequência ou se clicar em **Encerrar apresentação**.
5. Digite uma pergunta sobre BRASIL 2075 ou permita o reconhecimento de fala do navegador (requer consentimento).
6. Abra **Revisão visual e sincronização (operador)** e confira quadros a 25%, 50% e 75%, além de toda fala em movimentos reais. Não marque os critérios sem ver o conteúdo.

## O que esses filmes operacionalizam efetivamente
**Sim:** um avatar de apresentação **baseado em clipes autorizados**, seguido de diálogo em texto + voz de navegador durante a sessão, sem consumo de créditos de vídeo. Se os clipes forem do rosto real do apresentador e suas bocas estiverem sincronizadas com a própria narração, esse desempenho estará presente **somente enquanto o clipe toca**.

**Não:** os vídeos não garantem rig facial, malha volumétrica anatomicamente fiel ou sincronização labial **ao vivo** de qualquer frase. Durante perguntas livres, a fotografia permanece estática e as respostas usam a voz disponível pelo navegador. Não extrapole visemas de uma gravação para outra sem gerar/controlar sequências novas e revisar seus tempos.

## Revisão de pré-produção
- Confirmar se ambos exibem claramente o rosto do mesmo apresentador. Se contiverem apenas slides, não servem como base de captura de expressão facial.
- Identificar trechos de fala em close frontal com boa iluminação, boca e mandíbula livres.
- Separar clipes de **repouso**, fala, piscadas e transição apenas se as imagens realmente permitirem.
- Verificar movimentos de cabeça, cortes, compressão, máscaras, barba e óculos: os ângulos devem manter geometria coerente.
- O segundo vídeo só serve como complemento para captura facial quando contém vistas úteis, em vez de apenas material gráfico.
- Use áudio limpo previamente aprovado para qualquer etapa de lip sync de um rig 3D; não substitua sem autorização.

## Auditoria técnica gratuita
Em `scripts/audit_videos.sh` existe uma auditoria opcional FFmpeg para metadados, amostras visuais, nível de áudio e intervalos de tela escura. Execute em Linux/WSL:
```bash
bash nexus-persona-v6/scripts/audit_videos.sh video1.mp4 video2.mp4
```
O script gera um diretório de auditoria, **não** efetua reconhecimento facial, transcrição ou verificação labial. É necessário inspeção humana das imagens e áudio.

**Estado:** V6 em testes. O ambiente de revisão automática não conseguiu extrair os quadros nesta sessão porque a conta do serviço de quadros está sem créditos; não declarar que a sincronia labial dos vídeos foi comprovada. O roteiro técnico de Blender V5 permanece independente desta avaliação.
