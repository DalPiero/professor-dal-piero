# NEXUS PERSONA — FASE 5: primeira malha facial tridimensional
**Estado:** projeto técnico Blender + interface de revisão entregues; o arquivo BLEND/GLB exige execução do Blender e verificação visual. Não equivale a reconstrução biométrica a partir da fotografia.

## Entregas presentes neste diretório
- `build_persona.py`: constrói cabeça volumétrica QUAD/triangular, olhos, sobrancelhas, óculos, barba, pescoço, busto acadêmico e uma superfície de boca. Inclui shape keys `JawOpen`, `Smile`, `Frown`, `Surprise`, `BrowInnerUp`, `BrowDown`, `BlinkLeft`, `BlinkRight`, `BlinkBoth` e `MOUTH_A` até `MOUTH_H`. Adiciona animação de teste para confirmar deformações.
- `index.html`: comparador com fotografia de referência e visualizador 3D que importa o GLB **localmente**, permite girar o modelo e manipular os morph targets.
- `.github/workflows/nexus-persona-v5.yml`: fluxo para construir e oferecer BLEND, GLB e PNG como artefatos do GitHub Actions.
- Mantém a interface falada/interativa V4 em `nexus-persona-v4/index.html` (diretório no mesmo ramo).

## Primeiro teste visual no Blender (Windows)
1. Instale uma versão compatível do Blender (3.6 ou posterior).
2. Salve sua fotografia de referência em uma pasta local. O padrão de demonstração é a imagem autorizada do projeto; se desejar precisão anatômica superior, forneça também vistas laterais reais.
3. Abra PowerShell na pasta `nexus-persona-v5`. Execute:
```powershell
& "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" -b -t 4 -P build_persona.py -- --photo "C:\caminho\foto.png"
```
Ajuste o caminho do programa conforme a sua instalação. O diretório atual recebe:
- `NEXUS_PERSONA_V5_PROTOTIPO.blend` com a fotografia empacotada quando fornecida;
- `NEXUS_PERSONA_V5_MALHA.glb` (se o exportador glTF estiver disponível);
- `NEXUS_PERSONA_V5_PREVIEW.png` (se a renderização funcionar).
Se uma saída falhar, examine as mensagens do Blender: não confunda conclusão do script com validação visual.

## Construção na nuvem pelo GitHub
Inicialmente, o arquivo de automação existe **somente na ramificação V5**. Portanto, o botão manual **Run workflow** pode não aparecer: o GitHub exige que o fluxo esteja também na ramificação principal para o disparo manual. Nesta fase, observe as execuções automáticas disparadas por novos commits (push), quando habilitadas no repositório. Depois de revisar e incorporar o workflow ao ramo principal, será possível acessar **Actions → NEXUS PERSONA V5 - Build Blender Proxy → Run workflow**, selecionar o ramo V5 e iniciar a construção. Após execução bem-sucedida, baixe o artefato `NEXUS_PERSONA_V5_BLENDER`. Os arquivos só existirão após uma execução bem-sucedida; verifique os logs em caso de erro.

## Visualizar e controlar a malha
Abra `index.html` com internet (carrega a biblioteca Three.js) e carregue o GLB gerado. Os sliders correspondem às shape keys presentes no objeto exportado. Experimente sorriso, surpresa, mandíbula, piscadas e `MOUTH_A..H`; a demonstração automática NÃO é sincronização fonética de nenhuma narração. O arquivo GLB fica no seu computador durante a importação pelo navegador.

## Próximo passo: expressão facial fiel e lip sync
Este primeiro busto técnico prova estrutura, controles e exportação, mas NÃO assegura identidade tridimensional fiel. Para avançar com qualidade:
- validar a silhueta frontal e obter fotografia lateral esquerda/direita sob luz uniforme, voluntariamente;
- revisar manualmente topologia periocular, lábios, mandíbula, barba, dentes e óculos;
- modelar uma malha facial final que preserve os visemas e a expressão aprovada;
- aplicar visemas temporizados usando a gravação autorizada pelo `nexus-persona-v4/aplicar_visemas.py`, confirmar correspondência de nomes e revisar cada fonema;
- renderizar clipe aprovado e carregá-lo na interface V4; o áudio final é a gravação limpa aprovada.
O avatar deve permanecer identificado como personagem digital.

## Critérios de teste antes de uso com plateia
Inspecione as shape keys individualmente e misturadas; feche ambos os olhos; verifique abertura da boca e ausência de interseções entre barba/lábios/dentes; verifique rotação da câmera e imagem lateral; teste GLB; examine legibilidade de gestos em auditório e acessibilidade.
**Limite técnico:** uma única fotografia, ainda que de boa resolução, não fornece anatomia lateral nem geometria oculta. O que não é observado nesta referência foi aproximado e necessita aprovação artística.
