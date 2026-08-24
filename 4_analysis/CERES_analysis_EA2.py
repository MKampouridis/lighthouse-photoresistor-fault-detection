# First, let's read the file to understand its structure and to check for float-valued vectors with all values below -0.01
file_paths = [
    './CERES_results/EA2/Tasks/TH_5000.txt',
    './CERES_results/EA2/Tasks/TH_10000.txt',
    './CERES_results/EA2/Tasks/TH_15000.txt',
    './CERES_results/EA2/Tasks/TH_20000.txt',
    './CERES_results/EA2/Tasks/TH_25000.txt',
    './CERES_results/EA2/Tasks/TH_30000.txt',
    './CERES_results/EA2/Tasks/TH_35000.txt'
    ]

# Since the file might be large, we'll read it in chunks and check each vector
files_with_tuples_below_threshold = {}
threshold = -0.015

for file_path in file_paths:
    tuples_below_threshold = []
    with open(file_path, 'r') as file:
        for line in file:
            # Each line contains a tuple of a binary vector and a float vector
            # We need to extract the float vector and check its values
            try:
                # Extracting and evaluating the tuple
                tuple_data = eval(line)
                binary_vector, float_vector = tuple_data

                # Check if all values in the float vector are below the threshold
                if all(value < threshold for value in float_vector):
                    tuples_below_threshold.append(tuple_data)
            except Exception as e:
                # If there's an error in processing a line, we'll skip it and continue with the next
                continue
    files_with_tuples_below_threshold[file_path] = tuples_below_threshold

summary = {file: {"count": len(tuples), "tuples_below_threshold": tuples[:]}
           for file, tuples in files_with_tuples_below_threshold.items()}

# Iterating through the summary dictionary and printing each item
for file, details in summary.items():
    print(f"File: {file}")
    print(f"Count: {details['count']}")
    print("Tuples Below Threshold:")
    for t in details['tuples_below_threshold']:
        print(t)
    print("\n")  # Adding a new line for separation between files
