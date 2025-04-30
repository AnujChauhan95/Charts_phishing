import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page setup
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

# Feature set
X = df[['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash',
        'n_questionmark', 'n_redirection']]

# Color mapping for dynamic charts
color_map = {
    'url_length': 'skyblue',
    'n_dots': 'olive',
    'n_hypens': 'coral',
    'n_underline': 'purple',
    'n_slash': 'limegreen',
    'n_questionmark': 'gold',
    'n_redirection': 'dodgerblue'
}

# --- TABS ---
eda_tab1, eda_tab2 = st.tabs(["📌 Dataset Summary", "📊  Visualizations"])

# --- Dataset Summary Tab ---
with eda_tab1:
    st.write("### Dataset Preview")
    st.dataframe(df.head())

    st.write("### Dataset Shape")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    st.write("### Data Types")
    st.write(df.dtypes)

    st.write("### Descriptive Statistics")
    st.dataframe(df.describe())

    st.write("### Correlation Heatmap")
    fig_corr, ax_corr = plt.subplots(figsize=(5, 4))
    sns.heatmap(df.corr(numeric_only=True), fmt=".2f", cmap="coolwarm", ax=ax_corr)
    st.pyplot(fig_corr)

# ---  Visualization Tab ---


    # ---- Distribution Chart ----
    with eda_tab2:
     st.subheader("🎯 Distribution of Phishing Labels")
     col1, col2 = st.columns([3, 1])
      with col1:
        fig1, ax1 = plt.subplots(figsize=(4, 2.5))
        sns.histplot(df['phishing'], color='crimson', stat='percent', ax=ax1)
        ax1.set_title('Phishing Label Distribution\n(0 = Legit, 1 = Phishing)', fontsize=10)
        ax1.set_xlabel('Label', fontsize=8)
        ax1.set_ylabel('%', fontsize=8)
        ax1.tick_params(axis='both', labelsize=7)
        st.pyplot(fig1)
     with col2:
        phishing_counts = df['phishing'].value_counts(normalize=True) * 100
        st.metric(label="Legit (%)", value=f"{phishing_counts[0]:.2f}%")
        st.metric(label="Phishing (%)", value=f"{phishing_counts[1]:.2f}%")

    # ---- Dropdown and Interactive Visuals ----
    st.markdown("## 📊 Interactive Feature Visualizations")
    dropdown_col, space_col = st.columns([2, 5])
    with dropdown_col:
        selected_column = st.selectbox("Select Feature to Visualize:", X.columns.tolist())

    selected_color = color_map.get(selected_column, 'steelblue')

    # Top 10 All Data
    st.markdown(f"#### 🔹 Top 10 `{selected_column}` Values (All Data)")
    fig_all, ax_all = plt.subplots(figsize=(4, 2.5))
    top10_all = df[selected_column].value_counts().nlargest(10).sort_index()
    sns.barplot(x=top10_all.index, y=top10_all.values, color=selected_color, ax=ax_all)
    ax_all.set_title(f"All Data: {selected_column}", fontsize=10)
    ax_all.set_xlabel(selected_column, fontsize=8)
    ax_all.set_ylabel("Count", fontsize=8)
    ax_all.tick_params(axis='both', labelsize=7)
    for i, v in enumerate(top10_all.values):
        ax_all.text(i, v + 0.2, str(v), ha='center', fontsize=7)
    st.pyplot(fig_all)

    # Top 10 Phishing Only
    st.markdown(f"#### 🔺 Top 10 `{selected_column}` Values (Phishing Only)")
    fig_phish, ax_phish = plt.subplots(figsize=(4, 2.5))
    top10_phishing = df[df['phishing'] == 1][selected_column].value_counts().nlargest(10).sort_index()
    sns.barplot(x=top10_phishing.index, y=top10_phishing.values, color=selected_color, ax=ax_phish)
    ax_phish.set_title(f"Phishing Only: {selected_column}", fontsize=10)
    ax_phish.set_xlabel(selected_column, fontsize=8)
    ax_phish.set_ylabel("Count", fontsize=8)
    ax_phish.tick_params(axis='both', labelsize=7)
    for i, v in enumerate(top10_phishing.values):
        ax_phish.text(i, v + 0.2, str(v), ha='center', fontsize=7)
    st.pyplot(fig_phish)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
