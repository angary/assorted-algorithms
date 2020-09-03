# Program to generate text from given text using markov chain
# Uses a very bare minimum graph ADT


import random
import string


class Vertex(object):
	def __init__(self):
		self.weights = {}

	def add_weight(self, dest):
		if dest in self.weights:
			self.weights[dest] += 1
		else:
			self.weights[dest] = 1

	def next_vals(self):
		return self.weights


class Graph(object):
	def __init__(self):
		self.g = {}

	def add_vertex(self, word):
		self.g[word] = Vertex()
	
	def add_edge(self, src, dest):
		if src not in self.g:
			self.add_vertex(src)
		self.g[src].add_weight(dest)

	def random_vertex(self):
		return random.choice(list(self.g))

	def get_next_word(self, src):
		if src in self.g:
			return self.g[src].next_vals()
		else:
			return {}


def main():

	# Scan value into an array
	file_path = (input("Enter file path: "))
	words = []
	with open(file_path, "r") as f:
		for line in f:
			for w in line.split():
				w.lower().translate(str.maketrans('', '', string.punctuation))
				words.append(w)
	
	# Transfer values to a graph
	g = Graph()
	for i in range(len(words) - 1):
		g.add_edge(words[i], words[i + 1])
	
	# Generate text
	word_count = int(input("Enter length of generated text: "))
	curr = g.random_vertex()
	for _ in range(word_count):
		print(curr, end = " ")
		next_words_dict = g.get_next_word(curr)
		if next_words_dict:
			next_words = list(next_words_dict.keys())
			weights = list(next_words_dict.values())
			curr = random.choices(next_words, weights)[0]
		else:
			curr = g.random_vertex()
	print()

if __name__ == "__main__":
	main()
