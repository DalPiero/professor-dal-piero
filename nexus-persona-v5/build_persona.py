# NEXUS PERSONA — PROTOTIPO TECNICO 3D, NÃO RETRATO BIOMÉTRICO
# Blender 3.6+ / 4.x — blender -b -P build_persona.py -- --photo /foto.png
# Saídas: NEXUS_PERSONA_V5_PROTOTIPO.blend, .glb, preview.png
# Formato: X esquerda/direita, Y profundidade (frente negativa), Z vertical
import bpy, math, os, sys, urllib.request
from mathutils import Vector
from math import sin, cos, pi, exp
args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
photo=None
for i,a in enumerate(args):
    if a=="--photo" and i+1<len(args): photo=os.path.abspath(args[i+1])
if photo and not os.path.isfile(photo): raise ValueError("Fotografia de referência não existe: "+photo)
OUT=os.path.abspath(os.environ.get("NEXUS_OUTPUT",os.getcwd()))
os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.resolution_x=1920;scene.render.resolution_y=1080
scene.render.resolution_percentage=70
scene.render.fps=24;scene.frame_start=1;scene.frame_end=192
scene.render.image_settings.file_format="PNG"
try: scene.render.engine="BLENDER_EEVEE_NEXT"
except Exception:
    try: scene.render.engine="BLENDER_EEVEE"
    except Exception: scene.render.engine="BLENDER_WORKBENCH"
