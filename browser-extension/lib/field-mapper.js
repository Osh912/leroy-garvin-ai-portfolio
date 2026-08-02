(() => {
  const KEY_RULES = [
    [/first\s*name|fname|given[-_ ]?name/i, "first_name"],
    [/last\s*name|lname|surname|family[-_ ]?name/i, "last_name"],
    [/^name$|full\s*name|applicant[-_ ]?name/i, "full_name"],
    [/e-?mail/i, "email"],
    [/phone|mobile|tel/i, "phone"],
    [/country/i, "country"],
    [/city|town/i, "city"],
    [/state|province|region/i, "state"],
    [/zip|postal|postcode/i, "zip_code"],
    [/linkedin/i, "linkedin"],
    [/portfolio|website|personal site|url/i, "portfolio"],
    [/github/i, "github"],
    [/current (job )?title|title|headline/i, "current_job_title"],
    [/resume|cv/i, "resume_file"],
    [/cover\s*letter/i, "cover_letter_file"],
  ];

  function labelFor(el) {
    if (!el) return "";
    if (el.labels && el.labels[0]) return el.labels[0].innerText.trim();
    const id = el.id;
    if (id) {
      const lab = document.querySelector(`label[for="${CSS.escape(id)}"]`);
      if (lab) return lab.innerText.trim();
    }
    const aria = el.getAttribute("aria-label");
    if (aria) return aria.trim();
    const ph = el.getAttribute("placeholder");
    if (ph) return ph.trim();
    return el.name || el.id || "";
  }

  function mapKey(label, name, id) {
    const blob = `${label} ${name || ""} ${id || ""}`;
    for (const [re, key] of KEY_RULES) {
      if (re.test(blob)) return key;
    }
    return null;
  }

  function setNativeValue(el, value) {
    if (value == null || value === "") return false;
    const tag = el.tagName;
    if (tag === "SELECT") {
      const opts = [...el.options];
      const match = opts.find(
        (o) =>
          o.value.toLowerCase() === String(value).toLowerCase() ||
          o.text.toLowerCase() === String(value).toLowerCase() ||
          o.text.toLowerCase().includes(String(value).toLowerCase())
      );
      if (!match) return false;
      el.value = match.value;
    } else {
      el.focus();
      el.value = String(value);
    }
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
    el.classList.add("jm-autofilled");
    return true;
  }

  function collectInputs(root = document) {
    const nodes = root.querySelectorAll("input, textarea, select");
    const out = [];
    nodes.forEach((el, idx) => {
      if (el.type === "hidden" || el.type === "submit" || el.type === "button") return;
      if (el.disabled) return;
      const label = labelFor(el);
      const key = mapKey(label, el.name, el.id);
      out.push({
        index: idx,
        tag: el.tagName.toLowerCase(),
        type: el.type || "",
        name: el.name || "",
        id: el.id || "",
        label,
        mapped_key: key,
        required: !!el.required,
      });
    });
    return out;
  }

  function applyFill(session, confirmedKeys) {
    if (!session || !session.fillable_fields) return { filled: [], skipped: [] };
    const filled = [];
    const skipped = [];
    const nodes = document.querySelectorAll("input, textarea, select");
    nodes.forEach((el) => {
      if (window.JMSafety.isSubmitControl(el)) return;
      const label = labelFor(el);
      if (window.JMSafety.isSensitiveLabel(label) || window.JMSafety.isSensitiveLabel(el.name)) {
        el.classList.add("jm-manual-review");
        skipped.push({ label, reason: "sensitive" });
        return;
      }
      const key = mapKey(label, el.name, el.id);
      if (!key || !confirmedKeys.includes(key)) {
        if (el.required || el.type === "file") el.classList.add("jm-manual-review");
        return;
      }
      if (key === "resume_file" || key === "cover_letter_file") {
        el.classList.add("jm-manual-review");
        skipped.push({ label, reason: "file_upload_manual", key });
        return;
      }
      let value = session.fillable_fields[key];
      if (key === "full_name") {
        value = [session.fields.first_name, session.fields.last_name].filter(Boolean).join(" ");
      }
      if (value == null) {
        skipped.push({ label, reason: "missing_verified_value", key });
        el.classList.add("jm-manual-review");
        return;
      }
      if (setNativeValue(el, value)) filled.push({ label, key, value });
      else {
        el.classList.add("jm-manual-review");
        skipped.push({ label, reason: "could_not_set", key });
      }
    });
    return { filled, skipped };
  }

  function highlightManualReview() {
    document.querySelectorAll("input, textarea, select").forEach((el) => {
      const label = labelFor(el);
      if (window.JMSafety.isSensitiveLabel(label)) el.classList.add("jm-manual-review");
      if (el.type === "file") el.classList.add("jm-manual-review");
      if (el.required && !el.value) el.classList.add("jm-manual-review");
    });
  }

  window.JMFieldMapper = {
    labelFor,
    mapKey,
    collectInputs,
    applyFill,
    highlightManualReview,
    setNativeValue,
  };
})();
