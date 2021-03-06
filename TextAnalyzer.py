import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
from requests.exceptions import HTTPError
from collections import Counter
import re
import matplotlib.pyplot as plt

class TextAnalyzer:

    def __init__(self, src, **kargs):
        '''intialize the class with a string of some sort'''

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
                self._content = src
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
                    self._soup = bs(response.text, 'lxml')
                    self._my_soup = self._soup.prettify()
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
        self._orig_content = self._content

    def set_content_to_tag(self, tag, tag_id):
        '''tag(str) --Tag to read
        tag_id()--ID of tag to read'''
        try:
            s = str(self._soup.find(tag, id=tag_id).text)
            self._content = s
        except:
            pass

    def reset_content(self):
        '''Resets _content to full text that was originally loaded.  Useful after a call to
        set_content_to_tag()'''
        self._content = self._my_soup

    def _word(self, casesensitive=False):
        '''Returns words in _content as list.
        casesensitive(bool)--if False makes all words uppercase'''

        li = []
        s = self._content
        s = re.sub(r"([^a-zA-Z'])", ' ', s)

        # Return Upper case if false
        if casesensitive is False:
            s = s.upper()
            li = list(s.split(' '))
            li = list(filter(None, li))
            f_list = [l.strip() for l in li]
            return f_list
        else:
            li = list(s.split(' '))
            li = list(filter(None, li))
            f_list = [l.strip() for l in li]
            return f_list

    def common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False, r=True):
        '''Returns a list of 2 element tuples of the structure(word, num) where num is the number
        of times word shows up in _content
        to get the list from largest to smallest set r=True,  to get smallest count to largest set
        r = False'''
        # Error check than min and max are greater than 0
        if (minlen < 1):
            minlen = 1
        if (maxlen < 1):
            maxlen = 1
        # Set up and intialize lists to use in the function
        le = []
        wordfreq = []
       # li is the incoming list
        if casesensitive is False:
            li = self._word(casesensitive = False)
        else:
            li = self._word()
            li = list(filter(None, li))

        # create a list with min and max settings
        for el in li:
            if (len(el) <= maxlen) and (len(el) >= minlen):
                # le is the new list being created
                le.append(el)

        for w in le:
            # word freq is a list of counts of the words
            wordfreq.append(li.count(w))
        # wl is a list of tuples with the word and count
        wl = zip(le, wordfreq)
        results = set(wl)
        l = list(results)
        l.sort(key = lambda x: x[1], reverse=r)
        if (count <= len(l)) and (count > 0):
            return l[:count]
        if (count == 0):
            count = len(l)
            return l[:count]

    def char_distribution(self, casesenitive=False, letters_only=False):
        '''Returns a list of 2 element tuples of the format(char, num) where num
        is the number of times char shows up in _content. The list should
        be sorted by num in descending order.'''
        newstring = ''
        s = self._content
        if (casesenitive is False) and (letters_only is False):

            s = s.upper()
            c = Counter(s)
        if (casesenitive is True) and (letters_only is False):

            c = Counter(s)
        if (casesenitive is False) and (letters_only is True):

            s = s.upper()
            t = s.isalpha()
            if t:
                c = Counter(s)
            else:
                for el in s:
                    if el.isalpha():
                        newstring += el
                c = Counter(newstring)

        if (casesenitive is True) and (letters_only is True):

            t = s.isalpha()
            if t:
                c = Counter(s)
            else:
                for el in s:
                    if el.isalpha():
                        newstring += el
                c = Counter(newstring)


        l = list(c.items())

        l.sort(key=lambda x: x[1], reverse=True)
        return l

    def plot_common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        '''plots the most common words catch min length error'''

        data = self.common_words(minlen, maxlen, count, casesensitive)

        df = pd.DataFrame(data, columns=['WORDS', 'COUNT'])

        df.plot(kind='bar', x='WORDS', y='COUNT')
        plt.title('Words in ' + self._src_type)
        plt.show()



    def plot_char_distribution(self, casesenitive=False, letters_only=False):
        '''plots character distribution'''
        data = self.char_distribution(casesenitive, letters_only)
        df = pd.DataFrame(data, columns=['LETTERS', 'COUNT'])
        print(df)
        df.plot(kind='bar', x='LETTERS', y='COUNT')
        plt.title('Characters in ' + self._src_type)
        plt.show()

    def avg_word_length(self):
        '''The average word length in _content rounded to the 100th place(3.82)'''
        li = self._word()
        average = sum(len(word)for word in li)/len(li)
        average = round(average, 2)
        return average

    def word_count(self):
        '''the number of words in _content'''
        li = self._word()
        return len(li)



    def distinct_word_count(self):
        '''The number of distinct words in _content. This should not be case sensitive
        "You" and "you" should be considered the same word.'''
        li = self._word()
        s = set(li)
        return len(s)



    def words(self):
        '''A list of all words used in _content, including repeats, in all uppercase letters.'''

        li = self._word()
        return li

    def positivity(self):
        '''A positivity score calculated as follows:
        Create a local tally var with intial val of 0
        Increment tally by 1 for every word in self.words found in positive.txt
        Decrement tally by 1 for every word in self.words found in negative.txt
        calculate scores as follows:
        round (tally /self.word_count * 1000)'''

        tally = 0
        words = self._word()
        try:
            with open('positive.txt', 'r') as p_file:
                p_str = p_file.read()
                p_str = p_str.replace('\n', ' ')
        except ValueError:
            pass
        try:
            with open('negative.txt','r') as n_file:
                n_str = n_file.read()
                n_str = n_str.replace('\n', ' ')

        except ValueError:
            pass
        p_list = p_str.split(' ')
        n_list = n_str.split(' ')

        for word in words:
            if word in p_list:
                tally += 1
        for word in words:
            if word in n_list:
                tally -=1

        score = round(tally / self.word_count() * 1000)
        return score




    def is_palindrome(self):
        '''returns a list of palindromes over 3 characters long'''
        # Inner function to reverse the word
        def _reverse(word):
            return word[::-1]
        # creates a set to avoid duplicates of words.
        se = set(self.words())
        # intialize a new list to return
        n_li =[]
        # check the set for palindromes
        for word in se:
            if (len(word)>=3):
                rev = _reverse(word)
                if rev == word:
                    #create the list and return it.
                    n_li.append(rev)
        return n_li

    def distinct_word_case(self, minlen=1, maxlen=10, letter = 'A'):
        se = set(self._word(casesensitive=True))
        li = []
        for word in se:
            if (len(word) <= maxlen) and (len(word) >= minlen):
                for w in word:
                    if letter in w:
                        li.append(word)

        return li
    def any_count(self, count = 1):
        li = self.common_words(count=0, r=False)
        le = []
        for el in li:
            x = el[1]
            if x == count:
                le.append(el)
        return le

    def main():
        url = 'https://www.webucator.com/how-to/address-by-bill-clinton-1997.cfm'
        path = 'pride-and-prejudice.txt'
        text = '''The outlook wasn't brilliant for the Mudville Nine that day;
               the score stood four to two, with but one inning more to play.
               And then when Cooney died at first, and Barrows did the same,
               a sickly silence fell upon the patrons of the game.'''
        address = ['https://www.webucator.com/how-to/george-bushs-inaugural-address.cfm',
                   'https://www.webucator.com/how-to/harry-s-trumans-inaugural-address.cfm',
                   'https://www.webucator.com/how-to/william-mckinleys-inaugural-address.cfm',
                   'https://www.webucator.com/how-to/zachary-taylors-inaugural-address.cfm']

        ta = TextAnalyzer(path)

        # ta.set_content_to_tag('div', 'content-main')

        # print(ta._src_type)

        # print(ta._content)
        #for a in address:
        #    ta = TextAnalyzer(a)
        #    ta.set_content_to_tag(tag = 'div', tag_id='content-main')
        #    print(ta.positivity())


        # ta._word(casesensitive=False)
        #li = ta.common_words(minlen=1, casesensitive=False)
        #li = sorted(li, reverse=True)
        #print(li)
        #print(len(ta.is_palindrome()))
        # print(ta.char_distribution(caseseni
        #print(len(ta.distinct_word_case(minlen=1, maxlen=4, letter='A')))
        # tive=False, letters_only=False))
        # print(ta.char_distribution(casesenitive=True, letters_only=False))
        # print(ta.char_distribution(casesenitive=False, letters_only=True))
        # print(ta.char_distribution(casesenitive=True, letters_only=True))
        # print(ta._word(casesensitive=True))
        # print(ta.avg_word_length())
        #ta.plot_char_distibution(letters_only=True)
        #print(ta.positivity())
        #print(ta.common_words(minlen=11))
        #print(ta.common_words())
        #ta = TextAnalyzer(path)
        #print(ta.distinct_word_case(maxlen=5, letter='A'))
        print(len(ta.any_count(count = 1)))


if __name__ == '__main__':
    TextAnalyzer.main()
