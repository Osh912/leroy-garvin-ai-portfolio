(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  const QUICK_FILTERS = [
    "AI Operations",
    "Workflow Automation",
    "Technical Support",
    "Solutions Engineer",
    "Customer Success",
    "Python",
    "n8n",
    "Airtable",
  ];

  const STAGES = [
    "saved",
    "ready",
    "applied",
    "recruiter_contact",
    "first_interview",
    "technical_interview",
    "final_interview",
    "offer",
    "rejected",
  ];

  const state = { jobs: [], apps: [], packets: [], quick: new Set() };

  function switchView(name) {
    $$(".view").forEach((v) => v.classList.remove("active"));
    $$(".tab").forEach((t) => t.classList.toggle("active", t.dataset.view === name));
    $(`#view-${name}`).classList.add("active");
  }

  async function api(path, options = {}) {
    const res = await fetch(path, {
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options,
    });
    if (!res.ok) throw new Error((await res.text()) || res.statusText);
    return res.json();
  }

  function escapeHtml(s) {
    return String(s ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }
  function escapeAttr(s) {
    return escapeHtml(s).replaceAll("'", "&#39;");
  }

  function downloadText(filename, text) {
    const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  function formatSalary(job) {
    return job.estimated_salary || job.salary_text || "Not listed";
  }
  function matchPct(job) {
    return Math.round(job.match_score || job.match_percentage || job.score || 0);
  }
  function whyFit(job) {
    return job.why_match || job.score_breakdown?.why_match || "";
  }
  function fmtDate(iso) {
    if (!iso) return "—";
    try {
      return new Date(iso).toLocaleString();
    } catch {
      return String(iso);
    }
  }

  function componentBars(job) {
    const comps = job.score_breakdown?.components || {};
    const keys = [
      ["skill_match", "Skill"],
      ["resume_match", "Resume"],
      ["portfolio_match", "Portfolio"],
      ["experience_fit", "Experience"],
      ["remote_eligibility", "Remote"],
      ["salary_fit", "Salary"],
    ];
    return keys
      .map(([k, label]) => {
        const score = comps[k]?.score ?? job.score_breakdown?.[k];
        if (score == null) return "";
        return `<span class="tag">${label}: ${Math.round(score)}</span>`;
      })
      .join("");
  }

  function jobCard(job, opts = {}) {
    const projects = (job.matched_projects || [])
      .slice(0, 4)
      .map((p) => `<span class="tag">${escapeHtml(p.name)}</span>`)
      .join("");
    const why = whyFit(job);
    const rank = job.rank || opts.rank;
    const top = job.is_top_10 || opts.top;
    const posting = job.posting_url || job.url;
    const careers = job.careers_url || "";
    const packageReady = job.package_ready === true;
    return `<article class="job-card ${top ? "top-opportunity" : ""}" data-id="${job.id}">
      <div class="job-card-head">
        <div>
          ${rank ? `<span class="rank-badge">#${rank}</span>` : ""}
          ${packageReady ? `<span class="package-ready">Apply Package Ready</span>` : ""}
          <h3>${escapeHtml(job.title)}</h3>
          <p class="meta company"><strong>${escapeHtml(job.company)}</strong></p>
          <div class="verify-row">
            <span class="remote-badge ${job.remote_verified ? "ok" : "bad"}">${escapeHtml(job.remote_verified_label || "✗ Not Verified Remote")}</span>
          </div>
        </div>
        <div class="metrics">
          <span class="score match">Match ${matchPct(job)}%</span>
        </div>
      </div>
      <dl class="job-facts job-facts-4">
        <div><dt>Source</dt><dd>${escapeHtml(job.source_display || job.source)}</dd></div>
        <div><dt>Date found</dt><dd>${escapeHtml(fmtDate(job.date_found || job.found_at))}</dd></div>
        <div><dt>Salary</dt><dd>${escapeHtml(formatSalary(job))}</dd></div>
        <div><dt>Active check</dt><dd>${job.is_active === false ? "Inactive" : "Verified active / kept"}</dd></div>
      </dl>
      <p class="meta">
        ${posting ? `<a href="${escapeAttr(posting)}" target="_blank" rel="noopener noreferrer">Job posting</a>` : "No posting URL"}
        ${careers ? ` · <a href="${escapeAttr(careers)}" target="_blank" rel="noopener noreferrer">Careers page</a>` : ""}
      </p>
      <div class="tags">${componentBars(job)}</div>
      ${why ? `<div class="why-box"><h4>Why this job matches Leroy</h4><p>${escapeHtml(why)}</p></div>` : ""}
      <div class="projects-row">
        <span class="projects-label">Portfolio to cite</span>
        <div class="tags">${projects || '<span class="tag">No strong project overlap</span>'}</div>
      </div>
      <div class="card-actions">
        ${posting ? `<a class="btn primary" href="${escapeAttr(posting)}" target="_blank" rel="noopener noreferrer">Open Job</a>` : ""}
        <button type="button" class="btn" data-action="prep" data-id="${job.id}">Interview Prep</button>
        <button type="button" class="btn" data-action="generate" data-id="${job.id}">Resume + Cover</button>
        <button type="button" class="btn" data-action="export-job" data-id="${job.id}">Export</button>
        <button type="button" class="btn" data-action="track" data-id="${job.id}">Save to Tracker</button>
      </div>
    </article>`;
  }

  function appCard(app) {
    return `<article class="app-card">
      <h3>${escapeHtml(app.position)}</h3>
      <p class="meta">${escapeHtml(app.company)} · ${escapeHtml(app.stage_label || app.status)} · Match ${Math.round(app.application_score)}</p>
      ${app.status === "ready" ? `<span class="package-ready">Apply Package Ready</span>` : ""}
      <div class="card-actions">
        ${app.status === "ready" || app.status === "saved" ? `<button type="button" class="btn primary" data-action="approve" data-id="${app.id}">Approve to Apply</button>` : ""}
        <button type="button" class="btn" data-action="open-app" data-id="${app.id}">Open Packet</button>
        <button type="button" class="btn" data-action="export-app" data-id="${app.id}">Export</button>
      </div>
    </article>`;
  }

  function packetCard(p) {
    const projects = (p.projects || []).map((x) => `<span class="tag">${escapeHtml(x.name)}</span>`).join("");
    return `<article class="job-card top-opportunity">
      <div class="job-card-head">
        <div>
          <span class="rank-badge">#${p.rank}</span>
          <span class="package-ready">Apply Package Ready</span>
          <h3>${escapeHtml(p.title)}</h3>
          <p class="meta company"><strong>${escapeHtml(p.company)}</strong></p>
        </div>
        <div class="metrics"><span class="score match">Match ${Math.round(p.match_score || p.match_percentage)}%</span></div>
      </div>
      <div class="why-box"><h4>Why this job matches Leroy</h4><p>${escapeHtml(p.why_match || "")}</p></div>
      <div class="tags">${projects}</div>
      <div class="card-actions">
        ${p.url ? `<a class="btn primary" href="${escapeAttr(p.url)}" target="_blank" rel="noopener noreferrer">Open Job</a>` : ""}
        <button type="button" class="btn" data-action="prep" data-id="${p.job_id}">Interview Prep</button>
        <button type="button" class="btn" data-action="approve" data-id="${p.application_id}">Approve to Apply</button>
        <button type="button" class="btn" data-action="export-app" data-id="${p.application_id}">Export</button>
      </div>
    </article>`;
  }

  function renderQuickFilters() {
    $("#quick-filters").innerHTML = QUICK_FILTERS.map(
      (label) =>
        `<button type="button" class="chip ${state.quick.has(label) ? "active" : ""}" data-quick="${escapeAttr(label)}">${escapeHtml(label)}</button>`
    ).join("");
  }

  function searchParams() {
    const qf = [...state.quick].join(",");
    const params = new URLSearchParams({
      persist: "true",
      strict_level: "true",
      fully_remote_only: String($("#flt-remote").checked),
      us_only: String($("#flt-us").checked),
      min_salary: String($("#flt-min-salary").value || 60000),
      prefer_no_degree: "true",
      block_five_plus_years: "true",
      verify_active: "true",
      require_salary_listed: "false",
    });
    if (qf) params.set("quick_filters", qf);
    return params;
  }

  async function loadDashboard() {
    const data = await api("/api/dashboard");
    $("#stat-grid").innerHTML = [
      ["New jobs today", data.new_jobs_today],
      ["Applications ready", data.applications_ready],
      ["Interviews scheduled", data.interviews_scheduled],
      ["Follow-ups due", data.follow_ups_due],
    ]
      .map(([l, n]) => `<div class="stat"><div class="n">${n}</div><div class="l">${l}</div></div>`)
      .join("");

    const refreshed = data.refreshed_at || data.last_refresh?.refreshed_at;
    $("#last-refresh").textContent = refreshed
      ? `Last refresh: ${fmtDate(refreshed)} · Production mode · Auto-apply off`
      : "Last refresh: not yet run — click Morning Refresh or Search Jobs";

    const hi = data.highest_probability_interview_this_week;
    $("#highest-interview").innerHTML = hi
      ? `<strong>Top tracked opportunity:</strong> ${escapeHtml(hi.company)} — ${escapeHtml(hi.position)} · Match ${Math.round(hi.interview_probability)} · ${escapeHtml(hi.status)}`
      : `<strong>Top tracked opportunity:</strong> Prepare Top 10 packets to surface your best verified matches.`;

    $("#best-jobs").innerHTML =
      data.best_new_opportunities.map((j, i) => jobCard(j, { rank: j.rank || i + 1, top: true })).join("") ||
      "<p class='note'>No verified live jobs yet. Run Morning Refresh.</p>";
    $("#recent-apps").innerHTML =
      data.recent_applications.map(appCard).join("") || "<p class='note'>No tracker activity yet.</p>";
  }

  async function loadJobs() {
    const q = $("#job-q").value.trim();
    const min = $("#min-score").value || 0;
    const qf = [...state.quick].join(",");
    const jobs = await api(
      `/api/jobs?q=${encodeURIComponent(q)}&min_score=${min}&limit=80&quick_filters=${encodeURIComponent(qf)}`
    );
    jobs.sort((a, b) => matchPct(b) - matchPct(a));
    state.jobs = jobs;
    $("#jobs-list").innerHTML =
      jobs.map((j, i) => jobCard(j, { rank: j.rank || (j.is_top_10 ? i + 1 : null), top: j.is_top_10 })).join("") ||
      "<p class='note'>No verified jobs match filters.</p>";
  }

  async function loadTracker() {
    const apps = await api("/api/applications");
    state.apps = apps.filter((a) => !/acme|example|demo company|test company/i.test(a.company));
    $("#tracker-table tbody").innerHTML = state.apps
      .map((a) => {
        const opts = STAGES.map(
          (s) => `<option value="${s}" ${s === a.status ? "selected" : ""}>${s.replaceAll("_", " ")}</option>`
        ).join("");
        return `<tr data-id="${a.id}">
          <td>${escapeHtml(a.company)}</td>
          <td>${escapeHtml(a.position)}</td>
          <td>${escapeHtml(a.salary || "—")}</td>
          <td><select class="status" data-field="status">${opts}</select></td>
          <td><input type="date" data-field="interview_date" value="${a.interview_date || ""}"></td>
          <td><input type="date" data-field="follow_up_date" value="${a.follow_up_date || ""}"></td>
          <td>${Math.round(a.application_score)}</td>
          <td class="row-actions">
            ${a.status === "ready" || a.status === "saved" ? `<button type="button" class="btn primary" data-action="approve" data-id="${a.id}">Approve</button>` : ""}
            <button type="button" class="btn" data-action="prep-app" data-id="${a.job_id}">Prep</button>
            <button type="button" class="btn" data-action="export-app" data-id="${a.id}">Export</button>
            <button type="button" class="btn" data-action="open-app" data-id="${a.id}">Packet</button>
          </td>
        </tr>`;
      })
      .join("");
  }

  async function loadPacketsFromReady() {
    const apps = await api("/api/applications");
    const ready = apps
      .filter((a) => (a.status === "ready" || a.status === "saved") && !/acme|example|demo company|test company/i.test(a.company))
      .sort((a, b) => (b.application_score || 0) - (a.application_score || 0))
      .slice(0, 10)
      .map((a, i) => ({
        rank: i + 1,
        job_id: a.job_id,
        application_id: a.id,
        company: a.company,
        title: a.position,
        match_score: a.application_score,
        match_percentage: a.application_score,
        why_match: a.notes || "",
        projects: a.portfolio_refs || [],
        url: "",
      }));
    state.packets = ready;
    $("#packets-list").innerHTML =
      ready.map(packetCard).join("") ||
      "<p class='note'>No packages yet. Click <strong>Prepare Top 10 Packets</strong>.</p>";
  }

  function showPrep(prepOut) {
    const prep = prepOut.prep || {};
    const list = (arr) => (arr || []).map((q) => `<li>${escapeHtml(q)}</li>`).join("");
    const stars = (prep.star_answers || [])
      .map(
        (s) => `<article class="star-block">
          <h4>${escapeHtml(s.title)}</h4>
          <p><strong>S:</strong> ${escapeHtml(s.situation)}</p>
          <p><strong>T:</strong> ${escapeHtml(s.task)}</p>
          <p><strong>A:</strong> ${escapeHtml(s.action)}</p>
          <p><strong>R:</strong> ${escapeHtml(s.result)}</p>
        </article>`
      )
      .join("");
    $("#detail-title").textContent = `Interview Prep · ${prepOut.title} @ ${prepOut.company}`;
    $("#detail-body").innerHTML = `<div class="packet">
      <p class="meta">Truthful prep only · Auto-apply off · Saved locally</p>
      <h3>Why Leroy is a good fit</h3>
      <p>${escapeHtml(prep.why_leroy_is_a_good_fit || "")}</p>
      <h3>Likely questions</h3><ul>${list(prep.likely_interview_questions)}</ul>
      <h3>Technical</h3><ul>${list(prep.technical_questions)}</ul>
      <h3>Behavioral</h3><ul>${list(prep.behavioral_questions)}</ul>
      <h3>STAR answers</h3>${stars}
      <h3>Questions to ask</h3><ul>${list(prep.questions_leroy_should_ask)}</ul>
      <div class="card-actions">
        <button type="button" class="btn" id="copy-prep">Copy Prep Markdown</button>
      </div>
    </div>`;
    $("#detail-dialog").showModal();
    $("#copy-prep")?.addEventListener("click", () => navigator.clipboard.writeText(prepOut.prep_markdown || ""));
  }

  async function showPacket(jobId) {
    const packet = await api(`/api/jobs/${jobId}/generate`, { method: "POST" });
    const projects = packet.matched_projects
      .map((p) => `<a class="project-link" href="${escapeAttr(p.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(p.name)}</a>`)
      .join("");
    $("#detail-title").textContent = `Resume + Cover · Match ${Math.round(packet.score)}%`;
    $("#detail-body").innerHTML = `<div class="packet">
      <div class="why-box"><h4>Why this job matches Leroy</h4><p>${escapeHtml(packet.why_match || "")}</p></div>
      <h3>Portfolio matches</h3>${projects}
      <h3>Tailored resume</h3><pre>${escapeHtml(packet.tailored_resume)}</pre>
      <h3>Cover letter</h3><pre>${escapeHtml(packet.cover_letter)}</pre>
      <div class="card-actions">
        <button type="button" class="btn" id="copy-resume">Copy Resume</button>
        <button type="button" class="btn" id="copy-cover">Copy Cover</button>
        <button type="button" class="btn" data-action="export-job" data-id="${jobId}">Export All</button>
      </div>
    </div>`;
    $("#detail-dialog").showModal();
    $("#copy-resume")?.addEventListener("click", () => navigator.clipboard.writeText(packet.tailored_resume));
    $("#copy-cover")?.addEventListener("click", () => navigator.clipboard.writeText(packet.cover_letter));
  }

  async function exportApp(appId) {
    const bundle = await api(`/api/applications/${appId}/export`);
    downloadText(bundle.resume_filename, bundle.resume);
    downloadText(bundle.cover_filename, bundle.cover_letter);
    await navigator.clipboard.writeText(bundle.portfolio_url);
    alert(`Exported resume + cover.\nPortfolio URL copied:\n${bundle.portfolio_url}`);
  }
  async function exportJob(jobId) {
    const bundle = await api(`/api/jobs/${jobId}/export`);
    downloadText(bundle.resume_filename, bundle.resume);
    downloadText(bundle.cover_filename, bundle.cover_letter);
    await navigator.clipboard.writeText(bundle.portfolio_url);
    alert(`Exported resume + cover.\nPortfolio URL copied:\n${bundle.portfolio_url}`);
  }

  $$(".tab").forEach((tab) =>
    tab.addEventListener("click", () => {
      switchView(tab.dataset.view);
      if (tab.dataset.view === "pipeline") loadPacketsFromReady();
      if (tab.dataset.view === "tracker") loadTracker();
    })
  );

  $("#quick-filters").addEventListener("click", (e) => {
    const chip = e.target.closest("[data-quick]");
    if (!chip) return;
    const label = chip.dataset.quick;
    if (state.quick.has(label)) state.quick.delete(label);
    else state.quick.add(label);
    renderQuickFilters();
    loadJobs();
  });

  $("#btn-morning").addEventListener("click", async () => {
    const btn = $("#btn-morning");
    btn.disabled = true;
    btn.textContent = "Refreshing…";
    try {
      const result = await api("/api/pipeline/morning-refresh", { method: "POST" });
      state.packets = (result.top_10 || []).filter((p) => !/acme|example/i.test(p.company));
      $("#packets-list").innerHTML = state.packets.map(packetCard).join("") || "<p class='note'>No packets.</p>";
      $("#pipeline-note").textContent = `Production refresh: fetched ${result.fetched}, matched ${result.matched}, inactive removed ${result.rejected_inactive || 0}, packets ${result.packets_prepared}.`;
      await Promise.all([loadDashboard(), loadJobs(), loadTracker()]);
      switchView("pipeline");
    } catch (err) {
      $("#pipeline-note").textContent = String(err.message || err);
    } finally {
      btn.disabled = false;
      btn.textContent = "Morning Refresh";
    }
  });

  $("#btn-prepare-top10").addEventListener("click", async () => {
    const btn = $("#btn-prepare-top10");
    btn.disabled = true;
    btn.textContent = "Preparing…";
    try {
      const result = await api("/api/pipeline/prepare-top10", { method: "POST" });
      state.packets = (result.packets || []).filter((p) => !/acme|example/i.test(p.company));
      $("#packets-list").innerHTML = state.packets.map(packetCard).join("") || "<p class='note'>No packets.</p>";
      await Promise.all([loadDashboard(), loadTracker()]);
      switchView("pipeline");
    } catch (err) {
      $("#pipeline-note").textContent = String(err.message || err);
    } finally {
      btn.disabled = false;
      btn.textContent = "Prepare Top 10 Packets";
    }
  });

  $("#btn-search").addEventListener("click", async () => {
    const btn = $("#btn-search");
    btn.disabled = true;
    btn.textContent = "Searching…";
    try {
      const result = await api(`/api/jobs/search?${searchParams().toString()}`, { method: "POST" });
      $("#search-note").textContent =
        `Fetched ${result.fetched}, matched ${result.matched} live verified jobs` +
        `, removed ${result.rejected_inactive || 0} inactive` +
        `, purged ${result.purged_placeholders?.jobs_removed || 0} placeholders` +
        `. Refreshed ${fmtDate(result.refreshed_at)}. Auto-apply: off.`;
      await Promise.all([loadJobs(), loadDashboard()]);
    } catch (err) {
      $("#search-note").textContent = String(err.message || err);
    } finally {
      btn.disabled = false;
      btn.textContent = "Search Jobs";
    }
  });

  $("#btn-refresh-jobs").addEventListener("click", loadJobs);
  $("#job-q").addEventListener("keydown", (e) => {
    if (e.key === "Enter") loadJobs();
  });

  document.addEventListener("click", async (e) => {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;
    const id = Number(btn.dataset.id);
    const action = btn.dataset.action;
    try {
      if (action === "generate") await showPacket(id);
      if (action === "prep" || action === "prep-app") {
        btn.disabled = true;
        showPrep(await api(`/api/jobs/${id}/interview-prep`, { method: "POST" }));
        btn.disabled = false;
      }
      if (action === "track") {
        await api(`/api/applications/from-job/${id}?status=ready`, { method: "POST" });
        await Promise.all([loadDashboard(), loadTracker(), loadPacketsFromReady()]);
        switchView("tracker");
      }
      if (action === "approve") {
        if (!confirm("Approve this application? Marks Applied only — nothing is auto-submitted.")) return;
        await api(`/api/applications/${id}/approve`, { method: "POST" });
        await Promise.all([loadDashboard(), loadTracker(), loadPacketsFromReady()]);
        alert("Marked Applied. Submit the listing yourself.");
      }
      if (action === "export-app") await exportApp(id);
      if (action === "export-job") await exportJob(id);
      if (action === "open-app") {
        const apps = state.apps.length ? state.apps : await api("/api/applications");
        const app = apps.find((a) => a.id === id);
        if (!app) return;
        $("#detail-title").textContent = `${app.company} · ${app.position}`;
        $("#detail-body").innerHTML = `<div class="packet">
          <p class="meta">Stage: ${escapeHtml(app.stage_label || app.status)} · Match ${Math.round(app.application_score)}</p>
          ${app.status === "ready" ? `<span class="package-ready">Apply Package Ready</span>` : ""}
          <h3>Resume</h3><pre>${escapeHtml(app.tailored_resume || "Not generated")}</pre>
          <h3>Cover</h3><pre>${escapeHtml(app.cover_letter || "Not generated")}</pre>
        </div>`;
        $("#detail-dialog").showModal();
      }
    } catch (err) {
      alert(String(err.message || err));
      btn.disabled = false;
    }
  });

  $("#tracker-table").addEventListener("change", async (e) => {
    const el = e.target;
    const tr = el.closest("tr[data-id]");
    if (!tr || !el.dataset.field) return;
    const id = Number(tr.dataset.id);
    if (el.dataset.field === "status" && el.value === "applied") {
      el.value = state.apps.find((a) => a.id === id)?.status || "ready";
      alert("Use Approve to mark Applied.");
      return;
    }
    const body = {};
    body[el.dataset.field] = el.value || null;
    await api(`/api/applications/${id}`, { method: "PATCH", body: JSON.stringify(body) });
    await loadDashboard();
  });

  $("#import-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(e.target).entries());
    if (/acme|example corp|demo company|test company/i.test(payload.company || "")) {
      alert("Placeholder companies are blocked in Production Mode.");
      return;
    }
    const job = await api("/api/jobs/manual", { method: "POST", body: JSON.stringify(payload) });
    e.target.reset();
    await Promise.all([loadJobs(), loadDashboard()]);
    switchView("jobs");
    await showPacket(job.id);
  });

  renderQuickFilters();
  Promise.all([loadDashboard(), loadJobs(), loadTracker(), loadPacketsFromReady()]).catch((err) => {
    $("#stat-grid").innerHTML = `<p class="warn">Failed to load API: ${escapeHtml(err.message || err)}</p>`;
  });
})();
