(() => {
  function detect() {
    return (
      location.hostname.includes("workable.com") ||
      !!document.querySelector("[data-jm-fixture-platform='workable'], .application-form, #application-form")
    );
  }

  function collect() {
    const mapped = window.JMFieldMapper.collectInputs(document);
    mapped.forEach((f) => {
      if (!f.mapped_key && /firstname|first_name/i.test(f.name + f.id)) f.mapped_key = "first_name";
      if (!f.mapped_key && /lastname|last_name/i.test(f.name + f.id)) f.mapped_key = "last_name";
      if (!f.mapped_key && /email/i.test(f.name + f.id)) f.mapped_key = "email";
      if (!f.mapped_key && /phone|tel/i.test(f.name + f.id)) f.mapped_key = "phone";
      if (!f.mapped_key && /resume|cv/i.test(f.name + f.id + f.label)) f.mapped_key = "resume_file";
      if (!f.mapped_key && /cover/i.test(f.name + f.id + f.label)) f.mapped_key = "cover_letter_file";
    });
    return mapped;
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.workable = { detect, collect, name: "workable" };
})();
