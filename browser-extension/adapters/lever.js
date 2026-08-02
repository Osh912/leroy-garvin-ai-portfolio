(() => {
  function detect() {
    return location.hostname.includes("lever.co") ||
      !!document.querySelector(".application-form, [data-qa='btn-submit'], [data-jm-fixture-platform='lever']");
  }

  function collect() {
    const mapped = window.JMFieldMapper.collectInputs(document);
    mapped.forEach((f) => {
      if (!f.mapped_key && /name/i.test(f.name) && !/last|first/i.test(f.name)) f.mapped_key = "full_name";
      if (!f.mapped_key && /urls\[LinkedIn\]|linkedin/i.test(f.name + f.label)) f.mapped_key = "linkedin";
      if (!f.mapped_key && /urls\[GitHub\]|github/i.test(f.name + f.label)) f.mapped_key = "github";
      if (!f.mapped_key && /urls\[Portfolio\]|portfolio|website/i.test(f.name + f.label)) f.mapped_key = "portfolio";
    });
    return mapped;
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.lever = { detect, collect, name: "lever" };
})();
