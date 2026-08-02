const API_BASE = "http://127.0.0.1:8787";

chrome.runtime.onInstalled.addListener(() => {
  console.info("Job Machine Safe Autofill installed. Localhost-only. Never auto-submits.");
});

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg?.type === "JM_PING") {
    fetch(`${API_BASE}/api/autofill/health`)
      .then((r) => r.json())
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: String(err) }));
    return true;
  }
  if (msg?.type === "JM_ACTIVE") {
    fetch(`${API_BASE}/api/autofill/active`)
      .then((r) => r.json())
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: String(err) }));
    return true;
  }
  return false;
});
