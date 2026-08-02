(() => {
  function detectPlatform(url = location.href) {
    const u = String(url || "").toLowerCase();
    const host = location.hostname.toLowerCase();
    if (host.includes("greenhouse.io") || u.includes("greenhouse.io")) return "greenhouse";
    if (host.includes("lever.co") || u.includes("jobs.lever.co")) return "lever";
    if (host.includes("ashbyhq.com")) return "ashby";
    if (host.includes("smartrecruiters.com")) return "smartrecruiters";
    if (host.includes("myworkdayjobs.com") || host.includes("workday.com")) return "workday";
    if (host.includes("indeed.com")) return "indeed";
    if (host.includes("linkedin.com")) return "linkedin";
    if (document.querySelector("[data-jm-fixture-platform]")) {
      return document.querySelector("[data-jm-fixture-platform]").getAttribute("data-jm-fixture-platform");
    }
    return "generic";
  }

  window.JMPlatformDetect = { detectPlatform };
})();
