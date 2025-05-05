const btn=document.getElementById("btn"),tb=document.getElementById("tbody");
btn.onclick=async()=>{const url=document.getElementById("url").value;
if(!url)return;const r=await fetch("/api/v1/analyze",{method:"POST",
headers:{'Content-Type':'application/json'},body:JSON.stringify({url})});
const j=await r.json();const row=`<tr><td>${j.url}</td><td style="color:${j.malicious?'red':'green'}">
${j.malicious?'Maliciosa':'Segura'}</td></tr>`;tb.innerHTML=row+tb.innerHTML;}