def mat(name,col,rough=0.7,metal=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF")
    if p:
        p.inputs["Base Color"].default_value=(*col,1)
        p.inputs["Roughness"].default_value=rough
        p.inputs["Metallic"].default_value=metal
    return m
skin=mat("PELE_PROVISORIA_NAO_BIOMETRICA",(.67,.45,.35))
lip=mat("BOCA_INTERIOR",(.065,.017,.027))
iris=mat("IRIS_CASTANHO",(.19,.125,.084))
white=mat("OLHOS",(.89,.88,.82))
hair=mat("BARBA_BRANCA",(.81,.80,.76))
coat=mat("BLAZER_AZUL_MARINHO",(.035,.055,.12))
black=mat("CAMISA_PRETA",(.022,.023,.027))
gold=mat("OCULOS_ARMAÇÃO",(.10,.095,.08),.22,.55)
floor=mat("FUNDO_AZUL",(.035,.072,.115))
# Face human-like volumetric proxy: anterior curvature, jaw taper, nasal and cheek planes.
VERT=[];FACES=[];segs=64;rings=42
for i in range(rings+1):
    p=pi*(i+.02)/(rings+.04)
    z=1.90+1.12*cos(p)
    t=(z-1.90)/1.12
    jaw=1-.28*max(0,-t)**1.6
    for j in range(segs):
        th=2*pi*j/segs
        x=.83*sin(p)*cos(th)*jaw
        y=-.69*sin(p)*sin(th)
        if y<0:
            nose=exp(-(x/.13)**2-((z-1.88)/.27)**2)
            cheek=exp(-((abs(x)-.39)/.22)**2-((z-1.71)/.33)**2)
            brow=exp(-((abs(x)-.32)/.20)**2-((z-2.25)/.10)**2)
            y-=.18*nose +.04*cheek +.05*brow
        VERT.append([x,y,z])
for i in range(rings):
    for j in range(segs):
        a=i*segs+j;b=i*segs+(j+1)%segs;c=(i+1)*segs+(j+1)%segs;d=(i+1)*segs+j
        FACES.append((a,b,c,d))
# Mouth dark surface is a disconnected patch within same mesh so ONE set of visemes drives face AND mouth.
mouth_indices=[]
steps=32;cy=-.734;cz=1.47
center=len(VERT);VERT.append([0,cy,cz]);mouth_indices.append(center)
for i in range(steps):
    a=2*pi*i/steps
    # thin rest mouth, wider than high.
    VERT.append([.33*cos(a),cy-.018,cz+.025*sin(a)])
    mouth_indices.append(len(VERT)-1)
mouth_face_start=len(FACES)
for i in range(steps): FACES.append((center,center+1+i,center+1+((i+1)%steps)))
mesh=bpy.data.meshes.new("TOPOLOGIA_FACIAL_ESTUDO")
mesh.from_pydata(VERT,[],FACES);mesh.update()
head=bpy.data.objects.new("CABECA_3D_PROVISORIA_CONTROLAVEL",mesh)
bpy.context.collection.objects.link(head)
head.data.materials.append(skin);head.data.materials.append(lip)
for poly in mesh.polygons:
    if poly.index>=mouth_face_start: poly.material_index=1
for poly in mesh.polygons: poly.use_smooth=True
head.shape_key_add(name="Basis")
base=[Vector(v) for v in VERT]
def G(x,z,cx,cz,sx,sz):
    return exp(-((x-cx)/sx)**2-((z-cz)/sz)**2)
# eye and brow surface deformation of upper facial mask, jaw / mouth lower zone
def deform(name,mode,amp=1):
    sk=head.shape_key_add(name=name)
    for i,v in enumerate(base):
        x,y,z=v
        d=Vector((0,0,0))
        front=max(0,min(1,(-y-.27)/.35))
        if i in mouth_indices:
            if i==center: sk.data[i].co=v;continue
            # map vertical viseme opening and width to mouth mesh
            heights={"MOUTH_A":.165,"MOUTH_B":.028,"MOUTH_C":.10,"MOUTH_D":.048,
                     "MOUTH_E":.11,"MOUTH_F":.036,"MOUTH_G":.06,"MOUTH_H":.018}
            widths={"MOUTH_A":.88,"MOUTH_B":.82,"MOUTH_C":.76,"MOUTH_D":1.0,
                    "MOUTH_E":1.17,"MOUTH_F":.77,"MOUTH_G":.97,"MOUTH_H":.85}
            if name in heights:
                d.x=(widths[name]-1)*x;d.z=(heights[name]/.025-1)*(z-cz);d.y=-.015
            elif mode=="jaw":
                d.z=2.8*(z-cz);d.y=-.024
            elif mode=="smile":d.x=.13*x;d.z=.12*(abs(x)/.33)
        else:
            if mode=="jaw" or mode.startswith("phoneme"):
                strength=G(x,z,0,1.46,.48,.26)*front
                d.z-=.16*strength*amp;d.y-=.035*strength*amp
            if mode=="smile":
                d.z+=.09*(G(x,z,-.30,1.48,.17,.16)+G(x,z,.30,1.48,.17,.16))*front
                d.x+=(.07 if x>0 else -.07)*G(x,z,(.32 if x>0 else -.32),1.48,.16,.13)*front
            if mode=="frown":
                d.z-=.075*(G(x,z,-.34,1.52,.20,.18)+G(x,z,.34,1.52,.20,.18))*front
            if mode=="surprise":
                d.z+=.083*(G(x,z,-.31,2.28,.28,.13)+G(x,z,.31,2.28,.28,.13))*front
            if mode=="brow_inner":
                d.z+=.09*G(x,z,0,2.29,.28,.16)*front
            if mode=="brow_down":
                d.z-=.065*(G(x,z,-.34,2.27,.21,.14)+G(x,z,.34,2.27,.21,.14))*front
            if mode in ("blink_L","blink_R","blink"):
                if mode=="blink" or (mode=="blink_L" and x<0) or (mode=="blink_R" and x>0):
                    d.z-=.064*G(x,z,(-.34 if x<0 else .34),2.11,.22,.12)*front
        sk.data[i].co=v+d
    sk.value=0;sk.slider_min=0;sk.slider_max=1
for n,mode in [("JawOpen","jaw"),("Smile","smile"),("Frown","frown"),
                ("Surprise","surprise"),("BrowInnerUp","brow_inner"),("BrowDown","brow_down"),
                ("BlinkLeft","blink_L"),("BlinkRight","blink_R"),("BlinkBoth","blink")]:
    deform(n,mode)
for v in "ABCDEFGH": deform("MOUTH_"+v,"phoneme")
# Eye geometry + brows + glasses (separate objects; proxies until likeness approved).
def sphere(name,location,scale,material,segments=32,rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=location)
    o=bpy.context.object;o.name=name;o.scale=scale
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o
for sign,tag in [(-1,"ESQUERDO"),(1,"DIREITO")]:
    x=sign*.335
    sphere("OLHO_"+tag,(x,-.625,2.095),(.185,.095,.089),white)
    sphere("IRIS_"+tag,(x,-.716,2.095),(.074,.024,.075),iris)
    sphere("PUPILA_"+tag,(x,-.738,2.095),(.037,.013,.044),black)
    sphere("SOBRANCELHA_"+tag,(x,-.677,2.24),(.218,.035,.034),hair)
# Eyelids are REAL separate mesh morphs; they lower over visible eyeballs.
# They supplement head-surface Blink keys and have identical names for GLB slider linking.
for sign,tag in [(-1,"L"),(1,"R")]:
    x0=sign*.335;vs=[];fs=[];cols=16
    for row in range(2):
        for j in range(cols+1):
            u=-1+2*j/cols
            x=x0+u*.183
            arch=max(0,1-u*u)**.5
            z=(2.186+.019*arch) if row==0 else (2.142+.004*arch)
            y=-.743+.018*u*u
            vs.append((x,y,z))
    for j in range(cols):
        fs.append((j,j+1,cols+2+j,cols+1+j))
    me=bpy.data.meshes.new("PALPEBRA_"+tag+"_MALHA")
    me.from_pydata(vs,[],fs);me.update()
    eyelid=bpy.data.objects.new("PALPEBRA_"+tag,me)
    bpy.context.collection.objects.link(eyelid)
    me.materials.append(skin)
    eyelid.shape_key_add(name="Basis")
    # Left and right can close independently, both also exposed.
    names=["BlinkLeft","BlinkRight","BlinkBoth"]
    for name in names:
        k=eyelid.shape_key_add(name=name)
        should_close=name=="BlinkBoth" or (name=="BlinkLeft" and sign<0) or (name=="BlinkRight" and sign>0)
        if should_close:
            for j,v in enumerate(vs):
                if j>=cols+1:  # lower edge of upper lid moves over iris
                    k.data[j].co=(v[0],v[1]-.019,v[2]-.122)
                else:
                    k.data[j].co=(v[0],v[1]-.009,v[2]-.014)
        k.value=0
    for poly in me.polygons: poly.use_smooth=True
def curve(name,pts,material,thick=.009,cyclic=False):
    cu=bpy.data.curves.new(name,"CURVE");cu.dimensions="3D"
    c=cu.splines.new("POLY");c.points.add(len(pts)-1)
    for p,xyz in zip(c.points,pts):p.co=(*xyz,1)
    c.use_cyclic_u=cyclic;cu.bevel_depth=thick;cu.bevel_resolution=3
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o)
    o.data.materials.append(material);return o
