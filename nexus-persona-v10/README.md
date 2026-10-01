# NEXUS PERSONA V10 — Respostas imediatas para audiência

**Estado:** versão interativa para teste e apresentação supervisionada. A base local responde a perguntas abrangidas por seus tópicos; não é uma IA geral executando offline.

## 1. Como testar agora, sem custos
1. Baixe e extraia o ZIP deste ramo.
2. Abra a pasta `nexus-persona-v10`. Para perguntas **digitadas**, abra `index.html` no Chrome ou Edge.
3. No Windows com Python instalado, execute `INICIAR_NEXUS_WINDOWS.bat` para abrir a interface pelo endereço local `http://127.0.0.1:8765/`. Esse método é preferível para testar o microfone, que pode não funcionar ao abrir arquivos pelo protocolo `file://`.
4. Pressione **Apresentar com Filme 2** para exibir a gravação original.
5. Pressione **Abrir perguntas** e selecione um tema ou digite uma pergunta. A resposta aparece imediatamente e, se o navegador disponibilizar síntese vocal, será lida pela **voz provisória identificada como tal**.
6. Experimente **Iniciar conversa**. Com autorização do microfone, ouve cada pergunta, pausa a captação durante a resposta e escuta outra pergunta depois da fala. Para essa função, mantenha marcada a caixa de voz provisória ou configure o servidor autorizado.
7. Use **Encerrar conversa** para interromper o reconhecimento e a resposta em andamento.

## 2. O que realmente está pronto
- Vídeo e trejeitos do **Filme 2** como única referência visual.
- Amostra `Voz Dal Piero(2).mp3` para comparação vocal.
- Base institucional com perguntas sobre BRASIL 2075, seus núcleos, piloto, princípios éticos, infraestrutura e avatar.
- Respostas de contexto: após uma pergunta atendida, pode-se pedir **Explique melhor**.
- Perguntas desconhecidas recebem mensagem de limitação; o avatar não deve inventar respostas.
- Respostas em voz provisória opcional do próprio navegador; ativada inicialmente por conveniência e sempre identificada.
- Microfone quando o navegador oferecer SpeechRecognition, com consentimento.
- Respostas inéditas e voz oficial via `server.mjs` privado, **apenas após implantação segura e verificação da voz**.
- Movimento editorial discreto com quadro real do Filme 2 e, opcionalmente, módulo GLB para malha **efetivamente aprovada**. **Ainda não há malha facial canônica validada nem lip sync fonético ao vivo.**

## 3. Perguntas de demonstração
- O que é BRASIL 2075?
- Qual é o papel da universidade?
- Como funciona o piloto de 90 dias?
- O que é NEXUS EDU?
- O que é NEXUS MED?
- O que é NEXUS ODONTO?
- Quais são suas fontes?
- A inteligência artificial substituirá professores?
- Explique melhor. (após uma resposta)

O conteúdo segue a estrutura resumida do projeto; **não** significa que toda informação de seus PDFs esteja indexada.

## 4. Ativar perguntas inéditas + voz autorizada
O HTML, sozinho, não opera um modelo conversacional nem transforma um MP3 em gerador de frases novas. `server.mjs` foi preparado para um serviço de texto e TTS com identificação vocal verificada.

Implante o servidor Node.js 20+ em ambiente seguro, com TLS/HTTPS; defina secretamente:
```
OPENAI_API_KEY=...
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=<ID VERIFICADO NA CONTA DA VOZ AUTORIZADA>
ALLOWED_ORIGIN=https://SEU-SITE
ACCESS_TOKEN=<TOKEN PRIVADO DO OPERADOR>
PORT=8787
```
Configure o endpoint `https://SEU-SERVIDOR/api/chat` na interface. Use esse modo somente com um **operador privado confiável**, nunca em um quiosque público com token global. O serviço pode ter custo por uso e deve ter limite financeiro de execução. Não insira credenciais na página pública ou no GitHub.

O identificador de personagem no Creative Claw e o identificador de voz numa conta ElevenLabs são tipos diferentes; não os troque sem validação. A amostra fornecida é uma referência, não um `voice_id`. Não gere uma segunda clonagem sem necessidade.

## 5. Responsabilidade, privacidade e limitações
- Perguntas institucionais conhecidas são respondidas sem custo de geração.
- Recursos de microfone diferem entre navegadores e alguns enviam áudio a um serviço do fornecedor; obtenha consentimento.
- A leitura por voz provisória é distinta da gravação do autor; deixe a indicação visível.
- Não fotografe/grave ou retenha perguntas de membros da audiência sem autorização apropriada.
- Gestos 3D sincronizados dependem de GLB revisado. O movimento do enquadramento do vídeo não equivale a sincronização labial.
- Antes de publicar para uso irrestrito, é necessária autenticação individual, testes de privacidade, revisão de acessibilidade e auditoria do conteúdo institucional.

## 6. Verificação
A pasta `tests` contém verificações de sintaxe e consulta real à base local. Execute `node tests/smoke.mjs` na pasta `nexus-persona-v10`. Isso não substitui testar vídeo, permissão de microfone e identidade vocal no equipamento do evento.
