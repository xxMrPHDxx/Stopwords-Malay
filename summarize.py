from os import listdir, rename, remove
from json import loads as load_json, dumps as to_json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from utils import *
from main import tokenize_words

def load_stemmer():
	factory = StemmerFactory()
	return factory.create_stemmer()

def open_files(*filepaths, mode='r', encoding='utf-8'):
	return [open(file, mode, encoding=encoding) for file in filepaths]

from sys import exit
# stemmer = load_stemmer()
# for article in map([open('articles/{}'.format(file), 'r', encoding='utf-8').read() for file in listdir('articles')], lambda doc : doc.split('\n\n')):
# 	for parag in article:
# 		print((parag, stemmer.stem(parag)))
# 	break
# exit()

def read_file(filename, encoding='utf-8'):
	return open(filename, 'r', encoding=encoding).read()

# for wrong in filter(listdir('articles'), lambda file: re.match(r'^.+?\.json$', file)):
# 	correct = 'articles/{}.txt'.format(wrong.split('.')[0])
# 	wrong = 'articles/{}'.format(wrong)
# 	try: rename(wrong, correct)
# 	except FileExistsError: remove(wrong)
# exit()

articles = ({
	'title': file.split('.')[0], 
	'article': read_file('articles/{}.txt'.format(file)), 
	'items': load_json(read_file('values/{}.json'.format(file)))
} for file in map(listdir('articles'), lambda x: x.split('.')[0]))
stopwords = open_files('stopword-list.txt')[0].read().split('\n')

def evaluate_articles(articles):
	for article in articles:
		title, article, items = [article[key] for key in article]

		# summary = ''
		values = {}
		values_array = []
		for sentence in map(re.split(r'[.!?]+', article), lambda text: re.sub(r'(^[^\S]+|[^\S]+$)', '', text)):
			i = 0
			# s_sentence = ''
			total = 0
			words = tokenize_words(sentence)
			if len(words) == 0: continue
			for word in words:
				if word in stopwords: continue
				total += 1
				# if i == 0: word = ''.join([word[0].upper(), word[1:]])
				# s_sentence = word if len(sentence) == 0 else '{} {}'.format(s_sentence, word)
				i += 1
			total /= len(words)
			# summary = s_sentence if len(summary) == 0 else '{}. {}'.format(summary, s_sentence)
			values_array.append(total)
			values[sentence] = total
		if len(values_array) > 0: yield title, article, values, values_array

def order(arr, reversed=False):
	orders = []
	for item in sorted(arr):
		for i in range(len(arr)):
			if item == arr[i]: orders.append(i)
	return orders[::-1] if reversed else orders

for title, article, values, values_array in evaluate_articles(articles):
	# print(values_array)
	# print(mean(values_array))

	summary = ''
	res = [sentence for sentence in values]
	limit = 3
	for i in order(values_array, True):
		# if limit == 0: break
		limit -= 1
		print({res[i]: values[res[i]]})
		summary += '{}. '.format(res[i])

	with open('summary/{}.txt'.format(title), 'w', encoding='utf-8') as file:
		file.write(summary)

	# print(res)
	# for sentence in values:
	# 	if values[sentence] > 1.161 * mean(values_array): summary += sentence + '. '
	print(summary)
	break