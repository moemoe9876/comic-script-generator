# Selling the Comic Script Generator

This document explains a practical, low-friction plan for selling the Comic Script Generator to YouTube creators. I reviewed the codebase (modular agents, Streamlit front-end, config) and produced an actionable strategy that covers product options, a recommended simple pricing model, hosting & deployment options, legal & safety notes, minimal code changes to support a "bring-your-own-API-key (BYO-key)" flow, and a short launch checklist.

Short summary / Recommendation (one-line)

- Easiest, lowest-risk path: sell the source code as a one-time purchase (Gumroad) **and** offer a hosted subscription for creators who want a turnkey service. Let hosted users provide their own Gemini API key (BYO-key) to avoid handling AI billing while you charge for hosting, UI, maintenance and support.

Why this approach works

- Selling source is fast to set up (Gumroad or Paddle) and requires no operational overhead.
- Hosting + BYO-key removes your need to pay for large AI bills and greatly simplifies compliance and billing complexity while still providing value (UX, convenience, reliability).
- Offering both options captures both power users (who want the code) and creators who want an easy one-click service.

Contents

- Product options (what to sell)
- Recommended simple pricing model
- BYO-key hosting architecture & security notes
- Minimal code changes to support user API keys
- Payment / auth options and recommended integrations
- Legal & content-safety checklist
- Deployment & launch checklist
- Marketing & distribution ideas
- Next steps & suggested priorities

## Product options (which SKUs to offer)

Offer two clear SKUs. Keep it extremely simple.

1) One-time Source License (digital download)
- What: Full repository packaged with an installation guide and a short README on how to self-host locally. Include an explicit small-license file (e.g., LICENSE.md or TERMS_FOR_BUYERS.md) that permits personal / client usage but not reselling.
- Delivery: Gumroad / Paddle (automated download link after purchase)
- Support: Optional paid support add-on (hourly or small fixed fee).

2) Hosted Service (subscription)
- What: You host a Streamlit deployment and sell access to creators. They sign up and either provide their Gemini API key (recommended) or pay extra for a hosted key usage plan (advanced). The hosted product gives them the UI and convenience, no setup.
- Delivery: Create a simple signup + billing flow (Stripe Checkout or Gumroad subscription). After sign-up they get access to the Streamlit app.
- Support: Included in plan price.

Keep only those two SKUs initially — no coupons, affiliate programs, or complex tiering until you validate demand.

## Recommended simple pricing model (start simple)

Option A — Lowest friction (recommended)
- Source code (one-time): $29–$79 depending on how polished the docs are. Suggested launch price: $39.
- Hosted access (subscription): single flat monthly plan. Suggested: $19/month (indie creator) or $49/month if you provide heavy run quota or managed API key usage.
- Free trial: 7-day trial or 3 free runs to let users see output quality.

Option B — Alternative (if you want pay-per-use)
- Free tier: 3 free runs / month
- Paid: $9/month for 20 runs, $29/month for unlimited small usage (or pay-per-run $1–$3). This is more complex to implement and bill; avoid it initially.

Why BYO-key helps pricing

- BYO-key means you charge only for hosting and UI (predictable costs) while the user pays for the AI usage directly to Google. That lets you keep subscription price low and eliminates the risk of enormous AI bills.

## BYO-key hosting architecture (how it works)

High level (minimal complexity):

1. User signs up and logs in to your hosted Streamlit app (or you gate the app behind a simple membership link after purchase).
2. In the user settings (sidebar) they paste their Gemini API key once.
3. The Streamlit session stores the API key in server-side user profile or encrypted store (see security notes). For simplicity you can store it in the Streamlit session for short-lived sessions and re-prompt on reconnect.
4. When processing a comic, your app uses the user's API key to make Gemini calls. The app never stores the key unencrypted for long durations unless the user opts in.

This keeps billing responsibility with the user and makes your hosting costs predictable (CPU, storage) rather than AI call costs.

Security and operational notes

- Never log the full API key. Mask the key in logs.
- If you persist keys: encrypt them at rest (e.g., AWS KMS, or a secrets-encrypted DB column). Or better: don't persist long-term — ask the user to paste it every session or until logout.
- Rate-limit uploads and processing to prevent abuse from malicious users.
- Enforce maximum file sizes (streamlit_config.MAX_FILE_SIZE_MB) and runtime limits.
- Quotas: for a hosted plan, put a reasonable CPU/time quota (for example: max 2 concurrent runs per account) to prevent resource starvation.

