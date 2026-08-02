(() => {
  "use strict";

  const state = {
    session: null,
    classification: null,
    confirmed: false,
    log: [],
  };

  function adapterFor(platform) {
    const adapters = window.JMAdapters || {};
    return adapters[platform] || adapters.generic;
  }

  function addLog(msg) {
    const line = `${new Date().toISOString()} ${msg}`;
    state.log.unshift(line);
    state.log = state.log.slice(0, 40);
    window.JMAutofillAPI.logEvent({ message: msg, url: location.href });
    render();
  }

  function ensureRoot() {
    let root = document.getElementById("jm-safe-autofill-root");
    if (!root) {
      root = document.createElement("div");
      root.id = "jm-safe-autofill-root";
      document.documentElement.appendChild(root);
    }
    return root;
  }

  function render() {
    const root = ensureRoot();
    const s = state.session;
    if (!s) {
      root.innerHTML = `<div class="jm-panel">
        <h1>Job Machine Safe Autofill</h1>
        <p class="jm-sub">No active session. In Job Machine click <strong>Open Application</strong> first (localhost:8787).</p>
        <div class="jm-actions"><button class="jm-btn" id="jm-refresh">Retry connect</button></div>
        <p class="jm-mini">Never auto-submits · No CAPTCHA bypass · Localhost API only</p>
      </div>`;
      root.querySelector("#jm-refresh")?.addEventListener("click", boot);
      return;
    }

    const c = state.classification?.classification || {};
    const autofill = c.autofill_candidates || [];
    const manual = [...(c.manual_review || []), ...(c.sensitive_manual || [])];
    const files = s.files || {};
    const safety = s.safety_check || {};

    root.innerHTML = `<div class="jm-panel">
      <h1>Safe Autofill Preview</h1>
      <p class="jm-sub">${escapeHtml(s.company)} — ${escapeHtml(s.position)}<br>
      Platform: <strong>${escapeHtml(s.platform)}</strong> · Confirm required · Submit never clicked</p>
      <div class="jm-row"><span>Resume</span><strong>${escapeHtml(files.resume_version || "tailored")} (${files.resume_pdf || files.resume_txt ? "ready" : "missing"})</strong></div>
      <div class="jm-row"><span>Cover</span><strong>${escapeHtml(files.cover_version || "tailored")} (${files.cover_pdf || files.cover_txt ? "ready" : "missing"})</strong></div>
      <div class="jm-ok"><strong>Values to enter after Confirm</strong>
        <ul class="jm-list">${
          autofill
            .map((f) => `<li>${escapeHtml(f.label || f.mapped_key)} → ${escapeHtml(String(f.value))}</li>`)
            .join("") || "<li>No standard fields detected yet</li>"
        }</ul>
      </div>
      <div class="jm-warn"><strong>Manual review required</strong>
        <ul class="jm-list">${
          manual
            .slice(0, 12)
            .map((f) => `<li>${escapeHtml(f.label || f.name || "field")} (${escapeHtml(f.action || "review")})</li>`)
            .join("") || "<li>None flagged yet</li>"
        }</ul>
      </div>
      <div class="jm-mini">Safety: company ${safety.items?.correct_company ? "✓" : "✗"} · title ${
        safety.items?.correct_job_title ? "✓" : "✗"
      } · contact ${safety.items?.contact_information_verified ? "✓" : "✗"} · claims ${
        safety.items?.no_unsupported_claims_detected ? "✓" : "review"
      }</div>
      <div class="jm-actions">
        <button class="jm-btn primary" id="jm-confirm" ${state.confirmed ? "disabled" : ""}>Confirm Autofill</button>
        <button class="jm-btn" id="jm-suggest">Suggested answers…</button>
        <button class="jm-btn" id="jm-mark">Mark as Submitted</button>
        <button class="jm-btn" id="jm-map">Field map</button>
        <a class="jm-btn" href="${window.JMAutofillAPI.fileDownloadUrl(s.application_id, "resume")}" target="_blank">Resume file</a>
        <a class="jm-btn" href="${window.JMAutofillAPI.fileDownloadUrl(s.application_id, "cover")}" target="_blank">Cover file</a>
      </div>
      <p class="jm-mini">Activity log</p>
      <ul class="jm-list">${state.log
        .slice(0, 6)
        .map((l) => `<li>${escapeHtml(l)}</li>`)
        .join("")}</ul>
    </div>`;

    root.querySelector("#jm-confirm")?.addEventListener("click", onConfirm);
    root.querySelector("#jm-mark")?.addEventListener("click", onMark);
    root.querySelector("#jm-suggest")?.addEventListener("click", onSuggest);
    root.querySelector("#jm-map")?.addEventListener("click", onMap);
  }

  function escapeHtml(s) {
    return String(s ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  async function onConfirm() {
    if (!state.session) return;
    if (!confirm("Confirm Autofill of verified standard fields only?\n\nSubmit will NOT be clicked.")) return;
    state.confirmed = true;
    const keys = Object.keys(state.session.fillable_fields || {});
    // Include full_name synthetic mapping
    keys.push("full_name");
    window.JMSafety.guardSubmitButtons();
    const result = window.JMFieldMapper.applyFill(state.session, keys);
    window.JMFieldMapper.highlightManualReview();
    addLog(`Autofill confirmed. Filled ${result.filled.length}; skipped ${result.skipped.length}. Submit not clicked.`);
    alert(
      `Filled ${result.filled.length} verified fields.\nHighlighted fields need your review.\nFile uploads and sensitive questions remain manual.\nSubmit was NOT clicked.`
    );
    render();
  }

  async function onMark() {
    if (!state.session) return;
    if (!confirm("Mark this application as Submitted in Job Machine?\nOnly click after YOU submitted manually.")) return;
    const res = await window.JMAutofillAPI.markSubmitted(state.session.application_id, {
      application_url: location.href,
      platform: state.session.platform,
      notes: "Manually submitted; Safe Autofill companion did not click Submit.",
    });
    addLog(`Marked submitted: ${res.submission?.submitted_at || "ok"}`);
    alert(res.message || "Marked submitted.");
  }

  async function onSuggest() {
    const q = prompt("Paste a custom question for a Suggested Answer (not auto-filled):");
    if (!q) return;
    const ans = await window.JMAutofillAPI.suggestAnswer(state.session.application_id, q);
    if (ans.sensitive || !ans.suggested_answer) {
      alert(`${ans.label || "Manual required"}\n\n${ans.note || ""}\n\nSource facts:\n- ${(ans.source_facts || []).join("\n- ")}`);
      return;
    }
    const ok = confirm(
      `Suggested Answer (review required)\n\n${ans.suggested_answer}\n\nSource facts:\n- ${(ans.source_facts || []).join(
        "\n- "
      )}\n\nCopy to clipboard? Nothing will be submitted.`
    );
    if (ok) {
      await navigator.clipboard.writeText(ans.suggested_answer);
      addLog("Suggested answer copied — paste manually after edit.");
    }
  }

  function onMap() {
    const detected = state.classification?.classification?.autofill_candidates || [];
    const lines = (state.classification?.classification
      ? [
          ...(state.classification.classification.autofill_candidates || []),
          ...(state.classification.classification.manual_review || []),
          ...(state.classification.classification.sensitive_manual || []),
        ]
      : []
    ).map((f) => `${f.label || f.name} => ${f.mapped_key || "unmapped"} [${f.action}]`);
    alert(`Field map (${lines.length})\n\n${lines.slice(0, 40).join("\n") || "No fields"}`);
  }

  async function boot() {
    try {
      window.JMSafety.guardSubmitButtons();
      const platform = window.JMPlatformDetect.detectPlatform();
      const active = await window.JMAutofillAPI.getActiveSession();
      if (!active.active || !active.session) {
        state.session = null;
        render();
        return;
      }
      state.session = active.session;
      // Company/role file guard
      const token = `${state.session.files?.verify_token || ""}`.toLowerCase();
      addLog(`Session loaded for ${state.session.company} / ${state.session.position} (${platform}). token=${token}`);
      const adapter = adapterFor(platform);
      const detected = adapter.collect();
      state.classification = await window.JMAutofillAPI.classify(state.session.application_id, detected);
      addLog(`Detected ${detected.length} fields on ${platform}. Confirm required before fill.`);
      render();
    } catch (err) {
      state.session = null;
      ensureRoot().innerHTML = `<div class="jm-panel">
        <h1>Safe Autofill</h1>
        <p class="jm-sub">Cannot reach Job Machine at http://127.0.0.1:8787 — ${escapeHtml(err.message || err)}</p>
        <div class="jm-actions"><button class="jm-btn" id="jm-refresh">Retry</button></div>
      </div>`;
      document.getElementById("jm-refresh")?.addEventListener("click", boot);
    }
  }

  // Expose for tests / manual remount
  window.JMSafeAutofill = { boot, state, neverClickSubmit: () => window.JMSafety.neverClickSubmit() };

  boot();
})();
