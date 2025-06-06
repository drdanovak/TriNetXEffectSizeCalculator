import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

st.title("Novak's TriNetX Effect Size Calculator")
st.markdown("Calculate effect sizes from Risk Ratios, Odds Ratios, or Hazard Ratios (TriNetX outcomes).")

# Feature selection
add_p = st.checkbox("Add p-value column")
add_ci = st.checkbox("Add confidence interval columns (for ratios and effect sizes)")
add_forest = st.checkbox("Show forest plot of effect sizes")

# Editable Table for Input
columns = ['Outcome', 'Risk, Odds, or Hazard Ratio']
if add_ci:
    columns += ['Lower CI (Ratio)', 'Upper CI (Ratio)']
if add_p:
    columns += ['p-value']
df = pd.DataFrame({col: [""] if 'Outcome' in col else [1.0] for col in columns})
edited_df = st.data_editor(df, num_rows="dynamic", key="input_table")

# Compute effect size and (optionally) CIs
results_df = edited_df.copy()
results_df = results_df[results_df['Outcome'].astype(str).str.strip() != ""]
results_df['Risk, Odds, or Hazard Ratio'] = pd.to_numeric(results_df['Risk, Odds, or Hazard Ratio'], errors='coerce')
results_df['Effect Size'] = np.log(results_df['Risk, Odds, or Hazard Ratio']) * (np.sqrt(3) / np.pi)

if add_ci:
    results_df['Lower CI (Ratio)'] = pd.to_numeric(results_df['Lower CI (Ratio)'], errors='coerce')
    results_df['Upper CI (Ratio)'] = pd.to_numeric(results_df['Upper CI (Ratio)'], errors='coerce')
    # CI for effect size is calculated by applying the formula to the CI bounds of the ratio
    results_df['Lower CI (Effect Size)'] = np.log(results_df['Lower CI (Ratio)']) * (np.sqrt(3) / np.pi)
    results_df['Upper CI (Effect Size)'] = np.log(results_df['Upper CI (Ratio)']) * (np.sqrt(3) / np.pi)

# Table display
def ama_table_html(df, ci=False, pval=False):
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
            <th>Risk, Odds, or Hazard Ratio</th>"""
    if ci:
        html += "<th>Lower CI (Ratio)</th><th>Upper CI (Ratio)</th>"
    html += "<th>Effect Size</th>"
    if ci:
        html += "<th>Lower CI (Effect Size)</th><th>Upper CI (Effect Size)</th>"
    if pval:
        html += "<th>p-value</th>"
    html += "</tr>"
    for _, row in df.iterrows():
        html += f"<tr><td class='left'>{row['Outcome']}</td><td>{row['Risk, Odds, or Hazard Ratio']}</td>"
        if ci:
            html += f"<td>{row.get('Lower CI (Ratio)','')}</td><td>{row.get('Upper CI (Ratio)','')}</td>"
        html += f"<td>{row['Effect Size']}</td>"
        if ci:
            html += f"<td>{row.get('Lower CI (Effect Size)','')}</td><td>{row.get('Upper CI (Effect Size)','')}</td>"
        if pval:
            html += f"<td>{row.get('p-value','')}</td>"
        html += "</tr>"
    html += "</table>"
    return html

st.markdown("### Calculated Effect Sizes Table")
if not results_df.empty:
    components.html(ama_table_html(results_df.round(4), ci=add_ci, pval=add_p), height=350, scrolling=True)
else:
    st.info("Enter at least one Outcome and Ratio to see results.")

# Forest plot (if checked)
if add_forest and not results_df.empty:
    st.markdown("### Forest Plot of Effect Sizes")
    fig, ax = plt.subplots(figsize=(6, max(1.5, 0.6 * len(results_df))))
    y_pos = np.arange(len(results_df))
    ax.errorbar(
        results_df['Effect Size'],
        y_pos,
        xerr=[
            results_df['Effect Size'] - results_df.get('Lower CI (Effect Size)', results_df['Effect Size']),
            results_df.get('Upper CI (Effect Size)', results_df['Effect Size']) - results_df['Effect Size']
        ] if add_ci else None,
        fmt='o',
        color='black',
        capsize=5,
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels(results_df['Outcome'])
    ax.axvline(0, color='grey', linestyle='--', lw=1)
    ax.set_xlabel('Effect Size')
    ax.set_ylabel('Outcome')
    plt.gca().invert_yaxis()
    st.pyplot(fig)

st.markdown("---")
st.markdown(
    "**Citation for Original Study on Computing Effect Sizes from Odds Ratios:**  \n"
    "Chinn S. A simple method for converting an odds ratio to effect size for use in meta-analysis. "
    "Stat Med. 2000;19(22):3127-3131. "
    "[doi:10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m](https://doi.org/10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m), PMID: 11113947"
)
