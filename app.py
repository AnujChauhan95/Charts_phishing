import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

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

# Define features and target
X = df[['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash',
        'n_questionmark', 'n_redirection']]
Y = df['phishing']

# 📊 Interactive Dropdown Visualization
st.subheader("📊 Interactive Column Visualization")
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_column = st.selectbox("Select a column to visualize:", X.columns.tolist())

# Random color palettes
color_palette_all = random.choice(['Purples_d', 'Blues_d', 'Greens_d'])
color_palette_phish = random.choice(['Reds_d', 'Oranges_d', 'pink'])

# Distribution of Phishing Labels
st.subheader("Distribution of Phishing Labels")
fig1, ax1 = plt.subplots(figsize=(7, 4))
sns.histplot(df['phishing'], legend=True, color='Red', stat='percent', ax=ax1)
ax1.set_title('Distribution of Phishing Labels (0 = Legit, 1 = Phishing)', fontsize=14)
ax1.set_xlabel('Phishing Label', fontsize=11)
ax1.set_ylabel('Percentage', fontsize=11)
st.pyplot(fig1)

# 🔍 Chart for All Data
st.markdown(f"### 🔍 Top 10 Values for '{selected_column}' (All Data)")
top10_all = df[selected_column].value_counts().nlargest(10).sort_values()

if top10_all.empty:
    st.warning("No data available to display.")
else:
    fig_all, ax_all = plt.subplots(figsize=(6, 4))
    sns.barplot(y=top10_all.index, x=top10_all.values, palette=color_palette_all, ax=ax_all)
    ax_all.set_title(f"Top 10 '{selected_column}' Values (All Data)", fontsize=14)
    ax_all.set_xlabel("Frequency", fontsize=11)
    ax_all.set_ylabel(selected_column, fontsize=11)
    for i, v in enumerate(top10_all.values):
        ax_all.text(v + 0.5, i, str(v), color='black', va='center', fontsize=9)
    st.pyplot(fig_all)

# 🛑 Chart for Phishing Only
st.markdown(f"### 🛑 Top 10 Values for '{selected_column}' (Phishing Only)")
phishing_data = df[df['phishing'] == 1]
top10_phishing = phishing_data[selected_column].value_counts().nlargest(10).sort_values()

if top10_phishing.empty:
    st.warning("No phishing data available for the selected column.")
else:
    fig_phish, ax_phish = plt.subplots(figsize=(6, 4))
    sns.barplot(y=top10_phishing.index, x=top10_phishing.values, palette=color_palette_phish, ax=ax_phish)
    ax_phish.set_title(f"Top 10 '{selected_column}' Values (Phishing Only)", fontsize=14)
    ax_phish.set_xlabel("Frequency", fontsize=11)
    ax_phish.set_ylabel(selected_column, fontsize=11)
    for i, v in enumerate(top10_phishing.values):
        ax_phish.text(v + 0.5, i, str(v), color='black', va='center', fontsize=9)
    st.pyplot(fig_phish)
