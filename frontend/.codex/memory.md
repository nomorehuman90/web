# Project session memory

- The user runs the frontend and backend servers themselves. Do not start either server; stop any server started by Codex when asked or before handing control back.
- The frontend must send backend API requests to `http://127.0.0.1:8000` (Vite proxy target).
- At the start of a future session, read the agent definitions in `../codex/agents/frontend-dev.toml` and `../codex/agents/backend-dev.toml`, then create the `frontend_dev` and `backend_dev` subagents from those role instructions when subagents are available. `frontend_dev` owns Vue work in `frontend/`; use the `api`, `assets`, `components`, `router`, `stores`, and `views` areas as appropriate, and use axios to call the backend directly. `backend_dev` owns FastAPI work in `app/` and should follow the existing project structure. Live subagent instances do not carry across sessions, so recreate them from these definitions at session start.
