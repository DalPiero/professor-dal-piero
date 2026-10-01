// Tests ONLY — fake model and fake voice services. No external requests or costs.
globalThis.fetch=async function(input){
 const url=String(input);
 if(url.includes("api.openai.com/v1/responses")){
   return new Response(JSON.stringify({output:[{content:[{type:"output_text",text:"O BRASIL 2075 propõe investigação universitária."}]}]}),{status:200,headers:{"content-type":"application/json"}});
 }
 if(url.includes("api.elevenlabs.io")){
   return new Response(JSON.stringify({audio_base64:Buffer.from("FAKE_AUDIO_FOR_TESTS").toString("base64"),
    alignment:{characters:["O"," ","B"],character_start_times_seconds:[0,.15,.25],character_end_times_seconds:[.15,.25,.4]}}),
    {status:200,headers:{"content-type":"application/json"}});
 }
 throw Error("Unexpected network request in test: "+url);
};