## Minimal code changes to support BYO-key (low-risk)

Goal: Allow an authenticated user to provide their own Gemini API key via the Streamlit UI and ensure the modular agents use that key when calling Gemini.

Suggested minimal approach (no major refactor):

1. Add a text input in `streamlit_app.py` sidebar where users paste their Gemini API key (this is purely UI change).
2. After user provides the key, set it into the environment before the modular agents create their `genai` clients OR pass the key to `MainCoordinator` and have the coordinator pass it to agents.

Why this is needed: currently `modular_agents/config.py` reads `GEMINI_API_KEY` from environment at import-time. Also `PageAnalyzer` calls `genai.configure(api_key=config.GEMINI_API_KEY)` inside its constructor. To use a user key, you must make sure that configuration happens after the user-supplied key is known.

Two concrete minimal options (choose one):

A) Quick (fewer code edits)
- In `streamlit_app.py`, move the import of `MainCoordinator` to after the user provides an API key (or after reading session state). For example:
  - Prompt for `user_key = st.sidebar.text_input('Your Gemini API Key (optional)')`.
  - If `user_key` is provided, set `os.environ['GEMINI_API_KEY'] = user_key` before creating `MainCoordinator()`.
- This works because `config.GEMINI_API_KEY` reads from `os.getenv` when `config` is imported by `MainCoordinator` and its agents. You must ensure `MainCoordinator` and `PageAnalyzer` are imported after you set the env var.

Trade-offs:
- Very low code change but fragile if modules are imported earlier.
- Avoids modifying multiple files.

B) Clean (recommended for maintainability)
- Add an optional `api_key` argument to `MainCoordinator.__init__(api_key=None, ...)`.
- In `MainCoordinator.__init__`, pass this API key to agents or set `config.GEMINI_API_KEY` dynamically and call `genai.configure(...)` as needed.
- Update `PageAnalyzer`, `StorySummarizer`, and `ScriptGenerator` to accept an optional api_key and use it when configuring `genai`.

Trade-offs:
- Slightly more code to change but robust and explicit.
- Safer for future multi-tenant deployments.

Minimal code hints (pseudocode, not a patch):

- Add UI input in `streamlit_app.py` sidebar:
  - `user_gemini_key = st.sidebar.text_input('Gemini API key (paste here to use your key)')`
  - When creating the coordinator: `coordinator = MainCoordinator(model_name=..., temperature=..., api_key=user_gemini_key)`

- Add optional parameter to `MainCoordinator.__init__` and pass it to `PageAnalyzer` and other agents or call a small helper that runs `genai.configure(api_key=api_key)` before instantiating the agents.

Note: Because this repo currently calls `genai.configure(api_key=...)` inside `PageAnalyzer.__init__`, ensure you set the desired api_key before instantiating `PageAnalyzer`.

## Payment & authentication options (simple choice to start)

A. Selling source (one-time): Gumroad or Paddle
- Setup: Create a product on Gumroad with the zip bundle of the repo and docs. Gumroad handles payments and delivers the file immediately. They also handle VAT.
- Pros: Very fast to set up, no backend or webhooks required.
- Cons: One-time revenue only.

B. Hosted subscription: Stripe Checkout (recommended)
- Use Stripe Checkout + Customer Portal for subscriptions. It's the most professional and flexible option.
- After successful billing webhook, create an account in your app (or let users sign up manually and verify payment via webhook) and enable the Streamlit URL for them.
- For auth you can use simple email-based magic link (e.g., Netlify Identity) or Firebase Auth if you need quick user accounts.

C. Very minimal gating option (fastest to launch)
- Sell the hosted app as a private link. After purchase, you manually add buyer emails to an allowlist (works only for a small number of clients).

Recommended integration order (fast -> more advanced):
1. Gumroad to sell source code.
2. Manual hosted customers initially (private link) while you validate demand.
3. Add Stripe Checkout + webhook automation for signups once you reach a few customers.

## Legal & content safety checklist (important when selling to creators)

- Terms of Service (TOS) + Acceptable Use Policy: Make it explicit users must have the right to upload any comic content they process. Disclaim you are not responsible for copyright violations.
- Privacy Policy: Explain how API keys (if stored) are handled and whether any data leaves your servers.
- DMCA: Provide an email/contact for takedown requests.
- Disclaimers: Be clear that the hosted service does not provide legal clearance for copyrighted content.
- Refund policy: For digital downloads, follow platform rules (Gumroad/Paddle). For hosted subscriptions, provide a simple 7-day refund window.

