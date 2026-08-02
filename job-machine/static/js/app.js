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
    "recruiter_viewed",
    "recruiter_replied",
    "phone_screen",
    "technical_interview",
    "hiring_manager",
    "final_interview",
    "offer",
    "accepted",
    "rejected",
    "withdrawn",
  ];

  const STAGE_ALIASES = {
    recruiter_contact: "recruiter_replied",
    first_interview: "phone_screen",
    interview: "phone_screen",
  };

  const state = {
    jobs: [],
    apps: [],
    packets: [],
    quick: new Set(),
    charts: [],
    assistant: null,
    assistantAppId: null,
    assistantPanel: "prepare",
  };

  function normalizeStage(s) {
    const key = String(s || "saved").toLowerCase().replaceAll(" ", "_");
    return STAGE_ALIASES[key] || key;
  }

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
      ["interview_readiness", "Readiness"],
      ["experience_fit", "Readiness"],
      ["remote_eligibility", "Remote"],
      ["salary_fit", "Salary"],
      ["career_growth", "Growth"],
      ["resume_match", "Resume"],
      ["portfolio_match", "Portfolio"],
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
        <button type="button" class="btn primary" data-action="prepare-app" data-id="${job.id}">Prepare Application</button>
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
        <button type="button" class="btn" data-action="open-assistant" data-id="${app.id}">Assistant</button>
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
        <button type="button" class="btn primary" data-action="prepare-app" data-id="${p.job_id}">Prepare Application</button>
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
        const current = normalizeStage(a.status);
        const opts = STAGES.map(
          (s) =>
            `<option value="${s}" ${s === current ? "selected" : ""}>${s.replaceAll("_", " ")}</option>`
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
            <button type="button" class="btn" data-action="prepare-app" data-id="${a.job_id}">Prepare</button>
            <button type="button" class="btn" data-action="open-application" data-id="${a.id}">Open App</button>
            <button type="button" class="btn" data-action="mark-submitted" data-id="${a.id}">Submitted</button>
            <button type="button" class="btn" data-action="open-assistant" data-id="${a.id}">Assistant</button>
            <button type="button" class="btn" data-action="prep-app" data-id="${a.job_id}">Prep</button>
            <button type="button" class="btn" data-action="export-app" data-id="${a.id}">Export</button>
            <button type="button" class="btn" data-action="open-app" data-id="${a.id}">Packet</button>
          </td>
        </tr>`;
      })
      .join("");
  }

  function fmtVal(v) {
    if (v === null || v === undefined || v === "") return "—";
    if (typeof v === "number") return Number.isInteger(v) ? String(v) : String(v);
    return String(v);
  }

  function destroyCharts() {
    (state.charts || []).forEach((c) => {
      try {
        c.destroy();
      } catch (_) {
        /* ignore */
      }
    });
    state.charts = [];
  }

  function makeChart(canvasId, type, labels, values, label) {
    if (typeof Chart === "undefined") return;
    const el = document.getElementById(canvasId);
    if (!el) return;
    const chart = new Chart(el, {
      type,
      data: {
        labels,
        datasets: [
          {
            label: label || "",
            data: values.map((v) => (v == null ? 0 : v)),
            backgroundColor: "rgba(47, 93, 69, 0.45)",
            borderColor: "rgba(47, 93, 69, 0.95)",
            borderWidth: 1.5,
            tension: 0.25,
            fill: type === "line",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: type === "doughnut" || type === "pie" ? {} : { y: { beginAtZero: true } },
      },
    });
    state.charts.push(chart);
  }

  async function loadAnalytics() {
    const data = await api("/api/analytics");
    $("#analytics-meta").textContent =
      `Sample size: ${data.sample_size} · Generated ${fmtDate(data.generated_at)} · Fabricated: ${data.fabricated} · Auto-send follow-ups: off`;

    const kpiLabels = {
      applications_submitted_today: "Applications Submitted Today",
      applications_this_week: "Applications This Week",
      applications_this_month: "Applications This Month",
      recruiter_replies: "Recruiter Replies",
      recruiter_response_rate: "Recruiter Response Rate %",
      interview_invitations: "Interview Invitations",
      recruiter_screens: "Recruiter Screens",
      technical_interviews: "Technical Interviews",
      final_interviews: "Final Interviews",
      job_offers: "Job Offers",
      rejections: "Rejections",
      ghosted_applications: "Ghosted Applications",
      follow_ups_due: "Follow-ups Due",
      average_days_until_response: "Avg Days Until Response",
      average_days_until_interview: "Avg Days Until Interview",
      offer_rate: "Offer Rate %",
      interview_rate: "Interview Rate %",
      resume_download_count: "Resume Download Count",
    };
    $("#analytics-kpis").innerHTML = Object.entries(kpiLabels)
      .map(([k, label]) => {
        const v = data.kpis?.[k];
        return `<div class="stat"><div class="n">${fmtVal(v)}</div><div class="l">${label}</div></div>`;
      })
      .join("");

    $("#analytics-insights").innerHTML = (data.insights || [])
      .map((line) => `<li>${escapeHtml(line)}</li>`)
      .join("");

    const sm = data.success_metrics || {};
    const verLabel = (v) =>
      v && v.version
        ? `${v.version} (${v.reply_rate ?? 0}% replies · ${v.applications} apps)`
        : "";
    const smRows = [
      ["Best Performing Resume Version", verLabel(sm.best_performing_resume_version)],
      ["Best Performing Cover Letter", verLabel(sm.best_performing_cover_letter)],
      [
        "Highest Response Companies",
        (sm.highest_response_companies || [])
          .map((x) => `${x.company} (${x.rate ?? 0}%)`)
          .join(", "),
      ],
      [
        "Highest Interview Companies",
        (sm.highest_interview_companies || [])
          .map((x) => `${x.company} (${x.rate ?? 0}%)`)
          .join(", "),
      ],
      [
        "Highest Salary Companies",
        (sm.highest_salary_companies || [])
          .map((x) => `${x.company} ($${Math.round(x.average_salary || 0)})`)
          .join(", "),
      ],
      [
        "Most Responsive Recruiters",
        (sm.most_responsive_recruiters || [])
          .map((x) => `${x.recruiter} (${x.replies})`)
          .join(", "),
      ],
      [
        "Fastest Interview Response",
        (sm.fastest_interview_response || [])
          .map((x) => `${x.company} (${x.days}d)`)
          .join(", "),
      ],
      [
        "Average Salary of Interviews",
        sm.average_salary_of_interviews != null
          ? `$${Math.round(sm.average_salary_of_interviews)}`
          : "",
      ],
      [
        "Average Salary of Offers",
        sm.average_salary_of_offers != null ? `$${Math.round(sm.average_salary_of_offers)}` : "",
      ],
    ];
    $("#analytics-success").innerHTML = smRows
      .map(
        ([l, v]) =>
          `<div class="metric-row"><span>${escapeHtml(l)}</span><strong>${escapeHtml(v || "Insufficient data")}</strong></div>`
      )
      .join("");

    const ia = data.interview_analytics || {};
    $("#analytics-interview").innerHTML = [
      ["Behavioral pass rate %", ia.behavioral_interview_pass_rate],
      ["Technical pass rate %", ia.technical_interview_pass_rate],
      ["Questions asked most often", (ia.questions_asked_most_often || []).map((q) => q.question).join("; ")],
      ["Weakest topics", (ia.weakest_interview_topics || []).map((t) => t.topic).join("; ")],
      ["Strongest topics", (ia.strongest_interview_topics || []).map((t) => t.topic).join("; ")],
      ["Coding-question companies", (ia.companies_that_ask_coding_questions || []).join(", ")],
      ["Multi-round companies", (ia.companies_with_multiple_interview_rounds || []).map((c) => c.company).join(", ")],
    ]
      .map(([l, v]) => `<div class="metric-row"><span>${escapeHtml(l)}</span><strong>${escapeHtml(fmtVal(v) || "—")}</strong></div>`)
      .join("") + `<p class="note">${escapeHtml(ia.note || "")}</p>`;

    const reports = data.reports || {};
    const weekly = reports.weekly_job_search_report || {};
    const monthly = reports.monthly_performance_report || {};
    $("#analytics-reports").innerHTML = `
      <div class="metric-row"><span>Weekly applications</span><strong>${fmtVal(weekly.applications)}</strong></div>
      <div class="metric-row"><span>Weekly replies / interviews / offers</span><strong>${fmtVal(weekly.replies)} / ${fmtVal(weekly.interviews)} / ${fmtVal(weekly.offers)}</strong></div>
      <div class="metric-row"><span>Monthly response / interview / offer %</span><strong>${fmtVal(monthly.response_rate)} / ${fmtVal(monthly.interview_rate)} / ${fmtVal(monthly.offer_rate)}</strong></div>
      <div class="metric-row"><span>By company</span><strong>${escapeHtml(Object.keys(reports.applications_by_company || {}).slice(0, 6).join(", ") || "—")}</strong></div>
      <div class="metric-row"><span>By role</span><strong>${escapeHtml(Object.keys(reports.applications_by_role || {}).slice(0, 6).join(", ") || "—")}</strong></div>
    `;

    $("#analytics-followups").innerHTML =
      (data.followups || [])
        .map(
          (f) => `<article class="job-card followup-card">
            <div class="job-card-top">
              <div>
                <h3>${escapeHtml(f.company)} — ${escapeHtml(f.position)}</h3>
                <p class="meta">${f.days_since_application} days since apply · ${f.recommended_cadence_days}-day cadence · ${escapeHtml(f.status)}</p>
              </div>
              <div class="card-actions">
                ${
                  f.status === "pending_approval"
                    ? `<button type="button" class="btn primary" data-action="approve-followup" data-id="${f.application_id}" data-cadence="${f.recommended_cadence_days}">Approve draft</button>`
                    : `<span class="package-ready">Approved — send manually</span>`
                }
                <button type="button" class="btn" data-action="copy-followup" data-id="${f.application_id}">Copy email</button>
              </div>
            </div>
            <pre class="followup-body">${escapeHtml(`Subject: ${f.subject}\n\n${f.body}`)}</pre>
          </article>`
        )
        .join("") ||
      "<p class='note'>No follow-ups due. Recommendations appear 3 / 7 / 14 days after Applied.</p>";

    destroyCharts();
    const charts = data.charts || {};
    $("#analytics-charts").innerHTML = [
      ["chart-apps-time", "Applications over time"],
      ["chart-by-company", "Applications by company"],
      ["chart-by-role", "Applications by role"],
      ["chart-salary", "Salary distribution"],
      ["chart-funnel", "Interview funnel"],
      ["chart-response", "Response rate trend"],
    ]
      .map(
        ([id, title]) =>
          `<div class="chart-card"><h3>${title}</h3><div class="chart-wrap"><canvas id="${id}"></canvas></div></div>`
      )
      .join("");

    makeChart(
      "chart-apps-time",
      "line",
      charts.applications_over_time?.labels || [],
      charts.applications_over_time?.values || [],
      "Applications"
    );
    makeChart(
      "chart-by-company",
      "bar",
      charts.applications_by_company?.labels || [],
      charts.applications_by_company?.values || [],
      "Apps"
    );
    makeChart(
      "chart-by-role",
      "bar",
      charts.applications_by_role?.labels || [],
      charts.applications_by_role?.values || [],
      "Apps"
    );
    makeChart(
      "chart-salary",
      "bar",
      charts.salary_distribution?.buckets?.labels || [],
      charts.salary_distribution?.buckets?.values || [],
      "Count"
    );
    makeChart(
      "chart-funnel",
      "bar",
      charts.interview_funnel?.labels || [],
      charts.interview_funnel?.values || [],
      "Count"
    );
    makeChart(
      "chart-response",
      "line",
      charts.response_rate_trend?.labels || [],
      charts.response_rate_trend?.values || [],
      "Response %"
    );
  }

  async function downloadAnalyticsExport(fmt) {
    const res = await fetch(`/api/analytics/export/${fmt}`);
    if (!res.ok) throw new Error(await res.text());
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `recruiter_analytics.${fmt === "xlsx" ? "xlsx" : fmt}`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function currentAssistantApp() {
    const apps = state.assistant?.applications || [];
    return apps.find((a) => a.application_id === state.assistantAppId) || null;
  }

  function switchAssistantPanel(name) {
    state.assistantPanel = name;
    $$("[data-assistant-panel]").forEach((c) =>
      c.classList.toggle("active", c.dataset.assistantPanel === name)
    );
    $$(".assistant-panel").forEach((p) =>
      p.classList.toggle("active", p.id === `assistant-panel-${name}`)
    );
  }

  function renderAssistantAppList() {
    const apps = state.assistant?.applications || [];
    $("#assistant-app-list").innerHTML =
      apps
        .map((a) => {
          const active = a.application_id === state.assistantAppId ? "active" : "";
          const done = a.checklist_complete ? " · checklist ✓" : "";
          return `<button type="button" class="assistant-app-item ${active}" data-action="select-assistant-app" data-id="${a.application_id}">
            <strong>${escapeHtml(a.company)}</strong>
            <span>${escapeHtml(a.position)}</span>
            <span class="meta">${escapeHtml(a.stage_label || a.status)}${done}</span>
          </button>`;
        })
        .join("") || "<p class='note'>No applications yet. Use Prepare Application on a job.</p>";
  }

  function renderAssistantPrepare(app) {
    if (!app) {
      $("#assistant-prepare-body").innerHTML =
        "<p class='note'>Choose an application on the left, or use <strong>Prepare Application</strong> on a job card.</p>";
      return;
    }
    const projects = (app.portfolio_refs || [])
      .map((p) => `<span class="tag">${escapeHtml(p.name || "")}</span>`)
      .join("");
    $("#assistant-prepare-body").innerHTML = `
      <div class="metric-row"><span>Company / Role</span><strong>${escapeHtml(app.company)} — ${escapeHtml(app.position)}</strong></div>
      <div class="metric-row"><span>Prepared at</span><strong>${escapeHtml(fmtDate(app.prepared_at) || "Not prepared yet")}</strong></div>
      <div class="metric-row"><span>Checklist</span><strong>${app.checklist_complete ? "Complete" : "Incomplete"}</strong></div>
      <div class="projects-row" style="margin-top:0.75rem"><span class="projects-label">Portfolio matches</span><div class="tags">${projects || "<span class='tag'>None yet</span>"}</div></div>
      <h3 style="margin:1rem 0 0.4rem">Recruiter summary</h3>
      <pre class="followup-body">${escapeHtml(app.recruiter_summary || "Run Prepare Application to generate.")}</pre>
      <h3 style="margin:1rem 0 0.4rem">Tailored resume</h3>
      <pre class="followup-body">${escapeHtml(app.tailored_resume || "Not generated")}</pre>
      <h3 style="margin:1rem 0 0.4rem">Cover letter</h3>
      <pre class="followup-body">${escapeHtml(app.cover_letter || "Not generated")}</pre>
      <div class="card-actions" style="margin-top:0.75rem">
        ${app.job_id ? `<button type="button" class="btn primary" data-action="prepare-app" data-id="${app.job_id}">Prepare Application</button>` : ""}
        <button type="button" class="btn primary" data-action="open-application" data-id="${app.application_id}">Open Application</button>
        <button type="button" class="btn" data-action="mark-submitted" data-id="${app.application_id}">Mark as Submitted</button>
        <button type="button" class="btn" data-action="export-app" data-id="${app.application_id}">Export Packet</button>
        ${
          app.status === "ready" || app.status === "saved"
            ? `<button type="button" class="btn" data-action="approve" data-id="${app.application_id}">Approve to Apply</button>`
            : ""
        }
      </div>`;
  }

  function renderAssistantChecklist(app) {
    const labels = state.assistant?.checklist_labels || {};
    const cl = app?.checklist || {};
    $("#assistant-checklist").innerHTML = app
      ? Object.keys(labels)
          .map((k) => {
            const checked = !!cl[k];
            return `<label class="check checklist-item">
              <input type="checkbox" data-check-key="${k}" ${checked ? "checked" : ""}>
              ${checked ? "✓" : "○"} ${escapeHtml(labels[k])}
            </label>`;
          })
          .join("")
      : "<p class='note'>Select an application first.</p>";
  }

  function fillAssistantNotes(app) {
    const form = $("#assistant-notes-form");
    if (!form) return;
    const n = app?.application_notes || {};
    form.recruiter_name.value = n.recruiter_name || "";
    form.hiring_manager.value = n.hiring_manager || "";
    form.referral.value = n.referral || "";
    form.salary_discussed.value = n.salary_discussed || "";
    form.interview_notes.value = n.interview_notes || "";
    form.follow_up_reminders.value = n.follow_up_reminders || "";
  }

  function fillAssistantOffer(app) {
    const form = $("#assistant-offer-form");
    if (!form) return;
    const o = app?.offer || {};
    form.salary.value = o.salary ?? "";
    form.bonus.value = o.bonus || "";
    form.benefits.value = o.benefits || "";
    form.pto.value = o.pto || "";
    form.remote_policy.value = o.remote_policy || "";
    form.career_growth.value = o.career_growth || "";
    form.overall_score.value = o.overall_score ?? "";
    form.notes.value = o.notes || "";
  }

  function renderAssistantCalendar() {
    const events = state.assistant?.calendar || [];
    $("#assistant-calendar-list").innerHTML =
      events
        .map(
          (ev) => `<article class="job-card">
            <div class="job-card-head">
              <div>
                <h3>${escapeHtml(ev.company || "")}</h3>
                <p class="meta">${escapeHtml(ev.date || "")} ${escapeHtml(ev.time || "")} · ${escapeHtml(ev.stage_label || ev.interview_stage || "")}</p>
                <p class="meta">${escapeHtml(ev.position || "")}</p>
                ${(ev.interviewers || []).length ? `<p class="meta">Interviewers: ${escapeHtml((ev.interviewers || []).join(", "))}</p>` : ""}
                ${ev.meeting_link ? `<p class="meta"><a href="${escapeAttr(ev.meeting_link)}" target="_blank" rel="noopener noreferrer">Meeting link</a></p>` : ""}
              </div>
              <div class="card-actions">
                <button type="button" class="btn" data-action="delete-calendar" data-id="${ev.application_id}" data-event="${escapeAttr(ev.id)}">Remove</button>
              </div>
            </div>
          </article>`
        )
        .join("") || "<p class='note'>No interviews scheduled yet. Add one above for the selected application.</p>";
  }

  function renderAssistantLessons() {
    const lessons = state.assistant?.lessons || [];
    $("#assistant-lessons-list").innerHTML =
      lessons
        .map(
          (L) => `<article class="job-card">
            <h3>${escapeHtml(L.company)} — ${escapeHtml(L.position)}</h3>
            <p class="meta">${escapeHtml(L.interview_date || "Date not set")} · ${escapeHtml(L.stage || "")}</p>
            ${L.what_went_well ? `<div class="why-box"><h4>Went well</h4><p>${escapeHtml(L.what_went_well)}</p></div>` : ""}
            ${L.what_to_improve ? `<div class="why-box"><h4>Improve</h4><p>${escapeHtml(L.what_to_improve)}</p></div>` : ""}
            ${(L.questions_asked || []).length ? `<ul>${(L.questions_asked || []).map((q) => `<li>${escapeHtml(q)}</li>`).join("")}</ul>` : ""}
          </article>`
        )
        .join("") || "<p class='note'>No lessons logged yet.</p>";
  }

  function renderAssistantOffers() {
    const offers = state.assistant?.offers?.offers || [];
    $("#assistant-offers-table tbody").innerHTML =
      offers
        .map(
          (o) => `<tr>
            <td>${escapeHtml(o.company)}</td>
            <td>${escapeHtml(o.position)}</td>
            <td>${o.salary != null ? "$" + Math.round(o.salary).toLocaleString() : "—"}</td>
            <td>${escapeHtml(o.bonus || "—")}</td>
            <td>${escapeHtml(o.benefits || "—")}</td>
            <td>${escapeHtml(o.pto || "—")}</td>
            <td>${escapeHtml(o.remote_policy || "—")}</td>
            <td>${escapeHtml(o.career_growth || "—")}</td>
            <td>${o.overall_score != null ? escapeHtml(String(o.overall_score)) : "—"}</td>
          </tr>`
        )
        .join("") ||
      `<tr><td colspan="9" class="note">No offer details recorded yet. Enter real terms above for a selected application.</td></tr>`;
  }

  function renderAssistantSelected() {
    const app = currentAssistantApp();
    const contact = state.assistant?.contact || {};
    $("#assistant-meta").textContent = app
      ? `Active: ${app.company} — ${app.position} · Local only · Contact on file: ${contact.email || ""} · ${contact.phone || ""}`
      : `Local only · Contact on file: ${contact.email || ""} · Portfolio: ${contact.portfolio || ""} · Select or prepare an application.`;
    if (app) {
      const calForm = $("#assistant-calendar-form");
      if (calForm && !calForm.company.value) calForm.company.value = app.company || "";
    }
    renderAssistantAppList();
    renderAssistantPrepare(app);
    renderAssistantChecklist(app);
    fillAssistantNotes(app);
    fillAssistantOffer(app);
    renderAssistantCalendar();
    renderAssistantLessons();
    renderAssistantOffers();
  }

  async function loadAssistant() {
    state.assistant = await api("/api/assistant");
    if (
      state.assistantAppId &&
      !(state.assistant.applications || []).some((a) => a.application_id === state.assistantAppId)
    ) {
      state.assistantAppId = null;
    }
    if (!state.assistantAppId && (state.assistant.applications || []).length) {
      state.assistantAppId = state.assistant.applications[0].application_id;
    }
    renderAssistantSelected();
  }

  async function selectAssistantApp(appId) {
    state.assistantAppId = appId;
    const bundle = await api(`/api/assistant/applications/${appId}`);
    if (state.assistant) {
      const idx = (state.assistant.applications || []).findIndex((a) => a.application_id === appId);
      if (idx >= 0) state.assistant.applications[idx] = bundle;
      else state.assistant.applications.unshift(bundle);
    }
    renderAssistantSelected();
  }

  async function prepareApplication(jobId) {
    const bundle = await api(`/api/assistant/prepare/${jobId}`, { method: "POST" });
    state.assistantAppId = bundle.application_id;
    await loadAssistant();
    switchView("assistant");
    switchAssistantPanel("prepare");
    return bundle;
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
      if (tab.dataset.view === "analytics") loadAnalytics().catch((err) => {
        $("#analytics-meta").textContent = String(err.message || err);
      });
      if (tab.dataset.view === "assistant") loadAssistant().catch((err) => {
        $("#assistant-meta").textContent = String(err.message || err);
      });
      if (tab.dataset.view === "career") loadCareerAgent().catch((err) => {
        $("#career-meta").textContent = String(err.message || err);
      });
    })
  );

  function switchCareerPanel(name) {
    $$("[data-career-panel]").forEach((c) =>
      c.classList.toggle("active", c.dataset.careerPanel === name)
    );
    $$("#view-career .assistant-panel").forEach((p) =>
      p.classList.toggle("active", p.id === `career-panel-${name}`)
    );
  }

  async function loadCareerAgent() {
    const status = await api("/api/career-agent/status");
    const brief = await api("/api/career-agent/daily-brief");
    const today = await api("/api/career-agent/todays-brief");
    const coach = await api("/api/career-agent/coach");
    const weekly = await api("/api/career-agent/coach/weekly-report");
    const crm = await api("/api/career-agent/crm");
    $("#career-meta").textContent =
      `Last run: ${status.last_run?.ran_at || "not yet"} · Trigger: ${status.last_run?.trigger || "—"} · RUN NOW available · Auto-apply: off · Alerts ≥${status.alert_threshold || 90}%`;

    $("#career-today-stats").innerHTML = [
      ["Jobs searched", today.jobs_searched_today ?? "—"],
      ["Verified remote", today.verified_remote_jobs ?? 0],
      ["New today", today.new_jobs_today ?? 0],
      ["Apps ready", today.applications_ready ?? 0],
      ["Apps sent", today.applications_sent ?? 0],
      ["Recruiter replies", today.recruiter_replies ?? 0],
      ["Interviews", today.interviews_scheduled ?? 0],
      ["Offers", today.offers ?? 0],
      ["Avg salary", today.average_salary != null ? `$${Math.round(today.average_salary)}` : "—"],
    ]
      .map(([l, n]) => `<div class="stat"><div class="n">${escapeHtml(String(n))}</div><div class="l">${l}</div></div>`)
      .join("");

    $("#career-today-top10").innerHTML =
      (today.top_10_opportunities || [])
        .map(
          (j) => `<article class="job-card">
            <h3>${escapeHtml(j.title)}</h3>
            <p class="meta">${escapeHtml(j.company)} · Match ${j.score}% · ${escapeHtml(j.salary || "")}</p>
          </article>`
        )
        .join("") || "<p class='note'>No opportunities yet. Click RUN NOW.</p>";

    $("#career-today-trends").innerHTML = [
      [
        "Top companies",
        (today.top_companies_hiring || []).map((c) => `${c.company} (${c.roles})`).join(", ") || "—",
      ],
      [
        "Skill trends",
        (today.skill_trends || []).map((s) => s.technology).slice(0, 8).join(", ") || "—",
      ],
      [
        "Missing keywords",
        (today.missing_keywords || []).map((s) => s.skill_or_tech).slice(0, 8).join(", ") || "—",
      ],
    ]
      .map(([l, v]) => `<div class="metric-row"><span>${escapeHtml(l)}</span><strong>${escapeHtml(String(v))}</strong></div>`)
      .join("");

    $("#career-notifications").innerHTML =
      (brief.notifications || [])
        .map(
          (n) =>
            `<article class="job-card"><h3>${escapeHtml(n.type)}</h3><p class="meta">${escapeHtml(n.message)}</p></article>`
        )
        .join("") || "<p class='note'>No notifications. Alerts appear for Match Score ≥ 90% / 80% and due follow-ups.</p>";

    $("#career-brief-stats").innerHTML = [
      ["New jobs today", (brief.new_jobs_found || []).length],
      ["Best tracked", (brief.best_opportunities || []).length],
      ["Follow-ups due", (brief.follow_ups_due_today || []).length],
      ["Upcoming interviews", (brief.upcoming_interviews || []).length],
      ["Closing ≤48h", (brief.jobs_closing_within_48_hours || []).length],
      ["Recruiters viewing", (brief.recruiters_viewing_applications || []).length],
    ]
      .map(([l, n]) => `<div class="stat"><div class="n">${n}</div><div class="l">${l}</div></div>`)
      .join("");

    $("#career-best").innerHTML =
      (brief.best_opportunities || [])
        .map(
          (j) => `<article class="job-card">
            <h3>${escapeHtml(j.title)}</h3>
            <p class="meta">${escapeHtml(j.company)} · Match ${j.score}% ${j.notify ? "· ALERT ≥80" : ""}</p>
            <p class="meta">${escapeHtml(j.salary || "")}</p>
          </article>`
        )
        .join("") || "<p class='note'>No scored jobs yet. Run Morning Agent.</p>";

    const hi = brief.highest_interview_probability || {};
    const sal = brief.salary_trends || {};
    $("#career-brief-details").innerHTML = [
      ["Highest match opportunity", hi.company ? `${hi.company} — ${hi.position} (${hi.match_score})` : "—"],
      ["Salary avg / median", sal.samples ? `$${sal.average} / $${sal.median} (n=${sal.samples})` : sal.note || "—"],
      [
        "Companies hiring repeatedly",
        (brief.companies_hiring_repeatedly || []).map((c) => `${c.company} (${c.open_roles_tracked})`).join(", ") || "—",
      ],
      [
        "Missing skills",
        (brief.missing_skills_appearing_frequently || []).map((s) => s.skill_or_tech).slice(0, 8).join(", ") || "—",
      ],
      [
        "Cert suggestions",
        (brief.recommended_certifications || []).map((c) => c.suggestion).slice(0, 2).join(" · ") || "—",
      ],
    ]
      .map(([l, v]) => `<div class="metric-row"><span>${escapeHtml(l)}</span><strong>${escapeHtml(String(v))}</strong></div>`)
      .join("");

    $("#career-coach").innerHTML = [
      ["Resume weaknesses", (coach.resume_weaknesses || []).join(" · ")],
      ["Portfolio weaknesses", (coach.portfolio_weaknesses || []).join(" · ")],
      [
        "Interview performance",
        `Behavioral ${coach.interview_performance?.behavioral_pass_rate ?? "—"}% · Technical ${
          coach.interview_performance?.technical_pass_rate ?? "—"
        }%`,
      ],
      [
        "ATS missing keywords",
        (coach.ats_keyword_coverage?.missing_from_resume_samples || [])
          .map((k) => k.keyword)
          .slice(0, 8)
          .join(", ") || "—",
      ],
    ]
      .map(([l, v]) => `<div class="metric-row"><span>${escapeHtml(l)}</span><strong>${escapeHtml(String(v))}</strong></div>`)
      .join("");

    $("#career-weekly-actions").innerHTML = (weekly.recommended_actions || [])
      .map((a) => `<li>[${escapeHtml(a.area)}] ${escapeHtml(a.action)}</li>`)
      .join("") || "<li>No actions yet.</li>";

    $("#crm-list").innerHTML =
      (crm.contacts || [])
        .map(
          (c) => `<article class="job-card">
            <h3>${escapeHtml(c.recruiter_name || "Recruiter")} — ${escapeHtml(c.company)}</h3>
            <p class="meta">${escapeHtml(c.email || "")} · ${escapeHtml(c.phone || "")}</p>
            <p class="meta">Last: ${escapeHtml(c.last_contact || "—")} · Follow-up: ${escapeHtml(c.follow_up_date || "—")}</p>
            <p class="meta">${escapeHtml(c.notes || "")}</p>
            <p class="meta">Referrals: ${escapeHtml(c.referral_opportunities || "—")}</p>
            <div class="card-actions">
              <button type="button" class="btn" data-action="crm-delete" data-id="${c.id}">Delete</button>
            </div>
          </article>`
        )
        .join("") || "<p class='note'>No CRM contacts yet. Add one or import from applications.</p>";
  }

  $$("[data-career-panel]").forEach((chip) =>
    chip.addEventListener("click", () => switchCareerPanel(chip.dataset.careerPanel))
  );

  async function runCareerAgent(endpoint, btn, doneLabel) {
    btn.disabled = true;
    const prev = btn.textContent;
    btn.textContent = "Running…";
    try {
      const result = await api(endpoint, { method: "POST" });
      if (result.skipped) {
        alert(result.reason || "Run skipped — another search is in progress.");
      } else {
        alert(
          `Career Agent 2.0 finished (${result.trigger || "run"}).\n` +
            `Fetched ${result.refresh?.fetched ?? "—"}, matched ${result.refresh?.matched ?? "—"}.\n` +
            `Notifications: ${(result.notifications || []).length}. Auto-apply: off.`
        );
      }
      await loadCareerAgent();
      switchCareerPanel("today");
    } catch (err) {
      $("#career-meta").textContent = String(err.message || err);
    } finally {
      btn.disabled = false;
      btn.textContent = doneLabel || prev;
    }
  }

  $("#btn-career-run-now")?.addEventListener("click", () =>
    runCareerAgent("/api/career-agent/run-now", $("#btn-career-run-now"), "RUN NOW")
  );

  $("#btn-career-run")?.addEventListener("click", () =>
    runCareerAgent("/api/career-agent/run-morning", $("#btn-career-run"), "Run Morning Agent")
  );

  $("#btn-career-brief")?.addEventListener("click", async () => {
    await api("/api/career-agent/daily-brief?rebuild=true");
    await loadCareerAgent();
  });

  $("#btn-career-weekly")?.addEventListener("click", async () => {
    await api("/api/career-agent/coach/weekly-report", { method: "POST" });
    await loadCareerAgent();
    switchCareerPanel("coach");
  });

  $("#btn-crm-import")?.addEventListener("click", async () => {
    const r = await api("/api/career-agent/crm/import-from-applications", { method: "POST" });
    alert(`Imported ${r.created}, skipped ${r.skipped}. Auto-email: off.`);
    await loadCareerAgent();
    switchCareerPanel("crm");
  });

  $("#crm-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(e.target).entries());
    await api("/api/career-agent/crm", { method: "POST", body: JSON.stringify(payload) });
    e.target.reset();
    await loadCareerAgent();
    switchCareerPanel("crm");
  });

  $("#intel-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const raw = Object.fromEntries(new FormData(e.target).entries());
    const payload = {};
    if (raw.application_id) payload.application_id = Number(raw.application_id);
    if (raw.job_id) payload.job_id = Number(raw.job_id);
    const intel = await api("/api/career-agent/interview-intelligence", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    $("#intel-body").innerHTML = `
      <div class="metric-row"><span>Company / Role</span><strong>${escapeHtml(intel.company)} — ${escapeHtml(intel.position)}</strong></div>
      <div class="why-box"><h4>30s elevator pitch</h4><p>${escapeHtml(intel.elevator_pitch_30s)}</p></div>
      <div class="why-box"><h4>Company research</h4><p>${escapeHtml(intel.company_research)}</p></div>
      <div class="metric-row"><span>Financial overview</span><strong>${escapeHtml(
        intel.financial_overview?.available
          ? (intel.financial_overview.figures || []).join("; ")
          : intel.financial_overview?.note || "Unavailable"
      )}</strong></div>
      <div class="metric-row"><span>Products</span><strong>${escapeHtml((intel.products || []).join(" · "))}</strong></div>
      <div class="metric-row"><span>Competitors</span><strong>${escapeHtml((intel.competitors || []).join(" · "))}</strong></div>
      <div class="metric-row"><span>Culture</span><strong>${escapeHtml((intel.company_culture || []).join(" · "))}</strong></div>
      <div class="metric-row"><span>Latest news</span><strong>${escapeHtml(
        intel.latest_news?.available ? (intel.latest_news.items || []).join(" · ") : intel.latest_news?.note || "Unavailable"
      )}</strong></div>
      <div class="metric-row"><span>Technical topics</span><strong>${escapeHtml((intel.technical_topics_likely || []).join(", "))}</strong></div>
      <h3>STAR answers</h3>
      ${(intel.star_answers || [])
        .map(
          (s) => `<article class="star-block"><h4>${escapeHtml(s.title)}</h4>
            <p><strong>S:</strong> ${escapeHtml(s.situation)}</p>
            <p><strong>T:</strong> ${escapeHtml(s.task)}</p>
            <p><strong>A:</strong> ${escapeHtml(s.action)}</p>
            <p><strong>R:</strong> ${escapeHtml(s.result)}</p></article>`
        )
        .join("")}
      <h3>Questions to ask</h3>
      <ul>${(intel.questions_to_ask_interviewer || []).map((q) => `<li>${escapeHtml(q)}</li>`).join("")}</ul>
      <h3>Salary negotiation notes</h3>
      <pre class="followup-body">${escapeHtml(JSON.stringify(intel.salary_negotiation_notes, null, 2))}</pre>
      <p class="note">${escapeHtml((intel.notes || []).join(" "))}</p>
    `;
    switchCareerPanel("intel");
  });

  $("#btn-assistant-refresh")?.addEventListener("click", () =>
    loadAssistant().catch((err) => {
      $("#assistant-meta").textContent = String(err.message || err);
    })
  );

  $$("[data-assistant-panel]").forEach((chip) =>
    chip.addEventListener("click", () => switchAssistantPanel(chip.dataset.assistantPanel))
  );

  $("#assistant-checklist")?.addEventListener("change", async (e) => {
    const input = e.target.closest("input[data-check-key]");
    if (!input || !state.assistantAppId) return;
    const key = input.dataset.checkKey;
    try {
      const bundle = await api(`/api/assistant/applications/${state.assistantAppId}/checklist`, {
        method: "PATCH",
        body: JSON.stringify({ [key]: input.checked }),
      });
      const idx = (state.assistant?.applications || []).findIndex(
        (a) => a.application_id === state.assistantAppId
      );
      if (idx >= 0) state.assistant.applications[idx] = bundle;
      renderAssistantSelected();
    } catch (err) {
      alert(String(err.message || err));
    }
  });

  $("#assistant-notes-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!state.assistantAppId) return alert("Select an application first.");
    const payload = Object.fromEntries(new FormData(e.target).entries());
    const bundle = await api(`/api/assistant/applications/${state.assistantAppId}/notes`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    });
    const idx = (state.assistant?.applications || []).findIndex(
      (a) => a.application_id === state.assistantAppId
    );
    if (idx >= 0) state.assistant.applications[idx] = bundle;
    alert("Notes saved locally.");
    renderAssistantSelected();
  });

  $("#assistant-calendar-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!state.assistantAppId) return alert("Select an application first.");
    const payload = Object.fromEntries(new FormData(e.target).entries());
    await api(`/api/assistant/applications/${state.assistantAppId}/calendar`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    e.target.reset();
    await loadAssistant();
    switchAssistantPanel("calendar");
  });

  $("#assistant-lesson-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!state.assistantAppId) return alert("Select an application first.");
    const payload = Object.fromEntries(new FormData(e.target).entries());
    await api(`/api/assistant/applications/${state.assistantAppId}/lessons`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    e.target.reset();
    await loadAssistant();
    switchAssistantPanel("lessons");
  });

  $("#assistant-offer-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!state.assistantAppId) return alert("Select an application first.");
    const payload = Object.fromEntries(new FormData(e.target).entries());
    if (payload.salary === "") delete payload.salary;
    if (payload.overall_score === "") delete payload.overall_score;
    await api(`/api/assistant/applications/${state.assistantAppId}/offer`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    });
    await loadAssistant();
    switchAssistantPanel("offers");
    alert("Offer details saved locally.");
  });

  $("#btn-refresh-analytics")?.addEventListener("click", () =>
    loadAnalytics().catch((err) => {
      $("#analytics-meta").textContent = String(err.message || err);
    })
  );

  document.querySelectorAll("[data-export]").forEach((btn) =>
    btn.addEventListener("click", async () => {
      try {
        await downloadAnalyticsExport(btn.dataset.export);
      } catch (err) {
        alert(String(err.message || err));
      }
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
      if (action === "prepare-app") {
        const label = btn.textContent;
        btn.disabled = true;
        btn.textContent = "Preparing…";
        try {
          await prepareApplication(id);
          alert("Application prepared locally. Review checklist before you submit.");
        } finally {
          btn.disabled = false;
          btn.textContent = label.includes("Prepare") ? label : "Prepare Application";
        }
      }
      if (action === "open-assistant" || action === "select-assistant-app") {
        await selectAssistantApp(id);
        switchView("assistant");
        switchAssistantPanel("prepare");
      }
      if (action === "delete-calendar") {
        const eventId = btn.dataset.event;
        if (!confirm("Remove this calendar event?")) return;
        await api(`/api/assistant/applications/${id}/calendar/${encodeURIComponent(eventId)}`, {
          method: "DELETE",
        });
        await loadAssistant();
      }
      if (action === "open-application") {
        const session = await api(`/api/autofill/applications/${id}/open`, { method: "POST" });
        if (!session.application_url) {
          alert("No application URL on this job.");
          return;
        }
        window.open(session.application_url, "_blank", "noopener,noreferrer");
        alert(
          `Opened ${session.company} — ${session.position}\nPlatform: ${session.platform}\n\n` +
            "In the browser extension: review the preview, then click Confirm Autofill.\n" +
            "Submit is NEVER clicked for you. After you submit manually, click Mark as Submitted."
        );
        if (document.getElementById("view-assistant")?.classList.contains("active")) {
          await loadAssistant();
        }
      }
      if (action === "mark-submitted") {
        if (!confirm("Mark as Submitted only after YOU manually submitted the application?")) return;
        const notes = prompt("Optional submission notes:", "Manually submitted by Leroy.") || "";
        const result = await api(`/api/applications/${id}/mark-submitted`, {
          method: "POST",
          body: JSON.stringify({ notes }),
        });
        alert(result.message || "Marked submitted.");
        await Promise.all([loadDashboard(), loadTracker(), loadAssistant().catch(() => null)]);
      }
      if (action === "crm-delete") {
        if (!confirm("Delete this CRM contact?")) return;
        await api(`/api/career-agent/crm/${id}`, { method: "DELETE" });
        await loadCareerAgent();
      }
      if (action === "export-app") await exportApp(id);
      if (action === "export-job") await exportJob(id);
      if (action === "approve-followup") {
        const cadence = Number(btn.dataset.cadence || 3);
        if (!confirm("Approve this follow-up draft? Nothing will be emailed automatically.")) return;
        const result = await api(
          `/api/analytics/followups/${id}/approve?cadence_days=${cadence}`,
          { method: "POST" }
        );
        await navigator.clipboard.writeText(`Subject: ${result.subject}\n\n${result.body}`);
        alert(result.message || "Approved. Email copied — send manually.");
        await loadAnalytics();
      }
      if (action === "copy-followup") {
        const card = btn.closest(".followup-card");
        const text = card?.querySelector(".followup-body")?.textContent || "";
        await navigator.clipboard.writeText(text);
        alert("Follow-up email copied.");
      }
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
