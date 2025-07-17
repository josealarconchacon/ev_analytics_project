import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar(df, x, y, title, filename):
    sns.barplot(data=df, x=x, y=y)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"output/{filename}")
    plt.clf()

def plot_line(df, x, y, title, filename):
    df.plot(x=x, y=y, kind='line', marker='o', title=title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"output/{filename}")
    plt.clf()
