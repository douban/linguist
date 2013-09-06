# -*- coding: utf-8 -*-

import re
import urllib
from os.path import realpath, dirname, splitext, basename, join

import yaml
import mime
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


class BlobHelper(object):
    """
    DEPRECATED Avoid mixing into Blob classes. Prefer functional interfaces
    like `Language.detect` over `Blob#language`. Functions are much easier to
    cache and compose.

    Avoid adding additional bloat to this module.

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
        guesses = mime.Types.of(self.name)
        mimetypes = [mt for mt in guesses if mt.is_ascii]
        if mimetypes:
            self.__mime_type = mimetypes[0]
        elif guesses:
            self.__mime_type = guesses[0]
        else:
            self.__mime_type = None
        return self.__mime_type

    @property
    def mime_type(self):
        """
        Public: Get the actual blob mime type

        Examples

          # => 'text/plain'
          # => 'text/html'

        Returns a mime type String.
        """
        return self._mime_type.to_s if self._mime_type else 'text/plain'

    @property
    def is_binary_mime_type(self):
        """
        Internal: Is the blob binary according to its mime type

        Return true or false
        """
        return self._mime_type.is_binary if self._mime_type else False

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
        return self.ext_name == '.stl'

    @property
    def is_pdf(self):
        """
        Public: Is the blob a supported 3D model format?

        Return true or false
        """
        return self.ext_name == '.pdf'

    @property
    def is_csv(self):
        """
        Public: Is this blob a CSV file?

        Return true or false
        """
        return self.is_text and self.ext_name == '.csv'

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
        return len(filter(re.compile('\S').search, self.lines))

    @property
    def is_safe_to_colorize(self):
        """
        Public: Is the blob safe to colorize?

        We use Pygments for syntax highlighting blobs. Pygments
        can be too slow for very large blobs or for certain
        corner-case blobs.

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
            self._lines = re.split('\r\n|\r|\n', self.data)
        else:
            self._lines = []
        return self._lines

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
    def language(self):
        """
        Public: Detects the Language of the blob.

        May load Blob#data

        Returns a Language or nil if none is detected
        """
        if hasattr(self, '_language'):
            return self._language

        _data = getattr(self, '_data', False)
        if _data and isinstance(_data, basestring):
            data = _data
        else:
            data = lambda: '' if (self.is_binary_mime_type or self.is_binary) else self.data
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
