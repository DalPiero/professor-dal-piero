# NEXUS PERSONA — CENA AUDIOVISUAL 2.5D NO BLENDER
# Uso: blender -b -P blender_nexus_stage.py -- /caminho/foto_autorizada.png
# Faz movimento de câmera sobre a foto ORIGINAL, sem gerar outro rosto.
# NÃO produz lip sync, NÃO cria escultura 3D do rosto.
import bpy, sys, os, math
from mathutils import Vector
args = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
if not args or not os.path.isfile(args[0]):
    raise RuntimeError("Informe como argumento uma fotografia PNG/JPG autorizada que exista.")
photo = os.path.abspath(args[0])
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
try:
    scene.render.engine='BLENDER_EEVEE_NEXT'
except (TypeError, ValueError):
    scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1920
scene.render.resolution_y=1080
scene.render.resolution_percentage=100
scene.render.fps=24
scene.frame_start=1
scene.frame_end=288   # 12s
scene.render.image_settings.file_format='FFMPEG'
scene.render.ffmpeg.format='MPEG4'
scene.render.ffmpeg.codec='H264'
scene.render.ffmpeg.constant_rate_factor='MEDIUM'
scene.render.filepath=os.path.abspath("NEXUS_PERSONA_2_5D_SEM_AUDIO.mp4")
world=bpy.data.worlds.new("Estudio_sobrio") if not bpy.data.worlds else bpy.data.worlds[0]
scene.world=world
world.use_nodes=True
world.node_tree.nodes.get("Background").inputs["Color"].default_value=(0.02,.046,.085,1)
world.node_tree.nodes.get("Background").inputs["Strength"].default_value=.75
img=bpy.data.images.load(photo,check_existing=True)
# Plano 16:9 que exibe integralmente a foto: o "object-fit contain" se resolve pelo material
bpy.ops.mesh.primitive_plane_add(size=2,location=(0,0,0))
plane=bpy.context.object
plane.name="FOTOGRAFIA_ORIGINAL_SEM_ALTERAR_ROSTO"
# Evitar esticar a identidade facial ou cortar a fotografia
original_ratio=img.size[0]/img.size[1]
max_w,max_h=8.45,4.72
photo_w=min(max_w,max_h*original_ratio)
photo_h=photo_w/original_ratio
plane.scale=(photo_w/2,photo_h/2,1)
mat=bpy.data.materials.new("ImagemAutorizada")
mat.use_nodes=True
nodes=mat.node_tree.nodes;nodes.clear()
tex=nodes.new("ShaderNodeTexImage");tex.image=img;tex.extension="CLIP"
em=nodes.new("ShaderNodeEmission");em.inputs["Strength"].default_value=1
out=nodes.new("ShaderNodeOutputMaterial")
mat.node_tree.links.new(tex.outputs["Color"],em.inputs["Color"])
mat.node_tree.links.new(em.outputs["Emission"],out.inputs["Surface"])
plane.data.materials.clear();plane.data.materials.append(mat)
# Fundo respeita o formato institucional — tela universitária, sem hologramas
bpy.ops.object.camera_add(location=(0,0,13))
cam=bpy.context.object;cam.name="CAMERA_EDITORIAL";scene.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=9.6
def aim(obj,point=(0,0,0)):
    obj.rotation_euler=(Vector(point)-obj.location).to_track_quat('-Z','Y').to_euler()
aim(cam)
for f,scale,x in [(1,9.6,-.10),(96,9.45,0),(192,9.2,.06),(288,9.35,0)]:
    cam.data.ortho_scale=scale;cam.data.keyframe_insert(data_path="ortho_scale",frame=f)
    cam.location.x=x;cam.keyframe_insert(data_path="location",frame=f)
# Transparência/mascara facial não usadas: nenhuma invenção anatômica.
scene.view_settings.view_transform='Standard'
print("PRONTO PARA RENDER: plano fotográfico cinematográfico. NÃO É AVATAR FACIAL RIGGADO.")
bpy.ops.render.render(animation=True)
