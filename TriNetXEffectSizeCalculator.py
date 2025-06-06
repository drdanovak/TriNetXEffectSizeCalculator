import streamlit as st
import numpy as np

st.title("Effect Size Calculator")
st.markdown("Calculate effect size from Risk Ratio, Odds Ratio, or Hazard Ratio (TriNetX outcomes).")

# Input section
ratio_type = st.selectbox("Select Ratio Type", ["Risk Ratio", "Odds Ratio", "Hazard Ratio"])
ratio_value = st.number_input(f"Enter the {ratio_type}", min_value=0.0001, value=1.0, step=0.01)

# Calculate effect size
effect_size = np.log(ratio_value) * (np.sqrt(3) / np.pi)

# Display results
st.markdown("---")
st.write(f"### Effect Size: {effect_size:.4f}")
