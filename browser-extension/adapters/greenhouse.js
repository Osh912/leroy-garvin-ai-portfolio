(() => {
  function detect() {
    return location.hostname.includes("greenhouse.io") ||
      !!document.querySelector("#application-form, #main_fields, [data-jm-fixture-platform='greenhouse']");
  }

  function collect() {
    const mapped = window.JMFieldMapper.collectInputs(document);
    // Greenhouse-specific aliases
    mapped.forEach((f) => {
      if (!f.mapped_key && /job_application_first_name|first_name/i.test(f.name + f.id)) f.mapped_key = "first_name";
      if (!f.mapped_key && /job_application_last_name|last_name/i.test(f.name + f.id)) f.mapped_key = "last_name";
      if (!f.mapped_key && /job_application_email|email/i.test(f.name + f.id)) f.mapped_key = "email";
      if (!f.mapped_key && /job_application_phone|phone/i.test(f.name + f.id)) f.mapped_key = "phone";
      if (!f.mapped_key && /resume/i.test(f.name + f.id + f.label)) f.mapped_key = "resume_file";
      if (!f.mapped_key && /cover.?letter/i.test(f.name + f.id + f.label)) f.mapped_key = "cover_letter_file";
    });
    return mapped;
  }

  window.JMAdapters = window.JMAdapters || {};
  window.JMAdapters.greenhouse = { detect, collect, name: "greenhouse" };
})();
