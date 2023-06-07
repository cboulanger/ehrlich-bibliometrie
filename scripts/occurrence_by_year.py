# The code that follows was almost completely generated by GPT-4 following my prompts.

import re
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from scripts.utils import truncate

def save_occurrences(articles_df, regex_list, file):
    # create a copy of the dataframe
    df = articles_df[['author','year','title','doi']]
    # Find the occurrences of each regex in the text files
    for regex in regex_list:
        regex_occurrences = []
        for text in articles_df['text']:
            regex_occurrences.append(len(re.findall(regex, text)))
        df[regex] = regex_occurrences
    df = df[~(df[regex_list] == 0).all(axis=1)]
    df.to_excel(file, index=False)

def plot_occurrences(articles_df, regex_list, first_year=None, last_year=None):

    # Find the occurrences of each regex in the text files
    for regex in regex_list:
        regex_occurrences = []
        for text in articles_df['text']:
            regex_occurrences.append(len(re.findall(regex, text)))
        articles_df[regex] = regex_occurrences

    # Group the occurrences by year
    grouped_occurrences = articles_df.groupby('year').agg({regex: sum for regex in regex_list})

    # Find the article with the most occurrences of the first regex in each year
    first_regex = regex_list[0]
    top_articles = articles_df.loc[articles_df.groupby('year')[first_regex].idxmax()]
    top_articles = top_articles.loc[top_articles[first_regex] > 0]
    if first_year is not None:
        top_articles = top_articles.loc[top_articles['year'] >= first_year]
    if last_year is not None:
        top_articles = top_articles.loc[top_articles['year'] <= last_year]
    top_articles = top_articles.reset_index(drop=True)



    years = grouped_occurrences.index
    n_years = len(years)
    bar_width = 0.8 / len(regex_list)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6), gridspec_kw={'width_ratios': [3, 1]})

    for idx, regex in enumerate(regex_list):
        x = np.arange(n_years) + idx * bar_width
        y = grouped_occurrences[regex]
        ax1.bar(x, y, width=bar_width, label=regex, color=plt.cm.Dark2(idx))
        # add number on top of bar chart
        if idx == 0:
            for i, v in enumerate(grouped_occurrences[regex]):
                ax1.text(i - 0.25, v + 0.25, str(v), fontsize=9)

    ax1.set_xticks(np.arange(n_years))
    ax1.set_xticklabels(years)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(base=5))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(base=1))
    ax1.grid(axis='x', which='minor', linestyle=':', alpha=0.5)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Occurrences of search terms')
    ax1.legend()

    # Create the box with the numbered list of top articles
    top_articles_list = [
        f'{i+1}. {row["author"]} ({row["year"]}) {truncate(row["title"], 30)} [{row[first_regex]}]'
        for i, row in top_articles.iterrows()
    ]
    ax2.axis('off')
    for i, text in enumerate(top_articles_list):
        ax2.text(0, 1 - i * 0.05, text, fontsize=10, verticalalignment='top')

    plt.tight_layout()
    return plt
