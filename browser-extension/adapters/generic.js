(() => {
  function detect() {
    return true;
  }

  function collect() {
    return window.JMFieldMapper.collectInputs(document);
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.generic = { detect, collect, name: "generic" };
})();
