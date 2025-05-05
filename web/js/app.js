const btn=document.getElementById("btn");
const tb=document.getElementById("tbody");
const urlIn=document.getElementById("url");
const histBody=document.getElementById("hist-body");
const exportBtn=document.getElementById("export");
const pieCtx=document.getElementById("pie");

let hist=JSON.parse(localStorage.getItem("hist")||"[]");
let chart=null;

function saveHist(){localStorage.setItem("hist",JSON.stringify(hist))}

function flagList(obj){
  return Object.entries(obj).filter(x=>x[1]===true).map(x=>x[0]).join(", ");
}

function renderHist(){
  histBody.innerHTML="";
  const counts={malicious:0,safe:0};
  hist.forEach(r=>{
    const tr=document.createElement("tr");
    tr.innerHTML=`
      <td>${r.url}</td>
      <td style="color:${r.malicious?'red':'green'}">${r.malicious?'Maliciosa':'Segura'}</td>
      <td>${flagList(r.details)}</td>`;
    histBody.appendChild(tr);
    r.malicious?counts.malicious++:counts.safe++;
  });
  if(chart)chart.destroy();
  chart=new Chart(pieCtx,{type:"pie",data:{labels:["Maliciosas","Seguras"],datasets:[{data:[counts.malicious,counts.safe]}]}});
}

function addResult(j){
  const row=`
    <tr>
      <td>${j.url}</td>
      <td style="color:${j.malicious?'red':'green'}">${j.malicious?'Maliciosa':'Segura'}</td>
      <td>${flagList(j.details)}</td>
    </tr>`;
  tb.innerHTML=row+tb.innerHTML;
  hist.unshift(j);
  if(hist.length>50)hist.pop();
  saveHist();
  renderHist();
}

btn.onclick=async()=>{
  const url=urlIn.value.trim();
  if(!url)return;
  btn.classList.add("is-loading");btn.disabled=true;
  try{
    const r=await fetch("/api/v1/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url})});
    if(r.ok){const j=await r.json();addResult(j);}
  }finally{
    btn.classList.remove("is-loading");btn.disabled=false;
  }
};

exportBtn.onclick=()=>{
  const blob=new Blob([JSON.stringify(hist)],{type:"application/json"});
  const a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="analise.json";
  a.click();
};

function initTabs(){
  document.querySelectorAll(".tabs li").forEach(li=>{
    li.onclick=()=>{
      document.querySelectorAll(".tabs li").forEach(x=>x.classList.remove("is-active"));
      li.classList.add("is-active");
      const tab=li.getAttribute("data-tab");
      document.querySelectorAll(".tab-content").forEach(div=>{div.style.display=div.id===tab?"":"none"});
    };
  });
}

renderHist();
initTabs();
