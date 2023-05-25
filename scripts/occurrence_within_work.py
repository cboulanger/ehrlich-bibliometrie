# The code that follows was almost completely generated by GPT-4 following my prompts.

import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

# Function to extract the year from the book title
def extract_year(title):
    year = re.search(r'\((\d{4})\)', title)
    return int(year.group(1)) if year else None

def plot_occurrences(corpus_dir, regex_list):

    # Read the text files and store them in a DataFrame
    book_data = []

    for file in os.listdir(corpus_dir):
        if file.endswith('.txt'):
            with open(os.path.join(corpus_dir, file), 'r', encoding='utf-8') as f:
                text = f.read()
                book_data.append({'book_title': os.path.splitext(file)[0], 'text': text})

    books_df = pd.DataFrame(book_data)

    # Count the occurrences of each ngram in the books
    occurrences = {}

    for regex in regex_list:
        regex_occurrences = []
        for text in books_df['text']:
            regex_occurrences.append([m.start() / len(text) for m in re.finditer(regex, text)])
        occurrences[regex] = regex_occurrences

    # Extract years from book titles and sort the books by year
    books_df['year'] = books_df['book_title'].apply(extract_year)
    books_df = books_df.sort_values(by='year', ascending=False).reset_index(drop=True)

    # Create an array of ones to span the whole x-axis
    book_normalized_lengths = [1] * len(books_df)

    marker_shapes = ['o', 's', '^']  # dot, square, triangle (add more shapes as needed)
    marker_colors = ['red', 'blue', 'green']  # add more colors as needed

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 5), gridspec_kw={'width_ratios': [4, 1]})

    y = range(len(books_df))

    ax1.barh(y, book_normalized_lengths, color='lightgray', edgecolor='black', linewidth=1)

    for regex, shape, color, counts in zip(regex_list, marker_shapes, marker_colors, occurrences.values()):
        for i, positions in enumerate(counts):
            x_positions = [pos * book_normalized_lengths[i] for pos in positions]
            ax1.scatter(x_positions, [i] * len(x_positions), marker=shape, label=regex, color=color, edgecolors=color, s=50)
            #ax1.annotate("context", (i, x_positions, [i] * len(x_positions)), textcoords="offset points", xytext=(-20, 0), ha='center', fontsize=8, visible=False)

    ax1.set_yticks(y)
    ax1.set_yticklabels(books_df['book_title'])
    ax1.set_xlabel('Normalized text length')
    ax1.set_ylabel('Books (sorted by year)')
    ax1.grid(axis='x')

    # # Enable mplcursors for hover interactivity
    # cursor = mplcursors.cursor(ax1, hover=True)
    #
    # # Display context when hovering over the marker
    # @cursor.connect("add")
    # def on_add(sel):
    #     sel.annotation.set_visible(True)
    #     sel.annotation.draggable()
    #     sel.annotation.set_text(sel.annotation)
    #
    # @cursor.connect("remove")
    # def on_remove(sel):
    #     sel.annotation.set_visible(False)

    # Create a custom legend
    legend_handles = [plt.scatter([], [], marker=shape, label=' '.join(ngram), color=color, edgecolors='black', s=50) for ngram, shape, color in zip(regex_list, marker_shapes, marker_colors)]
    ax1.legend(handles=legend_handles, loc='upper center')

    # Create a bar chart to visualize the number of occurrences
    ngram_counts = np.array([[len(positions) for positions in count_list] for count_list in occurrences.values()]).T
    bar_width = 0.8 / len(regex_list)

    for idx, (ngram, color) in enumerate(zip(regex_list, marker_colors)):
        ax2.barh(np.array(y) + idx * bar_width, ngram_counts[:, idx], height=bar_width, label=ngram, color=color)

    ax2.set_yticks([])
    ax2.set_xlabel('Number of occurrences')
    ax2.grid(axis='x')

    plt.tight_layout()
    return plt