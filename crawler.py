from utils import *
from main import get_article, word_counts
from sys import getrecursionlimit
import inspect
import json

CRAWLED, YIELDED = [], []
def crawl(start_url, matcher=r'^/.*$', depth=0):
	global CRAWLED, YIELDED
	print('At depth={}'.format(depth))
	protocol, arg = start_url.split('://')
	domain, arg = arg.split('/')
	for url in set(filter(map(filter(open_url(start_url).find_all('a'), has_key('href')), get_key('href')), text_matcher(matcher))):
		try:
			url = '{}://{}{}'.format(protocol, domain, url)
			if re.match(r'^https://www\.hmetro\.com\.my/.+?/\d{4}/\d{2}/\d{6}/.+$', url) and not url in YIELDED:
				YIELDED.append(url)
				yield url, get_article(url)
			elif re.match(r'^https://www\.hmetro\.com\.my/[^/?#]+$', url) and not url in CRAWLED and len(inspect.stack()) < getrecursionlimit(): 
				CRAWLED.append(url)
				yield from crawl(url, matcher, depth=depth+1)
		except RecursionError: break

if __name__ == '__main__':
	counter = 1
	for url, article in crawl('https://www.hmetro.com.my/'):
		title = url.split('/')[-1]
		filename = 'values/{}.json'.format(title)
		filename2 = 'articles/{}.txt'.format(title)
		with open(filename, 'w', encoding='utf-8') as file:
			file.write(json.dumps(word_counts(article)))
		with open(filename2, 'w', encoding='utf-8') as file:
			file.write(article)
		print('Got {} article: {}'.format(counter, title))
		counter += 1