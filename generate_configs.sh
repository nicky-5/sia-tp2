#!/bin/bash

mkdir configs
mkdir configs/all
rm configs/all/*

# Array of available selection methods
selection_methods=("elite_selection" "roulette_selection" "boltzmann_selection" "universal_selection" "tournament_prob" "ranking" "tournament_det")

# Function to generate JSON with given parameters
generate_json() {
    cat <<EOF
{
    "population_size": 10,
    "population_class": "$1",
    "child_rate": 0.9,
    "mutation_rate": 0.5,
    "mutation_delta": 0.1,
    "mutation_method": "multi_gene",
    "gene_to_modify": 3,
    "uniform_mutation": true,
    "A": $2,
    "selection_method_1": "$3",
    "selection_method_2": "$4",
    "B": $5,
    "replacement_method": "youth_replacement",
    "replacement_selection_method_1": "$6",
    "replacement_selection_method_2": "$7",
    "crossover_method": "uniform",
    "boltzmann_temperature_start": 100,
    "boltzmann_temperature_end": 20,
    "boltzmann_temperature_constant": 0.1,
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
}

# Loop to generate JSON with different values
for population_class in "ARCHER" "WARRIOR" "INFILTRATOR" "DEFENDER"; do
    for a in 0.1 0.2 0.3 0.4 0.5; do
        for b in 0.1 0.2 0.3 0.4 0.5; do
            for ((i=0; i<${#selection_methods[@]}; i++)); do
                for ((j=0; j<${#selection_methods[@]}; j++)); do
                    if [[ $i -ne $j ]]; then
                        filename="config_${population_class}_a${a}_b${b}_${selection_methods[$i]}_${selection_methods[$j]}.json"
                        generate_json $population_class $a ${selection_methods[$i]} ${selection_methods[$j]} $b ${selection_methods[$(($i+1))]} ${selection_methods[$(($j+1))]} > "configs/all/$filename"
                        echo "Generated $filename"
                    fi
                done
            done
        done
    done
done
