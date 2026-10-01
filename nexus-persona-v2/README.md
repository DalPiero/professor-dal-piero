# NEXUS PERSONA V2 — Manual de entrega

Protótipo **funcional sem serviços pagos** (modo local) e **integração conversacional opcional** (servidor com custos próprios).

## 1. Testar agora
Abra `index.html` em um navegador moderno. Carregue a fotografia autorizada. Escolha tema, digite pergunta, use **Ouvir resposta** e, se suportado, **Microfone**. O modo local não envia foto/perguntas ao servidor da aplicação nem memoriza histórico após fechar a página.

O que está pronto:
- Avatar fotográfico estático carregado pelo usuário, com indicador de fala animado;
- Texto, síntese vocal do navegador, reconhecimento de fala quando suportado;
- Apresentação guiada, perguntas da plateia e base institucional estruturada;
- Histórico da sessão e exportação, idioma da voz e controle de velocidade;
- Interface responsiva, rótulos e elementos de acessibilidade;
- Modo conversacional opcional via HTTPS.

**Limitações reais:** não há rig 3D, lip sync facial, tradução automática universal, voz clonada hospedada nem aprendizagem permanente. O arquivo executa respostas fechadas e pode deixar de responder a perguntas fora da base. Uma representação estática com barras animadas não equivale a um rosto animado.

## 2. Publicar a interface
Hospede a pasta `nexus-persona-v2` em um site HTTPS. GitHub Pages permite páginas estáticas; para experimentar nesta ramificação, configure a fonte de publicação manualmente ou publique em hospedagem estática. Faça isso sem alterar o site institucional principal.

## 3. Servidor opcional para perguntas inéditas
`server.mjs` requer Node.js 20+, conectividade e uma chave de API **do responsável pelo servidor**. Rode em serviço hospedado com proteção TLS e **não** em GitHub Pages.
Ambiente:
```
OPENAI_API_KEY=...  # somente no ambiente seguro do servidor
PORT=8787
ALLOWED_ORIGIN=https://DOMINIO-EXATO-DO-SITE
ACCESS_TOKEN=... # segredo do servidor; NÃO publicar no frontend
MODEL=gpt-4.1-mini
node server.mjs
```

**Antes de integrar:** o HTML atual envia perguntas sem token e, por desenho, um servidor autenticado rejeitará essas chamadas. Para uso real com público é obrigatório acrescentar **sessões autenticadas emitidas por backend, com cookies HttpOnly e proteção antiabuso**, ou um proxy autenticado equivalente. NÃO inclua um token fixo no HTML. O servidor é uma base técnica de referência, não um endpoint público pronto. Há limites de requisições por IP, CORS e de tamanho de entrada; adicione monitoramento, política de retenção, testes de segurança e revisão do conteúdo antes de disponibilizar.

## 4. Voz, animação e tradução
- A voz no protótipo vem do navegador, não é a voz autêntica do autor.
- Para usar voz autorizada, exige-se serviço/licença de síntese e backend seguro.
- Para lip sync real, requer pipeline de rastreamento facial/rig 3D, visemas, animação e testes editoriais; marque o avatar claramente como digital.
- A seleção de língua altera a preferência de voz; tradução de respostas necessita serviço autorizado ou conteúdo específico por idioma.
- Não capture nem treine dados de plateia sem consentimento explícito.

## 5. Critérios de aceitação
Teste no navegador de destino e, no mínimo: perguntas cobertas e não cobertas; funcionamento sem microfone; bloqueio do microfone; ausência de voz local; recusa de foto grande; exportação; navegação por teclado; rede desligada no modo local; proteção a chaves de API e fluxo consentido de dados.

Base: BRASIL 2075, NEXUS PERSONA e apresentação universitária fornecidos no projeto.
