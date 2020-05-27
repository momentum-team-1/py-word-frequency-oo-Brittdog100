import string

STOP_WORDS = [
	'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has',
	'he', 'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to',
	'were', 'will', 'with'
]


class FileReader:
	def __init__(self, filename):
		self.src = filename

	def read_contents(self):
		"""
		This should read all the contents of the file
		and return them as one string.
		"""
		with open(self.src) as file:
			return file.readlines()


class WordList:
	def __init__(self, text):
		self.raw_text = text
		self.word_list = []
		self.longest = 0

	def extract_words(self):
		"""
		This should get all words from the text. This method
		is responsible for lowercasing all words and stripping
		them of punctuation.
		"""
		for line in self.raw_text:
			stripped = line.translate(str.maketrans('', '', string.punctuation))
			for wd in stripped.split():
				word = wd.strip().lower()
				if len(word) > self.longest:
					self.longest = len(word)
				self.word_list.append(word)

	def remove_stop_words(self):
		"""
		Removes all stop words from our word list. Expected to
		be run after extract_words.
		"""
		for forbidden in STOP_WORDS:
			self.word_list = [word for word in self.word_list if word != forbidden]

	def get_freqs(self):
		"""
		Returns a data structure of word frequencies that
		FreqPrinter can handle. Expected to be run after
		extract_words and remove_stop_words. The data structure
		could be a dictionary or another type of object.
		"""
		output = {}
		for word in self.word_list:
			if word not in output:
				output[word] = 1
			else:
				output[word] += 1
		return output


class FreqPrinter:
	def __init__(self, freqs):
		self.list = freqs

	def print_freqs(self):
		"""
		Prints out a frequency chart of the top 10 items
		in our frequencies data structure.

		Example:
		  her | 33   *********************************
		which | 12   ************
		  all | 12   ************
		 they | 7    *******
		their | 7    *******
		  she | 7    *******
		 them | 6    ******
		 such | 6    ******
	   rights | 6    ******
		right | 6    ******
		"""
		i = 0
		temp = []
		longest = 0
		for word in sorted(self.list, key=self.list.get, reverse=True):
			temp.append(word)
			if len(word) > longest:
				longest = len(word)
			i += 1
			if i > 9:
				break
		for word in temp:
			print(word.rjust(longest, ' '),'|',"*" * self.list[word])
				



if __name__ == "__main__":
	import argparse
	import sys
	from pathlib import Path

	parser = argparse.ArgumentParser(
		description='Get the word frequency in a text file.')
	parser.add_argument('file', help='file to read')
	args = parser.parse_args()

	file = Path(args.file)
	if file.is_file():
		reader = FileReader(file)
		word_list = WordList(reader.read_contents())
		word_list.extract_words()
		word_list.remove_stop_words()
		printer = FreqPrinter(word_list.get_freqs())
		printer.print_freqs()
	else:
		print(f"{file} does not exist!")
		sys.exit(1)
