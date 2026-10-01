# NEXUS PERSONA — FASE 4 (FOTO INTEGRADA / AUDITÓRIO / PREPARO PARA LIP SYNC)
**Status: protótipo em testes.** Não foi implementado um rosto 3D fotorrealista nem lip sync ao vivo.
## 1 — Abrir e ver a fotografia imediatamente
Abra `index.html` nesta pasta no navegador **com acesso à internet**. Agora a foto autorizada está **preconfigurada** e aparece na abertura; não é mais obrigatório selecioná-la. Imagem de referência da apresentação: https://cdn.creativeclaw.co/u/5dd90fe8/images/1d6c7262-d831-4938-8dba-fee75fd88dae.png. O HTML carrega a imagem deste endereço; no primeiro acesso, a internet é necessária. Se estiver sem rede, baixe essa foto e use **Selecionar fotografia** — a aplicação mostra mensagem clara quando a imagem remota não pode carregar. O carregamento local não envia a foto para a nuvem do protótipo.
## 2 — Apresentação + perguntas do público
- Apresentação institucional com voz sintética do navegador;
- Perguntas digitadas ou microfone autorizado; modo auditório com leitura automática de respostas;
- Base local sem custo; opcionalmente servidor próprio para perguntas inéditas;
- Player para vídeo de avatar APROVADO com voz e boca já sincronizadas; legendas WEBVTT; teleprompter e tela cheia;
- Botão para restaurar a foto oficial e indicar se houver falha.
O vídeo só terá sincronização labial real se **já tiver sido produzido e aprovado** com sincronização. Para respostas inéditas, a foto permanece estática com movimento sutil de enquadramento, e a barra mostra atividade de áudio sem fingir boca articulada.
## 3 — Próxima fase Blender: rig facial real
Incluí `aplicar_visemas.py`, um SCRIPT DE PRODUÇÃO que importa a sequência de visemas gerada pelo Rhubarb Lip Sync e anima shape keys **num rosto tridimensional previamente modelado, autorizado e aprovado**. Ele não converte sozinho uma única foto frontal em um rosto tridimensional fiel. Para utilizá-lo:
1. Produza ou aprove um busto 3D do apresentador. Confirme olhos, barba, pele, óculos e perfis com referências adicionais;
2. Configure shape keys MOUTH_A, MOUTH_B, ..., MOUTH_H na malha;
3. Gere `boca.json` com Rhubarb a partir do áudio autorizado (`rhubarb -f json -o boca.json narracao.wav`);
4. Abra o .blend e selecione a malha facial;
5. Execute `blender projeto.blend -b -P aplicar_visemas.py -- boca.json narracao.wav`;
6. Revise em vídeo todos os fonemas, inícios e encerramentos de frases, piscadas, dentes e falhas de rig; depois renderize;
7. Reinsira a gravação limpa aprovada no MASTER final. Não publique sem teste de sincronização, privacidade e identidade.
A documentação oficial de Blender contempla shape keys como controles de deformação e Rhubarb exporta JSON com mouthCues A–H/X. Trata-se de uma etapa técnica preparada, não de um avatar 3D já concluído.
## 4 — Limitações técnicas e privacidade
A foto **preconfigurada** é externa e aparece com internet; não está fisicamente embutida no ZIP. A foto local escolhida substitui a referência nesta sessão. Microfone depende do navegador e permissão; o fornecedor pode processar fala remotamente. Escolher o idioma da voz não traduz automaticamente o conteúdo. Nunca cole credenciais de IA em páginas HTML públicas; o backend opcional da V2 requer uma implantação protegida.
Acesso ao servidor por token na interface destina-se **somente a testes privados por operador confiável**. Para audiências públicas, use um backend com sessões individuais, limites de uso, auditoria e política de privacidade.
## 5 — Testes de aceitação
- Foto aparece em Chrome/Edge com internet, sem seleção manual;
- Falha de rede exibe instrução e opção para carregar foto local;
- Restaurar fotografia funciona;
- Pergunta local aparece e a resposta pode ser lida em voz alta;
- Modo auditório respeita caixa de seleção;
- Microfone negado não bloqueia perguntas digitadas;
- Player audiovisual aceita MP4 com áudio previamente sincronizado;
- Sem alegação indevida de animação labial para respostas inéditas;
- Arquivos Blender passam por testes técnicos em instalação real antes de publicação.
