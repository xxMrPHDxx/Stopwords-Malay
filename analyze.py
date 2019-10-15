from os import listdir
from json import loads as load_json, dumps as to_json

from utils import *

def mean(arr): return sum(arr) / len(arr)
def var(arr): 
	avg = mean(arr)
	return sum([(x - avg)**2 for x in arr]) / (len(arr) - 1)

def get_freq_table(limit=None):
	files = listdir('article/') if limit == None or not isinstance(limit, int) else listdir('article/')[:limit]
	freqs = [load_json(open('article/{}'.format(file), 'r', encoding='utf-8').read()) for file in files]
	freq_table = {}
	for freq in freqs:
		for word in freq:
			if word in freq_table: freq_table[word] += freq[word]
			else: freq_table[word] = freq[word]
	return freqs, freq_table

def calculate_mean_and_variance(freqs, freq_table):
	freq_array = [{word: []} for word in freq_table]
	total = len(freq_array)
	i = 0
	for word in freq_table:
		for freq in freqs:
			if word in freq: freq_array[i][word].append(freq[word])
			else: freq_array[i][word].append(0)
		arr = freq_array[i][word]
		freq_array[i][word] = {'mean': mean(arr), 'var': var(arr)}
		i += 1
		print('Done {} out of {}'.format(i, total))
	return freq_array

if __name__ == '__main__':

	result = calculate_mean_and_variance(*get_freq_table())

	with open('result.json', 'w', encoding='utf-8') as file:
		file.write(to_json(result))