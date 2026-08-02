(() => {
  const SENSITIVE_RE =
    /disability|disabled|veteran|military|gender|sex\b|race|ethnic|hispanic|latin[oa]|sexual orientation|pronoun|criminal|conviction|background check|sponsor|visa|work authorization|authorized to work|require sponsorship|salary|compensation|desired pay|expected (pay|salary)|eeo|equal opportunity|voluntary self|protected veteran|demograph/i;

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
    });
  }

  function neverClickSubmit() {
    // Hard rule: companion never programmatically clicks submit controls.
    return false;
  }

  window.JMSafety = {
    isSensitiveLabel,
    isSubmitControl,
    guardSubmitButtons,
    neverClickSubmit,
  };
})();
