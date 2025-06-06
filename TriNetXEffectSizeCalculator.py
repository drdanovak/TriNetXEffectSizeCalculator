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
results_df = results_df[results_df['Outcome'].astype(str).str.strip() != ""]  # only non-empty rows
results_df['Effect Size'] = np.log(results_df['Risk, Odds, or Hazard Ratio']) * (np.sqrt(3) / np.pi)

st.markdown("### Calculated Effect Sizes Table")
if not results_df.empty:
    st.table(results_df.round(4).reset_index(drop=True))  # <--- index removed here
else:
    st.info("Enter at least one Outcome and Ratio to see results.")

st.markdown("---")
st.markdown(
    "**Citation for Original Study on Computing Effect Sizes from Odds Ratios:**  \n"
    "Chinn S. A simple method for converting an odds ratio to effect size for use in meta-analysis. "
    "Stat Med. 2000;19(22):3127-3131. "
    "[doi:10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m](https://doi.org/10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m), PMID: 11113947"
)
