
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

st.subheader("Sample Data")
st.dataframe(df.head())

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

# Prepare features
X = df.loc[:, ['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash',
               'n_questionmark', 'n_redirection']]
Y = df['phishing']

# Function to plot top 10 histograms
def plot_top10_histograms(data, color='skyblue'):
    for column in data.columns:
        top10 = data[column].value_counts().nlargest(10).sort_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=top10.index, y=top10.values, color=color, ax=ax)
        ax.set_title(f'Top 10 Frequency Values of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

st.subheader("Top 10 Value Frequencies for Each Feature")
plot_top10_histograms(X, color='purple')

# Function to plot top 10 phishing-only histograms
def plot_top10_for_phishing_only(X, Y, color='red'):
    phishing_data = X[Y == 1]
    for column in phishing_data.columns:
        top10 = phishing_data[column].value_counts().nlargest(10).sort_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=top10.index, y=top10.values, color=color, ax=ax)
        ax.set_title(f'Top 10 {column} values (phishing = 1)')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

st.subheader("Top 10 Values for Features (Phishing Only)")
plot_top10_for_phishing_only(X, Y)
