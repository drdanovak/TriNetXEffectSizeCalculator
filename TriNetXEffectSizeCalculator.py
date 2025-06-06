import streamlit as st
import pandas as pd
import numpy as np

st.title("Novak's TriNetX Effect Size Calculator")
st.markdown("Calculate effect sizes from Risk Ratios, Odds Ratios, or Hazard Ratios (TriNetX outcomes).")

# Initialize editable DataFrame
df = pd.DataFrame({
    'Outcome': [""],
    'Risk, Odds, or Hazard Ratio': [1.0],
})

edited_df = st.data_editor(df, num_rows="dynamic")

# Calculate Effect Sizes
edited_df['Effect Size'] = np.log(edited_df['Risk, Odds, or Hazard Ratio']) * (np.sqrt(3) / np.pi)

# Display resulting DataFrame
st.markdown("### Calculated Effect Sizes")
st.dataframe(edited_df)

st.markdown("---")
st.markdown("**Citation for Original Study:**\n\nChinn S. A simple method for converting an odds ratio to effect size for use in meta-analysis. Stat Med. 2000;19(22):3127-3131. doi:10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m, PMID: 11113947")
