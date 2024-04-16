#!/bin/bash

rm -r ideal
mkdir ideal

# Define parameter values
population_classes=("WARRIOR" "INFILTRATOR" "DEFENDER" "ARCHER")
population_sizes=(20 30 40 50 60 70 80 90 100 200 400 750)

# Define minimum fitness values for each class
declare -A min_fitness_values=(
    ["WARRIOR"]=41.24
    ["INFILTRATOR"]=54.99
    ["DEFENDER"]=58.24
    ["ARCHER"]=61.85
)

# Iterate through parameter combinations
for class in "${population_classes[@]}"; do
    min_fitness=${min_fitness_values[$class]}
    for size in "${population_sizes[@]}"; do
        # Create JSON object
        json=$(cat <<EOF
{
    "population_size": $size,
    "population_class": "$class",
    "child_rate": 0.9,
    "mutation_rate": 0.6,
    "mutation_delta": 0.9,
    "mutation_method": "multi_gene",
    "gene_to_modify": 3,
    "uniform_mutation": true,
    "A": 0.305,
    "selection_method_1": "boltzmann_selection",
    "selection_method_2": "tournament_det",
    "B": 0.310,
    "replacement_method": "youth",
    "replacement_selection_method_1": "boltzmann_selection",
    "replacement_selection_method_2": "ranking",
    "crossover_method": "single_point", 
    "boltzmann_temperature_start": 10,
    "boltzmann_temperature_end": 1,
    "boltzmann_temperature_constant": 1,
    "end_criteria": "min_fitness",
    "max_generations": 1000,
    "content_criteria_limit": 10,
    "content_criteria_delta": 0.0000001,
    "structure_criteria_stats_delta": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    "structure_criteria_similar_gen_threshold": 0.1,
    "structure_criteria_individual_prop": 0.1,
    "end_delta": 0.1,
    "min_fitness": $min_fitness
}
EOF
)
        # Define output filename
        output_filename="ideal/output_${class}_${size}.json"
        
        # Write JSON to file
        echo "$json" > "$output_filename"
        echo "Generated $output_filename"
    done
done
