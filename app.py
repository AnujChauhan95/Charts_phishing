
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Phishing Feature Analysis", layout="wide")
st.title("Phishing Detection Data Exploration")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("web-page-phishing.csv")

df = load_data()

# Fill missing values
cat_col = ['n_at', 'n_tilde', 'n_redirection']
for col in cat_col:
    df[col] = df[col].fillna(df[col].median())


# Distribution of Phishing Labels
st.subheader("Distribution of Phishing Labels")
fig1, ax1 = plt.subplots()
sns.histplot(df['phishing'], legend=True, color='Red', stat='percent', ax=ax1)
ax1.set_title('Distribution of Phishing Labels (0 = Legit, 1 = Phishing)')
st.pyplot(fig1)

# Define features and target
X = df[['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash',
        'n_questionmark', 'n_redirection']]
Y = df['phishing']

# Interactive dropdown for column selection
st.subheader("Interactive Column Visualization")

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
