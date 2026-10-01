# NEXUS PERSONA — transferir visemas temporizados para um rig REAL existente.
# Blender 4.x/5.x. Requer: OBJETO da face com Shape Keys chamadas
# "MOUTH_A"..."MOUTH_H" (ou escolha correspondência na constante MAP).
# Requer JSON de Rhubarb Lip Sync criado de gravação AUTORIZADA.
# Uso: blender projeto_persona.blend -b -P aplicar_visemas.py -- boca.json [voz.wav]
# Este script NÃO cria geometria facial 3D de uma foto e NÃO infere expressão exata.
import bpy, json, sys, os
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if not args or not os.path.isfile(args[0]):
    raise RuntimeError("Falta JSON de visemas. Exemplo: -- boca.json voz.wav")
json_path=os.path.abspath(args[0])
audio_path=os.path.abspath(args[1]) if len(args)>1 else None
if audio_path and not os.path.isfile(audio_path):
    raise RuntimeError("Áudio informado não existe")
with open(json_path,encoding='utf-8') as f: data=json.load(f)
cues=data.get("mouthCues")
if not isinstance(cues,list) or not cues:
    raise RuntimeError("JSON não contém mouthCues")
obj=bpy.context.active_object
if not obj or obj.type!='MESH' or not obj.data.shape_keys:
    raise RuntimeError("Selecione ANTES um modelo facial verdadeiro com shape keys")
blocks=obj.data.shape_keys.key_blocks
mapping={c:"MOUTH_"+c for c in "ABCDEFGH"}
found={c:blocks.get(name) for c,name in mapping.items()}
missing=[name for c,name in mapping.items() if found[c] is None]
if missing:
    raise RuntimeError("Rig incompleto; faltam visemas "+", ".join(missing)+
                       ". Não crie visemas artificiais sobre a fotografia estática.")
fps=bpy.context.scene.render.fps/bpy.context.scene.render.fps_base
def key_all(frame,active=None,power=0):
    for c,k in found.items():
        k.value=power if c==active else 0.0
        k.keyframe_insert(data_path='value',frame=frame)
prev=0
key_all(1)
max_t=0
for item in cues:
    start=float(item['start'])
    end=float(item['end'])
    name=str(item['value']).upper()
    if name not in "ABCDEFGHX" or end<start:raise RuntimeError("Cue inválida")
    first=max(1,round(start*fps)+1)
    last=max(first+1,round(end*fps)+1)
    if first>prev+1:key_all(first-1)
    # A/B/C etc. são categorias aproximadas de movimento labial;
    # a revisão HUMANA do áudio em português é obrigatória.
    key_all(first,name if name!="X" else None,0.85)
    key_all(last,None)
    prev=last
    max_t=max(max_t,end)
scene=bpy.context.scene
scene.frame_start=1
scene.frame_end=max(2,round(max_t*fps)+1)
if audio_path:
    # Faixa de áudio original, não uma locução gerada pelo software de rig.
    if hasattr(scene,"sequence_editor_create"):
        seq=scene.sequence_editor_create()
        if hasattr(seq,"strips"):
            seq.strips.new_sound("NARRACAO_APROVADA",audio_path,channel=1,frame_start=1)
        elif hasattr(seq,"sequences"):
            seq.sequences.new_sound("NARRACAO_APROVADA",audio_path,channel=1,frame_start=1)
scene.render.resolution_x=1920;scene.render.resolution_y=1080
scene.render.resolution_percentage=100
scene.render.fps=24
scene.render.filepath="//NEXUS_PERSONA_RIG_TESTE"
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("NEXUS_PERSONA_VISEMAS_ANIMADOS.blend"))
print("Rig existente animado com",len(cues),"visemas temporizados. REVISAO facial e de sincronizacao PENDENTE.")
