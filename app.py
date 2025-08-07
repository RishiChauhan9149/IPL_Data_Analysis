import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="IPL Dashboard", layout="wide")
st.title("🏏 IPL Data Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("matches.csv")
    return df

df = load_data()

# Validate essential columns
required_columns = ['Season', 'team1', 'team2', 'winner', 'toss_decision', 'venue']
missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Missing required columns in dataset: {', '.join(missing)}")
    st.stop()

# Sidebar options
st.sidebar.header("Filter Options")
seasons = sorted(df['Season'].dropna().unique())
selected_season = st.sidebar.multiselect("Select Season(s):", seasons, default=seasons)

filtered_df = df[df['Season'].isin(selected_season)]

# Overview
st.subheader("📊 Overview Stats")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", filtered_df.shape[0])
col2.metric("Total Teams", len(pd.unique(filtered_df['team1'].dropna().tolist() + filtered_df['team2'].dropna().tolist())))
col3.metric("Unique Winners", filtered_df['winner'].nunique())
col4.metric("Total Venues", filtered_df['venue'].nunique())

# Yearly wins
st.subheader("🏆 Wins by Team Over the Years")
team_wins = filtered_df[['Season', 'winner']].dropna()
wins = team_wins.groupby(['Season', 'winner']).size().unstack(fill_value=0)

fig1, ax1 = plt.subplots(figsize=(14, 6))
wins.plot(kind='bar', stacked=True, ax=ax1)
ax1.set_title("Year-wise team Wins")
ax1.set_xlabel("Season")
ax1.set_ylabel("Wins")
ax1.set_xticklabels(wins.index, rotation=45)
ax1.legend(title='winner',bbox_to_anchor=(1.02, 1),loc='upper left', borderaxespad=0.)
plt.xticks(rotation=45)
st.pyplot(fig1)

# Toss Decision Analysis
st.subheader("🪙 Toss Decision Insights")
toss_df = filtered_df.groupby(['toss_decision']).size()

fig2, ax2 = plt.subplots()
toss_df.plot.pie(autopct='%1.1f%%', ax=ax2, startangle=90)
plt.title("Toss Decision Distribution")
ax2.axis('equal')
st.pyplot(fig2)

# Most Winning Teams
st.subheader("🥇 Overall Most Winning Teams")
team_win_count = filtered_df['winner'].value_counts()

fig3, ax3 = plt.subplots()
sns.barplot(x=team_win_count.values, y=team_win_count.index, ax=ax3)
plt.title("Total Wins by Team")
plt.xlabel("Wins")
plt.ylabel("Teams")
st.pyplot(fig3)

# Match Venues
st.subheader("🏟️ Matches Played at Top Venues")
venue_count = filtered_df['venue'].value_counts().head(10)

fig4, ax4 = plt.subplots()
sns.barplot(x=venue_count.values, y=venue_count.index, ax=ax4)
plt.title("Top 10 Match Venues")
plt.xlabel("Matches Played")
plt.ylabel("Venue")
st.pyplot(fig4)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | IPL Dataset via Kaggle")

