
/* NEXUS V9 — optional, manually approved 3D facial rig.
   The ORIGINAL Film 2 remains sole visual identity reference.
   Do NOT substitute a generic model for the person in the film.
   If no verified GLB is selected, visual fallback is a camera-like 2.5D
   move of a real paused Film 2 frame, with no claim of lip sync. */
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
const byId=id=>document.getElementById(id);
const canvas=byId("rigCanvas"),rootBox=byId("rigStage"),input=byId("rigFile");
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x081a2b);
const camera=new THREE.PerspectiveCamera(36,1,.01,100);
camera.position.set(0,-7.5,2.1);
const renderer=new THREE.WebGLRenderer({antialias:true,canvas,powerPreference:"low-power"});
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.5));
renderer.outputColorSpace=THREE.SRGBColorSpace;
scene.add(new THREE.HemisphereLight(0xf8f6eb,0x3a5c81,2.2));
const key=new THREE.DirectionalLight(0xffffff,2.3);
key.position.set(-3,-4,7);scene.add(key);
const fill=new THREE.DirectionalLight(0xa2b6d3,1.0);
fill.position.set(4,-2,4);scene.add(fill);
const controls=new OrbitControls(camera,canvas);
controls.enableDamping=true;controls.target.set(0,0,1.7);
let model=null,modelURL=null,dict={},playing=false,playback=null,alignment=null,wasLoaded=false;
let timeBase=performance.now(),blinkAt=0,lastFrame=performance.now(),currentJaw=0;
const morph=(key,v)=>{for(const {mesh,index} of dict[key]||[])mesh.morphTargetInfluences[index]=v};
function resize(){
const r=rootBox.getBoundingClientRect();
if(r.width<20||r.height<20)return;
camera.aspect=r.width/r.height;camera.updateProjectionMatrix();
renderer.setSize(r.width,r.height,false)
}
new ResizeObserver(resize).observe(rootBox);
function reset(){
for(const k of Object.keys(dict))morph(k,0);
currentJaw=0;
}
function load(file){
if(!file||!/\.glb$/i.test(file.name)||file.size>180*1024*1024){
byId("rigStatus").textContent="Selecione GLB da malha facial aprovada, até 180 MB.";return;
}
playing=false;reset();
if(model){scene.remove(model);model.traverse(x=>{if(x.isMesh){x.geometry.dispose();for(const m of Array.isArray(x.material)?x.material:[x.material])m.dispose()}})}
if(modelURL)URL.revokeObjectURL(modelURL);
modelURL=URL.createObjectURL(file);
byId("rigStatus").textContent="Carregando modelo facial revisado...";
new GLTFLoader().load(modelURL,gltf=>{
model=gltf.scene;scene.add(model);dict={};
model.traverse(mesh=>{
if(mesh.isMesh&&mesh.morphTargetDictionary){
for(const [name,index]of Object.entries(mesh.morphTargetDictionary)){
(dict[name]||=[]).push({mesh,index});
}
}
});
wasLoaded=true;
const box=new THREE.Box3().setFromObject(model),center=box.getCenter(new THREE.Vector3());
const d=box.getSize(new THREE.Vector3());
controls.target.copy(center);
camera.position.copy(center).add(new THREE.Vector3(0,-Math.max(d.x,d.y,d.z)*2.2,d.z*.12));
controls.update();
rootBox.hidden=false;resize();
const names=Object.keys(dict);
byId("rigStatus").textContent=names.length
 ? "Malha carregada. "+names.length+" controles identificados; revise identidade e deformações antes do público."
 : "GLB sem shape keys detectáveis. Exportar com morph targets ativos.";
},null,()=>byId("rigStatus").textContent="Não foi possível abrir o GLB. Verifique a exportação.");
}
input.addEventListener("change",e=>load(e.target.files[0]));
function trackAt(t){
if(!alignment||!Array.isArray(alignment.characters))return null;
const starts=alignment.character_start_times_seconds||[];
const ends=alignment.character_end_times_seconds||[];
let lo=0,hi=starts.length-1;
while(lo<=hi){const m=(lo+hi)>>1;if(starts[m]<=t)lo=m+1;else hi=m-1}
const idx=Math.max(0,hi);
if(t<starts[idx]||t>ends[idx]+.035)return null;
return alignment.characters[idx]||null
}
// Approximate vowel category mapping, NOT a phonetic conversion.
function approximateViseme(char){
if(!char||/\s/.test(char))return null;
const c=char.toLocaleUpperCase("pt-BR").normalize("NFD").replace(/[\u0300-\u036f]/g,"");
if("A".includes(c))return "MOUTH_A";
if("E".includes(c))return "MOUTH_E";
if("I".includes(c))return "MOUTH_C";
if("O".includes(c))return "MOUTH_D";
if("U".includes(c))return "MOUTH_G";
if("MBP".includes(c))return "MOUTH_B";
if("FV".includes(c))return "MOUTH_F";
return "MOUTH_H";
}
window.addEventListener("nexus-motion",e=>{
playing=!!e.detail.active;
playback=e.detail.player||null;
alignment=e.detail.alignment||null;
timeBase=performance.now();
if(!playing)reset();
});
function renderFrame(now){
requestAnimationFrame(renderFrame);
if(!wasLoaded){return}
const frameDt=Math.max(0,Math.min(.2,(now-lastFrame)/1000));lastFrame=now;
let jaw=0,tag=null;
if(playing){
 const currentT=playback && Number.isFinite(playback.currentTime)?playback.currentTime:(now-timeBase)/1000;
 tag=trackAt(currentT);
 jaw=tag?0.38:0.04;
 if(playback && !playback.paused && !alignment){jaw=.12+.10*Math.abs(Math.sin(currentT*11));}
 const target=jaw;
 currentJaw+=(target-currentJaw)*Math.min(1,frameDt*16);
 morph("JawOpen",currentJaw);
 for(const v of "ABCDEFGH")morph("MOUTH_"+v,tag===null?0:(tag && approximateViseme(tag)==="MOUTH_"+v)?.60:0);
 // Only blink an actual prepared eyelid rig; periodic movement is illustrative.
 const phase=now/1000;
 const blink=Math.exp(-Math.pow(((phase%4.7)-3.62)*12,2));
 morph("BlinkBoth",blink);
 // No head turn unless approved rig: a tiny natural vertical position shift only.
 model.position.z=.006*Math.sin(phase*1.6);
 }else{
 currentJaw+=(0-currentJaw)*Math.min(1,frameDt*11);morph("JawOpen",currentJaw);
 model.position.z=0;
 }
 controls.update();renderer.render(scene,camera);
}
requestAnimationFrame(renderFrame);
