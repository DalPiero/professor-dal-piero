# NEXUS PERSONA V7 — Fotografia + voz + trejeitos REAIS do Filme 2

## Entrega implementada
`index.html` conserva a interface de perguntas do NEXUS V6 e acrescenta o modo **Presença digital — Filme 2**.

- A foto padrão é a fotografia institucional autorizada enviada ao projeto.
- Um clique em **Apresentar com o Filme 2** exibe o próprio arquivo MP4, com **seu áudio original e as expressões efetivamente presentes no filme**, sem substituir o rosto ou refazer voz.
- Em **Abrir perguntas**, o filme é pausado e a interface utiliza o banco institucional local, ou servidor opcional em sessão privada. **Perguntas inéditas usam voz do navegador**, claramente diferente da voz original; a voz do filme NÃO consegue pronunciar frases novas simplesmente por estar num arquivo MP4.
- O operador pode **marcar manualmente** início/fim de piscadas, sobrancelhas, olhar, movimentos de cabeça, pausas, movimentos labiais e postura. As marcas são exportadas em JSON de referência. Nenhuma classificação automática das expressões ou treinamento biométrico é feito nesta etapa.
- A aplicação impede sobreposição intencional do som do filme 2 com o player anterior; perguntas interrompem a reprodução do filme.

## Teste
1. Baixe esta ramificação e abra `nexus-persona-v7/index.html` com internet.
2. Confira a fotografia na abertura; clique em **Apresentar com o Filme 2** e escute a gravação.
3. Escolha pontos onde o rosto esteja bem visível, marque início e fim do gesto e selecione a categoria. Confira a reprodução e exporte o JSON.
4. Clique em **Abrir perguntas**; use texto/microfone e confirme que o vídeo original pausa e que a resposta NÃO finge ser gravação original.
5. Verifique visualmente se voz e boca do próprio Filme 2 coincidem; essa auditoria não foi concluída automaticamente.

## Próxima fase — avatar com fala espontânea e gestos fiéis
Um arquivo pré-gravado resolve **apresentações com a voz e gestos reais**; não resolve sozinho **respostas inéditas com a mesma voz e o mesmo rosto articulado**.
Para a versão em tempo real:
- Rever as imagens reais do filme 2 para decidir quais trejeitos, ângulos e visemas são observáveis. Não afirmar o que não foi conferido.
- Revisar a malha do V5 contra a referência frontal e possíveis vistas laterais autorizadas.
- Retarget manualmente as referências para head/eyebrow/eye/mouth controllers ou usar rastreamento facial autorizado, com revisão artística.
- Sintetizar respostas novas por serviço de voz autorizado **no servidor**, preservando credenciais fora do navegador, conforme orçamento e consentimento; não há serviço gratuito/clonado integrado nesta V7.
- Obter tempos de fonemas/visemas da **mesma gravação aprovada**, dirigir o rig e comparar rigorosamente boca/voz. Só então chamar de lip sync facial.
- Manter a identificação de avatar digital para o público, oferecer alternativa em texto e respeitar retenção/consentimento nas perguntas.
- Reutilizar os dois vídeos para apresentações pré-gravadas e não misturar suas falas fora de contexto.

## Arquivos-fonte de mídia
Filme 1: `https://cdn.creativeclaw.co/u/5dd90fe8/videos/0228548f-b112-414c-9815-7cbff820e3ce.mp4`
Filme 2: `https://cdn.creativeclaw.co/u/5dd90fe8/videos/11cead6e-fce2-4fe3-a730-552bcea8d253.mp4`
Foto: `https://cdn.creativeclaw.co/u/5dd90fe8/images/1d6c7262-d831-4938-8dba-fee75fd88dae.png`

## Custos, segurança e estado
Nenhuma operação paga de geração foi executada na V7. Os MP4 e a foto são servidos externamente e necessitam conexão. O arquivo HTML foi verificado quanto à sintaxe, mas é necessário testar reprodução e microfone no dispositivo de apresentação. A análise automática dos quadros foi bloqueada por saldo 0; **não há laudo visual de lip sync**.
