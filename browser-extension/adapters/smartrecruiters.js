(() => {
  function detect() {
    return location.hostname.includes("smartrecruiters.com") ||
      !!document.querySelector("[data-jm-fixture-platform='smartrecruiters']");
  }

  function collect() {
    return window.JMFieldMapper.collectInputs(document);
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.smartrecruiters = { detect, collect, name: "smartrecruiters" };
})();