for sign,name in [(-1,"LENTE_ESQUERDA"),(1,"LENTE_DIREITA")]:
    points=[(sign*.35+.20*cos(t*2*pi/56),-.775,2.095+.13*sin(t*2*pi/56)) for t in range(56)]
    curve("ARMACAO_"+name,points,gold,.008,True)
curve("PONTE_OCULOS",[(-.15,-.77,2.12),(0,-.80,2.14),(.15,-.77,2.12)],gold,.007)
# Beard separated into side zones so mouth patch stays visible (proxy)
sphere("BARBA_QUEIXO",(0,-.57,1.20),(.46,.30,.27),hair)
for x in [-.49,.49]:
    sphere("BARBA_LATERAL_"+str(x),(x,-.44,1.48),(.23,.22,.43),hair)
for x in [-.17,.17]:
    sphere("BIGODE_"+str(x),(x,-.704,1.59),(.17,.08,.052),hair)
# Torso, blazer and shoulders: neutral non-medical academic attire
sphere("PEITO_BLAZER",(0,.11,.58),(1.12,.55,.83),coat)
sphere("CAMISA",(0,-.40,.91),(.34,.10,.44),black)
sphere("PESCOCO",(0,-.02,1.11),(.31,.30,.43),skin)
# Photo reference side-by-side, if provided. Kept separate, never used as geometry claim.
if photo:
    pic=bpy.data.images.load(photo,check_existing=True)
    pw,ph=pic.size;aspect=pw/max(ph,1)
    refw=2.70;refh=refw/aspect
    if refh>3.95: refh=3.95;refw=refh*aspect
    bpy.ops.mesh.primitive_plane_add(size=2,location=(-3.05,0,1.66))
    o=bpy.context.object;o.name="REFERENCIA_FOTOGRAFICA_NAO_GEOMETRIA"
    o.scale=(refw/2,refh/2,1)
    # plane lies XY by default: rotate to XZ, facing camera at negative Y
    o.rotation_euler[0]=pi/2
    m=bpy.data.materials.new("FOTO_ORIGINAL_SEM_REGENERACAO");m.use_nodes=True
    nd=m.node_tree.nodes;nd.clear()
    t=nd.new("ShaderNodeTexImage");t.image=pic
    e=nd.new("ShaderNodeEmission");e.inputs["Strength"].default_value=1
    out=nd.new("ShaderNodeOutputMaterial")
    m.node_tree.links.new(t.outputs["Color"],e.inputs["Color"]);m.node_tree.links.new(e.outputs[0],out.inputs["Surface"])
    o.data.materials.append(m)
