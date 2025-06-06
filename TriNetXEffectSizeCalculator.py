import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

st.title("Novak's TriNetX Effect Size Calculator")
st.markdown("Calculate effect sizes from Risk Ratios, Odds Ratios, or Hazard Ratios (TriNetX outcomes).")

# --- Sidebar options ---
st.sidebar.header("🛠️ Table and Plot Options")
add_p = st.sidebar.checkbox("Add p-value column")
add_ci = st.sidebar.checkbox("Add confidence interval columns (for ratios and effect sizes)")
add_forest = st.sidebar.checkbox("Show forest plot of effect sizes")

if add_forest:
    st.sidebar.subheader("Forest Plot Settings")
    forest_title = st.sidebar.text_input("Plot Title", "Effect Size Forest Plot")
    dot_color = st.sidebar.color_picker("Dot Color", "#2a5599")
    error_color = st.sidebar.color_picker("Error Bar Color", "#666666")
    marker_size = st.sidebar.slider("Marker Size", 6, 30, 12)
    error_width = st.sidebar.slider("Error Bar Width", 1, 5, 2)
    show_hline = st.sidebar.checkbox("Show horizontal line at zero", True)
    label_fontsize = st.sidebar.slider("Outcome Label Font Size", 8, 20, 12)
    x_fontsize = st.sidebar.slider("X-axis Font Size", 8, 20, 12)
    fig_width = st.sidebar.slider("Figure Width", 4, 12, 6)
    fig_height = st.sidebar.slider("Figure Height", 3, 15, 4 + 1, help="Increase if you have many outcomes")
    x_min = st.sidebar.number_input("X-axis minimum", value=-1.0, step=0.1)
    x_max = st.sidebar.number_input("X-axis maximum", value=1.5, step=0.1)
    show_grid = st.sidebar.checkbox("Show Grid Lines", False)
    invert_y = st.sidebar.checkbox("Invert Y-axis", True)

# Editable Table for Input
columns = ['Outcome', 'Risk, Odds, or Hazard Ratio']
defaults = {"Outcome": [""], "Risk, Odds, or Hazard Ratio": [1.0]}
if add_ci:
    columns += ['Lower CI (Ratio)', 'Upper CI (Ratio)']
    defaults['Lower CI (Ratio)'] = [""]
    defaults['Upper CI (Ratio)'] = [""]
if add_p:
    columns += ['p-value']
    defaults['p-value'] = [""]

df = pd.DataFrame({col: defaults[col] for col in columns})

# Use st.data_editor with no dtype restrictions to allow any (pos/neg) values, and manually handle conversion
edited_df = st.data_editor(df, num_rows="dynamic", key="input_table")

# Compute effect size and (optionally) CIs
results_df = edited_df.copy()
results_df = results_df[results_df['Outcome'].astype(str).str.strip() != ""]
results_df['Risk, Odds, or Hazard Ratio'] = pd.to_numeric(results_df['Risk, Odds, or Hazard Ratio'], errors='coerce')
results_df['Effect Size'] = np.log(np.abs(results_df['Risk, Odds, or Hazard Ratio'])) * (np.sqrt(3) / np.pi) * np.sign(results_df['Risk, Odds, or Hazard Ratio'])

if add_ci:
    results_df['Lower CI (Ratio)'] = pd.to_numeric(results_df['Lower CI (Ratio)'], errors='coerce')
    results_df['Upper CI (Ratio)'] = pd.to_numeric(results_df['Upper CI (Ratio)'], errors='coerce')
    # CI for effect size is calculated by applying the formula to the CI bounds of the ratio
    # Use np.abs to ensure log works for negative or positive ratios, keep sign
    results_df['Lower CI (Effect Size)'] = np.log(np.abs(results_df['Lower CI (Ratio)'])) * (np.sqrt(3) / np.pi) * np.sign(results_df['Lower CI (Ratio)'])
    results_df['Upper CI (Effect Size)'] = np.log(np.abs(results_df['Upper CI (Ratio)'])) * (np.sqrt(3) / np.pi) * np.sign(results_df['Upper CI (Ratio)'])

if add_p:
    results_df['p-value'] = pd.to_numeric(results_df['p-value'], errors='coerce')

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
    components.html(ama_table_html(results_df.round(6), ci=add_ci, pval=add_p), height=350, scrolling=True)
else:
    st.info("Enter at least one Outcome and Ratio to see results.")

# Forest plot (if checked)
if add_forest and not results_df.empty:
    st.markdown("### Forest Plot of Effect Sizes")
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    y_pos = np.arange(len(results_df))
    effect = results_df['Effect Size']

    if add_ci and 'Lower CI (Effect Size)' in results_df.columns and 'Upper CI (Effect Size)' in results_df.columns:
        lower_err = (effect - results_df['Lower CI (Effect Size)']).clip(lower=0).fillna(0)
        upper_err = (results_df['Upper CI (Effect Size)'] - effect).clip(lower=0).fillna(0)
        xerr = [lower_err, upper_err]
    else:
        xerr = None

    ax.errorbar(
        effect,
        y_pos,
        xerr=xerr,
        fmt='o',
        color=dot_color,
        ecolor=error_color,
        capsize=5,
        markersize=marker_size,
        elinewidth=error_width,
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels(results_df['Outcome'], fontsize=label_fontsize)
    if show_hline:
        ax.axvline(0, color='grey', linestyle='--', lw=1)
    ax.set_xlabel('Effect Size', fontsize=x_fontsize)
    ax.set_ylabel('Outcome', fontsize=label_fontsize)
    ax.set_xlim(x_min, x_max)
    if invert_y:
        ax.invert_yaxis()
    if show_grid:
        ax.grid(axis='x', linestyle='--', alpha=0.7)
    ax.set_title(forest_title, fontsize=x_fontsize + 2)
    st.pyplot(fig)

st.markdown("---")
st.markdown(
    "**Citation for Original Study on Computing Effect Sizes from Odds Ratios:**  \n"
    "Chinn S. A simple method for converting an odds ratio to effect size for use in meta-analysis. "
    "Stat Med. 2000;19(22):3127-3131. "
    "[doi:10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m](https://doi.org/10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m), PMID: 11113947"
)
