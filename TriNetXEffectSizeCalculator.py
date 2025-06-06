import streamlit as st
import pandas as pd
import numpy as np

st.title("Novak's TriNetX Effect Size Calculator")
st.markdown("Calculate effect sizes from Risk Ratios, Odds Ratios, or Hazard Ratios (TriNetX outcomes).")

# Editable Table for Input
df = pd.DataFrame({
    'Outcome': [""],
    'Risk, Odds, or Hazard Ratio': [1.0],
})
edited_df = st.data_editor(df, num_rows="dynamic", key="input_table")

# Compute Effect Size only for filled rows
results_df = edited_df.copy()
results_df = results_df[results_df['Outcome'].astype(str).str.strip() != ""]
results_df['Effect Size'] = np.log(results_df['Risk, Odds, or Hazard Ratio']) * (np.sqrt(3) / np.pi)
results_df = results_df.round(4)

def ama_table_html(df):
    if df.empty:
        return ""
    html = """
    <style>
    .ama-table { border-collapse:collapse; font-family:Arial,sans-serif; font-size:14px; }
    .ama-table th, .ama-table td { border:1px solid #222; padding:6px 12px; }
    .ama-table th { background:#f8f8f8; font-weight:bold; text-align:center; }
    .ama-table td { text-align:right; }
    .ama-table td.left { text-align:left; }
    </style>
    <table class="ama-table">
        <tr>
            <th>Outcome</th>
            <th>Risk, Odds, or Hazard Ratio</th>
            <th>Effect Size</th>
        </tr>
    """
    for _, row in df.iterrows():
        html += f"""
        <tr>
            <td class="left">{row['Outcome']}</td>
            <td>{row['Risk, Odds, or Hazard Ratio']}</td>
            <td>{row['Effect Size']}</td>
        </tr>
        """
    html += "</table>"
    return html

st.markdown("### Calculated Effect Sizes Table")
if not results_df.empty:
    st.markdown(ama_table_html(results_df), unsafe_allow_html=True)
else:
    st.info("Enter at least one Outcome and Ratio to see results.")

st.markdown("---")
st.markdown(
    "**Citation for Original Study on Computing Effect Sizes from Odds Ratios:**  \n"
    "Chinn S. A simple method for converting an odds ratio to effect size for use in meta-analysis. "
    "Stat Med. 2000;19(22):3127-3131. "
    "[doi:10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m](https://doi.org/10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m), PMID: 11113947"
)
