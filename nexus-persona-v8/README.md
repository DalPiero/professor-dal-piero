# NEXUS PERSONA V8 — FILME 2 + VOZ DO AUTOR (BASE ÚNICA)

## Decisão de identidade
Esta edição **não utiliza fotos antigas, Filme 1 nem rostos sintéticos anteriores**.
A referência visual única é `2Conhecimento Deve Circular.mp4`.
A referência de voz única carregada nesta edição é `Voz Dal Piero(2).mp3`.

No protótipo, o arquivo visual original permanece intacto durante a apresentação, preservando o rosto e os trejeitos **efetivamente gravados**. Ao receber uma pergunta, o Filme 2 é pausado no último quadro real. Não se inventam gestos ou uma nova expressão para uma fala inédita.

Fontes de mídia da edição:
- **ÚNICO VÍDEO:** https://cdn.creativeclaw.co/u/5dd90fe8/videos/11cead6e-fce2-4fe3-a730-552bcea8d253.mp4
- **ÚNICA AMOSTRA VOCAL:** https://cdn.creativeclaw.co/u/5dd90fe8/audio/fb294ade-7ee7-4a26-8fce-1023ab38cffe.mp3

O conteúdo do MP3 deve ser revisado pelo operador, inclusive trechos não destinados à divulgação pública. Não assumir que a amostra foi aprovada para ser tocada integralmente em um evento sem essa revisão.

## Como testar de graça
1. Baixe a ramificação `nexus-persona-v8` e abra `nexus-persona-v8/index.html` no Chrome ou Edge **com internet**.
2. Pressione **Apresentar com Filme 2**. Isso toca o vídeo e o áudio originais.
3. Escute a amostra da voz no controle separado e confirme se corresponde à voz desejada.
4. Pressione **Abrir perguntas**; o vídeo pausa e a interface responde com textos institucionais locais.
5. A caixa **voz provisória do navegador** começa desmarcada de propósito. Se marcada, anuncia expressamente a voz provisória, que não é a do autor.
6. Use a ferramenta de marcação para selecionar e exportar trechos reais de olhar, piscadas, gestos e boca, para futura animação 3D.

## Respostas inéditas com a voz oficial
**A amostra MP3 NÃO é um modelo de síntese.** O servidor `server.mjs` já contém integração opcional com o endpoint de síntese de fala da ElevenLabs, mas só utilizará a voz correta se ela estiver cadastrada e for explicitamente selecionada pelo responsável na própria conta.

Configuração de servidor Node.js 20+ em hospedagem HTTPS com ambiente privado:
```sh
OPENAI_API_KEY="chave_privada_do_projeto"
ACCESS_TOKEN="token_privado_temporario_do_operador"
ALLOWED_ORIGIN="https://endereco-exato-do-site"
ELEVENLABS_API_KEY="chave_privada_da_conta"
ELEVENLABS_VOICE_ID="id_verificado_da_voz_autorizada"
PORT=8787
node server.mjs
```
NÃO inclua as chaves acima no GitHub, na página ou em capturas de tela. O ID de personagem de outro aplicativo não pode ser presumido equivalente ao `ELEVENLABS_VOICE_ID`.

**Custo:** chamadas a provedores podem ser cobradas. Esta entrega não gastou créditos de geração. Se faltar qualquer uma das variáveis de voz, o servidor retorna a resposta em texto, **sem fingir que sintetizou a voz do autor**.

**Segurança:** o token digitado na página é aceitável somente para ensaio privado com um operador confiável. Para uso público, substitua o token comum por autenticação individual, autorização por sessão, limitação de gastos e política de consentimento/privacidade. Nunca libere o endpoint privado ao público sem esse trabalho.

## O avatar que esta versão realmente entrega
- PRESENÇA: reprodução fiel de rosto/gestos/voz presentes no Filme 2;
- MODO PERGUNTAS: mantém um quadro real pausado, obtém resposta local ou por servidor;
- VOZ INÉDITA: disponível apenas após integração testada e autorizada com `ELEVENLABS_VOICE_ID`;
- GESTOS: exportação manual de segmentos do filme em JSON para orientar retarget na malha;
- AINDA NÃO CONCLUÍDO: movimento de boca sincronizado à voz clonada durante respostas inéditas, reconstrução 3D fiel, validação quadro a quadro dos trejeitos.

A futura etapa de movimento facial deve extrair os referenciais do **Filme 2 somente**, ajustar uma malha revisada aos movimentos observados e aplicar visemas temporizados ao áudio gerado e aprovado. Não sobreponha o Filme 2 original sobre frases diferentes nem altere os lábios por aproximação que possa deturpar a identidade.

## Checklist de aprovação antes de apresentar
- Vídeo original carrega, emite áudio e apresenta a identidade pretendida;
- MP3 contém apenas gravação autorizada à divulgação;
- ao perguntar, vídeo para e não deixa duas vozes soarem ao mesmo tempo;
- perguntas desconhecidas recebem recusa fundamentada;
- resposta gerada sem voz configurada NÃO é identificada como voz do autor;
- voz sintetizada, quando configurada, é comparada auditivamente com a amostra, verificando pronúncia e ritmo;
- interação por microfone exige autorização;
- não há foto antiga ou Filme 1 na interface V8.
