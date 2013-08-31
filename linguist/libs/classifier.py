# -*- coding: utf-8 -*-
import os
import sys
import math
from functools import partial

is_py27 = sys.version_info >= (2, 7)
if is_py27:
    from collections import Counter
from tokenizer import Tokenizer


class Classifier(object):
    """ Language bayesian classifier. """

    verbosity = int(os.environ.get('LINGUIST_DEBUG', '0'))

    @classmethod
    def train(cls, db, language, data):
        """
        Set LINGUIST_DEBUG=1 or =2 to see probabilities per-token,
        per-language.  See also dump_all_tokens, below.

        Public: Train classifier that data is a certain language.

          db       - Hash classifier database object
          language - String language of data
          data     - String contents of file

          Examples

            Classifier.train(db, 'Ruby', "def hello; end")

          Returns nothing.
        """
        tokens = Tokenizer.tokenize(data)
        db['tokens_total'] = db.get('tokens_total', 0)
        db['languages_total'] = db.get('languages_total', 0)
        db['tokens'] = db.get('tokens', {})
        db['language_tokens'] = db.get('language_tokens', {})
        db['languages'] = db.get('languages', {})

        for token in tokens:
            db['tokens'][language] = db['tokens'].get(language, {})
            db['tokens'][language][token] = db['tokens'][language].get(token, 0)
            db['tokens'][language][token] += 1
            db['language_tokens'][language] = db['language_tokens'].get(language, 0)
            db['language_tokens'][language] += 1
            db['tokens_total'] += 1

        db['languages'][language] = db['languages'].get(language, 0)
        db['languages'][language] += 1
        db['languages_total'] += 1

    def __init__(self, db={}):
        self.tokens = db.get('tokens')
        self.tokens_total = db.get('tokens_total')
        self.languages = db.get('languages')
        self.languages_total = db.get('languages_total')
        self.language_tokens = db.get('language_tokens')

    def __repr__(self):
        return '<Classifier>'

    @classmethod
    def classify(cls, db, tokens, languages=[]):
        """
        Public: Guess language of data.

        db        - Hash of classifer tokens database.
        data      - Array of tokens or String data to analyze.
        languages - Array of language name Strings to restrict to.

        Examples

          Classifier.classify(db, "def hello; end")
          # => [ 'Ruby', 0.90], ['Python', 0.2], ... ]

        Returns sorted Array of result pairs. Each pair contains the
        String language name and a Float score.
        """
        languages = languages or db.get('languages', {}).keys()
        return cls(db)._classify(tokens, languages)

    def _classify(self, tokens, languages):
        """
        Internal: Guess language of data

        data      - Array of tokens or String data to analyze.
        languages - Array of language name Strings to restrict to.

        Returns sorted Array of result pairs. Each pair contains the
        String language name and a Float score.
        """
        if tokens is None:
            return []

        if isinstance(tokens, basestring):
            tokens = Tokenizer.tokenize(tokens)

        scores = {}
        if self.verbosity >= 2:
            self.dump_all_tokens(tokens, languages)
        for language in languages:
            scores[language] = self.tokens_probability(tokens, language) + self.language_probability(language)
            if self.verbosity >= 1:
                print '%10s = %10.3f + %7.3f = %10.3f\n' % (language,
                                                            self.tokens_probability(tokens, language),
                                                            self.language_probability(language),
                                                            scores[language])
        return sorted(scores.iteritems(), key=lambda t: t[1], reverse=True)

    def tokens_probability(self, tokens, language):
        """
        Internal: Probably of set of tokens in a language occuring - P(D | C)

        tokens   - Array of String tokens.
        language - Language to check.

        Returns Float between 0.0 and 1.0.
        """
        token_probability = partial(self.token_probability, language=language)
        return reduce(lambda x, y: x + math.log(token_probability(y)), tokens, 0.0)

    def token_probability(self, token, language=''):
        """
        Internal: Probably of token in language occuring - P(F | C)

        token    - String token.
        language - Language to check.

        Returns Float between 0.0 and 1.0.
        """
        probability = float(self.tokens.get(language, {}).get(token, 0))
        if probability == 0.0:
            return 1 / float(self.tokens_total)
        else:
            return probability / float(self.language_tokens[language])

    def language_probability(self, language):
        """
        Internal: Probably of a language occuring - P(C)

        language - Language to check.

        Returns Float between 0.0 and 1.0.
        """
        return math.log(float(self.languages[language]) / float(self.languages_total))

    def dump_all_tokens(self, tokens, languages):
        """
        Internal: show a table of probabilities for each <token,language> pair.

        The number in each table entry is the number of "points" that each
        token contributes toward the belief that the file under test is a
        particular language.  Points are additive.

        Points are the number of times a token appears in the file, times
        how much more likely (log of probability ratio) that token is to
        appear in one language vs.  the least-likely language.  Dashes
        indicate the least-likely language (and zero points) for each token.
        """
        maxlen = max([len(token) for token in tokens])

        print '%ss' % maxlen
        print '    #' + ''.join(['%10s' for lang in languages])

        if not is_py27:
            return

        tokmap = Counter(tokens)
        for tok, count in tokmap.most_common():
            arr = [(lang, self.token_probability(tok, lang)) for lang in languages]
            minlen = min([n for lang, n in arr])
            minlog = math.log(minlen)

            if not reduce(lambda x, y: x and y[1] == arr[0][1], arr, True):
                print '%*s%5d' % (maxlen, tok, count)

                for ent in arr:
                    if ent[1] == minlen:
                        print '         -'
                    else:
                        print '%10.3f' % (math.log(ent[1]) - minlog)
