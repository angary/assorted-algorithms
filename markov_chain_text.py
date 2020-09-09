# Program to generate text from given text using markov chain
# Uses a very bare minimum graph ADT


import random
import string


class Vertex(object):
	def __init__(self):
		self.neighbours = {}

	def add_edge(self, dest):
		if dest in self.neighbours:
			self.neighbours[dest] += 1
		else:
			self.neighbours[dest] = 1

	def next_vertices(self):
		return self.neighbours


class Graph(object):
	def __init__(self):
		self.g = {}

	def add_vertex(self, word):
		self.g[word] = Vertex()
	
	def add_edge(self, src, dest):
		if src not in self.g:
			self.add_vertex(src)
		self.g[src].add_edge(dest)

	def random_vertex(self):
		return random.choice(list(self.g))

	def next_vertices(self, src):
		if src in self.g:
			return self.g[src].next_vertices()
		else:
			return {}


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
	g = Graph()
	for i in range(len(words) - 1):
		g.add_edge(words[i], words[i + 1])
	
	# Generate text
	word_count = int(input("Enter length of generated text: "))
	curr = g.random_vertex()
	for _ in range(word_count):
		print(curr, end = " ")
		next_words_dict = g.next_vertices(curr)
		if next_words_dict:
			next_words = list(next_words_dict.keys())
			weights = list(next_words_dict.values())
			curr = random.choices(next_words, weights)[0]
		else:
			curr = g.random_vertex()
	print()

if __name__ == "__main__":
	main()
