import {spawn} from "node:child_process";
import assert from "node:assert/strict";
const port=18787,origin="https://nexus.example.test",base="http://127.0.0.1:"+port;
const env={...process.env,PORT:String(port),ALLOWED_ORIGIN:origin,ACCESS_TOKEN:"test-operator",OPENAI_API_KEY:"test-model",ELEVENLABS_API_KEY:"test-voice",ELEVENLABS_VOICE_ID:"test-authorized-voice"};
const child=spawn(process.execPath,["--import",new URL("./mock_api.mjs",import.meta.url).pathname,new URL("../server.mjs",import.meta.url).pathname],{env,stdio:["ignore","pipe","pipe"]});
let stdout="",stderr="";child.stdout.on("data",d=>stdout+=d);child.stderr.on("data",d=>stderr+=d);
try{
 let started=false;
 for(let i=0;i<45;i++){
   if(child.exitCode!==null)throw Error("Backend exited: "+stderr);
   if(stdout.includes("servidor")){started=true;break}
   await new Promise(r=>setTimeout(r,150));
 }
 assert.ok(started,"Backend did not start: "+stderr);
 const send=(originValue,token)=>fetch(base+"/api/chat",{method:"POST",headers:{"origin":originValue,"authorization":token,"content-type":"application/json"},body:JSON.stringify({message:"Qual é o projeto?"})});
 const wrongOrigin=await send("https://unauthorized.example.test","Bearer test-operator");
 assert.equal(wrongOrigin.status,403);
 console.log("PASS: blocks foreign origins");
 const wrongToken=await send(origin,"Bearer invalid");
 assert.equal(wrongToken.status,401);
 console.log("PASS: blocks unauthenticated requests");
 const ok=await send(origin,"Bearer test-operator");
 assert.equal(ok.status,200);
 const body=await ok.json();
 assert.ok(body.answer.includes("BRASIL 2075"));
 assert.equal(body.voice_status,"official_voice_configured");
 assert.ok(typeof body.audio_base64==="string" && body.audio_base64.length>0);
 assert.deepEqual(body.alignment?.characters,["O"," ","B"]);
 console.log("PASS: question → model → authorized voice → time-alignment response (MOCKED, no real AI/voice services)");
}catch(e){console.error(e);process.exitCode=1}finally{
 child.kill("SIGTERM");
 await new Promise(r=>{if(child.exitCode!==null||child.signalCode!==null)return r();child.once("exit",r);setTimeout(r,700)});
}
