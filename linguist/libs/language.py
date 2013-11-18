# -*- coding: utf-8 -*-

import re
import urllib
from os.path import realpath, dirname, basename, splitext, join
from collections import defaultdict

import yaml
from pygments import lexers
from pygments import highlight
from pygments.formatters import HtmlFormatter

from classifier import Classifier
from samples import DATA

DIR = dirname(realpath(__file__))
POPULAR_PATH = join(DIR, "popular.yml")
LANGUAGES_PATH = join(DIR, "languages.yml")

POPULAR = yaml.load(open(POPULAR_PATH))
LANGUAGES = yaml.load(open(LANGUAGES_PATH))


class ItemMeta(type):
    def __getitem__(cls, item):
        return cls.find_by_name(item)


class Language(object):
    """
    Language names that are recognizable by GitHub. Defined languages
    can be highlighted, searched and listed under the Top Languages page.

    Languages are defined in `lib/linguist/languages.yml`.
    """

    __metaclass__ = ItemMeta
    languages = []
    index = {}
    name_index = {}
    alias_index = {}
    extension_index = defaultdict(list)
    filename_index = defaultdict(list)
    primary_extension_index = {}

    _colors = []
    _ace_modes = []

    # Valid Languages types
    TYPES = ('data', 'markup', 'programming')

    @staticmethod
    def detectable_markup():
        # Names of non-programming languages that we will still detect
        # Returns an array
        return ["CSS", "Less", "Sass", "TeX"]

    @classmethod
    def create(cls, attributes={}):
        language = cls(attributes)
        cls.languages.append(language)

        # All Language names should be unique. Raise if there is a duplicate.
        if language.name in cls.name_index:
            raise ValueError("Duplicate language name: %s" % language.name)
        # Language name index
        name = language.name
        cls.index[name] = cls.name_index[name] = language
        cls.index[name.lower()] = cls.name_index[name.lower()] = language

        # All Language aliases should be unique.
        # Raise if there is a duplicate.
        for name in language.aliases:
            if name in cls.alias_index:
                raise ValueError("Duplicate alias: %s " % name)
            cls.index[name] = cls.alias_index[name] = language

        for extension in language.extensions:
            if not extension.startswith('.'):
                raise ValueError("Extension is missing a '.': %s" % extension)
            cls.extension_index[extension].append(language)

        if language.primary_extension in cls.primary_extension_index:
            raise ValueError("Duplicate primary extension: %s" % language.primary_extension)
        cls.primary_extension_index[language.primary_extension] = language

        for filename in language.filenames:
            cls.filename_index[filename].append(language)
        return language

    def __init__(self, attributes={}):
        # name is required
        if 'name' not in attributes:
            raise KeyError('missing name')
        self.name = attributes['name']

        # Set type
        self.type = attributes.get('type')
        if self.type and self.type not in self.TYPES:
            raise ValueError('invalid type: %s' % self.type)

        self.color = attributes['color']

        # Set aliases
        aliases = attributes.get('aliases', [])
        self.aliases = [self.default_alias_name] + aliases

        # Lookup Lexer object
        lexer = attributes.get('lexer') or self.name
        self.lexer = lexers.find_lexer_class(lexer)
        if not self.lexer:
            raise TypeError('%s is missing lexer' % self.name)

        self.ace_mode = attributes['ace_mode']
        self.wrap = attributes.get('wrap') or False

        # Set legacy search term
        self.search_term = attributes.get('search_term') or self.default_alias_name

        # Set extensions or default to [].
        self.extensions = attributes.get('extensions', [])
        self.filenames = attributes.get('filenames', [])

        self.primary_extension = attributes.get('primary_extension')
        if not self.primary_extension:
            raise KeyError('%s is missing primary extension' % self.name)

        # Prepend primary extension unless its already included
        if self.primary_extension not in self.extensions:
            self.extensions = [self.primary_extension] + self.extensions

        # Set popular, and searchable flags
        self.popular = attributes.get('popular', False)
        self.searchable = attributes.get('searchable', True)

        # If group name is set, save the name so we can lazy load it later
        group_name = attributes.get('group_name')
        if group_name:
            self._group = None
            self.group_name = group_name
        else:
            self._group = self

    def __repr__(self):
        return '<Language name:%s>' % self.name

    def __eq__(self, target):
        return self.name == target.name and self.extensions == target.extensions

    @classmethod
    def find_by_name(cls, name):
        """
        Public: Look up Language by its proper name.

        name - The String name of the Language

         Examples

           Language.find_by_name('Ruby')
           # => #<Language name:"Ruby">

        Returns the Language or nil if none was found.
        """
        return cls.name_index.get(name) or cls.find_by_alias(name)

    @classmethod
    def find_by_filename(cls, filename):
        """
        Public: Look up Languages by filename.
        filename - The path String.

        Examples
          Language.find_by_filename('foo.rb')
          # => [#<Language name:"Ruby">]

        Returns all matching Languages or [] if none were found.
        """
        name, extname = basename(filename), splitext(filename)[1]

        lang = cls.primary_extension_index.get(extname)
        langs = lang and [lang] or []
        langs.extend(cls.filename_index.get(name, []))
        langs.extend(cls.extension_index.get(extname, []))
        return list(set(langs))

    @classmethod
    def find_by_alias(cls, name):
        """
        Public: Look up Language by one of its aliases.

        name - A String alias of the Language

        Examples

          Language.find_by_alias('cpp')
          # => #<Language name:"Ruby">

        Returns the Language or nil if none was found.
        """
        return cls.alias_index.get(name)

    @classmethod
    def colors(cls):
        if cls._colors:
            return cls._colors
        cls._colors = sorted(filter(lambda l: l.color, cls.all()), key=lambda l: l.name.lower())
        return cls._colors

    @classmethod
    def ace_modes(cls):
        if cls._ace_modes:
            return cls._ace_modes
        cls._ace_modes = sorted(filter(lambda l: l.ace_mode, cls.all()), key=lambda l: l.name.lower())
        return cls._ace_modes

    @classmethod
    def all(cls):
        """
        Public: Get all Languages
        Returns an Array of Languages
        """
        return cls.languages

    @classmethod
    def detect(cls, name, data, mode=None):
        """
        Public: Detects the Language of the blob.

          name - String filename
          data - String blob data. A block also maybe passed in for lazy
                 loading. This behavior is deprecated and you should
                 always pass in a String.
          mode - Optional String mode (defaults to nil)

        Returns Language or nil.

        A bit of an elegant hack. If the file is executable but
        extensionless, append a "magic" extension so it can be
        classified with other languages that have shebang scripts.
        """
        extname = splitext(name)[1]
        if not extname and mode and (int(mode, 8) & 05 == 05):
            name += ".script!"

        possible_languages = cls.find_by_filename(name)

        if not possible_languages:
            return

        if len(possible_languages) == 1:
            return possible_languages[0]

        data = data() if callable(data) else data
        if data is None or data == "":
            return

        _pns = [p.name for p in possible_languages]
        result = Classifier.classify(DATA, data, _pns)
        if result:
            return cls[result[0][0]]

    def colorize(self, text, options={}):
        return highlight(text, self.lexer(), HtmlFormatter(**options))

    @property
    def group(self):
        return self._group or self.find_by_name(self.group_name)

    @property
    def is_popular(self):
        """
        Is it popular?
        Returns true or false
        """
        return self.popular

    @property
    def is_unpopular(self):
        """
        Is it not popular?
        Returns true or false
        """
        return not self.popular

    @property
    def is_searchable(self):
        """
        Is it searchable?

        Unsearchable languages won't by indexed by solr and won't show
        up in the code search dropdown.

        Returns true or false
        """
        return self.searchable

    @property
    def default_alias_name(self):
        """
        Internal: Get default alias name
        Returns the alias name String
        """
        return re.sub('\s', '-', self.name.lower())

    @property
    def escaped_name(self):
        """
        Public: Get URL escaped name.

        Examples:
          "C%23"
          "C%2B%2B"
          "Common%20Lisp"

        Returns the escaped String.
        """
        return urllib.quote(self.name, '')

extensions = DATA['extnames']
filenames = DATA['filenames']
popular = POPULAR

for name, options in sorted(LANGUAGES.iteritems(), key=lambda k: k[0]):
    options['extensions'] = options.get('extensions', [])
    options['filenames'] = options.get('filenames', [])

    def _merge(data, item_name):
        items = data.get(name, [])
        for item in items:
            if item not in options[item_name]:
                options[item_name].append(item)

    _merge(extensions, 'extensions')
    _merge(filenames, 'filenames')

    Language.create(dict(name=name,
                         color=options.get('color'),
                         type=options.get('type'),
                         aliases=options.get('aliases', []),
                         lexer=options.get('lexer'),
                         ace_mode=options.get('ace_mode'),
                         wrap=options.get('wrap'),
                         group_name=options.get('group'),
                         searchable=options.get('searchable', True),
                         search_term=options.get('search_term'),
                         extensions=sorted(options['extensions']),
                         primary_extension=options.get('primary_extension'),
                         filenames=options['filenames'],
                         popular=name in popular))
