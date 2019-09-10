import string
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import os
import requests
from requests.exceptions import HTTPError


class TextAnalyzer:

    def __init__(self, src, *args):
        # intialize the class with a string of some sort

        self._src_type = ''
        self._content = ''
        self._orig_content = ''
        self.path = ''
        self.url = ''

        self._my_soup = ''
        # Avoids crashing if passed something other than string.
        try:
            # Test for text first
            try:
                src += ''
                self._src_type = 'text'
            except:
                # Don't crash just move on
                pass
            # Test for url
            try:
                src.index("http", 0, 4)
                self._src_type = 'url'
                self.url = src
            # If url try to get the url
                try:
                    response = requests.get(self.url)
                    response.raise_for_status()
                    self.soup = bs(response.text, 'lxml')
                    self._my_soup = self.soup.prettify()
                # If error print error
                except HTTPError as http_err:
                    print(f'HTTP error occurred {http_err}')
                    pass
                except Exception as err:
                    print(f'Other error occurred: {err}')
                    pass

            # Don't crash on Value Error
            except ValueError:
                pass

            # Test for text file
            try:
                src.index(".txt", -4)
                self._src_type = 'path'
                self.path = src
                with open(self.path, 'r') as file:
                    self._content = file.read()
                    self._content = self._content.replace('\n', ' ')

            except ValueError:
                pass
            except:
                print('file not found')
        except:

            pass

    def discover_url(self):
        # Go get url
        pass

    def set_content_to_tag(self, tag, tag_id):
        # tag(str) --Tag to read
        # tag_id()--ID of tag to read
        try:
            s = str(self.soup.find(tag, id=tag_id).text)
            self._content = s
        except:
            pass

    def reset_content(self):
        # Resets _content to full text that was originally loaded.  Useful after a call to
        # set_content_to_tag()
        self._content = self._my_soup

    def _word(self, casesensitive=False):
        # Returns words in _content as list.
        # casesensitive(bool)--if False makes all words uppercase
        li = []

        trans = self._content.maketrans('', '', string.punctuation)
        self._content = self._content.translate(trans)

        # Return Upper case if false
        if casesensitive is False:
            self._content = self._content.upper()
            li = list(self._content.split(' '))
            return li
        else:
            li = list(self._content.split(' '))
            return li

    def common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        # Returns a list of 2 element tuples of the structure(word, num) where num is the number
        # of times word shows up in _content
        pass

    def char_distribution(self, casesenitive=False, letters_only=False):
        # Returns a list of 2 element tuples of the format(char, num) where num
        # is the number of times char shows up in _content. The list should
        # be sorted by num in descending order.
        pass

    def plot_common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        # plots the most common words
        pass

    def plot_char_distibution(self, casesensitive=False, letters_only=False):
        # plots character distribution
        pass

    def avg_word_length(self):
        # The average word length in _content rounded to the 100th place(3.82)
        pass

    def word_count(count):
        # the number of words in _content
        pass

    def distinct_word_count(self):
        # The number of distinct words in _content. This should not be case sensitive
        # "You" and "you" should be considered the same word.
        pass

    def words(self):
        # A list of all words used in _content, including repeats, in all uppercase letters.
        pass

    def positivity(self):
        # A positivity score calculated as follows:
        # Create a local tally var with intial val of 0
        # Increment tally by 1 for every word in self.words found in positive.txt
        # Decrement tally by 1 for every word in self.words found in negative.txt
        # calculate scores as follows:
        # round (tally /self.word_count * 1000)
        pass

    def main():
        url = 'https://www.webucator.com/how-to/address-by-bill-clinton-1997.cfm'
        path = 'pride-and-prejudice.txt'
        text = '''The outlook wasn't brilliant for the Mudville Nine that day;
            the score stood four to two, with but one inning more to play.
            And then when Cooney died at first, and Barrows did the same,
            a sickly silence fell upon the patrons of the game.'''
        ta = TextAnalyzer(path)

        #ta.set_content_to_tag('div', 'content-main')

        #print(ta._src_type)

        #print(ta._content)
        ta = TextAnalyzer(path)
        #ta._word(casesensitive=False)
        print(ta._word(casesensitive=False))

if __name__ == '__main__':
    TextAnalyzer.main()
