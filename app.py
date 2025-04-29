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
fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.histplot(df['phishing'], legend=True, color='Red', stat='percent', ax=ax1)
ax1.set_title('Distribution of Phishing Labels (0 = Legit, 1 = Phishing)', fontsize=16)
ax1.set_xlabel('Phishing Label', fontsize=12)
ax1.set_ylabel('Percentage', fontsize=12)
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
st.markdown(f"### 🔍 Top 10 Values for '{selected_column}' (All Data)")
top10_all = df[selected_column].value_counts().nlargest(10).sort_values()
fig_all, ax_all = plt.subplots(figsize=(8, 5))
sns.barplot(y=top10_all.index, x=top10_all.values, palette='Blues_d', ax=ax_all)
ax_all.set_title(f"Top 10 '{selected_column}' Values (All Data)", fontsize=16)
ax_all.set_xlabel("Frequency", fontsize=12)
ax_all.set_ylabel(selected_column, fontsize=12)
for i, v in enumerate(top10_all.values):
    ax_all.text(v + 0.5, i, str(v), color='black', va='center', fontsize=10)
st.pyplot(fig_all)

# Plot for phishing = 1
st.markdown(f"### 🛑 Top 10 Values for '{selected_column}' (Phishing Only)")
phishing_data = df[df['phishing'] == 1]
top10_phishing = phishing_data[selected_column].value_counts().nlargest(10).sort_values()
fig_phish, ax_phish = plt.subplots(figsize=(8, 5))
sns.barplot(y=top10_phishing.index, x=top10_phishing.values, palette='Reds_d', ax=ax_phish)
ax_phish.set_title(f"Top 10 '{selected_column}' Values (Phishing Only)", fontsize=16)
ax_phish.set_xlabel("Frequency", fontsize=12)
ax_phish.set_ylabel(selected_column, fontsize=12)
for i, v in enumerate(top10_phishing.values):
    ax_phish.text(v + 0.5, i, str(v), color='black', va='center', fontsize=10)
st.pyplot(fig_phish)
