import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('ideal_many_populaitons.csv')

# Get unique class names
classes = df['class'].unique()
plt.rcParams['figure.dpi'] = 300

for c in classes:
    class_df = df[df['class'] == c]

    # Example data
    x = class_df['population']
    y = class_df['gen_mean']
    errors = class_df['gen_error']

    # Plot with error bars
    plt.figure(figsize=(10, 6))
    plt.errorbar(x, y, yerr=errors, fmt='o', color='blue', ecolor='red', capsize=5, label='Data with Error Bars')

    # Set labels and title
    plt.title('Population size and Number of generations for ' + c)
    plt.xlabel('Mean Generations')
    plt.ylabel('Population Size')
    plt.grid(True)

    # Add legend
    # plt.legend()

    # Show plot
    plt.tight_layout()
    plt.show()
