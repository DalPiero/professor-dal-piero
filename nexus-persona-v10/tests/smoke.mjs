import fs from "node:fs";
import vm from "node:vm";
import assert from "node:assert/strict";
const root=new URL("../",import.meta.url);
const read=f=>fs.readFileSync(new URL(f,root),"utf8");
const html=read("index.html"), knowledge=read("knowledge.js"),server=read("server.mjs"),motion=read("avatar_motion.js");
const inline=html.split("<script>")[1]?.split("</script>")[0];
assert.ok(inline?.includes("renderSuggestions"));
new vm.Script(inline,{filename:"index.html inline JS"});
new vm.Script(server.replace(/^import http from "node:http";/m,"const http={};"),{filename:"server.mjs"});
new vm.Script(motion.replace(/^import .*?;$/gm,""),{filename:"avatar_motion.js"});
console.log("PASS: sintaxe dos três módulos");
const context={};vm.runInNewContext(knowledge,context);
const kb=context.NEXUS_KB;assert.ok(kb?.resolve && kb.topics?.length>=18);
const cases=[
["O que é BRASIL 2075?","brasil"],
["Como funciona o piloto de 90 dias?","piloto"],
["O que é NEXUS EDU?","edu"],
["O que é NEXUS MED?","med"],
["O que é NEXUS ODONTO?","odonto"],
["O que é NEXUS UNIVERSAL?","universal"],
["Qual é o papel da universidade?","papel"],
["A IA vai substituir os professores?","autonomia"],
["Quem é você?","avatar"],
["Qual é a preocupação com privacidade?","etica"],
["Quais são suas fontes?","documentos"]
];
for(const [q,id] of cases){
 const result=kb.resolve(q,null);
 assert.equal(result.id,id,JSON.stringify({q,result}));
 assert.ok(result.answer.length>25);
}
const follow=kb.resolve("Explique melhor","edu");
assert.equal(follow.id,"edu");assert.ok(follow.answer.toLowerCase().includes("pedagogic"));
assert.equal(kb.resolve("Como tratar fungo numa roseira?",null).found,false);
console.log("PASS: 11 perguntas, acompanhamento contextual e limitação da base");
for(const id of ["q","ask","mic","startLive","stopLive","browserVoice","liveSignal","modeInfo","localSource","avatarVideo","rigFile","answer"]){
 assert.ok(html.includes('id="'+id+'"'),"ID missing: "+id)
}
assert.ok(html.includes('id="browserVoice" type="checkbox" checked'),"A voz provisória não está ativada por padrão");
assert.ok(html.includes("NEXUS_KB.resolve(question,contextTopic)"));
assert.ok(html.includes('script src="./knowledge.js"'));
assert.ok(html.includes("avatar_motion.js"));
console.log("PASS: interface local conecta texto, contexto, voz e microfone");
assert.ok(html.includes("11cead6e-fce2-4fe3-a730-552bcea8d253.mp4"));
assert.ok(html.includes("fb294ade-7ee7-4a26-8fce-1023ab38cffe.mp3"));
assert.ok(!html.includes("0228548f-b112-414c-9815-7cbff820e3ce"));
assert.ok(!html.includes("1d6c7262-d831-4938-8dba-fee75fd88dae"));
console.log("PASS: Filme 2 e amostra de voz, sem mídia anterior");
assert.ok(server.includes("ELEVENLABS_VOICE_ID")&&server.includes("/with-timestamps"));
assert.ok(server.includes("ACCESS_TOKEN")&&server.includes("ALLOWED_ORIGIN"));
console.log("PASS: integração opcional privada preparada");
console.log("RESULTADO: validação estática e consulta real da base local aprovadas. Testes de microfone e voz autorizada em navegador continuam necessários.");
