(() => {
  function detect() {
    return location.hostname.includes("ashbyhq.com") ||
      !!document.querySelector("[data-jm-fixture-platform='ashby'], form[class*='ashby']");
  }

  function collect() {
    return window.JMFieldMapper.collectInputs(document);
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.ashby = { detect, collect, name: "ashby" };
})();
