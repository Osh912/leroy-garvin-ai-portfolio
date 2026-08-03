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

  async function confirmAutofill(appId, body = {}) {
    return jmFetch(`/api/review-submit/applications/${appId}/autofill-confirmed`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async function readyForFinalReview(appId, body = {}) {
    return jmFetch(`/api/review-submit/applications/${appId}/ready-for-final-review`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async function confirmSubmission(appId, body = {}) {
    return jmFetch(`/api/review-submit/applications/${appId}/confirm-submission`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async function getPanel(appId) {
    return jmFetch(`/api/review-submit/applications/${appId}/panel`);
  }

  async function logEvent(payload) {
    try {
      await jmFetch("/api/autofill/log", { method: "POST", body: JSON.stringify(payload) });
    } catch (_) {
      /* offline ok */
    }
  }

  function fileDownloadUrl(appId, kind, format) {
    const q = format ? `?format=${encodeURIComponent(format)}` : "";
    return `${API_BASE}/api/autofill/applications/${appId}/files/${kind}${q}`;
  }

  async function fetchPreferredFile(appId, kind) {
    // Prefer PDF; fall back to DOCX automatically
    const order = ["pdf", "docx", "md"];
    let lastErr = null;
    for (const fmt of order) {
      try {
        const res = await fetch(fileDownloadUrl(appId, kind, fmt));
        if (!res.ok) {
          lastErr = new Error(await res.text());
          continue;
        }
        const blob = await res.blob();
        const cd = res.headers.get("content-disposition") || "";
        const match = /filename="?([^";]+)"?/i.exec(cd);
        const fallbackName =
          kind === "resume"
            ? fmt === "pdf"
              ? "resume.pdf"
              : fmt === "docx"
                ? "resume.docx"
                : "resume.md"
            : fmt === "pdf"
              ? "cover_letter.pdf"
              : fmt === "docx"
                ? "cover_letter.docx"
                : "cover_letter.md";
        const name = match ? match[1] : fallbackName;
        const type =
          fmt === "pdf"
            ? "application/pdf"
            : fmt === "docx"
              ? "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              : "text/markdown";
        return { file: new File([blob], name, { type }), format: fmt, filename: name };
      } catch (err) {
        lastErr = err;
      }
    }
    throw lastErr || new Error("No attachable file available");
  }

  window.JMAutofillAPI = {
    API_BASE,
    getActiveSession,
    getPayload,
    classify,
    suggestAnswer,
    markSubmitted,
    confirmAutofill,
    readyForFinalReview,
    confirmSubmission,
    getPanel,
    logEvent,
    fileDownloadUrl,
    fetchPreferredFile,
  };
})();
