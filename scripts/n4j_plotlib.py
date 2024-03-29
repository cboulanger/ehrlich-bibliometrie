from matplotlib import pyplot as plt

def limit_string(s, max_length):
    if len(s) <= max_length:
        return s
    else:
        return s[:max_length] + "..."

def plot_year_citations(data, dep_col, x_label = None, y_label=None, file=None, dpi=300, color="darkblue"):
    years = [d['year'] for d in data]
    dep_var = [limit_string(d[dep_col], 50) for d in data]
    citation_counts = [d['citations'] for d in data]

    # Create plot
    fig, ax = plt.subplots()

    # Set the x and y axis labels
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Scatter plot with citation counts as size
    ax.scatter(years, dep_var, s=citation_counts, color=color)

    # Connect the earliest and last point of each observed variable with a line
    #for dep_v in set(dep_var):
    #    dep_data = [(d['year'], d[dep_col]) for d in data if d[dep_col] == dep_v]
    #    dep_data.sort()
    #    ax.plot(*zip(*dep_data), color='grey', linewidth=0.5)

    # Save
    if file is not None:
        plt.savefig(file, bbox_inches="tight", dpi=dpi)

    # Show the plot
    return plt.show()

