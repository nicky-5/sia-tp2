#!/bin/bash

mkdir configs
mkdir configs/bolt
rm configs/bolt/*

# Define temperature constants and population classes
temperature_constants=(0.1 0.5 1.0 2.5 2.0)
population_classes=("ARCHER" "WARRIOR" "INFILTRATOR" "DEFENDER")

# Loop through different values of the temperature constant and population class
for temperature_constant in "${temperature_constants[@]}"
do
    for population_class in "${population_classes[@]}"
    do
        # Create the JSON string with the current temperature constant and population class
        json_data=$(cat <<EOF
{
    "population_size": 10,
    "population_class": "$population_class",
    "child_rate": 0.9,
    "mutation_rate": 0.5,
    "mutation_delta": 0.1,
    "mutation_method": "multi_gene",
    "gene_to_modify": 3,
    "uniform_mutation": true,
    "A": 0.1,
    "selection_method_1": "boltzmann_selection",
    "selection_method_2": "ranking",
    "B": 0.1,
    "replacement_method": "youth_replacement",
    "replacement_selection_method_1": "universal_selection",
    "replacement_selection_method_2": "tournament_det",
    "crossover_method": "uniform",
    "boltzmann_temperature_start": 10,
    "boltzmann_temperature_end": 1,
    "boltzmann_temperature_constant": $temperature_constant,
    "end_criteria": "content_criteria",
    "max_generations": 1000,
    "content_criteria_limit": 10,
    "content_criteria_delta": 0.0000001,
    "structure_criteria_stats_delta": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    "structure_criteria_similar_gen_threshold": 0.1,
    "structure_criteria_individual_prop": 0.1,
    "end_delta": 0.1,
    "min_fitness": 70
}
EOF
)

        # Output the JSON to a file with a name based on the temperature constant and population class
        echo "$json_data" > configs/bolt/config_${population_class}_temp_${temperature_constant}.json
    done
done
