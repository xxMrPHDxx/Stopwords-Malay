from kamus import *

class Stemmer:
	def __init__(self):
		self._prefixes = ['be', 'ber', 'di', 'ke', 'me', 'mem', 'men', 'meng', 'menge', 'pe', 'pem', 'pen', 'penge', 'per', 'te', 'ter']
		self._suffixes = ['an', 'i', 'kan']

	def __call__(self, item):
		if isinstance(item, str): # Stem
			words = []
			for word in re.split(r'[^\w-]+', item):
				if re.match(r'\d', word): words.append(word) # number stuff
				# if double word, return first word
				elif re.match(r'\w+-\w+', word): word = word.split('-')[0]
				
				# if word exists in dictinary, add to root word and continue
				# if word_exists(word): words.append(word)
				if len(word) < 4: words.append(word)
				else:
					# Check prefixes. If match, remove prefix
					for prefix in self._prefixes:
						before = word
						word = re.sub(r'^{}'.format(prefix), '', word)
						if not word_exists(word): word = before

					# Check suffixes, If match, remove suffix
					for suffix in self._suffixes:
						before = word
						word = re.sub(r'{}$'.format(suffix), '', word)
						if not word_exists(word): word = before

					words.append(word)
			return words

stemmer = Stemmer()
root = stemmer('Saya memberikan mewakili jawatankuasa itu ingin mengucapkan ribuan terima kasih atas kesudian dan keprihatinan')
print(root)