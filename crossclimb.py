import csv
from collections import deque, defaultdict

MAX_LEN = 7

def read_csv(path):
	words = set()
	with open(path, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			for word in row:
				words.add(word.lower())
	return words

# returns true if the distance between two words is 1 (i.e. oen step)
# The distance is defined as one letter chenged without affecting the others.
# EX. COOL and COOK have a distance of 1 (L->K). POOL and COOK have a distance of 2 (P->C, L->K).  
def step_check(word1, word2):
	distance = sum(a != b for a, b in zip(word1, word2))
	return distance == 1

def find_paths(words, start, end, max_length=MAX_LEN):
    # Precompute all valid transitions to reduce step_check calls
    transitions = defaultdict(list)
    for word1 in words:
        for word2 in words:
            if step_check(word1, word2):
                transitions[word1].append(word2)
    
    queue = deque([(start, [start])])
    paths = []
    
    while queue:
        current_word, path = queue.popleft()

        if len(path) > max_length:
            continue

        if current_word == end:
            paths.append(path)
            continue

        for word in transitions[current_word]:
            if word not in path:
                queue.append((word, path + [word]))

    return paths

def main(words_csv, start_word, end_word):
	words = read_csv(words_csv)
	start_word = start_word.lower()
	end_word = end_word.lower()

	words.add(start_word)
	words.add(end_word)
	
	paths = find_paths(words, start_word, end_word)
	
	print(f"All paths from '{start_word}' to '{end_word}' with a maximum length of {MAX_LEN}:")
	for path in paths:
		print(" -> ".join(path))

if __name__ == "__main__":
	#words_csv = "collegeman.csv" # nicked the CSV from https://gist.github.com/collegeman/79bd777c6747c08237d0
	words_csv = "litscape.csv" # nicked the list from https://www.litscape.com/words/length/4_letters/4_letter_words.html
	start_word = "rock"
	end_word = "roll"

	main(words_csv, start_word, end_word)
