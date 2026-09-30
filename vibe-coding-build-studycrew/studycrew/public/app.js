// StudyCrew page script. Shows text with textContent (never innerHTML), so names can't turn into running code.
const SLOTS = ["Mon 4 pm", "Tue 4 pm", "Wed 4 pm", "Thu 4 pm", "Fri 4 pm", "Sat 10 am", "Sun 10 am"];
const $ = s => document.querySelector(s);
const form = $("#join"), button = form.querySelector("button"), error = $("#error");
let token = "";

for (const s of SLOTS) {
  const label = document.createElement("label"), box = document.createElement("input");
  box.type = "checkbox"; box.name = "slots"; box.value = s;
  label.append(box, s); $("#slots").append(label);
}

function showCrew(crew) {
  form.hidden = true; $("#crew").hidden = false;
  $("#when").textContent = `${crew.slot} · ${crew.place}`;
  $("#what").textContent = `${crew.subject}, ${crew.chapter}`;
  $("#members").replaceChildren(...crew.members.map(n => { const li = document.createElement("li"); li.textContent = n; return li; }));
}

// Bot check (Cloudflare Turnstile). The page only gets a token; the server verifies it.
window.onTurnstileLoad = async () => {
  const config = await (await fetch("/api/config")).json();
  $("#codeRow").hidden = !config.classCode;
  window.turnstile.render("#turnstile", {
    sitekey: config.turnstileSiteKey,
    callback: t => { token = t; button.disabled = false; },
    "expired-callback": () => { token = ""; button.disabled = true; },
  });
};

form.addEventListener("submit", async e => {
  e.preventDefault(); error.textContent = ""; button.disabled = true;
  const data = Object.fromEntries(new FormData(form));
  data.slots = [...form.querySelectorAll("input[name=slots]:checked")].map(b => b.value);
  data.turnstileToken = token;
  try {
    const res = await fetch("/api/join", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(data) });
    const out = await res.json();
    if (!res.ok) throw new Error(out.error || "Something went wrong.");
    localStorage.setItem("studycrew-key", out.key);
    showCrew(out.crew);
  } catch (err) {
    error.textContent = err.message;
    window.turnstile?.reset(); token = "";
  }
});

// Coming back later? Show the same crew.
const key = localStorage.getItem("studycrew-key");
if (key) fetch(`/api/crew?key=${encodeURIComponent(key)}`).then(r => (r.ok ? r.json() : null)).then(out => out && showCrew(out.crew));
