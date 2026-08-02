# Job Machine architecture

Expandable layout for a future full AI job assistant.

```
job-machine/
  app/
    main.py              # FastAPI entry
    config.py            # Settings / env
    database.py          # SQLAlchemy engine
    models.py            # Job + Application tables
    schemas.py           # API contracts
    routers/api.py       # HTTP surface
    services/
      job_finder.py      # Aggregate + persist
      filters.py         # Remote/US/role filters
      scorer.py          # 1–100 opportunity score
      portfolio_matcher.py
      resume_tailor.py   # Template + optional OpenAI
      cover_letter.py
      truth_guard.py     # Fabrication scanner
      sources/           # Per-board adapters
    truth/               # Locked facts (do not invent beyond these)
  static/                # Dashboard UI
  data/                  # Local SQLite (gitignored)
```

## Extension points

1. Add a source adapter in `services/sources/` and register it in `job_finder.search_jobs`.
2. Add reminder workers that read `applications.follow_up_date`.
3. Add an ATS apply adapter that requires explicit human approval before submit.
4. Keep all generative paths behind `truth_guard` + `profile.json`.
