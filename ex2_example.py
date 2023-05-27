import random
import re
import statistics

from graph import PercentPerGeneration

# Constants
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
CIPHER_TEXT_FILE = "enc.txt"
PLAIN_TEXT_FILE = "plain.txt"
PERMUTATION_FILE = "perm.txt"
COMMON_WORD = "dict.txt"
FREQ_FILE = "Letter_Freq.txt"
FREQ_FILE2 = "Letter2_Freq.txt"

# Genetic Algorithm Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.2
MAX_GENERATIONS = 10000
# How much to take from the best solutions
SELECTION_BIASED = POPULATION_SIZE * 0.1
# How much to take from the best solutions for crossover
SELECTION_BIASED_CROSSOVER = POPULATION_SIZE * 1
CHANGE_LAMARCK = 0.5
COUNTER_CONVERGENCE = 100


# return dict key=letter, val=num apper
def statistic_letter(text):
    conter = 0
    letter_count = {}
    for letter in text:
        if letter.isalpha():
            letter = letter.lower()
            letter_count[letter] = letter_count.get(letter, 0) + 1
            conter += 1
    for key, value in letter_count.items():
        letter_count[key] = value / conter
    return (letter_count)


def file_to_arr(file_path):
    data_dict = set()
    with open(file_path, "r") as file:
        for line in file:
            data_dict.add(line.strip())
    return data_dict


# for each line the first word is key the secound value
def file_to_dict(file_path):
    data_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            words = line.lower().strip().split()
            if len(words) >= 2:
                key = words[1]
                value = words[0]
                data_dict[key] = float(value)
    return data_dict


def remove_special_characters(input_string):
    # Regular expression pattern to match special characters
    pattern = r'[^a-zA-Z0-9\s]'  # Matches any character that is not a letter, digit, or whitespace
    output_string = re.sub(pattern, '', input_string)
    return output_string


# delete duplicates and check that all the letters are found, if not add them at the end in random order
def missing_letters(letters):
    missing_letters = []
    combined_list_set = list(set(letters))
    # Sort the combined list
    combined_list_set.sort()
    # Check if all letters are present
    if len(combined_list_set) != 26:
        # Create a list of missing letters
        missing_letters = [chr(i) for i in range(ord('a'), ord('z') + 1) if chr(i) not in combined_list_set]
    return missing_letters


# Generate initial population
def generate_population():
    population = []
    for _ in range(POPULATION_SIZE):
        permutation = list(ALPHABET)
        random.shuffle(permutation)
        population.append(permutation)
    return population


# Calculate fitness score
def calculate_fitness(permutation):
    decrypted_text = cipher_text.translate(str.maketrans(ALPHABET, "".join(permutation)))
    decrypted_text_arr = remove_special_characters(decrypted_text).lower().strip().split()
    # Checks how many common words appear in the decoded text
    set1 = set(decrypted_text_arr)
    set2 = set(common_word)
    intersection = set1.intersection(set2)
    res_word = len(intersection)
    res_letter = calculate_statisc_letter(permutation)
    return res_word * 3 + res_letter * 0.00001


def calculate_statisc_letter(permutation):
    res = 0
    for key, value in sulotionFreq.items():
        letter = permutation[ALPHABET.index(key)]
        try:
            res += 1 / abs(value - real_freq[letter])
        except:
            res += 1000000
    return res


# Perform single-point crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(0, 26)
    child = fix_cross(parent1[:crossover_point], parent2[crossover_point:])
    return child


def fix_cross(a, b):
    combined_list = list(set(a + b))
    missing_letter = missing_letters(combined_list)

    # Add missing letters randomly to the combined list
    random.shuffle(missing_letter)
    combined_list += missing_letter

    # Return the combination
    return combined_list


# Perform mutation
def mutate(permutation):
    for i in range(1):  # int(len(ALPHABET)*MUTATION_RATE)):
        j = random.randint(0, len(ALPHABET) - 1)
        z = random.randint(0, len(ALPHABET) - 1)
        permutation[z], permutation[j] = permutation[j], permutation[z]
    return permutation


def smartMutate(permutation, indexes):
    for i in range(int(len(ALPHABET) * MUTATION_RATE)):
        j = indexes[i]
        # j = random.randint(0, len(ALPHABET) - 1)
        z = random.randint(0, len(ALPHABET) - 1)
        permutation[z], permutation[j] = permutation[j], permutation[z]
    return permutation


def sort_by_grade(objects, grades):
    def myFunc(x):
        return x[1]

    # Combine objects and grades into pairs
    pairs = zip(objects, grades)

    # Sort the pairs based on the grade value
    sorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    # Create a new array with pairs of object and grade
    result = [(obj, grade) for obj, grade in sorted_pairs]
    return result


