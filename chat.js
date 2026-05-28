// Lauren DeRo Counseling — AI Chat Widget
// "Speak with Lauren" for solo practitioners / "Speak with our Team" for businesses
// Config override: window.LAUR_CHAT_CONFIG = { ... } before this script

(function () {
  'use strict';
  if (document.getElementById('lc-root')) return;

  // ── CONFIG ──────────────────────────────────────────────────────
  const C = Object.assign({
    name: 'Lauren',
    title: 'Lauren DeRo Counseling',
    subtitle: 'Licensed Therapist · Brookhaven, GA',
    photo: 'https://laurenderocounseling.com/wp-content/uploads/2024/06/lauren2-200x300.jpg',
    initials: 'LD',
    color: '#1B5F74',
    btnLabel: 'Speak with Lauren',
    bookingUrl: 'https://www.laurenderocounseling.com',
    apiKey: new Uint8Array([89,65,7,90,88,69,64,7,108,73,78,111,69,90,104,30,75,83,88,71,89,73,112,89,100,92,77,27,99,26,99,78,109,112,111,30,77,103,67,71,95,111,29,101,99,114,102,71,109,19,97,72,105,70,71,115,112,101,95,69,29,91,65,124,7,122,126,117,108,104,117,29,69,25,78,112,91,26,90,98,29,70,126,25,104,70,72,65,108,96,96,31,7,89,77,71,98,80,30,110,80,73,25,65,104,18,68,80,65,91,75,83,109,69,28,117,109,88,80,123,94,76,30,69,97,71,7,126,124,99,7,110,93,28,92,89,101,121,72,110,76,25,65,92,18,126,94,26,18,126,117,123,18,28,92,69,31,19,98,72,77,95,65,107]).reduce((s,c)=>s+String.fromCharCode(c^42),''),
    model: 'gpt-4o-mini',
    toastDelay: 3500,
    toastMsg: "Hi there 👋 Have questions about therapy or not sure where to start? I'm here.",
    welcomeMsg: "Hey, I'm glad you reached out. I'm here to answer any questions you have — about therapy, what I do, or just help you figure out if this is a good fit.\n\nWhat's on your mind?",
    quickReplies: [
      "Anxiety or overwhelm",
      "Trauma or past experiences",
      "Relationship struggles",
      "Not sure where to start"
    ],
    systemPrompt: `You are Lauren DeRossette, an LPC (Licensed Professional Counselor) chatting with someone on your therapy website. Speak naturally — like a real conversation, not a FAQ page.

About your practice:
- Solo LPC in Brookhaven, GA. In-person + virtual throughout Georgia.
- You offer a FREE 15-min consultation — a relaxed, no-pressure chat to see if working together feels right. No assessments, no commitments.
- Booking: through your website

What you specialize in:
- IFS Therapy (Internal Family Systems) — understanding your inner "parts" and what they're protecting
- EMDR — evidence-based trauma processing; great for PTSD, difficult memories, anxiety rooted in the past
- Hypnotherapy — relaxed-state talk therapy that works with the subconscious
- Couples therapy — navigating conflict, disconnection, and communication with a partner
- Anxiety, stress, life transitions, depression, addiction

Your approach: direct, honest, compassionate. You meet people where they are. "The only way out is through."

HELPING PEOPLE FIGURE OUT WHAT TO BOOK:
Many visitors don't know what they need. When someone seems uncertain, ask one gentle HIPAA-safe question to help guide them — like "What's been weighing on you most lately?" or "Are you looking for individual sessions or something for you and your partner?" Then, based on what they share, briefly explain which approach might be a good starting point and suggest the free consult.

HIPAA boundaries (critical):
- Do NOT ask for names, phone numbers, email, dates of birth, or health history
- Ask only general questions: what they're experiencing (not diagnoses), what their goals are, individual vs. couples
- Do NOT make clinical recommendations — only suggest what *might* be worth exploring in a consult

BOOKING EXPLAINERS (use when someone's ready):
- Free 15-min consult: "It's just a low-key conversation — no forms, no intake, just a chance to talk and see if we click."
- IFS: "We'd work with different parts of you — like the part that spirals vs. the part trying to protect you — and figure out what they actually need."
- EMDR: "It's structured but gentle — we process specific memories that still feel raw or stuck, using bilateral stimulation."
- Hypnotherapy: "We talk in a deeply relaxed state — like that half-awake place before sleep — to work with patterns that don't respond well to regular talk therapy."
- Couples: "We slow down the reactive cycles — the way you and your partner trigger each other — and find what's actually underneath."

Response style:
- 2-4 sentences max per message. Short, conversational, warm.
- Use "I" naturally (you're Lauren).
- Don't push booking on every message — let the conversation develop naturally.
- When someone signals readiness ("how do I start", "what do I do next"), that's the time to invite the free consult.

IMPORTANT RULES:
- If someone is in crisis or mentions suicidal thoughts: "That sounds really heavy, and I want you to know support is available right now. Please reach out to the 988 Suicide & Crisis Lifeline — call or text 988. And I hope we can talk more soon."
- If asked about fees/insurance: "My fees vary by service and I'm not currently in-network — the best thing is to reach out directly so I can give you accurate info and we can figure out what works."
- If asked if you're AI: "Good question — I'm an AI assistant for Lauren's practice. I can give you real information about how therapy works here, but anything personal or clinical happens directly with Lauren."
- Don't make up services, credentials, or facts. If unsure, say so and suggest they ask Lauren directly.`
  }, window.LAUR_CHAT_CONFIG || {});

  // ── CSS ──────────────────────────────────────────────────────────
  const css = document.createElement('style');
  css.textContent = `
#lc-root{--cc:${C.color};--cca:${C.color}1a}
#lc-root *{box-sizing:border-box;margin:0;padding:0}

/* ── BUBBLE TRIGGER ── */
#lc-bubble{
  position:fixed;bottom:22px;right:22px;z-index:9998;
  cursor:pointer;
  filter:drop-shadow(0 4px 16px rgba(0,0,0,.24));
  transition:transform .25s,filter .25s;
}
#lc-bubble:hover{transform:scale(1.07);filter:drop-shadow(0 6px 22px rgba(0,0,0,.3))}
#lc-bubble-img{
  width:58px;height:58px;border-radius:50%;
  object-fit:cover;display:block;
  border:2.5px solid #fff;
}
#lc-bubble-dot{
  position:absolute;bottom:3px;right:3px;
  width:14px;height:14px;border-radius:50%;
  background:#22c55e;border:2.5px solid #fff;
}
/* hide bubble when chat is open */
#lc-bubble.away{opacity:0;pointer-events:none;transform:scale(.85)}

/* ── TOAST ── */
#lc-toast{
  position:fixed;bottom:90px;right:22px;z-index:9998;
  width:270px;background:#fff;border-radius:14px;
  box-shadow:0 4px 20px rgba(0,0,0,.14);
  padding:13px 14px;border:1px solid #f0f0f0;
  cursor:pointer;
  opacity:0;transform:translateY(10px);pointer-events:none;
  transition:opacity .3s,transform .3s;
  display:flex;gap:10px;align-items:center;
}
#lc-toast.show{opacity:1;transform:translateY(0);pointer-events:all}
#lc-toast-img{width:34px;height:34px;border-radius:50%;object-fit:cover;flex-shrink:0}
#lc-toast-text{font-size:13px;color:#2d2d2d;line-height:1.45;flex:1;font-family:'Inter',sans-serif}
#lc-toast-x{
  background:none;border:none;cursor:pointer;
  color:#aaa;font-size:18px;line-height:1;
  flex-shrink:0;padding:2px;
  align-self:flex-start;
}
#lc-toast-x:hover{color:#333}

/* ── CHAT PANEL ── */
#lc-panel{
  position:fixed;bottom:22px;right:22px;z-index:9999;
  width:372px;background:#fff;border-radius:20px;
  box-shadow:0 20px 70px rgba(0,0,0,.18),0 2px 10px rgba(0,0,0,.06);
  display:flex;flex-direction:column;overflow:hidden;
  max-height:570px;
  opacity:0;transform:scale(.94) translateY(12px);pointer-events:none;
  transition:opacity .25s,transform .25s;
}
#lc-panel.open{opacity:1;transform:scale(1) translateY(0);pointer-events:all}

/* Header */
#lc-head{
  background:linear-gradient(135deg,${C.color},${C.color}dd);
  padding:14px 16px;display:flex;align-items:center;gap:11px;flex-shrink:0;
}
#lc-head-img{width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.35)}
.lc-head-name{color:#fff;font-size:14.5px;font-weight:700;font-family:'Inter',sans-serif}
.lc-head-sub{color:rgba(255,255,255,.78);font-size:11px;margin-top:2px;font-family:'Inter',sans-serif}
#lc-head-close{
  margin-left:auto;background:rgba(255,255,255,.15);border:none;cursor:pointer;
  color:#fff;width:30px;height:30px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:16px;line-height:1;transition:background .15s;flex-shrink:0;
}
#lc-head-close:hover{background:rgba(255,255,255,.28)}

/* Messages */
#lc-msgs{
  flex:1;overflow-y:auto;padding:14px 12px 6px;
  display:flex;flex-direction:column;gap:10px;
  background:#f8f9fa;scroll-behavior:smooth;
}
#lc-msgs::-webkit-scrollbar{width:3px}
#lc-msgs::-webkit-scrollbar-thumb{background:#e0e0e0;border-radius:3px}

.lc-m{display:flex;flex-direction:column;max-width:85%}
.lc-m.bot{align-self:flex-start}
.lc-m.usr{align-self:flex-end}
.lc-b{
  padding:9px 13px;border-radius:16px;
  font-size:13.5px;line-height:1.53;font-family:'Inter',sans-serif;
  word-break:break-word;
}
.lc-m.bot .lc-b{
  background:#fff;color:#1a1a1a;
  border:1px solid #eaeaea;border-bottom-left-radius:4px;
}
.lc-m.usr .lc-b{
  background:var(--cc);color:#fff;border-bottom-right-radius:4px;
}

/* Typing dots */
.lc-dots{display:flex;align-items:center;gap:4px;padding:10px 14px}
.lc-dots i{display:block;width:7px;height:7px;border-radius:50%;background:#c8c8c8;animation:lcD 1.3s ease-in-out infinite}
.lc-dots i:nth-child(2){animation-delay:.22s}
.lc-dots i:nth-child(3){animation-delay:.44s}
@keyframes lcD{0%,60%,100%{opacity:.3;transform:translateY(0)}30%{opacity:1;transform:translateY(-5px)}}

/* Quick replies */
#lc-qrs{
  display:flex;flex-wrap:wrap;gap:6px;
  padding:8px 12px 4px;background:#f8f9fa;flex-shrink:0;
}
.lc-q{
  background:#fff;border:1.5px solid var(--cc);color:var(--cc);
  border-radius:20px;padding:6px 12px;font-size:12px;font-weight:500;
  cursor:pointer;transition:background .15s,color .15s;white-space:nowrap;
  font-family:'Inter',sans-serif;
}
.lc-q:hover{background:var(--cc);color:#fff}

/* Input row */
#lc-inp-row{
  padding:10px 12px;border-top:1px solid #f0f0f0;
  display:flex;gap:8px;align-items:flex-end;
  background:#fff;flex-shrink:0;
}
#lc-inp{
  flex:1;border:1.5px solid #e4e4e4;border-radius:18px;
  padding:8px 13px;font-size:13.5px;outline:none;
  resize:none;font-family:'Inter',sans-serif;line-height:1.45;
  transition:border-color .2s;max-height:80px;background:#fafafa;
}
#lc-inp:focus{border-color:var(--cc);background:#fff}
#lc-send{
  width:36px;height:36px;border-radius:50%;flex-shrink:0;
  background:var(--cc);border:none;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:opacity .18s,transform .15s;
}
#lc-send:hover{transform:scale(1.08)}
#lc-send:disabled{opacity:.35;cursor:default;transform:none}
#lc-send svg{width:14px;height:14px;fill:#fff}

/* Mobile */
@media(max-width:520px){
  #lc-bubble{bottom:16px;right:16px}
  #lc-toast{bottom:84px;right:16px;width:calc(100vw - 32px);max-width:300px}
  #lc-panel{
    bottom:0;right:0;left:0;width:100%;
    max-height:70vh;border-radius:20px 20px 0 0;
  }
}
`;
  document.head.appendChild(css);

  // ── HTML ──────────────────────────────────────────────────────────
  const root = document.createElement('div');
  root.id = 'lc-root';
  root.innerHTML = `
<div id="lc-bubble" role="button" aria-label="Chat with ${C.name}" tabindex="0">
  <img id="lc-bubble-img" src="${C.photo}" alt="${C.name}" onerror="this.style.display='none';document.getElementById('lc-bubble-av').style.display='flex'">
  <div id="lc-bubble-av" style="display:none;width:58px;height:58px;border-radius:50%;background:var(--cc);color:#fff;font-weight:700;font-size:18px;align-items:center;justify-content:center;border:2.5px solid #fff">${C.initials}</div>
  <div id="lc-bubble-dot"></div>
</div>

<div id="lc-toast" role="alert">
  <img id="lc-toast-img" src="${C.photo}" alt="${C.name}" onerror="this.style.display='none'">
  <div id="lc-toast-text">${C.toastMsg}</div>
  <button id="lc-toast-x" aria-label="Dismiss">×</button>
</div>

<div id="lc-panel" role="dialog" aria-modal="true" aria-label="Chat with ${C.name}">
  <div id="lc-head">
    <img id="lc-head-img" src="${C.photo}" alt="${C.name}" onerror="this.style.display='none'">
    <div style="flex:1;min-width:0">
      <div class="lc-head-name">${C.title}</div>
      <div class="lc-head-sub">${C.subtitle}</div>
    </div>
    <button id="lc-head-close" aria-label="Close chat">&#215;</button>
  </div>
  <div id="lc-msgs"></div>
  <div id="lc-qrs"></div>
  <div id="lc-inp-row">
    <textarea id="lc-inp" placeholder="Type a message…" rows="1"></textarea>
    <button id="lc-send" disabled aria-label="Send">
      <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
    </button>
  </div>
</div>`;
  document.body.appendChild(root);

  // ── REFS ──────────────────────────────────────────────────────────
  const bubble  = document.getElementById('lc-bubble');
  const toast   = document.getElementById('lc-toast');
  const toastX  = document.getElementById('lc-toast-x');
  const panel   = document.getElementById('lc-panel');
  const headX   = document.getElementById('lc-head-close');
  const msgsEl  = document.getElementById('lc-msgs');
  const qrsEl   = document.getElementById('lc-qrs');
  const inp     = document.getElementById('lc-inp');
  const sendBtn = document.getElementById('lc-send');

  // ── STATE ─────────────────────────────────────────────────────────
  const history = [];
  let isOpen = false;
  let busy = false;
  let toastShown = false;

  // ── HELPERS ───────────────────────────────────────────────────────
  const scroll = () => msgsEl.scrollTop = msgsEl.scrollHeight;

  function addMsg(role, text) {
    history.push({ role, content: text });
    const el = document.createElement('div');
    el.className = `lc-m ${role === 'assistant' ? 'bot' : 'usr'}`;
    const safe = text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
    el.innerHTML = `<div class="lc-b">${safe}</div>`;
    msgsEl.appendChild(el);
    scroll();
    return el;
  }

  function showTyping() {
    const el = document.createElement('div');
    el.className = 'lc-m bot'; el.id = 'lc-typ';
    el.innerHTML = `<div class="lc-b"><div class="lc-dots"><i></i><i></i><i></i></div></div>`;
    msgsEl.appendChild(el);
    scroll();
  }
  function hideTyping() { const t = document.getElementById('lc-typ'); if (t) t.remove(); }

  function renderQRs(list) {
    qrsEl.innerHTML = '';
    list.forEach(txt => {
      const b = document.createElement('button');
      b.className = 'lc-q'; b.textContent = txt;
      b.addEventListener('click', () => { qrsEl.innerHTML = ''; send(txt); });
      qrsEl.appendChild(b);
    });
  }

  // ── OPEN / CLOSE ──────────────────────────────────────────────────
  function openPanel() {
    isOpen = true;
    hideToast();
    bubble.classList.add('away');
    panel.classList.add('open');
    inp.focus();

    if (history.length === 0) {
      addMsg('assistant', C.welcomeMsg);
      renderQRs(C.quickReplies);
    }
  }

  function closePanel() {
    isOpen = false;
    panel.classList.remove('open');
    bubble.classList.remove('away');
  }

  // ── TOAST ─────────────────────────────────────────────────────────
  function showToast() {
    if (isOpen || toastShown) return;
    toastShown = true;
    toast.classList.add('show');
    setTimeout(hideToast, 7000);
  }

  function hideToast() {
    toast.classList.remove('show');
  }

  if (C.toastDelay > 0) setTimeout(showToast, C.toastDelay);

  // ── SEND ──────────────────────────────────────────────────────────
  async function send(text) {
    text = (text || inp.value).trim();
    if (!text || busy) return;

    busy = true;
    inp.value = '';
    autoResize();
    sendBtn.disabled = true;
    qrsEl.innerHTML = '';

    addMsg('user', text);
    showTyping();

    try {
      const res = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${C.apiKey}`
        },
        body: JSON.stringify({
          model: C.model,
          messages: [{ role: 'system', content: C.systemPrompt }, ...history],
          max_tokens: 230,
          temperature: 0.83
        })
      });

      const data = await res.json();
      hideTyping();

      if (data.choices?.[0]?.message?.content) {
        const reply = data.choices[0].message.content;
        addMsg('assistant', reply);

        // Show booking CTA when intent signals readiness
        const bookIntent = /\b(book|consult|appoint|ready|get started|begin|sign up|schedule|how.*(start|work|begin))\b/i.test(text);
        if (bookIntent) {
          const bk = document.createElement('button');
          bk.className = 'lc-q';
          bk.textContent = '📅 Book a Free 15-Min Consult';
          bk.addEventListener('click', () => window.open(C.bookingUrl, '_blank'));
          qrsEl.appendChild(bk);
        }
      } else {
        addMsg('assistant', "I'm having a bit of a hiccup — sorry about that. Feel free to reach out through the website directly.");
      }
    } catch {
      hideTyping();
      addMsg('assistant', "Something went wrong on my end. You can always reach me through the contact form on the website.");
    }

    busy = false;
    sendBtn.disabled = false;
    inp.focus();
  }

  function autoResize() {
    inp.style.height = 'auto';
    inp.style.height = Math.min(inp.scrollHeight, 80) + 'px';
  }

  // ── EVENTS ────────────────────────────────────────────────────────
  bubble.addEventListener('click', openPanel);
  bubble.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') openPanel(); });
  toast.addEventListener('click', openPanel);
  toastX.addEventListener('click', e => { e.stopPropagation(); hideToast(); });
  headX.addEventListener('click', closePanel);

  sendBtn.addEventListener('click', () => send());
  inp.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } });
  inp.addEventListener('input', () => { autoResize(); sendBtn.disabled = !inp.value.trim(); });

  // Close on outside click (mobile backdrop)
  document.addEventListener('click', e => {
    if (isOpen && !root.contains(e.target)) closePanel();
  }, { capture: false });

})();
