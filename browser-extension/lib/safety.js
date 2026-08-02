(() => {
  const SENSITIVE_RE =
    /disability|disabled|veteran|military|gender|sex\b|race|ethnic|hispanic|latin[oa]|sexual orientation|pronoun|criminal|conviction|background check|sponsor|visa|work authorization|authorized to work|require sponsorship|salary|compensation|desired (pay|comp|salary)|expected (pay|salary)|eeo|equal opportunity|voluntary self|protected veteran|demograph|start date|when can you start|earliest start|relocat|willing to move|i agree|terms (and|&) conditions|privacy policy|legal agreement|\bconsent\b|education|degree|university|certification|\bgpa\b/i;

  const SUBMIT_RE =
    /^(submit|submit application|send application|apply now|complete application|finish application)$/i;

  function isSensitiveLabel(text) {
    return SENSITIVE_RE.test(String(text || ""));
  }

  function isSubmitControl(el) {
    if (!el) return false;
    const type = (el.getAttribute("type") || "").toLowerCase();
    const text = `${el.innerText || ""} ${el.value || ""} ${el.getAttribute("aria-label") || ""}`.trim();
    if (type === "submit") return true;
    if (el.tagName === "BUTTON" && SUBMIT_RE.test(text)) return true;
    if (el.getAttribute("data-qa") === "btn-submit") return true;
    if (el.id && /submit/i.test(el.id) && /apply|application/i.test(text + el.id)) return true;
    return SUBMIT_RE.test(text);
  }

  function guardSubmitButtons(root = document) {
    const controls = root.querySelectorAll("button, input[type=submit], [role=button]");
    controls.forEach((el) => {
      if (!isSubmitControl(el)) return;
      el.setAttribute("data-jm-submit-guard", "1");
      el.setAttribute("title", "Job Machine Safe Autofill will never click Submit for you.");
      // Never programmatically click — only annotate
    });
  }

  function neverClickSubmit() {
    // Hard rule: companion never programmatically clicks submit controls.
    return false;
  }

  function markManualReviewRequired(el, reason) {
    if (!el) return;
    el.classList.add("jm-manual-review");
    el.setAttribute("data-jm-manual", "MANUAL REVIEW REQUIRED");
    if (reason) el.setAttribute("data-jm-manual-reason", reason);
    const parent = el.closest("label") || el.parentElement;
    if (parent && !parent.querySelector(".jm-manual-badge")) {
      const badge = document.createElement("span");
      badge.className = "jm-manual-badge";
      badge.textContent = "MANUAL REVIEW REQUIRED";
      parent.appendChild(badge);
    }
  }

  function detectPageErrors() {
    const text = (document.body?.innerText || "").toLowerCase();
    const hints = [];
    if (/no longer (available|accepting)|position (has been )?filled|job (is )?closed|expired/i.test(text)) {
      hints.push("expired_or_closed");
    }
    if (/sign in|log in|login required|create an account/i.test(text)) {
      hints.push("sign_in_required");
    }
    if (/captcha|recaptcha|hcaptcha|verify you are human/i.test(text)) {
      hints.push("captcha");
    }
    if (/already applied|duplicate application|you have already submitted/i.test(text)) {
      hints.push("duplicate_application");
    }
    if (/session (has )?expired|please try again/i.test(text)) {
      hints.push("session_expiration");
    }
    return hints;
  }

  window.JMSafety = {
    isSensitiveLabel,
    isSubmitControl,
    guardSubmitButtons,
    neverClickSubmit,
    markManualReviewRequired,
    detectPageErrors,
  };
})();
