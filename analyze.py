from os import listdir
from json import loads as load_json, dumps as to_json

from utils import *

def mean(arr): return sum(arr) / len(arr)
def var(arr): 
	avg = mean(arr)
	return sum([(x - avg)**2 for x in arr]) / (len(arr) - 1)

def get_freq_table(limit=None):
	files = listdir('values/') if limit == None or not isinstance(limit, int) else listdir('article/')[:limit]
	freqs = [load_json(open('values/{}'.format(file), 'r', encoding='utf-8').read()) for file in files]
	freq_table = {}
	for freq in freqs:
		for word in freq:
			if word in freq_table: freq_table[word] += freq[word]
			else: freq_table[word] = freq[word]
	return freqs, freq_table

def calculate_mean_and_variance(freqs, freq_table):
	freq_array = [{word: []} for word in freq_table]
	words = [word for word in freq_table]
	total = len(freq_array)
	i = 0
	for word in freq_table:
		for freq in freqs:
			if word in freq: freq_array[i][word].append(freq[word])
			else: freq_array[i][word].append(0)
		arr = freq_array[i][word]
		freq_array[i][word] = {'array': arr, 'mean': mean(arr), 'var': var(arr)}
		i += 1
		print('Done {} out of {}'.format(i, total))
	return {'results': freq_array, 'combined_freq_table': freqs, 'freq_table': freq_table, 'words': words}

from main import word_counts
def calculate_values():
	for title, article in ((file.split('.')[0], open('articles/{}'.format(file), 'r', encoding='utf-8').read()) for file in listdir('articles')):
		filename = 'values/{}.json'.format(title)
		with open(filename, 'w', encoding='utf-8') as file:
			file.write(to_json(word_counts(article)))

from sys import exit
from math import log

if __name__ == '__main__':
	# calculate_values()
	# exit()

	
	results = calculate_mean_and_variance(*get_freq_table())
	results, combined_freq_table, freq_table, words = results['results'], results['combined_freq_table'], results['freq_table'], results['words']
	total_words = len(words)

	stopwords = []
	
	results = {}
	for word in words:
		arr = []
		for document in combined_freq_table:
			arr.append(document[word] if word in document else 0)
		prob = sum(arr) / total_words
		entropy = prob * log(1.0 / prob)
		results[word] = {'probability': prob, 'entropy': entropy}
		if entropy > 0.1: stopwords.append(word)
	
	with open('result.json', 'w', encoding='utf-8') as file:
		file.write(to_json(results))

	with open('stopword-list.txt', 'w', encoding='utf-8') as file:
		file.write('\n'.join(stopwords))


	# with open('result.json', 'w', encoding='utf-8') as file:
	# 	file.write(to_json(result))