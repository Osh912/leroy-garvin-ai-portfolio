(() => {
  const API_BASE = "http://127.0.0.1:8787";

  async function jmFetch(path, options = {}) {
    const res = await fetch(`${API_BASE}${path}`, {
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || res.statusText);
    }
    const ct = res.headers.get("content-type") || "";
    if (ct.includes("application/json")) return res.json();
    return res;
  }

  async function getActiveSession() {
    return jmFetch("/api/autofill/active");
  }

  async function getPayload(appId) {
    return jmFetch(`/api/autofill/applications/${appId}/payload`);
  }

  async function classify(appId, detected) {
    return jmFetch(`/api/autofill/applications/${appId}/classify`, {
      method: "POST",
      body: JSON.stringify({ detected }),
    });
  }

  async function suggestAnswer(appId, question) {
    return jmFetch(`/api/autofill/applications/${appId}/suggest-answer`, {
      method: "POST",
      body: JSON.stringify({ question }),
    });
  }

  async function markSubmitted(appId, body = {}) {
    return jmFetch(`/api/autofill/applications/${appId}/mark-submitted`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async function logEvent(payload) {
    try {
      await jmFetch("/api/autofill/log", { method: "POST", body: JSON.stringify(payload) });
    } catch (_) {
      /* offline ok */
    }
  }

  function fileDownloadUrl(appId, kind) {
    return `${API_BASE}/api/autofill/applications/${appId}/files/${kind}`;
  }

  window.JMAutofillAPI = {
    API_BASE,
    getActiveSession,
    getPayload,
    classify,
    suggestAnswer,
    markSubmitted,
    logEvent,
    fileDownloadUrl,
  };
})();
