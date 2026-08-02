(() => {
  function detect() {
    return location.hostname.includes("indeed.com") ||
      !!document.querySelector("[data-jm-fixture-platform='indeed']");
  }

  function collect() {
    return window.JMFieldMapper.collectInputs(document);
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.indeed = { detect, collect, name: "indeed" };
})();
