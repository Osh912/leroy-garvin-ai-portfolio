(() => {
  "use strict";

  const state = {
    session: null,
    classification: null,
    confirmed: false,
    readyForFinal: false,
    showConfirmSubmit: false,
    pageErrors: [],
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

  function escapeHtml(s) {
    return String(s ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function checklistHtml(checklist) {
    const labeled = checklist?.labeled || [];
    if (!labeled.length) return "<li>Checklist unavailable</li>";
    return labeled
      .map(
        (item) =>
          `<li class="${item.ok ? "jm-ok-item" : "jm-warn-item"}">${item.ok ? "✓" : "○"} ${escapeHtml(
            item.label
          )}${item.leroy_confirm_required && !item.ok ? " <em>(confirm)</em>" : ""}</li>`
      )
      .join("");
  }

  function render() {
    const root = ensureRoot();
    const s = state.session;
    if (!s) {
      root.innerHTML = `<div class="jm-panel">
        <h1>Review &amp; Submit Assistant</h1>
        <p class="jm-sub">No active session. In Job Machine: Prepare → Approve to Apply → Open Official Application.</p>
        <div class="jm-actions"><button class="jm-btn" id="jm-refresh">Retry connect</button></div>
        <p class="jm-mini">Never auto-submits · Never clicks Submit · No CAPTCHA bypass · Localhost only</p>
      </div>`;
      root.querySelector("#jm-refresh")?.addEventListener("click", boot);
      return;
    }

    const c = state.classification?.classification || {};
    const autofill = c.autofill_candidates || [];
    const manual = [...(c.manual_review || []), ...(c.sensitive_manual || [])];
    const draftable = c.draftable || [];
    const files = s.files || {};
    const filenames = s.file_filenames || {};
    const checklist = s.submission_checklist || {};
    const dup = s.duplicate_check || {};
    const platform = s.platform || "generic";
    const manualOnlyPlatform = s.platform_manual_only || platform === "linkedin" || platform === "indeed";

    if (state.showConfirmSubmit) {
      root.innerHTML = `<div class="jm-panel">
        <h1>DID THE APPLICATION SUBMIT SUCCESSFULLY?</h1>
        <p class="jm-sub">${escapeHtml(s.company)} — ${escapeHtml(s.position)}<br>
        Platform: <strong>${escapeHtml(platform)}</strong></p>
        <p class="jm-mini">Only confirm after YOU clicked the employer Submit button. Job Machine never submits for you.</p>
        <label class="jm-mini">Optional confirmation number
          <input id="jm-conf-num" class="jm-input" placeholder="If employer showed one" />
        </label>
        <div class="jm-actions">
          <button class="jm-btn primary" id="jm-yes">Yes — Mark Applied</button>
          <button class="jm-btn" id="jm-no">No — Keep In Progress</button>
          <button class="jm-btn" id="jm-unsure">Unsure — Needs Verification</button>
          <button class="jm-btn" id="jm-back">Back</button>
        </div>
      </div>`;
      root.querySelector("#jm-yes")?.addEventListener("click", () => onConfirmOutcome("yes"));
      root.querySelector("#jm-no")?.addEventListener("click", () => onConfirmOutcome("no"));
      root.querySelector("#jm-unsure")?.addEventListener("click", () => onConfirmOutcome("unsure"));
      root.querySelector("#jm-back")?.addEventListener("click", () => {
        state.showConfirmSubmit = false;
        render();
      });
      return;
    }

    root.innerHTML = `<div class="jm-panel">
      <h1>Review &amp; Submit Assistant</h1>
      <p class="jm-sub">${escapeHtml(s.company)} — ${escapeHtml(s.position)}<br>
      Platform: <strong>${escapeHtml(platform)}</strong>
      ${manualOnlyPlatform ? " · <span class='jm-warn-inline'>Manual platform — Easy Apply not automated</span>" : ""}
      · Confirm required · Submit never clicked</p>
      ${
        dup.duplicate_warning
          ? `<div class="jm-warn"><strong>Duplicate warning</strong><br>${escapeHtml(dup.message || "")}</div>`
          : ""
      }
      ${
        state.pageErrors.length
          ? `<div class="jm-warn"><strong>Page signals</strong><ul class="jm-list">${state.pageErrors
              .map((e) => `<li>${escapeHtml(e)}</li>`)
              .join("")}</ul></div>`
          : ""
      }
      <div class="jm-row"><span>Resume file</span><strong>${escapeHtml(
        filenames.resume || files.resume_version || "tailored"
      )}</strong></div>
      <div class="jm-row"><span>Cover file</span><strong>${escapeHtml(
        filenames.cover || files.cover_version || "tailored"
      )}</strong></div>
      <div class="jm-row"><span>Match score</span><strong>${escapeHtml(String(s.match_score ?? "—"))}</strong></div>

      <div class="jm-ok"><strong>Preview Autofill (after Confirm)</strong>
        <ul class="jm-list">${
          autofill
            .map((f) => `<li>${escapeHtml(f.label || f.mapped_key)} → ${escapeHtml(String(f.value))}</li>`)
            .join("") || "<li>No standard fields detected yet</li>"
        }</ul>
      </div>
      <div class="jm-warn"><strong>MANUAL REVIEW REQUIRED</strong>
        <ul class="jm-list">${
          manual
            .slice(0, 14)
            .map(
              (f) =>
                `<li>${escapeHtml(f.label_flag || "MANUAL REVIEW REQUIRED")}: ${escapeHtml(
                  f.label || f.name || "field"
                )}</li>`
            )
            .join("") || "<li>None flagged yet</li>"
        }</ul>
      </div>
      ${
        draftable.length
          ? `<div class="jm-ok"><strong>Suggested Answer candidates</strong> (approval before insert)
              <ul class="jm-list">${draftable
                .slice(0, 6)
                .map((f) => `<li>${escapeHtml(f.label || f.name)}</li>`)
                .join("")}</ul></div>`
          : ""
      }

      <div class="jm-ok"><strong>Submission Review Checklist</strong>
        <ul class="jm-list">${checklistHtml(checklist)}</ul>
      </div>

      <div class="jm-actions">
        <button class="jm-btn primary" id="jm-confirm" ${state.confirmed ? "disabled" : ""}>Confirm Autofill</button>
        <button class="jm-btn" id="jm-suggest">Suggested answers…</button>
        <button class="jm-btn" id="jm-attach-resume">Attach Resume (PDF)</button>
        <button class="jm-btn" id="jm-attach-cover">Attach Cover (PDF)</button>
        <button class="jm-btn" id="jm-ready" ${state.readyForFinal ? "disabled" : ""}>READY FOR FINAL REVIEW</button>
        <button class="jm-btn primary" id="jm-did-submit">I Clicked Submit…</button>
        <button class="jm-btn" id="jm-map">Field map</button>
        <a class="jm-btn" href="${window.JMAutofillAPI.fileDownloadUrl(s.application_id, "resume")}" target="_blank">Download resume</a>
        <a class="jm-btn" href="${window.JMAutofillAPI.fileDownloadUrl(s.application_id, "cover")}" target="_blank">Download cover</a>
      </div>
      <p class="jm-mini">Attach Resume defaults to PDF (falls back to DOCX if PDF missing). READY FOR FINAL REVIEW never submits.</p>
      <p class="jm-mini">Activity log</p>
      <ul class="jm-list">${state.log
        .slice(0, 6)
        .map((l) => `<li>${escapeHtml(l)}</li>`)
        .join("")}</ul>
    </div>`;

    root.querySelector("#jm-confirm")?.addEventListener("click", onConfirm);
    root.querySelector("#jm-suggest")?.addEventListener("click", onSuggest);
    root.querySelector("#jm-ready")?.addEventListener("click", onReady);
    root.querySelector("#jm-attach-resume")?.addEventListener("click", () => onAttach("resume"));
    root.querySelector("#jm-attach-cover")?.addEventListener("click", () => onAttach("cover"));
    root.querySelector("#jm-did-submit")?.addEventListener("click", () => {
      state.showConfirmSubmit = true;
      render();
    });
    root.querySelector("#jm-map")?.addEventListener("click", onMap);
  }

  async function onAttach(kind) {
    if (!state.session) return;
    window.JMFieldMapper.highlightFileUploads(state.session);
    const inputs = [...document.querySelectorAll("input[type=file]")];
    const target = inputs.find((el) => {
      const label = window.JMFieldMapper.labelFor(el);
      const key = window.JMFieldMapper.mapKey(label, el.name, el.id);
      if (kind === "cover") return key === "cover_letter_file" || /cover/i.test(label + el.name);
      return key === "resume_file" || /resume|cv/i.test(label + el.name);
    }) || inputs[0];
    if (!target) {
      alert("No file upload field found on this page. Use Download resume/cover, then upload manually.");
      return;
    }
    try {
      const preferred = await window.JMFieldMapper.attachPreferredToInput(target, state.session, kind);
      addLog(`Attached ${preferred.filename} (${preferred.format}) to ${kind} field.`);
      alert(`Attached ${preferred.filename}.\n${preferred.format !== "pdf" ? "PDF was unavailable — used DOCX fallback." : "PDF selected by default."}`);
    } catch (err) {
      addLog(`Attach failed: ${err.message || err}`);
      alert(`Attach failed: ${err.message || err}\nDownload the file and upload manually.`);
    }
  }

  async function onConfirm() {
    if (!state.session) return;
    if (state.session.platform_manual_only) {
      alert(
        "This platform stays manual (LinkedIn Easy Apply / similar).\nComplete fields yourself. Submit is never clicked for you."
      );
      return;
    }
    if (!confirm("Confirm Autofill of verified standard fields only?\n\nSubmit will NOT be clicked.")) return;
    state.confirmed = true;
    const keys = Object.keys(state.session.fillable_fields || {});
    keys.push("full_name");
    window.JMSafety.guardSubmitButtons();
    const result = window.JMFieldMapper.applyFill(state.session, keys);
    window.JMFieldMapper.highlightManualReview();
    window.JMFieldMapper.highlightFileUploads(state.session);
    try {
      await window.JMAutofillAPI.confirmAutofill(state.session.application_id, {
        filled: result.filled,
        skipped: result.skipped,
      });
    } catch (_) {
      /* offline ok */
    }
    addLog(
      `Autofill confirmed. Filled ${result.filled.length}; skipped ${result.skipped.length}. Submit not clicked.`
    );
    alert(
      `Filled ${result.filled.length} verified fields.\nHighlighted fields need MANUAL REVIEW.\n` +
        `Download & attach the labeled resume/cover files.\nSubmit was NOT clicked.`
    );
    render();
  }

  async function onReady() {
    if (!state.session) return;
    if (
      !confirm(
        "READY FOR FINAL REVIEW?\n\nThis does NOT submit the application.\nYou must click the employer Submit button yourself."
      )
    ) {
      return;
    }
    try {
      const res = await window.JMAutofillAPI.readyForFinalReview(state.session.application_id, {
        required_questions_completed: true,
        sensitive_questions_reviewed_manually: true,
        no_blank_required_fields: true,
        fully_remote_verified: true,
      });
      state.readyForFinal = true;
      if (res.submission_checklist) state.session.submission_checklist = res.submission_checklist;
      addLog("READY FOR FINAL REVIEW — does not submit. Leroy must click employer Submit.");
      alert(res.message || "Ready for final review. Click the employer Submit yourself.");
    } catch (err) {
      alert(`Could not record ready state: ${err.message || err}`);
    }
    render();
  }

  async function onConfirmOutcome(outcome) {
    if (!state.session) return;
    const confEl = document.getElementById("jm-conf-num");
    const confirmation_number = confEl ? confEl.value.trim() : "";
    try {
      const res = await window.JMAutofillAPI.confirmSubmission(state.session.application_id, {
        outcome,
        confirmation_number: confirmation_number || null,
        application_url: location.href,
        platform: state.session.platform,
        notes: "Manually submitted; Review-and-Submit Assistant did not click Submit.",
      });
      addLog(`Submission confirmation: ${outcome} → ${res.status || "ok"}`);
      alert(res.message || `Outcome: ${outcome}`);
      if (outcome === "yes") {
        state.session = null;
      }
      state.showConfirmSubmit = false;
      render();
    } catch (err) {
      alert(`Confirm failed: ${err.message || err}`);
    }
  }

  async function onSuggest() {
    const q = prompt("Paste a custom question for a Suggested Answer (not auto-filled):");
    if (!q) return;
    const ans = await window.JMAutofillAPI.suggestAnswer(state.session.application_id, q);
    if (ans.sensitive || !ans.suggested_answer) {
      alert(
        `${ans.label || "MANUAL REVIEW REQUIRED"}\n\n${ans.note || ""}\n\nSource facts:\n- ${(
          ans.source_facts || []
        ).join("\n- ")}`
      );
      return;
    }
    const edited = prompt(
      `Suggested Answer (edit before copy). Nothing will be submitted.\n\nFacts:\n- ${(ans.source_facts || []).join(
        "\n- "
      )}`,
      ans.suggested_answer
    );
    if (edited == null) return;
    const ok = confirm("Copy edited Suggested Answer to clipboard?\nYou still must paste it yourself after review.");
    if (ok) {
      await navigator.clipboard.writeText(edited);
      addLog("Suggested answer copied — paste manually after approval.");
    }
  }

  function onMap() {
    const lines = (
      state.classification?.classification
        ? [
            ...(state.classification.classification.autofill_candidates || []),
            ...(state.classification.classification.manual_review || []),
            ...(state.classification.classification.sensitive_manual || []),
            ...(state.classification.classification.draftable || []),
          ]
        : []
    ).map((f) => `${f.label || f.name} => ${f.mapped_key || "unmapped"} [${f.action}]`);
    alert(`Field map (${lines.length})\n\n${lines.slice(0, 40).join("\n") || "No fields"}`);
  }

  async function boot() {
    try {
      window.JMSafety.guardSubmitButtons();
      // Hard rule: never click submit
      if (window.JMSafety.neverClickSubmit() !== false) {
        throw new Error("Safety contract broken");
      }
      const platform = window.JMPlatformDetect.detectPlatform();
      const active = await window.JMAutofillAPI.getActiveSession();
      if (!active.active || !active.session) {
        state.session = null;
        render();
        return;
      }
      state.session = active.session;
      state.pageErrors = window.JMSafety.detectPageErrors();
      const token = `${state.session.files?.verify_token || ""}`.toLowerCase();
      addLog(`Job opened: ${state.session.company} / ${state.session.position} (${platform}). token=${token}`);
      if (state.pageErrors.length) {
        addLog(`Page signals: ${state.pageErrors.join(", ")}`);
      }
      window.JMFieldMapper.highlightFileUploads(state.session);
      window.JMFieldMapper.highlightManualReview();
      const adapter = adapterFor(platform);
      const detected = adapter.collect();
      state.classification = await window.JMAutofillAPI.classify(state.session.application_id, detected);
      addLog(`Platform detected: ${platform}. Fields: ${detected.length}. Confirm required before fill.`);
      render();
    } catch (err) {
      state.session = null;
      ensureRoot().innerHTML = `<div class="jm-panel">
        <h1>Review &amp; Submit Assistant</h1>
        <p class="jm-sub">Cannot reach Job Machine at http://127.0.0.1:8787 — ${escapeHtml(err.message || err)}</p>
        <div class="jm-actions"><button class="jm-btn" id="jm-refresh">Retry</button></div>
      </div>`;
      document.getElementById("jm-refresh")?.addEventListener("click", boot);
    }
  }

  window.JMSafeAutofill = {
    boot,
    state,
    neverClickSubmit: () => window.JMSafety.neverClickSubmit(),
  };

  boot();
})();
