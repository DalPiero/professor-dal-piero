# NEXUS PERSONA V9 — Diálogo com a plateia, voz e movimento

**Esta versão está preparada para testes privados. Não está publicada no site principal e NÃO é um avatar facial fotorrealista com sincronização validada.**

## Objetivo e materiais canônicos
- ÚNICA referência de imagem, corpo e trejeitos: `2Conhecimento Deve Circular.mp4`, já referenciado no HTML.
- ÚNICA amostra vocal desta edição: `Voz Dal Piero(2).mp3`.
- A voz oficial cadastrada como personagem no acervo do projeto já existe, mas **seu identificador de personagem no Creative Claw não deve ser confundido com o `voice_id` de uma conta de ElevenLabs**. Não clonar novamente sem necessidade e autorização.
- Todas as fotografias e demais filmes de edições anteriores foram excluídos da interface nova.

## Funcionalidades implementadas
1. **Apresentação:** reprodução integral e intacta do Filme 2, incluindo os gestos e a voz que de fato constam nele.
2. **Perguntas:** área de perguntas por texto e microfone, resposta da base documental ou servidor autorizado.
3. **Diálogo contínuo:** botão `Iniciar conversa`, após consentimento, inicia um turno de reconhecimento de voz; o microfone é suspenso enquanto o avatar responde e reativado apenas depois do áudio terminar. O botão `Encerrar conversa` interrompe o ciclo.
4. **Voz oficial para respostas inéditas:** o servidor `server.mjs` usa um serviço de TTS configurado **somente com voz autorizada**, uma vez que o operador forneça `ELEVENLABS_VOICE_ID` da sua conta, `ELEVENLABS_API_KEY` e `OPENAI_API_KEY`; senão há resposta textual, nunca uma falsa voz "oficial".
5. **Movimento:** sem rig 3D, a imagem real do Filme 2 recebe apenas movimento editorial muito discreto na tela, sem alterar rosto ou simular a boca. **Com um GLB que tenha sido previamente modelado e aprovado a partir do Filme 2**, um painel adicional anima olhos, mandíbula, pálpebras e visemas presentes na malha; utilize `avatar_motion.js`.
6. **Alinhamento temporal:** o servidor pede áudio com tempos por caractere. O visualizador usa esses tempos para categorias aproximadas de boca, não fonemas verificados. A identidade, a fala e o resultado final exigem inspeção artística.
7. **Acessibilidade:** transcrição textual em tela, alternativa por teclado, avisos de ativação de microfone; preservada a base local para uso sem serviço pago.
8. **Privacidade:** o token inserido na página vale apenas para teste privado por um operador, fica na memória temporária da aba. Não exponha no computador da plateia. O fornecedor do microfone poderá processar áudio externamente, conforme navegador.

## Experimente sem custos
Baixe a ramificação e abra `nexus-persona-v9/index.html` no Chrome/Edge com internet. Pressione `Apresentar` para o filme original. Para testar perguntas locais, selecione uma das sugestões e pressione `Responder`; se quiser voz de demonstração marque **voz provisória do navegador**. O filme é pausado no quadro real quando começam as perguntas.

### Etapa audiovisual 3D — opcional
O campo `Importar malha facial autorizada` exige um arquivo GLB com shape keys, que ainda deve ser validado. **O script Blender V5 não deve ser tratado como o rosto definitivo**: é apenas proxy e a construção automática inicial foi cancelada. Com malha revisada e exportada para GLB, importe o arquivo. Observe os controles `JawOpen`, `BlinkBoth` e `MOUTH_A…H` conforme o arquivo realmente possuir. A animação aproximada usa os tempos da voz gerada.

## Configurar respostas inéditas com voz autorizada
Requer hospedagem do backend em HTTPS (NUNCA GitHub Pages, pois este só oferece site estático). Defina em **variáveis secretas do servidor**, sem salvar chaves em GitHub:
```sh
OPENAI_API_KEY=<chave_privada>
ELEVENLABS_API_KEY=<chave_privada>
ELEVENLABS_VOICE_ID=<id_de_voz_verificado_na_conta>
ACCESS_TOKEN=<token_privado_temporario>
ALLOWED_ORIGIN=https://DOMINIO-EXATO-ONDE-ESTA-A-INTERFACE
PORT=8787
node server.mjs
```
Configure o campo endpoint na aplicação com `https://SEU-SERVIDOR/api/chat`, marque `Habilitar integração privada`, escolha o modo de voz e **inicie a conversa**. O `voice_id` só deve ser cadastrado depois de confrontado com a amostra `Voz Dal Piero(2).mp3`. Este backend pode incorrer em custos dos provedores. **Nenhuma chave de API ou URL de servidor implantado foi fornecida nesta conversa; a operação com voz oficial para frases inéditas permanece condicional à configuração.**

### Para plateia em dispositivos próprios
O token fixo digitado no navegador NÃO deve ser utilizado em público. É necessária autenticação individual/por sessão, quotas por dispositivo, proteção antiabuso, consentimento e revisão jurídica/privacidade. Para auditório, o operador pode usar apenas a tela privada de controle.

## Validações obrigatórias antes da publicação
- Conferir na máquina de apresentação o carregamento do Filme 2, áudio e ausência de imagens anteriores.
- Validar o identificador autorizado da voz. Fazer um teste curto: pronúncia, sotaque, entonação, pausas e consistência com a amostra.
- Testar microfone permitido/negado, interrupções, perguntas não previstas, internet desconectada e encerramento da conversa.
- Inspecionar cada shape key isolada e combinada no GLB autorizado. Verificar se as aberturas labiais não deformam artificialmente a identidade.
- **Não declarar lip sync fidedigno, fala em tempo real com o autor nem avatar 3D canônico até essa revisão.**

## Arquivos
- `index.html`: painel de audiência, reprodução original, modo contínuo e importação 3D.
- `server.mjs`: backend opcional de texto e TTS com alinhamento temporal.
- `avatar_motion.js`: módulo do visor GLB e deformações temporizadas.
- `README.md`: estas instruções.
