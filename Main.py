# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud

# Improving Visualization
try:
    df = pd.read_csv("FRvideos.csv")
except FileNotFoundError:
    print("Error: File 'USvideos.csv' not found.")
    exit()

PLOT_COLORS = ["#268bd2", "#0052CC", "#FF5722", "#b58900", "#003f5c"]
pd.options.display.float_format = '{:.2f}'.format
sns.set(style="ticks")
plt.rcParams.update({
    'figure.figsize': (8, 5),
    'figure.dpi': 100,
    'axes.labelpad': 20,
    'axes.facecolor': "#ffffff",
    'axes.linewidth': 0.4,
    'axes.grid': True,
    'axes.labelsize': 14,
    'patch.linewidth': 0,
    'xtick.major.width': 0.2,
    'ytick.major.width': 0.2,
    'grid.color': '#9E9E9E',
    'grid.linewidth': 0.4,
    'font.family': 'Arial',
    'font.weight': '400',
    'font.size': 10,
    'text.color': '#282828',
    'savefig.pad_inches': 0.3,
    'savefig.dpi': 300
})

# Data Exploration
df["description"] = df["description"].fillna("")
print(df.describe())

# Data Visualization
def contains_capitalized_word(s):
    return any(w.isupper() for w in s.split())

df["contains_capitalized"] = df["title"].apply(contains_capitalized_word)

value_counts = df["contains_capitalized"].value_counts()
fig, ax = plt.subplots()
ax.pie(value_counts, labels=['No', 'Yes'], colors=['#003f5c', '#ffa600'],
       textprops={'color': '#040204'}, startangle=45, autopct='%1.1f%%')
ax.axis('equal')
ax.set_title('Title Contains Capitalized Word?')
plt.show()

df["title_length"] = df["title"].str.len()

fig, ax = plt.subplots()
sns.histplot(data=df, x="title_length", kde=False, color=PLOT_COLORS[4], ax=ax)
ax.set(xlabel="Title Length", ylabel="No. of videos", xticks=range(0, df["title_length"].max() + 10, 10))
plt.show()

fig, ax = plt.subplots()
ax.scatter(x=df['views'], y=df['title_length'], color=PLOT_COLORS[2], edgecolors="#000000", linewidths=0.5)
ax.set(xlabel="Views", ylabel="Title Length")
plt.show()

fig, ax = plt.subplots()
sns.boxplot(data=df, x="title_length", ax=ax)
ax.set(xlabel="Title Length", ylabel="No. of videos")
plt.show()

fig, ax = plt.subplots()
sns.countplot(data=df, x="contains_capitalized", ax=ax)
ax.set(xlabel="Contains Capitalized Word?", ylabel="No. of videos")
plt.show()

fig, ax = plt.subplots()
sns.barplot(data=df, x="contains_capitalized", y="views", ax=ax)
ax.set(xlabel="Contains Capitalized Word?", ylabel="Views")
plt.show()

# Correlation Analysis
numeric_columns = df.select_dtypes(include=['number', 'bool']).columns
h_labels = [x.replace('_', ' ').title() for x in numeric_columns]

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df[numeric_columns].corr(), annot=True, xticklabels=h_labels,
            yticklabels=h_labels, cmap=sns.cubehelix_palette(as_cmap=True), ax=ax)
plt.show()
