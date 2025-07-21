import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar(df, x, y, title, filename):
    sns.barplot(data=df, x=x, y=y, hue=x, palette="Blues_d", legend=False)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"output/{filename}")
    plt.clf()


def plot_line(df, x, y, title, filename):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=x, y=y, marker="o")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"output/{filename}")
    plt.clf()
