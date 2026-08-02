(() => {
  function detect() {
    return location.hostname.includes("myworkdayjobs.com") ||
      location.hostname.includes("workday.com") ||
      !!document.querySelector("[data-jm-fixture-platform='workday'], [data-automation-id]");
  }

  function collect() {
    const mapped = window.JMFieldMapper.collectInputs(document);
    mapped.forEach((f) => {
      const auto = document.getElementById(f.id)?.getAttribute("data-automation-id") || "";
      if (!f.mapped_key && /legalNameSection_firstName|firstName/i.test(auto + f.name + f.id)) f.mapped_key = "first_name";
      if (!f.mapped_key && /legalNameSection_lastName|lastName/i.test(auto + f.name + f.id)) f.mapped_key = "last_name";
      if (!f.mapped_key && /email/i.test(auto + f.name)) f.mapped_key = "email";
      if (!f.mapped_key && /phone/i.test(auto + f.name)) f.mapped_key = "phone";
    });
    return mapped;
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.workday = { detect, collect, name: "workday" };
})();
