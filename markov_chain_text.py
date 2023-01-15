# Program to generate text from given text using markov chain

import random
import string

word_graph = {}


def main():

    # Save words of text into an array
    file_path = (input("Enter file path: "))
    words = []
    with open(file_path, "r") as f:
        for line in f:
            for w in line.split():
                w.lower().translate(str.maketrans('', '', string.punctuation))
                words.append(w)

    # Transfer words to a graph
    for i, curr in enumerate(words[:-1]):
        next = words[i + 1]
        if curr in word_graph.keys():
            word_graph[curr][next] = word_graph[curr].get(next, 0) + 1
        else:
            word_graph[curr] = {next: 1}

    # Generate text
    word_count = int(input("Enter length of generated text: "))

    # Choose random starting word in dict
    curr = random.choice(list(word_graph.keys()))
    for _ in range(word_count):
        print(curr, end=" ")
        next_words_dict = word_graph[curr]
        if next_words_dict:
            next_words = list(next_words_dict.keys())
            weights = list(next_words_dict.values())
            curr = random.choices(next_words, weights)[0]
        else:
            curr = random.choice(list(word_graph.keys()))
    print()


if __name__ == "__main__":
    main()
