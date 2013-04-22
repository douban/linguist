# -*- coding: utf-8 -*-
import os
import re
from collections import defaultdict
from functools import partial

from file_blob import FileBlob

STARTS_WITH_DOT_REGEX = re.compile('\.[^/]')

class Repository(object):
    """
    A Repository is an abstraction of a Grit::Repo or a basic file
    system tree. It holds a list of paths pointing to Blobish objects.

    Its primary purpose is for gathering language statistics across
    the entire project.
    """

    def __init__(self, enum):
        """
        Public: Initialize a new Repository

        enum - Enumerator that responds to `each` and
            yields Blob objects

        Returns a Repository
        """
        self.enum = enum
        self.computed_stats = False
        self._language = self._size = None
        self.sizes = defaultdict(int)

    def __repr__(self):
        return '<Repository computed_stats:%s>' % self.computed_stats

    @classmethod
    def from_directory(cls, base_path):
        """
        Public: Initialize a new Repository from a File directory

        base_path - A path String

        Returns a Repository
        """
        blob = partial(FileBlob, base_path=base_path)
        enum = map(blob, cls.get_files(base_path))
        return cls(enum)

    @staticmethod
    def get_files(base_path):
        for root, dirs, files in os.walk(base_path):
            if STARTS_WITH_DOT_REGEX.search(root):
                continue
            for f in files:
                if f.startswith('.'):
                    continue
                yield os.path.join(root, f)

    @property
    def languages(self):
        """
        Public: Returns a breakdown of language stats.

          Examples

            # => { Language['Ruby'] => 46319,
                   Language['JavaScript'] => 258 }

          Returns a Hash of Language keys and Integer size values.
        """
        self.compute_stats
        return self.sizes

    @property
    def language(self):
        """
        Public: Get primary Language of repository.

        Returns a Language
        """
        self.compute_stats
        return self._language

    @property
    def size(self):
        """
        Public: Get the total size of the repository.

        Returns a byte size Integer
        """
        self.compute_stats
        return self._size

    @property
    def compute_stats(self):
        """
        Internal: Compute language breakdown for each blob in the Repository.

        Returns nothing
        """
        if self.computed_stats:
            return

        for blob in self.enum:
            # Skip files that are link
            if blob.is_link:
                continue

            # Skip files that are likely binary
            if blob.is_likely_binary:
                continue

            # Skip vendored or generated blobs
            if blob.is_vendored or blob.is_generated or blob.language is None:
                continue

            # Only include programming languages
            if blob.language.type == 'programming':
                self.sizes[blob.language.group] += blob.size

        # Compute total size
        self._size = reduce(lambda x, y: x+y[1], self.sizes.items(), 0)

        # Get primary language
        primary = sorted(self.sizes.items(), key=lambda t: t[1], reverse=True)
        if primary:
            self._language = primary[0][0]

        self.computed_stats = True
