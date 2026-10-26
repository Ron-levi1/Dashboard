# Clinical Research Dashboard

An interactive BI dashboard developed using **Python and Streamlit** to support the monitoring, analysis, and visualization of clinical research activities.

The dashboard provides an overview of research performance, financial metrics, and participant recruitment, enabling data-driven insights through an intuitive Hebrew interface.

### Live Dashboard

[Launch the Dashboard](https://dashboard-pfvrldtw8b3qnrpv8gotay.streamlit.app/)

## Key Features

- **Hospital Overview:** Consolidated research activity and key performance indicators (KPIs).
- **Departments, Investigators & Sponsors:** Interactive filtering, comparisons, and performance analysis.
- **Budget Monitoring:** Budget utilization, financial status, and identification of potential deviations.
- **Recruitment Tracking:** Participant recruitment progress and performance indicators.
- **Investigator Reports:** Detailed study-level information and investigator-specific summaries.
- **Financial Tracking:** Monitoring and analysis of research expenses and revenues.
- **Data Visualization:** Interactive charts, tables, and Excel export capabilities.

## Technologies

- Python
- Streamlit
- Pandas & NumPy
- Plotly
- Excel

## Getting Started

**Option 1: Online Access**

Open the [live dashboard](https://dashboard-pfvrldtw8b3qnrpv8gotay.streamlit.app/) and upload an Excel file containing the required research data.

A sample file with synthetic data is provided for demonstration purposes.

**Option 2: Local Installation**

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

- `app.py` – Main application, data processing, and dashboard components.
- `requirements.txt` – Python dependencies.
- `sample_dashboard_data.xlsx` – Synthetic dataset for demonstration and testing.

## Data & Privacy

The dashboard currently operates through manual Excel uploads and does not connect directly to hospital information systems.

The sample dataset contains synthetic information only. Sensitive clinical or organizational data should not be uploaded to public deployments without appropriate authorization.
