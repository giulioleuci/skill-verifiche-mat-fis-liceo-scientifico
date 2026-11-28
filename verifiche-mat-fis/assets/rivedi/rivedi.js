"use strict";
const LETTERE = "ABCDEFGHIJ", R = 2.3, TRACCIA = 0.15; // come omr.py
const ETICHETTA = { ok: "Letta", proposta: "Da confermare", annullata: "Annullata", vuota: "Vuota" };
const $ = (id) => document.getElementById(id);
const token = document.querySelector('meta[name="token"]').content;
let dati, ordine, corrente = 0, qn = 1, tenuta = 0, soloDubbi = true, timer = 0;
const dubbio = (d) => (d.stato === "proposta" || d.stato === "annullata") && !d.rivista;
const nDubbi = (f) => f.domande.filter(dubbio).length;
// con "da rivedere" resta in elenco anche l'ultima domanda toccata, per vedere (e disfare) la modifica
const righe = (f) => soloDubbi ? f.domande.filter(d => dubbio(d) || d.n === tenuta).sort((a, b) => a.conf - b.conf || a.n - b.n) : f.domande;
function h(tag, cls = "", ...figli) {
    const e = document.createElement(tag);
    e.className = cls;
    e.append(...figli);
    return e;
}
const svgEl = (tag, attr) => {
    const e = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const k in attr)
        e.setAttribute(k, String(attr[k]));
    return e;
};
function apri(i) {
    corrente = i;
    tenuta = 0;
    qn = righe(ordine[i])[0]?.n ?? 1;
    render();
}
function imposta(d, r) {
    d.risposta = r;
    d.rivista = true;
    tenuta = d.n;
    const l = righe(ordine[corrente]);
    qn = l[l.indexOf(d) + 1]?.n ?? d.n;
    render();
    salva();
}
function muovi(passo) {
    const l = righe(ordine[corrente]);
    const i = Math.max(0, Math.min(l.length - 1, l.findIndex(d => d.n === qn) + passo));
    qn = l[i]?.n ?? qn;
    render();
}
function render() {
    const f = ordine[corrente];
    $("conta").textContent = String(dati.fogli.reduce((s, x) => s + nDubbi(x), 0));
    $("coda").replaceChildren(...ordine.map((x, i) => {
        const b = h("button", i === corrente ? "attivo" : "", h("span", "", `${x.id} ${x.nome}`.trim()));
        if (nDubbi(x))
            b.append(h("span", "badge", String(nDubbi(x))));
        b.onclick = () => apri(i);
        return b;
    }));
    const img = $("scan"), src = `/img/${f.id}.png`;
    if (!img.src.endsWith(src)) {
        img.src = src;
        $("nome-img").src = `/img/${f.id}_nome.png`;
    }
    const nome = $("nome");
    if (document.activeElement !== nome)
        nome.value = f.nome;
    const ov = $("ov");
    ov.replaceChildren();
    const bolle = dati.geom[f.codice];
    for (const d of f.domande) {
        const riga = bolle[d.n - 1];
        if (d.n === qn)
            ov.append(svgEl("rect", { class: "banda", x: riga[0][0] - 14, y: riga[0][1] - 4, width: riga[riga.length - 1][0] - riga[0][0] + 20, height: 8 }));
        riga.forEach(([x, y], k) => {
            const scelta = d.risposta === LETTERE[k];
            const c = svgEl("circle", { cx: x, cy: y, r: R + 0.9, role: "button", "aria-label": `Domanda ${d.n}, alternativa ${LETTERE[k]}` });
            c.setAttribute("class", "c" + (d.fill[k] >= TRACCIA ? " segno" : "") + (d.risposta === "*" && d.fill[k] >= TRACCIA ? " ann" : "")
                + (scelta ? (d.rivista || d.stato === "ok" ? " ok" : " prop") : ""));
            c.addEventListener("click", () => { qn = d.n; imposta(d, scelta ? "" : LETTERE[k]); });
            ov.append(c);
        });
    }
    $("filtri").replaceChildren(...[["Da rivedere", true], ["Tutte", false]].map(([t, v]) => {
        const b = h("button", "", t);
        b.setAttribute("aria-pressed", String(soloDubbi === v));
        b.onclick = () => { soloDubbi = v; render(); };
        return b;
    }));
    const l = righe(f);
    $("righe").replaceChildren(...(l.length ? l.map(d => {
        const b = h("button", "riga" + (d.n === qn ? " attiva" : ""), h("span", "", String(d.n)), h("span", "chip", d.risposta || "—"), h("span", `s ${d.rivista ? "" : d.stato}`, d.rivista ? "Rivista" : ETICHETTA[d.stato]), h("span", "barre"));
        b.lastElementChild.append(...d.fill.map((v, k) => { const i = h("i"); i.style.height = `${Math.max(1, v * 100)}%`; i.title = `${LETTERE[k]} ${v}`; return i; }));
        b.onclick = () => { qn = d.n; render(); };
        return b;
    }) : [h("p", "vuoto", "Nessuna lettura da rivedere in questo foglio.")]));
    $("righe").querySelector(".attiva")?.scrollIntoView({ block: "nearest" });
}
function salva() {
    const stato = (t, errore = false) => { $("stato").textContent = t; $("stato").className = errore ? "errore" : ""; };
    stato("Salvataggio…");
    clearTimeout(timer);
    timer = window.setTimeout(async () => {
        try {
            const r = await fetch("/salva", {
                method: "POST", headers: { "X-Token": token, "Content-Type": "application/json" },
                body: JSON.stringify({ fogli: dati.fogli.map(f => ({ id: f.id, nome: f.nome, domande: f.domande.map(({ n, risposta, rivista }) => ({ n, risposta, rivista })) })) }),
            });
            if (r.ok)
                stato("Salvato");
            else
                stato(`Non salvato: ${await r.text()}`, true);
        }
        catch {
            stato("Non salvato: server non raggiungibile", true);
        }
    }, 400);
}
addEventListener("keydown", e => {
    if (!ordine.length || e.target.tagName === "INPUT" || e.ctrlKey || e.metaKey || e.altKey)
        return;
    const f = ordine[corrente], d = f.domande.find(x => x.n === qn), k = e.key, i = LETTERE.indexOf(k.toUpperCase());
    if (k === "ArrowDown")
        muovi(1);
    else if (k === "ArrowUp")
        muovi(-1);
    else if (k === "Enter")
        imposta(d, d.risposta);
    else if (k === "Backspace" || k === "Delete" || k === "0")
        imposta(d, "");
    else if (k === "*")
        imposta(d, "*");
    else if (k.length === 1 && i >= 0 && i < d.fill.length)
        imposta(d, LETTERE[i]);
    else if (k === "]")
        apri(Math.min(corrente + 1, ordine.length - 1));
    else if (k === "[")
        apri(Math.max(corrente - 1, 0));
    else
        return;
    e.preventDefault();
});
$("nome").addEventListener("input", e => { ordine[corrente].nome = e.target.value; salva(); });
$("nome").addEventListener("change", render);
(async () => {
    dati = await (await fetch("/letture.json")).json();
    const dub = (f) => Math.min(2, ...f.domande.filter(dubbio).map(d => d.conf)); // fogli piu' dubbi per primi
    ordine = dati.fogli.filter(f => f.domande.length).sort((a, b) => dub(a) - dub(b));
    if (dati.errori.length)
        $("avviso").textContent = `${dati.errori.length} file non letti: vedi il foglio Anomalie di risposte_scansioni.xlsx`;
    if (!ordine.length) {
        $("righe").replaceChildren(h("p", "vuoto", "Nessun foglio letto."));
        return;
    }
    apri(0);
})();
