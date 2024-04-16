
# TP2 SIA - Algoritmos Genéticos

[Enunciado](docs/SIA_TP2.pdf)

### Requisitos

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalación

Parado en la carpeta del tp2 ejecutar

```sh
pipenv install
```

para instalar las dependencias necesarias en el ambiente virtual

## Ejecución

Antes de ejecutar el main, se debe proveer un directorio con archivos de configuración. De manera predeterminada, el main toma el directorio config y ejecuta todos los archivos dentro de dicho archivo como archivos de configuración.

El main ejectutara cada archivo 100 veces y los resultados los pondra en output.csv.

```
pipenv run python main.py
```

Este script corre múltiples veces la función execute, para cada archivo de configuración.
Esta función analiza el archivo de configuración y ejecuta el algoritmo genético con los hiperparametros correspondientes.

## Configuración

El archivo de configuración es un json con los diferentes hiperparametros. Un ejemplo del archivo de configuración es el siguiente:

```json
{
    "population_size": 10,
    "population_class": "WARRIOR",
    "child_rate": 0.9,
    "mutation_rate": 0.5,
    "mutation_delta": 0.1,
    "mutation_method": "multi_gene",
    "gene_to_modify": 3,
    "uniform_mutation": true,
    "A": 0.9,
    "selection_method_1": "elite",
    "selection_method_2": "elite",
    "B": 0.4,
    "replacement_method": "youth_replacement",
    "replacement_selection_method_1": "elite",
    "replacement_selection_method_2": "elite",
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
    "min_fitness": 70
}
```

A continuación se explicara cada hiperparametro.

| Hiperparametro                           | Descripción                                                                                           |
|------------------------------------------|-------------------------------------------------------------------------------------------------------|
| population_size                          | Tamaño de la población                                                                                |
| population_class                         | Clase de la población                                                                                 |
|                                          | * "ARCHER"                                                                                            |
|                                          | * "WARRIOR"                                                                                           |
|                                          | * "DEFENDER"                                                                                          |
|                                          | * "INFILTRATOR"                                                                                       |
| child_rate                               | Porcentaje de la población que se en cada generación                                                  |
| mutation_rate                            | Probabilidad de que un individuo muta                                                                 |
| mutation_delta                           | Máxima mutación que un individuo podría sufrir                                                        |
| mutation_method                          | Método de mutación                                                                                    |
|                                          | * "gene"                                                                                              |
|                                          | * "multi_gene"                                                                                        |
| gene_to_modify                           | Gen a modificar en mutación de un solo gen                                                            |
| uniform_mutation                         | * true: Mutación se mantiene constante con el tiempo                                                  |
|                                          | * false: Mutación decrece con el tiempo                                                               |
| A                                        | Proporción en que se seleccionan individuos con selection_method_1                                    |
| selection_method_1                       | Método de selección 1. Una proporción A de la población sera elegido                                  |
| selection_method_2                       | Método de selección 2. Una proporción (1-A) de la población sera elegido                              |
| B                                        | Proporción en que se seleccionan individuos con replacement_selection_method_1 para reemplazar        |
| replacement_method                       | Método de reemplazo                                                                                   |
|                                          | * "youth_favoured": Sesgo joven                                                                       |
|                                          | * "traditional": tradicional                                                                          |
| replacement_selection_method_1           | Método de selección para el reemplazo 1. Una proporción B de la población sera elegido                |
| replacement_selection_method_2           | Método de selección para el reemplazo 2. Una proporción (1-B) de la población sera elegido            |
| crossover_method                         | Método de crossover                                                                                   |
|                                          | * "single_point": Un punto                                                                            |
|                                          | * "double_point": Dos puntos                                                                          |
|                                          | * "ring": Anular                                                                                      |
|                                          | * "uniform": Uniforme                                                                                 |
| boltzmann_temperature_start              | Temperatura inicial para los métodos de selección boltzmann                                           |
| boltzmann_temperature_end                | Temperatura final para los métodos de selección boltzmann                                             |
| boltzmann_temperature_constant           | Gradiente de decrecimiento de temperatura para los métodos de selección de boltzmann                  |
| end_criteria                             | Criterio de corte                                                                                     |
|                                          | * "max_generations": Máximo numero de generaciones                                                    |
|                                          | * "structure_criteria": Criterio de corte por estructura                                              |
|                                          | * "content_criteria": Criterio de corte por contenido                                                 |
|                                          | * "min_fitness": Entorno Optimo                                                                       |
| max_generations                          | Numero de generaciones maxima si el criterio de corte es maximo de numero de generaciones             |
| content_criteria_limit                   | Cantidad de generaciones similares corte por contenido                                                |
| content_criteria_delta                   | Diferencia máxima entre las mejores preforman ce entre cada generación para que se consideren iguales |
| structure_criteria_stats_delta           | Diferencia máxima entre cada gen para que se consideren iguales                                       |
| structure_criteria_similar_gen_threshold | Limite de generaciones similares estructuralmente                                                     |
| structure_criteria_individual_prop       | Proporción de individuos similares para cortar                                                        |
| min_fitness                              | Mínimo fitness para cuando el criterio de corte es de entorno óptimo                                  |

### Métodos de Selección

Los métodos de selección posible para selección o para reemplazo son los siguientes:

* "elite"
* "roulette"
* "universal"
* "boltzmann"
* "tournament_det": Torneo Determinístico
* "tournament_prob": Torneo Probabilístico
* "ranking"

