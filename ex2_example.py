import random

# Constants
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
CIPHER_TEXT_FILE = "enc.txt"
PLAIN_TEXT_FILE = "plain.txt"
PERMUTATION_FILE = "perm.txt"
COMMON_WORD = "dict.txt"
FREQ_FILE = "Letter_Freq.txt"

# Genetic Algorithm Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.3
MAX_GENERATIONS = 100
SELECTION_BIASED = POPULATION_SIZE * 0.2
SELECTION_BIASED_CROSSOVER = POPULATION_SIZE * 0.7


# Load encrypted text from file
with open(CIPHER_TEXT_FILE, "r") as file:
    cipher_text = file.read().lower()

def count_letter(text):
    letter_count = {}
    for letter in text:
        if letter.isalpha():
            letter = letter.lower()
            letter_count[letter] = letter_count.get(letter, 0) + 1
    return (letter_count)

def file_to_arr(file_path):
    data_dict = []
    with open(file_path, "r") as file:
        for line in file:
            data_dict.append(line.strip())
    return data_dict


def file_to_dict(file_path):
    data_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            words = line.lower().strip().split()
            if len(words) >= 2:
                key = words[1]
                value = words[0]
                data_dict[key] = value
    return data_dict

def statistically_population():
    dict_freq = file_to_dict(FREQ_FILE)
    freq = sorted(dict_freq, key=lambda k: dict_freq[k], reverse=True)
    dict_letter = count_letter(cipher_text.strip())
    arr_letter = sorted(dict_letter, key=lambda k: dict_letter[k],reverse=True)

    population = []
    for _ in range(POPULATION_SIZE):
        permutation = list(ALPHABET)
        random.shuffle(permutation)
        arr_letter_fix = arr_letter+missing_letters(arr_letter)
        for i in range(len(ALPHABET)):
            cipher_letter = arr_letter_fix[i]
            freq_letter = freq[i]
            permutation[ALPHABET.index(freq_letter)] = cipher_letter

        population.append(permutation)
    return population

def missing_letters(letters):
    missing_letters=[]
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
    decrypted_text_arr =  decrypted_text.lower().strip().split()
    fitness = count_words(decrypted_text_arr,common_word)
    return fitness

def count_words(decrypted_arr,common_word_arr):
    sum = 0
    for word in decrypted_arr:
        if word in common_word_arr:
            sum+=1
    return sum

# Perform single-point crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(8, 15)
    child = fix_cross(parent1[:crossover_point], parent2[crossover_point:])
    return child


def fix_cross(a, b):
    # Combine the two lists
    # Remove duplicates
    combined_list = list(set(a + b))
    #combined_list_set = list(set(combined_list))
    # Sort the combined list
    missing_letter = missing_letters(combined_list)
    #combined_list_set.sort()

    #if missing_letter:
    #    print("hiiiii")
    # Check if all letters are present
    """if len(combined_list_set) != 26:
        # Create a list of missing letters
        missing_letters = [chr(i) for i in range(ord('a'), ord('z') + 1) if chr(i) not in combined_list_set]"""

        # Add missing letters randomly to the combined list
    random.shuffle(missing_letter)
    combined_list += missing_letter

    # Return the combination
    return combined_list


# Perform mutation
def mutate(permutation):
    for i in range(int(len(ALPHABET)*MUTATION_RATE)):
        j = random.randint(0, len(ALPHABET) - 1)
        z = random.randint(0, len(ALPHABET) - 1)
        permutation[z], permutation[j] = permutation[j], permutation[z]
    return permutation


def sort_by_grade(objects, grades):
    # Combine objects and grades into pairs
    pairs = zip(objects, grades)

    # Sort the pairs based on the grade value
    sorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    # Create a new array with pairs of object and grade
    result = [(obj, grade) for obj, grade in sorted_pairs]

    return result


# Main genetic algorithm loop
def genetic_algorithm():
    #population = generate_population()
    population = statistically_population()
    generations = 0
    best_individual = None

    while generations < MAX_GENERATIONS:
        # Calculate fitness for each individual
        fitness_scores = [calculate_fitness(individual) for individual in population]

        # Find best individual
        best_individual = sort_by_grade(population, fitness_scores)
        # best_fitness = max(fitness_scores)
        # best_index = fitness_scores.index(best_fitness)
        # best_individual = population[best_index]

        # Termination condition: if perfect fitness is achieved
        final_ans = best_individual[0]
        print(final_ans)


        """"
        .2 חוזרים על הבאים K פעמים:
        a. חשב את המרחק לכל מסלול
        b. שכפל את המסלול הטוב ביותר להיות 5% מהאוכלוסייה החדשה
        c. לשאר יש לעשות crossover
        d. גורמים ל- 20% מוטציה על הפתרונות
        
        
        • 25% מהפתרונות מתקבלים ע"י רפליקציה של בחירה מתועדפת )selection biased )
        • 75% מהפתרונות מתקבלים ע"י crossover של בחירות מתועדפות )selection biased)
        • 3% מוטציות על כל פתרון חדש
        • אליטיזם – אנחנו מעתיקים את הפתרון הטוב ביותר כמו שהוא
        
        """
        # Create new population through selection, crossover, and mutation
        new_population = [mutate(best[0]) for best in best_individual[:int(SELECTION_BIASED)]]
        for_crossover = best_individual[:int(SELECTION_BIASED_CROSSOVER)]
        while len(new_population) < POPULATION_SIZE:
            parent1 = random.choice(for_crossover)[0]
            parent2 = random.choice(for_crossover)[0]
            child = crossover(parent1, parent2)
            if len(child)!=26:
                print("error")
            child = mutate(child)
            if len(child)!=26:
                print("error 2")
            new_population.append(child)

        population = new_population
        generations += 1

    # Output results to files
    #final_ans = best_individual[0]
    #print(final_ans)
    #best_individual = "".join(best_individual)
    decrypted_text = cipher_text.translate(str.maketrans(ALPHABET, "".join(final_ans[0])))
    with open(PLAIN_TEXT_FILE, "w") as file:
        file.write(decrypted_text)
    with open(PERMUTATION_FILE, "w") as file:
        file.write("".join(final_ans[0]))
    return generations


# Run the genetic algorithm
common_word = file_to_arr(COMMON_WORD)
total_steps = genetic_algorithm()
print(f"Total Steps: {total_steps}")