# move bust right but keep local mesh shape key coordinates
for ob in list(bpy.context.scene.objects):
    if ob.name.startswith(("CABECA","OLHO_","IRIS_","PUPILA_","PALPEBRA_","SOBRANCELHA_","ARMACAO_","PONTE_OCULOS","BARBA_","BIGODE_","PEITO_","CAMISA","PESCOCO")):
        ob.location.x+=1.60
# gallery stage
bpy.ops.mesh.primitive_plane_add(size=2,location=(0,.54,1.75))
back=bpy.context.object;back.name="PAINEL_ESTUDIO";back.scale=(5.75,2.8,1);back.rotation_euler=(pi/2,0,0);back.data.materials.append(floor)
def txt(name,string,where,size=.22):
    c=bpy.data.curves.new(name,"FONT");c.body=string;c.size=size;c.align_x="CENTER"
    o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o)
    o.location=where;o.rotation_euler=(pi/2,0,0);o.data.materials.append(hair)
txt("TITULO","NEXUS PERSONA | MALHA TECNICA V5",(0,-.01,3.33),.20)
txt("NOTA","ESQUERDA: REFERENCIA / DIREITA: PROXY 3D PROVISORIO",(0,-.01,-.03),.135)
# Camera and physically plausible studio light
bpy.ops.object.camera_add(location=(0,-11.4,2.03))
cam=bpy.context.object;cam.name="CAMERA_REVISAO"
def aim(ob,pt):ob.rotation_euler=(Vector(pt)-ob.location).to_track_quat("-Z","Y").to_euler()
aim(cam,(0,0,1.64));cam.data.type="ORTHO";cam.data.ortho_scale=6.85
scene.camera=cam
for pos,power,size in [((-3,-4,6),950,5),((4,-2,4),720,4)]:
    bpy.ops.object.light_add(type="AREA",location=pos)
    o=bpy.context.object;o.data.energy=power;o.data.shape="DISK";o.data.size=size;aim(o,(1.6,0,1.9))
scene.world.color=(.035,.035,.04)
# sample animation: each activated key proves controls can move mesh, NOT phonetic precision
def key(name,frm,v):
    k=head.data.shape_keys.key_blocks[name];k.value=v;k.keyframe_insert(data_path="value",frame=frm)
for n in ["Smile","Frown","Surprise","JawOpen","BlinkBoth"]+["MOUTH_"+a for a in "ABCDEFGH"]:
    key(n,1,0)
timeline=[("Smile",13,21),("BlinkBoth",29,32),("Surprise",43,52),
          ("JawOpen",63,71),("MOUTH_A",80,89),("MOUTH_E",97,106),
          ("Frown",127,137)]
timeline=[x for x in timeline if x[0] in head.data.shape_keys.key_blocks]
for name,start,end in timeline:
    key(name,start-2,0);key(name,start,1);key(name,end,1);key(name,end+3,0)
# Scripted sequence demonstrating all A-H visemes
for i,ch in enumerate("BCDFGH"):
    f=142+i*7
    if f+5>scene.frame_end: break
    key("MOUTH_"+ch,f-1,0);key("MOUTH_"+ch,f,1);key("MOUTH_"+ch,f+3,1);key("MOUTH_"+ch,f+5,0)
scene.frame_set(1)
# Select head (for easy inspection of shape keys on opening blend)
bpy.ops.object.select_all(action='DESELECT')
head.select_set(True);bpy.context.view_layer.objects.active=head
blend=os.path.join(OUT,"NEXUS_PERSONA_V5_PROTOTIPO.blend")
# Empacotar a fotografia dentro do .blend para não depender de links externos.
if photo:
    bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=blend)
# GLB should preserve named mesh morph targets when exporter installed.
try:
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,"NEXUS_PERSONA_V5_MALHA.glb"),
        export_format="GLB",export_morph=True,export_animations=True)
except Exception as e:
    print("AVISO: GLB indisponível nesta versão:",e)
try:
    scene.render.filepath=os.path.join(OUT,"NEXUS_PERSONA_V5_PREVIEW.png")
    bpy.ops.render.render(write_still=True)
except Exception as e:
    print("AVISO: Preview não renderizou:",e)
print("CRIADO:",blend,"SHAPE_KEYS:",list(head.data.shape_keys.key_blocks.keys()),
      "VERTICES:",len(mesh.vertices),"FACES:",len(mesh.polygons))
