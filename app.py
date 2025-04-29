import random

# Move dropdown to left-center
st.subheader("📊 Interactive Column Visualization")
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_column = st.selectbox("Select a column to visualize:", X.columns.tolist())

# Define dynamic color palette
color_palette_all = random.choice(['Purples_d', 'Blues_d', 'Greens_d'])
color_palette_phish = random.choice(['Reds_d', 'Oranges_d', 'pink'])

# Top 10 All Data
st.markdown(f"### 🔍 Top 10 Values for '{selected_column}' (All Data)")
top10_all = df[selected_column].value_counts().nlargest(10).sort_values()
fig_all, ax_all = plt.subplots(figsize=(6, 4))
sns.barplot(y=top10_all.index, x=top10_all.values, palette=color_palette_all, ax=ax_all)
ax_all.set_title(f"Top 10 '{selected_column}' Values (All Data)", fontsize=14)
ax_all.set_xlabel("Frequency", fontsize=11)
ax_all.set_ylabel(selected_column, fontsize=11)
for i, v in enumerate(top10_all.values):
    ax_all.text(v + 0.5, i, str(v), color='black', va='center', fontsize=9)
st.pyplot(fig_all)

# Top 10 Phishing Only
st.markdown(f"### 🛑 Top 10 Values for '{selected_column}' (Phishing Only)")
phishing_data = df[df['phishing'] == 1]
top10_phishing = phishing_data[selected_column].value_counts().nlargest(10).sort_values()
fig_phish, ax_phish = plt.subplots(figsize=(6, 4))
sns.barplot(y=top10_phishing.index, x=top10_phishing.values, palette=color_palette_phish, ax=ax_phish)
ax_phish.set_title(f"Top 10 '{selected_column}' Values (Phishing Only)", fontsize=14)
ax_phish.set_xlabel("Frequency", fontsize=11)
ax_phish.set_ylabel(selected_column, fontsize=11)
for i, v in enumerate(top10_phishing.values):
    ax_phish.text(v + 0.5, i, str(v), color='black', va='center', fontsize=9)
st.pyplot(fig_phish)