"delete later"


def res(sul):
    sum = 0
    real_sul = 'yxintozjcebldukmsvpqrhwgaf'
    for i in range(26):
        if real_sul[i] == sul[i]:
            sum += 1
    return sum / 26


# Main genetic algorithm loop
def genetic_algorithm():
    population = generate_population()
    generations = 0
    best_individual = None
    best_ans_for_generations = ""
    counter_convergence = COUNTER_CONVERGENCE
    while generations < MAX_GENERATIONS and counter_convergence:

        # Calculate fitness for each individual
        fitness_scores = [calculate_fitness(individual) for individual in population]
        # Find best individual
        best_individual = sort_by_grade(population, fitness_scores)
        x = best_individual

        final_ans = best_individual[0]
        print(final_ans)
        print("generations: ", generations)
        print("percent: ", res(final_ans[0]))
        print("counter_convergence: ", counter_convergence)

        if best_ans_for_generations != "" and best_ans_for_generations == final_ans[1]:
            counter_convergence -= 1
        else:
            counter_convergence = 100

        best_ans_for_generations = final_ans[1]
        # Create new population through selection, crossover, and mutation
        new_population = create_population_ver1(best_individual)

        population = new_population.copy()
        generations += 1

    writeRes(final_ans[0])
    return generations


def deleteLater(final_ans, generations):
    if 'yxintozjcebldukmsvpqrhwgaf' == "".join(final_ans[0]):
        print(generations)


def create_population_ver1(best_individual):
    new_population = []
    new_population.append(best_individual[0][0].copy())

    for i in range(5):
        new_population.append(mutate(best_individual[0][0].copy()))

    new_population.extend([mutate(best[0]) for best in best_individual[:int(SELECTION_BIASED)]])

    for_crossover = best_individual[:int(SELECTION_BIASED_CROSSOVER)]
    while len(new_population) < POPULATION_SIZE:
        parent1 = random.choice(for_crossover)[0]
        parent2 = random.choice(for_crossover)[0]
        child = crossover(parent1, parent2)
        if len(child) != 26:
            print("error")
        child = mutate(child)
        if len(child) != 26:
            print("error 2")
        new_population.append(child)
    # new_population.append(list('yxintozjcebldukmsvpqrhwgaf'))
    return new_population


def create_population_ver0(best_individual):
    new_population = generate_population()
    new_population[5] = best_individual[0][0]
    # new_population[2]=(list('yxintozjcebldukmsvpqrhwgaf'))
    return new_population


def lamarck_algorithm():
    # for graph - each generation information
    best_results = []
    worst_results = []
    average_results = []
    population = generate_population()  # generate random population
    generations = 0
    best_individual = None
    best_ans_for_generations = ""
    counter_convergence = COUNTER_CONVERGENCE
    while generations < MAX_GENERATIONS and counter_convergence:
        # Create new population through selection, crossover, and mutation
        [mutate(individual) for individual in population]

        if best_ans_for_generations != "":
            add = best_individual[0][0].copy()
            population[-1] = add

        # Calculate fitness for each individual
        fitness_scores = [calculate_fitness(individual) for individual in population]
        # Find best individual
        best_individual = sort_by_grade(population, fitness_scores)

        final_ans = best_individual[0]
        print(final_ans)
        print("generations: ", generations)
        print("percent: ", res(final_ans[0]))
        print("counter_convergence: ", counter_convergence)
        # information for graph
        best_results.append((best_individual[0][1]))
        worst_results.append((best_individual[-1][1]))
        average_results.append(statistics.mean(fitness_scores))

        if best_ans_for_generations != "" and best_ans_for_generations == final_ans[1]:
            counter_convergence -= 1
        else:
            counter_convergence = 200

        best_ans_for_generations = final_ans[1]
        # Create new population through selection, crossover, and mutation
        new_population = create_population_lamarck(best_individual)

        population = new_population
        generations += 1
    PercentPerGeneration(best_results, worst_results, average_results)
    writeRes(final_ans[0])
    return generations


