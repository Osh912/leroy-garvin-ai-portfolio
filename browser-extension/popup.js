chrome.runtime.sendMessage({ type: "JM_PING" }, (res) => {
  const el = document.getElementById("status");
  if (!res?.ok) {
    el.innerHTML = `<span class="bad">Job Machine offline</span> — start uvicorn on :8787`;
    return;
  }
  chrome.runtime.sendMessage({ type: "JM_ACTIVE" }, (active) => {
    if (active?.ok && active.data?.active) {
      const s = active.data.session;
      el.innerHTML = `<span class="ok">Active session</span><br>${s.company} — ${s.position}<br>Platform hint: ${s.platform}`;
    } else {
      el.innerHTML = `<span class="ok">API online</span> — no active Open Application session`;
    }
  });
});
