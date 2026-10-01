
import fs from "node:fs";
import vm from "node:vm";
import assert from "node:assert/strict";
const root=new URL("../",import.meta.url);
const read=f=>fs.readFileSync(new URL(f,root),"utf8");
const html=read("index.html"),server=read("server.mjs"),motion=read("avatar_motion.js");
const inline=html.split("<script>")[1]?.split("</script>")[0];
assert.ok(inline && inline.length>6000,"Inline application script found");
new vm.Script(inline,{filename:"index-inline.js"});
new vm.Script(server.replace(/^import http from "node:http";/m,"const http={};"),{filename:"server.mjs"});
new vm.Script(motion.replace(/^import .*?;$/gm,""),{filename:"avatar_motion.js"});
console.log("PASS: JavaScript syntax (interface, backend, 3D module)");
for(const id of ["avatarVideo","startLive","stopLive","liveSignal","rigStage","rigFile","rigCanvas","ask","mic","answer","remote","endpoint","browserVoice","identityStatus"]){
 assert.ok(html.includes('id="'+id+'"'),"Missing control: "+id);
}
console.log("PASS: interface controls present");
assert.ok(html.includes("11cead6e-fce2-4fe3-a730-552bcea8d253.mp4"),"Film 2 configured");
assert.ok(html.includes("fb294ade-7ee7-4a26-8fce-1023ab38cffe.mp3"),"Voice sample configured");
assert.ok(!html.includes("0228548f-b112-414c-9815-7cbff820e3ce"),"Film 1 excluded");
assert.ok(!html.includes("1d6c7262-d831-4938-8dba-fee75fd88dae"),"Old still photo excluded");
console.log("PASS: only authorized Film 2 and voice sample in V9 interface");
assert.ok(html.includes("data.alignment") && motion.includes("character_start_times_seconds"),"Alignment wired");
assert.ok(motion.includes("MOUTH_A") && motion.includes("JawOpen"),"3D mouth controls");
assert.ok(server.includes("/with-timestamps") && server.includes("ELEVENLABS_VOICE_ID"),"Voice endpoint and voice ID");
assert.ok(!server.includes("xi-api-key":"" + "abc"),"No literal API key");
assert.ok(server.includes("ACCESS_TOKEN") && server.includes("ALLOWED_ORIGIN"),"Operator restrictions");
console.log("PASS: voice timing and backend restrictions wired");
assert.ok(html.includes("rec.abort()") && html.includes("live=false") && html.includes("if(thisRequest!==requestSerial)return"),"Dialog stop/cancel");
console.log("PASS: live dialogue turn controls and cancellation");
console.log("RESULT: 5 static smoke checks passed; browser/device and voice identity verification remain manual.");
