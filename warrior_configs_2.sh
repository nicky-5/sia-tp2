#!/bin/bash

rm -r warrior

mkdir warrior

# Define parameter values
selection_methods=("elite" "roulette" "universal" "boltzmann" "tournament_det" "tournament_prob" "ranking")
A_values=(0.1 0.25 0.5)
B_values=(0.1 0.25 0.5)

# Iterate through parameter combinations
for selection_1 in "${selection_methods[@]}"; do
    for selection_2 in "${selection_methods[@]}"; do
        if [[ "$selection_2" != "$selection_1" ]]; then
            for replacement_1 in "${selection_methods[@]}"; do
                if [[ "$replacement_1" != "$selection_1" && "$replacement_1" != "$selection_2" ]]; then
                    for replacement_2 in "${selection_methods[@]}"; do
                        if [[ "$replacement_2" != "$replacement_1" ]]; then
                            for A in "${A_values[@]}"; do
                                for B in "${B_values[@]}"; do
                                    # Create JSON object
                                    json=$(cat <<EOF
{
    "population_size": 10,
    "population_class": "WARRIOR",
    "child_rate": 0.9,
    "mutation_rate": 0.6,
    "mutation_delta": 0.9,
    "mutation_method": "multi_gene",
    "gene_to_modify": 1,
    "uniform_mutation": true,
    "A": $A,
    "selection_method_1": "$selection_1",
    "selection_method_2": "$selection_2",
    "B": $B,
    "replacement_method": "traditional",
    "replacement_selection_method_1": "$replacement_1",
    "replacement_selection_method_2": "$replacement_2",
    "crossover_method": "uniform",
    "boltzmann_temperature_start": 10,
    "boltzmann_temperature_end": 1,
    "boltzmann_temperature_constant": 1,
    "end_criteria": "min_fitness",
    "max_generations": 200,
    "content_criteria_limit": 10,
    "content_criteria_delta": 0.0000001,
    "structure_criteria_stats_delta": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    "structure_criteria_similar_gen_threshold": 0.1,
    "structure_criteria_individual_prop": 0.1,
    "end_delta": 3,
    "min_fitness": 41.25
}
EOF
)
                                    # Define output filename
                                    output_filename="warrior/output_${selection_1}_${selection_2}_${replacement_1}_${replacement_2}_A${A}_B${B}.json"

                                    # Write JSON to file
                                    echo "$json" > "$output_filename"
                                    echo "Generated $output_filename"
                                done
                            done
                        fi
                    done
                fi
            done
        fi
    done
done