## Deployment checklist (hosted path)

Initial quick path (for testing / very small customers):
- Host on Streamlit Cloud or Render with a minimal server. Streamlit Cloud is easiest for developers but limited for user auth and heavy background tasks.
- Use a managed Postgres or small SQLite to store user metadata (prefer Postgres for production).
- Use HTTPS, secure cookies, and environment variables.

Production path (recommended for scale):
- Provider: Render / Fly / Railway / DigitalOcean / AWS
- App: Containerize the Streamlit app (Docker) and run behind a reverse proxy. Set worker limits and process queues for heavy jobs.
- Storage: Use S3-compatible store for temporary uploads or direct to ephemeral disk but clean up frequently.
- Background processing: Use a job queue (RQ/Celery) if you expect concurrent heavy loads; otherwise, limit concurrency.
- Monitoring: Add basic metrics (uptime, error rates, invocation counts) and alerting.

Minimum environment variables to configure on host:
- GEMINI_API_KEY (if you provide a server key) — otherwise rely on BYO-key flow.
- SECRET_KEY / SESSION_COOKIE_SECRET
- STRIPE_API_KEY (if hosting billing)

## Launch & marketing (how to reach creators)

- Micro-influencers: Send 5–10 personalized outreach emails to small YouTube creators who make listicles or comic commentary videos. Offer them free hosted access in exchange for a demo or shoutout.
- Product Hunt: Launch a polished page with images and a short demo video showing the app producing a script from a comic.
- Reddit & communities: r/YouTubers, r/ComicBookCollabs, r/ContentCreators — be careful with self-promotion rules, prefer value-first posts.
- Twitter/X + Threads: Short video demos showing a 30s before/after.

Simple partnership idea
- Offer an affiliate or referral discount to creators who share your product (only after you have a stable flow and Stripe automation).

## Pricing examples (pick one and keep it stable)

- Source only: $39 one-time
- Hosted: $19/month — BYO-key required; includes support & updates
- Trial: 7-day free trial or 3 free runs

If you want to be more aggressive: $9/month limited usage, $29/month unlimited (but you must implement quotas to protect costs).

## Short-term launch checklist (order + quick estimated time)

1. Create `SELLING.md` & product assets (screenshots, 1-min demo video) — (1–2 days) — DONE (this file)
2. Create Gumroad product and list the repo zip with README — (1–2 hours)
3. Set up a simple landing page with Buy button (Gumroad link) — (2–4 hours)
4. Offer 3–5 free hosted spots (manual onboarding) and collect feedback — (1–2 weeks)
5. Automate hosted signup using Stripe Checkout + webhook and simple allowlist logic — (1–3 days)
6. Add BYO-key UI (minimal Streamlit change) and publish hosted instance — (1 day)
7. Publish a short blog post + reach out to 10 creators — (1–2 days)

## Next steps & priorities (developer roadmap)

1. Implement the BYO-key UI and a safe way to inject the key into agent configs (choose either quick option A or clean option B described above).
2. Add a small admin allowlist page for manual customer onboarding while you validate demand.
3. Add usage & quota logging so you can see how many runs are happening and whether you need a worker queue.
4. Add a minimal Terms/Privacy/Refund page and a basic help page (how to get Polaris/Gemini API key, how to use the tool legally).

## Final notes & risks

- Copyright risk: The app processes user-provided comic content. Make sure your TOS clearly states the user must own the rights or have permission. You are not a legal shield.
- AI billing risk: If you host and provide your own Gemini API key to pay calls, you are fully on the hook for AI costs — avoid this early unless you know how to meter and bill precisely.
- Abuse risk: Rate-limit file uploads and processing. Scan for obvious abuse patterns.

---

If you'd like, I can do any of the following next:

- Add the minimal BYO-key UI change to `streamlit_app.py` and wire it safely (small patch). I can use the quick approach (move import/instantiation after the key) or the clean approach (extend `MainCoordinator` API).
- Create a download bundle (zip) in the repo that is ready for Gumroad delivery (add LICENSE_FOR_SALE.md + install instructions).
- Implement a small manual onboarding page for the hosted app that allows you to add customer emails to an allowlist.

Tell me which next step you prefer and I will implement it (I can also apply the code patch now if you want the BYO-key flow implemented immediately).