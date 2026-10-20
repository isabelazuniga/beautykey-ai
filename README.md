# BeautyKey AI — Web App

This is a Streamlit web app prototype for the BeautyKey AI IE Business School assignment. It includes a fictional demo dataset, a sales dashboard, a transparent opportunity-ranking heuristic, and rule-based commercial assistant examples.

## Deploy without installing Python
1. Upload `app.py`, `requirements.txt`, and this `README.md` to a GitHub repository.
2. In Streamlit Community Cloud, choose **Create app**, select the repository and `app.py`, then deploy.
3. Open the resulting web URL to use the app in a browser.

## Excel refresh
In the app sidebar, upload `BeautyKey_AI_Complete_Retail_Database.xlsx` and select **Account Targets**. The app reads account targets and aggregates sales from the **Current Sales** tab.

## Important limitations
- The demo data is fictional.
- The assistant is rule-based, not connected to a live LLM. A real model/API integration is a separate step and should use a securely stored secret, never a key committed to GitHub.
- Recommendations are decision support, not a validated forecast. Human review is required.
- No emails are sent, no CRM is updated, and no external data is retrieved automatically.