def darwin_algorithm():
    best_results = []
    worst_results = []
    average_results = []
    population = generate_population()
    generations = 0
    best_individual = None
    best_ans_for_generations = ""
    counter_convergence = COUNTER_CONVERGENCE
    while generations < MAX_GENERATIONS and counter_convergence:
        fitness_scores = [calculate_fitness(individual) for individual in population]

        results = beforAndAfterMutate(population)  # make mutation and calculate fitness
        # best_individual = sort_by_grade(population, fitness_scores)
        best_individual = (sorted(results.items(), key=lambda item: item[1], reverse=True))

        # if best_ans_for_generations != "":
        #     add = best_individual[0][0].copy()
        #     population[-1] = add

        final_ans = best_individual[0]
        print(final_ans)
        print("generations: ", generations)
        print("percent: ", res(final_ans[0]))
        print("counter_convergence: ", counter_convergence)

        # information for graph
        best_results.append((best_individual[0][1]))
        worst_results.append((best_individual[-1][1]))
        average_results.append(statistics.mean(fitness_scores))

        if best_ans_for_generations != "" and best_ans_for_generations == final_ans[1]:
            counter_convergence -= 1
        else:
            counter_convergence = 200

        best_ans_for_generations = final_ans[1]
        # Create new population through selection, crossover, and mutation
        new_population = create_population_darwin(best_individual)
        population = new_population.copy()
        generations += 1
    PercentPerGeneration(best_results, worst_results, average_results)
    writeRes(final_ans[0])
    return generations


def writeRes(final_ans):
    decrypted_text = cipher_text.translate(str.maketrans(ALPHABET, "".join(final_ans)))
    with open(PLAIN_TEXT_FILE, "w") as file:
        file.write(decrypted_text)
    with open(PERMUTATION_FILE, "w") as file:
        file.write("".join(final_ans))


# create new population with lamarck - duplicate the best individuals
def create_population_lamarck(best_individual):
    new_population = []
    count = int(SELECTION_BIASED)
    top_best_individual = best_individual[:10].copy()
    for best in top_best_individual:
        if len(new_population) >= POPULATION_SIZE:
            break
        for i in range(count):
            new_population.append(best[0].copy())
        count -= 1
    for_rest = best_individual
    # the rest of the population -> do crossover
    crossover_population(new_population, for_rest, "lamarck")
    return new_population


def create_population_darwin(best_individual):
    new_population = []
    count = int(SELECTION_BIASED)
    top_best_individual = best_individual[:10].copy()
    new_population.append(list(best_individual[0][0]).copy())
    for best in top_best_individual:
        for i in range(count):
            new_copy = mutate(list(best[0]))
            new_population.append(new_copy)
        count -= 1
    # creat new population
    new_group = new_population.copy()
    # add random individual
    for i in range(POPULATION_SIZE - len(new_population)):
        new_group.append(mutate(list(random.choice(best_individual)[0])).copy())
    # new_population = crossover_population(None, new_group, "darwin")
    return new_population


# take population and return new population after crossover
def crossover_population(dest_population, source_population, mode):
    if mode == "lamarck":
        # do this until we get the same size of population
        while len(dest_population) < POPULATION_SIZE:
            parent1 = random.choice(source_population)[0].copy()
            parent2 = random.choice(source_population)[0].copy()
            child = crossover(parent1, parent2)
            if len(child) != 26:
                print("error")
            child = mutate(child)
            if len(child) != 26:
                print("error 2")
            dest_population.append(child)
        return dest_population
    elif mode == "darwin":
        dest_population = []
        # do this until we get the same size of population
        while len(dest_population) < POPULATION_SIZE:
            parent1 = random.choice(source_population)
            parent2 = random.choice(source_population)
            child = mutate(crossover(parent1, parent2)).copy()
            if len(child) != 26:
                print("error")
            dest_population.append(child)
        return dest_population


# dict of population before And After Mutate, key=before, value=After
def beforAndAfterMutate(population):
    dict_map = {}
    for people in population:
        dict_map["".join(people)] = calculate_fitness(mutate(list(people)))
    return dict_map


def create_population_ver2(best_individual):
    new_population = []
    best = best_individual[0][0]
    for i in range(5):
        new_population.append(best)
    while len(new_population) < POPULATION_SIZE - 1:
        parent1 = random.choice(best_individual)[0]
        parent2 = random.choice(best_individual)[0]
        child = crossover(parent1, parent2)
        new_population.append(child)
        if len(child) != 26:
            print("error")
    for i in range(20):
        index = random.randint(0, 98)
        new_population[index] = mutate(new_population[index])
    new_population.append(best)
    return new_population


if __name__ == "__main__":
    with open(CIPHER_TEXT_FILE, "r") as file:
        cipher_text = file.read().lower()
    sum_enc_word = len((cipher_text.strip().split()))
    real_freq = file_to_dict(FREQ_FILE)
    # A sorted array of the most common letters according to the common letters file
    common_word = file_to_arr(COMMON_WORD)

    sulotionFreq = statistic_letter(cipher_text.strip())
    total_steps = genetic_algorithm()
    # total_steps = darwin_algorithm()
    # total_steps = lamarck_algorithm()
    print(f"Total Steps: {total_steps}")
