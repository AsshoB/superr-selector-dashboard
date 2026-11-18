# SupeRR Selector Season 2 — Round 1 Dashboard

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy publicly with Streamlit Community Cloud

1. Create/sign in to a GitHub account.
2. Create a new **public** repository (for example `superr-selector-dashboard`).
3. Upload `app.py`, `requirements.txt`, and the complete `data/` folder, preserving the folder structure.
4. Open https://share.streamlit.io/ and connect GitHub.
5. Choose the repository, branch `main`, and main file path `app.py`.
6. Click **Deploy**. Streamlit will provide a public `*.streamlit.app` URL.
7. Open the URL in an incognito window to verify it is publicly accessible before submitting it.

## Data note

The two CSVs are the strong-opposition Top 10 exports from the analysis. The dashboard displays their supplied metrics and scores. It does not recompute the underlying ball-by-ball model. The agreed evaluation weights are displayed separately from the exported composite scores to avoid implying that they were recalculated from those weights in this app.
