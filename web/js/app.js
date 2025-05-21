/* =================== refs =================== */
const $ = id => document.getElementById(id);
const btn      = $("btn"),
      urlIn    = $("url"),
      tbody    = $("tbody"),
      histBody = $("hist-body"),
      pieCtx   = $("pie");

const modal    = $("detailModal"),
      mTitle   = $("modalTitle"),
      mCnt     = $("modalContent");

$("modalClose").onclick = () => modal.classList.remove("is-active");
document.querySelector(".modal-background").onclick = $("modalClose").onclick;

/* ================= storage ================= */
let hist = JSON.parse(localStorage.getItem("hist") || "[]");
const save = () => localStorage.setItem("hist", JSON.stringify(hist));

/* ================= helpers ================= */
const icon = v =>
  `<i class="fa-solid fa-${v ? "check" : "xmark"} ${v ? "i-ok" : "i-bad"}"></i>`;

const flagsLine = d =>
  Object.entries(d)
    .filter(x => x[1] === true)
    .map(x => x[0])
    .join(", ");

function riskTag(score) {
  const lvl = score < 30 ? "baixo" : score < 70 ? "medio" : "alto";
  return `<span class="tag tag-risk ${lvl}">
           ${lvl[0].toUpperCase() + lvl.slice(1)}
         </span>`;
}

/* ================= render ================= */
function makeRow(j) {
  const tr = document.createElement("tr");
  tr.style.cursor = "pointer";
  tr.innerHTML = `
    <td>${j.url}</td>
    <td class="has-text-centered"
        style="color:${j.score >= 50 ? "red" : "green"}">${j.score}</td>
    <td class="has-text-centered">${flagsLine(j.details)}</td>
    <td>${j.screenshot ? `<img src="${j.screenshot}" width="60">` : ""}</td>`;
  tr.onclick = () => showModal(j);
  return tr;
}

function refreshHist() {
  histBody.innerHTML = "";
  let mal = 0, safe = 0;
  hist.forEach(r => {
    histBody.prepend(makeRow(r));
    r.score >= 50 ? mal++ : safe++;
  });
  if (window.chart) window.chart.destroy();
  window.chart = new Chart(pieCtx, {
    type: "pie",
    data: {
      labels: ["Maliciosas", "Seguras"],
      datasets: [{ data: [mal, safe] }]
    }
  });
}

/* ================= modal ================= */
const flagRow = (txt, val) =>
  `<tr><td>${txt}</td><td class="has-text-centered">${icon(val)}</td></tr>`;

function showModal(j) {
  const d = j.details;
  mTitle.textContent = j.url;
  mCnt.innerHTML = `
    <p><strong>Nível:</strong> ${riskTag(j.score)}
       &nbsp; <strong>Score:</strong> ${j.score}</p>
    ${j.screenshot ? `
      <div class="shot-wrap my-3">
        <img src="${j.screenshot}" style="max-width:95%">
      </div>` : ""}
    <table class="table is-fullwidth flag-table">
      <tbody>
        ${flagRow("Domínio popular (Top-1M)", d.popular_domain)}
        ${flagRow("Na blacklist PhishTank",   d.blacklist)}
        ${flagRow("Padrões suspeitos",        d.patterns)}
        ${flagRow("Domínio jovem (&lt;180d)", d.young_domain)}
        ${flagRow("SSL expirado",             d.ssl_expired)}
        ${flagRow("CN mismatch",              d.ssl_cn_mismatch)}
        ${flagRow("Dyn-DNS",                  d.dynamic_dns)}
        ${flagRow("Domínio parecido",         d.brand_similar)}
        ${flagRow("Redirect suspeito",        d.redirect_suspicious)}
        <tr><td>Hops</td>
            <td class="has-text-centered">${d.hops}</td></tr>
      </tbody>
    </table>`;
  modal.classList.add("is-active");
}

/* ================= submit ================= */
btn.onclick = async () => {
  let url = urlIn.value.trim();
  if (!url) return;
  if (!/^https?:\/\//i.test(url)) url = "http://" + url;

  btn.classList.add("is-loading");
  btn.disabled = true;
  try {
    const res = await fetch("/api/v2/score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    if (res.ok) {
      const j = await res.json();
      tbody.prepend(makeRow(j));
      hist.unshift(j);
      if (hist.length > 60) hist.pop();
      save();
      refreshHist();
    } else {
      alert("Erro " + res.status);
    }
  } finally {
    btn.disabled = false;
    btn.classList.remove("is-loading");
  }
};

/* ================= tabs ================= */
document.querySelectorAll(".tabs li").forEach(li => {
  li.onclick = () => {
    document.querySelectorAll(".tabs li")
      .forEach(x => x.classList.remove("is-active"));
    li.classList.add("is-active");
    const t = li.dataset.tab;
    document.querySelectorAll(".tab-content")
      .forEach(c => { c.style.display = c.id === t ? "" : "none"; });
  };
});

refreshHist();
