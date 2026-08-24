files_with_tuples_below_threshold = {}
threshold = -0.01# -0.019 for TH_noFirstValues; -0.01 for TH_firstValues
accuracy_threshold = -0.6
dataset = 'TH'
float_vector_elements = 7 if dataset == 'TH' else 8

file_paths = [
'./CERES_results/EA3/Tasks/' + dataset + '_firstValues.txt',
# './CERES_results/EA3/Tasks/' + dataset + '_nofirstValues.txt',
'./CERES_results/EA4/Tasks/' + dataset + '_firstValues.txt',
# './CERES_results/EA4/Tasks/' + dataset + '_nofirstValues.txt',
'./CERES_results/EA5/Tasks/' + dataset + '_firstValues.txt',
# './CERES_results/EA5/Tasks/' + dataset + '_nofirstValues.txt',
'./CERES_results/EA6/Tasks/' + dataset + '_firstValues.txt',
# './CERES_results/EA6/Tasks/' + dataset + '_nofirstValues.txt'
    ]

for file_path in file_paths:
    tuples_below_threshold = []
    with open(file_path, 'r') as file:
        for line in file:
            # Each line contains a tuple of a binary vector and a float vector
            # We need to extract the float vector and check its values
            try:
                # Extracting and evaluating the tuple
                # tuple_data = eval(line)
                binary_vector_part, float_vector_part = line.strip().split(']')
                binary_vector = eval(binary_vector_part + ']')  # Re-adding the closing bracket and converting to list
                float_vector = list(eval(float_vector_part))  # Converting to tuple and then to list

                # Check if all values in the float vector are below the threshold
                if all(value < threshold for value in float_vector):
                    if "nofirstValues" in file_path:
                        tuples_below_threshold.append([binary_vector, float_vector])
                    else:
                        if all(value2 < accuracy_threshold for value2 in float_vector[-float_vector_elements:]): # NOTE THAT FOR TH IT'S -7, FOR NLB IT'S -8.
                            tuples_below_threshold.append([binary_vector, float_vector])
            except Exception as e:
                # If there's an error in processing a line, we'll skip it and continue with the next
                continue
    files_with_tuples_below_threshold[file_path] = tuples_below_threshold

summary = {file: {"count": len(tuples), "tuples_below_threshold": tuples[:]}
           for file, tuples in files_with_tuples_below_threshold.items()}

unique_tuples = set()

# Iterating through the summary dictionary and printing each item
for file, details in summary.items():
    print(f"File: {file}")
    unique_file_tuples = []

    for t in details['tuples_below_threshold']:
        hashable_t = tuple(map(tuple, t))

        if hashable_t not in unique_tuples:
            unique_tuples.add(hashable_t)
            unique_file_tuples.append(t)

    print(f"Count of unique tuples: {len(unique_file_tuples)}")#details['count']}")
    print("Tuples Below Threshold:")
    for t in unique_file_tuples:
        print(t)
    print("\n")  # Adding a new line for separation between files
