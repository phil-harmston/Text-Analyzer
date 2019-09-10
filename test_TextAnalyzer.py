import unittest
from TextAnalyzer import TextAnalyzer


url = 'https://www.webucator.com/how-to/address-by-bill-clinton-1997.cfm'
path = 'pride-and-prejudice.txt'
text = '''The outlook wasn't brilliant for the Mudville Nine that day;
the score stood four to two, with but one inning more to play.
And then when Cooney died at first, and Barrows did the same,
a sickly silence fell upon the patrons of the game.'''


class TestTextAnalyzer(unittest.TestCase):
    def test_discover_url(self):
         ta = TextAnalyzer(url)
         self.assertEqual(ta._src_type, 'url')


    def test_discover_path(self):
         ta = TextAnalyzer(path)
         self.assertEqual(ta._src_type, 'path')

    def test_discover_text(self):
         ta = TextAnalyzer(text)
         self.assertEqual(ta._src_type, 'text')

    def test_set_content_to_tag(self):
        ta = TextAnalyzer(url)
        ta.set_content_to_tag('div', 'content-main')
        self.assertEqual(ta._content[0:25], '\n\nAddress by Bill Clinton')

    def test_reset_content(self):
        ta = TextAnalyzer(url)
        ta.set_content_to_tag('div', 'content-main')
        ta.reset_content()
        self.assertEqual(ta._content[0], '<')

    # def test_common_words(self):
    #     ta = TextAnalyzer(path, src_type='path')
    #     common_words = ta.common_words(minlen=5, maxlen=10)
    #     liz = common_words[0]
    #     self.assertEqual(liz[0], 'ELIZABETH')
    #
    # def test_avg_word_length(self):
    #     ta = TextAnalyzer(text, src_type='text')
    #     self.assertEqual(ta.avg_word_length, 4.16)
    #
    # def test_word_count(self):
    #     ta = TextAnalyzer(text, src_type='text')
    #     self.assertEqual(ta.word_count, 45)
    #
    # def test_distinct_word_count(self):
    #     ta = TextAnalyzer(text, src_type='text')
    #     self.assertEqual(ta.distinct_word_count, 38)
    #
    # def test_char_distribution(self):
    #     ta = TextAnalyzer(text, src_type='text')
    #     char_dist = ta.char_distribution(letters_only=True)
    #     self.assertEqual(char_dist[1][1], 20)
    #
    # def test_positivity(self):
    #     ta = TextAnalyzer(text, src_type='text')
    #     positivity = ta.positivity
    #     self.assertEqual(positivity, -44)


suite = unittest.TestLoader().loadTestsFromTestCase(TestTextAnalyzer)
unittest.TextTestRunner().run(suite)

if __name__=='__main__':
    unittest.main()
