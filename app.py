
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.subheader("Interactive Column Visualization")

# List of features to choose from
columns = X.columns.tolist()
selected_column = st.selectbox("Select a column to visualize:", columns)

# Plot for all data
st.markdown(f"### Top 10 Values for '{selected_column}' (All Data)")
top10_all = df[selected_column].value_counts().nlargest(10).sort_index()
fig_all, ax_all = plt.subplots(figsize=(6, 4))
sns.barplot(x=top10_all.index, y=top10_all.values, color='purple', ax=ax_all)
ax_all.set_title(f'Top 10 Frequency Values of {selected_column}')
ax_all.set_xlabel(selected_column)
ax_all.set_ylabel('Frequency')
st.pyplot(fig_all)

# Plot for phishing = 1
st.markdown(f"### Top 10 Values for '{selected_column}' (Phishing Only)")
phishing_data = df[df['phishing'] == 1]
top10_phishing = phishing_data[selected_column].value_counts().nlargest(10).sort_index()
fig_phish, ax_phish = plt.subplots(figsize=(6, 4))
sns.barplot(x=top10_phishing.index, y=top10_phishing.values, color='red', ax=ax_phish)
ax_phish.set_title(f'Top 10 {selected_column} values (phishing = 1)')
ax_phish.set_xlabel(selected_column)
ax_phish.set_ylabel('Frequency')
st.pyplot(fig_phish)
