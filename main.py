import json
from utils import *

def get_article(url):
	return '\n\n'.join( \
		filter(map(open_url(url).find('div', {'class': 'field-item even', 'property': 'content:encoded'}).find_all('p'), \
			lambda x : x.text
		), lambda x : len(x) > 0)
	)

def get_article_url(page=0, query='', matcher=r'^.*$'):
	url = 'https://www.hmetro.com.my/search?s={}{}'.format(query, '' if page == 0 else '&page={}'.format(page))
	for url in set(filter(map(filter(open_url(url).find_all('a'), has_key('href')), get_key('href')), text_matcher(matcher))):
		url = 'https://www.hmetro.com.my{}'.format(url)
		yield url, get_article(url)

def tokenize_words(document):
	return filter(map(re.split(r'[^\w\.,$\-]+', document.lower()), lambda text: re.sub(r'(^[\.]|[\.\?\!\,]+)', '', text)), lambda text: len(text) > 0)

def word_counts(document):
	freq_table = {}
	for word in tokenize_words(document):
		if word in freq_table: freq_table[word] += 1
		else: freq_table[word] = 1
	return freq_table

def get_articles(max=100, start_page=0):
	i, page = 0, start_page
	while True:
		for url, article in get_article_url(page=page, matcher=r'^/.+?/\d{4}/\d{2}/\d{6}/.+$'):
			yield url, article
			i += 1
			print('Got {}/{} article from page {}: {}'.format(i, max, page, url))
			if i >= max: return
		page += 1

if __name__ == '__main__':
	for url, article in get_articles(max=3000, start_page=57):
		filename = 'article/{}.json'.format(url.split('/')[-1])
		with open(filename, 'w', encoding='utf-8') as file:
			file.write(json.dumps(word_counts(article)))