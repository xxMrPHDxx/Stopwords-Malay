from utils import *

def word_exists(word):
	url = 'http://prpm.dbp.gov.my/cari1?keyword={word}'.format(word=word)
	return not 'Tiada maklumat tesaurus untuk kata' in open_url(url).text

if __name__ == '__main__':
	# print('kalau {}'.format('Exists' if word_exists('kalau') else 'Not Exists'))
	# print('kalaur {}'.format('Exists' if word_exists('kalaur') else 'Not Exists'))


	print(test())