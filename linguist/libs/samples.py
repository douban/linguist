# -*- coding: utf-8 -*-
import json
from os import listdir
from os.path import realpath, dirname, exists, join, splitext
from classifier import Classifier
from md5 import MD5

DIR = dirname(realpath(__file__))
ROOT = join(dirname(dirname(DIR)), "samples")
PATH = join(DIR, "samples.json")
DATA = {}

if exists(PATH):
    DATA = json.load(open(PATH))

class Samples(object):
    """
    Model for accessing classifier training data.
    """

    def __repr__(self):
        return '<Samples>'

    @classmethod
    def generate(self):
        data = self.data()
        json.dump(data, open(PATH, 'w'), indent=2)

    @classmethod
    def each(cls, func):
        for category in listdir(ROOT):
            if category in ('Binary', 'Text'):
                continue
            dirname = join(ROOT, category)
            for filename in listdir(dirname):
                if filename == 'filenames':
                    subdirname = join(dirname, filename)
                    for subfilename in listdir(subdirname):
                        func({'path': join(subdirname, subfilename),
                                'language': category,
                                'filename': subfilename})
                else:
                    _extname = splitext(filename)[1]
                    if _extname == '':
                        raise '%s is missing an extension, maybe it belongs in filenames/subdir' % (join(dirname, filename))
                    path = join(dirname, filename)
                    func({'path': join(dirname, filename),
                            'language': category,
                            'extname': _extname})


    @classmethod
    def data(cls):
        """
        Public: Build Classifier from all samples.

        Returns trained Classifier.
        """
        db = {}
        db['extnames'] = {}
        db['filenames'] = {}

        def _learn(sample):
            _extname = sample.get('extname')
            _filename = sample.get('filename')
            _langname = sample['language']

            if _extname:
                db['extnames'][_langname] = db['extnames'].get(_langname, [])
                if _extname not in db['extnames'][_langname]:
                    db['extnames'][_langname].append(_extname)
                    db['extnames'][_langname].sort()

            if _filename:
                db['filenames'][_langname] = db['filenames'].get(_langname, [])
                db['filenames'][_langname].append(_filename)
                db['filenames'][_langname].sort()

            data = open(sample['path']).read()
            Classifier.train(db, _langname, data)

        cls.each(_learn)

        db['md5'] = MD5.hexdigest(db)
        return db
