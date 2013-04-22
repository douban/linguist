# -*- coding: utf-8 -*-

import re
import urllib
import mimetypes
from os.path import realpath, dirname, splitext, basename, join, islink

import yaml
import charlockholmes
from pygments import lexers
from pygments import highlight
from pygments.formatters import HtmlFormatter

from language import Language
from generated import Generated

MEGABYTE = 1024 * 1024

DIR = dirname(realpath(__file__))
VENDOR_PATH = join(DIR, "vendor.yml")
VENDORED_PATHS = yaml.load(open(VENDOR_PATH))
VENDORED_REGEXP = re.compile('|'.join(VENDORED_PATHS))

# TODO python mimetypes 很不全
if not mimetypes.inited:
    mimetypes.init()
    mimetypes.add_type('application/x-ruby', '.rb')
    mimetypes.add_type('application/x-python', '.py')


class BlobHelper(object):
    """
    BlobHelper is a mixin for Blobish classes that respond to "name",
      "data" and "size" such as Grit::Blob.
    """

    @property
    def ext_name(self):
        """
        Public: Get the extname of the path

        Examples
          blob(name='foo.rb').extname
          # => '.rb'

        Returns a String
        """
        return splitext(self.name)[1].lower()

    @property
    def _mime_type(self):
        if hasattr(self, '__mime_type'):
            return self.__mime_type
        _type, _encoding = mimetypes.guess_type(self.name)
        self.__mime_encodeing = _encoding
        self.__mime_type = _type
        return _type

    @property
    def mime_type(self):
        """
        Public: Get the actual blob mime type

        Examples

          # => 'text/plain'
          # => 'text/html'

        Returns a mime type String.
        """
        return self._mime_type or 'text/plain'

    @property
    def is_binary_mime_type(self):
        """
        Internal: Is the blob binary according to its mime type

        Return true or false
        """
        self._mime_type
        return bool(self.__mime_encodeing)

    @property
    def is_likely_binary(self):
        """
        Internal: Is the blob binary according to its mime type,
        overriding it if we have better data from the languages.yml
        database.

        Return true or false
        """
        return self.is_binary_mime_type and not Language.find_by_filename(self.name)

    @property
    def content_type(self):
        """
        Public: Get the Content-Type header value

        This value is used when serving raw blobs.

        Examples

          # => 'text/plain; charset=utf-8'
          # => 'application/octet-stream'

        Returns a content type String.
        """
        if hasattr(self, '_content_type'):
            return self._content_type

        if self.is_binary_mime_type or self.is_binary:
            self._content_type = self.mime_type
        else:
            encoding = self.encoding
            self._content_type = "text/plain; charset=%s" % encoding.lower() if encoding else "text/plain"
        return self._content_type

    @property
    def disposition(self):
        """
        Public: Get the Content-Disposition header value

        This value is used when serving raw blobs.

          # => "attachment; filename=file.tar"
          # => "inline"

        Returns a content disposition String.
        """
        if self.is_text or self.is_image:
            return 'inline'
        elif self.name is None:
            return 'attachment'
        else:
            return 'attachment; filename=%s' % urllib.quote_plus(basename(self.name))

    @property
    def encoding(self):
        if self.detect_encoding:
            return self.detect_encoding.get('encoding')

    @property
    def detect_encoding(self):
        """
        Try to guess the encoding

        Returns: a hash, with :encoding, :confidence, :type
                 this will return nil if an error occurred during detection or
                 no valid encoding could be found
        """
        if hasattr(self, '_detect_encoding'):
            return self._detect_encoding

        if self.data:
            self._detect_encoding = charlockholmes.detect(self.data)
        return self._detect_encoding

    @property
    def is_image(self):
        """
        Public: Is the blob a supported image format?

        Return true or false
        """
        return self.ext_name in ('.png', '.jpg', '.jpeg', '.gif')

    @property
    def is_solid(self):
        """
        Public: Is the blob a support 3D model format?

        Return true or false
        """
        return self.ext_name in ('.stl', '.obj')

    @property
    def is_pdf(self):
        """
        Public: Is the blob a supported 3D model format?

        Return true or false
        """
        return self.ext_name == '.pdf'

    @property
    def is_text(self):
        """
        Public: Is the blob text?

        Return true or false
        """
        return not self.is_binary

    @property
    def is_binary(self):
        if self.data is None:
            # Large blobs aren't even loaded into memory
            return True
        elif self.data == "":
            # Treat blank files as text
            return False
        elif self.encoding is None:
            # Charlock doesn't know what to think
            return True
        else:
            # If Charlock says its binary
            return self.detect_encoding.get('type') == 'binary'

    @property
    def is_large(self):
        """
        Public: Is the blob too big to load?

        Return false or true
        """
        return self.size > MEGABYTE

    @property
    def loc(self):
        """
        Public: Get number of lines of code

        Requires Blob#data

        Returns Integer
        """
        return len(self.lines)

    @property
    def sloc(self):
        """
        Public: Get number of source lines of code

        Requires Blob#data

        Returns Integer
        """
        return len(filter(re.compile('\S').match, self.lines))

    @property
    def is_safe_to_colorize(self):
        """
        Public: Is the blob safe to colorize?

        We use Pygments.rb for syntax highlighting blobs, which
        has some quirks and also is essentially 'un-killable' via
        normal timeout.  To workaround this we try to
        carefully handling Pygments.rb anything it can't handle.

        Return true or false
        """
        return not self.is_large and self.is_text and not self.is_high_ratio_of_long_lines

    @property
    def is_high_ratio_of_long_lines(self):
        """
        Internal: Does the blob have a ratio of long lines?
        These types of files are usually going to make Pygments.rb
        angry if we try to colorize them.

        Return true or false
        """
        if self.loc == 0:
            return False
        return self.size / self.loc > 5000

    @property
    def is_viewable(self):
        """
        Public: Is the blob viewable?

        Non-viewable blobs will just show a "View Raw" link

        Return true or false
        """
        return not self.is_large and self.is_text

    @property
    def is_vendored(self):
        """
        Public: Is the blob in a vendored directory?

        Vendored files are ignored by language statistics.

        See "vendor.yml" for a list of vendored conventions that match
        this pattern.

        Return true or false
        """
        if VENDORED_REGEXP.search(self.name):
            return True

    @property
    def lines(self):
        """
        Public: Get each line of data

        Requires Blob#data

        Returns an Array of lines
        """
        if hasattr(self, '_lines'):
            return self._lines
        if self.is_viewable and self.data:
            self._lines = self.data.split(self.line_split_character, -1)
        else:
            self._lines = []
        return self._lines

    @property
    def line_split_character(self):
        """
        Character used to split lines. This is almost always "\n" except when Mac
        Format is detected in which case it's "\r".

        Returns a split pattern string.
        """
        if hasattr(self, '_line_split_character'):
            return self._line_split_character
        if self.is_mac_format:
            self._line_split_character = '\r'
        else:
            self._line_split_character = '\n'
        return self._line_split_character

    @property
    def is_mac_format(self):
        """
        Public: Is the data in ** Mac Format **. This format uses \r (0x0d) characters
        for line ends and does not include a \n (0x0a).

        Returns true when mac format is detected.
        """
        if not self.is_viewable:
            return

        data = self.data[0:4096]
        if '\r' in data:
            pos = data.index('\r')
            return data[pos + 1] != '\n'

    @property
    def is_generated(self):
        """
        Public: Is the blob a generated file?

        Generated source code is suppressed in diffs and is ignored by
        language statistics.

        May load Blob#data

        Return true or false
        """
        if hasattr(self, '_is_generated'):
            return self._is_generated

        def _data_func():
            return self.data

        self._is_generated = Generated.is_generated(self.name, _data_func)
        return self._is_generated

    @property
    def is_indexable(self):
        """
        Public: Should the blob be indexed for searching?

        Excluded:
          - Files over 0.1MB
          - Non-text files
          - Languages marked as not searchable
          - Generated source files

        Please add additional test coverage to
        `test/test_blob.rb#test_indexable` if you make any changes.

        Return true or false
        """
        if self.size > 100 * 1024:
            return False
        elif self.is_binary:
            return False
        elif self.ext_name == '.txt':
            return True
        elif self.language is None:
            return False
        elif not self.language.is_searchable:
            return False
        elif self.is_generated:
            return False
        else:
            return False

    @property
    def is_link(self):
        return islink(self.path)

    @property
    def language(self):
        """
        Public: Detects the Language of the blob.

        May load Blob#data

        Returns a Language or nil if none is detected
        """
        if hasattr(self, '_language'):
            return self._language

        def data():
            if self.is_binary_mime_type or self.is_binary:
                return ''
            return self.data
        self._language = Language.detect(self.name, data, self.mode)
        return self._language

    @property
    def lexer(self):
        """
        Internal: Get the lexer of the blob.

        Returns a Lexer.
        """
        return self.language.lexer if self.language else lexers.find_lexer_class('Text only')

    def colorize(self, options={}):
        """
        Public: Highlight syntax of blob

        options - A Hash of options (defaults to {})

        Returns html String
        """
        if not self.is_safe_to_colorize:
            return
        return highlight(self.data, self.lexer(), HtmlFormatter(**options))

    def colorize_without_wrapper(self, options={}):
        """
        Public: Highlight syntax of blob without the outer highlight div
        """
        text = self.colorize(options)
        if text:
            ret = re.compile(r'<div class="highlight"><pre>(.*?)<\/pre>\s*<\/div>', re.DOTALL).match(text)
            if ret:
                ret = ret.group(1)
        else:
            ret = ''
        return ret
