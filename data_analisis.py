import pandas as pd
import os
import shutil
import json


data = pd.read_csv('output.csv', index_col=0)
print(data)

# Assuming 'data' is your DataFrame
sorted_data = data.groupby('class').apply(
    lambda x: x.sort_values(by='best_performance_mean', ascending=False))

# Display the sorted DataFrame
print(sorted_data)

# Assuming 'data' is your DataFrame
top_10_per_class = data.groupby('class').apply(lambda x: x.reset_index(
).nlargest(50, 'best_performance_mean').sort_values(by='time_mean'))

# Display the top ten entries of each class
print(top_10_per_class.to_string())


# Check if the directory 'selected' exists
if os.path.exists('selected') and os.path.isdir('selected'):
    # If it exists, delete it
    shutil.rmtree('selected')
    print("Deleted directory: selected")

# Create the 'selected' directory if it doesn't exist
selected_dir = 'selected'
if not os.path.exists(selected_dir):
    os.makedirs(selected_dir)

for index, row in top_10_per_class.iterrows():
    print(row)
    file_path = row['index']
    print(file_path)
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        # Construct the destination path in the 'selected' directory
        dest_path = os.path.join(selected_dir, os.path.basename(file_path))
        # Copy the file to the 'selected' directory
        shutil.copyfile(file_path, dest_path)
        print(f"Copied file: {file_path} to {dest_path}")

# Define a dictionary to store the total counts of selection methods
total_selection_method_counts = {}

# Iterate over the JSON files in the 'selected' directory
for root, dirs, files in os.walk(selected_dir):
    for file_name in files:
        # Construct the file path
        file_path = os.path.join(root, file_name)

        # Load the JSON data
        with open(file_path, 'r') as file:
            json_data = json.load(file)

            # Get the selection methods for the current JSON file
            selection_methods = [json_data.get(
                f'selection_method_{i}') for i in range(1, 3)]

            # Accumulate the counts of selection methods
            for method in selection_methods:
                total_selection_method_counts[method] = total_selection_method_counts.get(
                    method, 0) + 1

# Print the total selection method counts
print("Total selection method counts:")
for method, count in total_selection_method_counts.items():
    print(f"{method}: {count}")


# Define a dictionary to store the total counts of replacement selection methods
total_replacement_method_counts = {}

# Iterate over the JSON files in the 'selected' directory
for root, dirs, files in os.walk(selected_dir):
    for file_name in files:
        # Construct the file path
        file_path = os.path.join(root, file_name)

        # Load the JSON data
        with open(file_path, 'r') as file:
            json_data = json.load(file)

            # Get the replacement selection methods for the current JSON file
            replacement_methods = [json_data.get(
                f'replacement_selection_method_{i}') for i in range(1, 3)]

            # If the replacement method is empty, consider it as "elite"
            replacement_methods = ['elite_selection' if method ==
                                   '' else method for method in replacement_methods]

            # Accumulate the counts of replacement selection methods
            for method in replacement_methods:
                total_replacement_method_counts[method] = total_replacement_method_counts.get(
                    method, 0) + 1

# Print the total replacement selection method counts
print("Total replacement selection method counts:")
for method, count in total_replacement_method_counts.items():
    print(f"{method}: {count}")
