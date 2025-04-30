import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Phishing Feature Visualizer", layout="wide")
st.markdown("<h1 style='text-align: center;'>🔍 Phishing Detection Data Exploration</h1>", unsafe_allow_html=True)
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("web-page-phishing.csv")

df = load_data()

# Fill missing values
cat_col = ['n_at', 'n_tilde', 'n_redirection']
for col in cat_col:
    df[col] = df[col].fillna(df[col].median())

# ---- Distribution Chart ----
st.subheader("🎯 Distribution of Phishing Labels")
col1, col2 = st.columns([3, 1])
with col1:
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.histplot(df['phishing'], color='crimson', stat='percent', ax=ax1)
    ax1.set_title('Phishing Label Distribution\n(0 = Legit, 1 = Phishing)')
    ax1.set_xlabel('Phishing Label')
    ax1.set_ylabel('Percentage')
    st.pyplot(fig1)
with col2:
    phishing_counts = df['phishing'].value_counts(normalize=True) * 100
    st.metric(label="Legit (%)", value=f"{phishing_counts[0]:.2f}%")
    st.metric(label="Phishing (%)", value=f"{phishing_counts[1]:.2f}%")

# Feature set
X = df[['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash',
        'n_questionmark', 'n_redirection']]

# Color mapping by feature
color_map = {
    'url_length': 'skyblue',
    'n_dots': 'olive',
    'n_hypens': 'coral',
    'n_underline': 'purple',
    'n_slash': 'limegreen',
    'n_questionmark': 'gold',
    'n_redirection': 'dodgerblue'
}

# ---- Interactive Dropdown ----
st.markdown("## 📊 Interactive Feature Visualizations")
dropdown_col, space_col = st.columns([2, 5])
with dropdown_col:
    selected_column = st.selectbox("Select Feature to Visualize:", X.columns.tolist())

selected_color = color_map.get(selected_column, 'steelblue')  # Default fallback color

# Top 10 All Data
st.markdown(f"#### 🔹 Top 10 `{selected_column}` Values (All Data)")
fig_all, ax_all = plt.subplots(figsize=(5, 3))
top10_all = df[selected_column].value_counts().nlargest(10).sort_index()
sns.barplot(x=top10_all.index, y=top10_all.values, color=selected_color, ax=ax_all)
ax_all.set_title(f"All Data: {selected_column}")
ax_all.set_xlabel(selected_column)
ax_all.set_ylabel("Count")
for i, v in enumerate(top10_all.values):
    ax_all.text(i, v + 0.5, str(v), ha='center', fontsize=8)
st.pyplot(fig_all)

# Top 10 Phishing Only
st.markdown(f"#### 🔺 Top 10 `{selected_column}` Values (Phishing Only)")
fig_phish, ax_phish = plt.subplots(figsize=(5, 3))
top10_phishing = df[df['phishing'] == 1][selected_column].value_counts().nlargest(10).sort_index()
sns.barplot(x=top10_phishing.index, y=top10_phishing.values, color=selected_color, ax=ax_phish)
ax_phish.set_title(f"Phishing Only: {selected_column}")
ax_phish.set_xlabel(selected_column)
ax_phish.set_ylabel("Count")
for i, v in enumerate(top10_phishing.values):
    ax_phish.text(i, v + 0.5, str(v), ha='center', fontsize=8)
st.pyplot(fig_phish)

st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
