(() => {
  function detect() {
    return location.hostname.includes("linkedin.com") ||
      !!document.querySelector("[data-jm-fixture-platform='linkedin']");
  }

  function collect() {
    // LinkedIn Easy Apply is restricted; external apply pages / company redirects use generic fields.
    return window.JMFieldMapper.collectInputs(document);
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.linkedin = { detect, collect, name: "linkedin" };
})();
