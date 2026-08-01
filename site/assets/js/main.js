(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var navList = document.querySelector(".nav-list");

  if (toggle && navList) {
    toggle.addEventListener("click", function () {
      var open = navList.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    navList.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navList.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Active nav link based on current path */
  var path = window.location.pathname.replace(/\/$/, "") || "/";
  var file = path.split("/").pop() || "index.html";

  document.querySelectorAll(".nav-list a[data-nav]").forEach(function (link) {
    var key = link.getAttribute("data-nav");
    var active = false;

    if (key === "home" && (path === "/" || file === "index.html" || file === "")) {
      active = true;
    } else if (key === "projects" && path.indexOf("/projects") !== -1) {
      active = true;
    } else if (key === "resume" && (file === "resume.html" || file === "resume")) {
      active = true;
    } else if (key === "about" && (file === "about.html" || file === "about")) {
      active = true;
    } else if (key === "contact" && (file === "contact.html" || file === "contact")) {
      active = true;
    }

    if (active) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
  });

  /* Smooth scroll for same-page hash links (fallback when CSS unsupported) */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      var id = anchor.getAttribute("href");
      if (!id || id === "#") return;
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
})();
