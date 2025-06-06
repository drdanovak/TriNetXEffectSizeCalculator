import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

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
results_df = results_df[results_df['Outcome'].astype(str).str.strip() != ""]  # only non-empty rows
results_df['Effect Size'] = np.log(results_df['Risk, Odds, or Hazard Ratio']) * (np.sqrt(3) / np.pi)

st.markdown("### Calculated Effect Sizes Table")
st.dataframe(results_df, use_container_width=True)

# HTML Table for copying
def to_html_table(df):
    html = "<table border='1' style='border-collapse:collapse;'>"
    html += "<tr>" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr>"
    for _, row in df.iterrows():
        html += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
    html += "</table>"
    return html

if not results_df.empty:
    html_table = to_html_table(results_df.round(4))
    st.markdown("#### Copy This Table (works great in Word):")
    components.html(f'''
        <button onclick="navigator.clipboard.writeText(document.getElementById('copytable').outerHTML);alert('✅ Table copied to clipboard! Paste into Word.')">
            📋 Copy Table to Clipboard
        </button>
        <div id="copytable">{html_table}</div>
    ''', height=250)

st.markdown("---")
st.markdown(
    "**Citation for Original Study:**  \n"
    "Chinn S. A simple method for converting an odds ratio to effect size for use in meta-analysis. "
    "Stat Med. 2000;19(22):3127-3131. "
    "[doi:10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m](https://doi.org/10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m), PMID: 11113947"
)
