# -*- coding: utf-8 -*-
import re
import json
from os import listdir
from os.path import realpath, dirname, exists, join, splitext
from collections import defaultdict

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
    def generate(cls):
        data = cls.data()
        json.dump(data, open(PATH, 'w'), indent=2)

    @classmethod
    def each(cls, func):
        for category in listdir(ROOT):
            if category in ('Binary', 'Text'):
                continue
            dir_name = join(ROOT, category)
            for filename in listdir(dir_name):
                if filename == 'filenames':
                    subdirname = join(dir_name, filename)
                    for subfilename in listdir(subdirname):
                        func({'path': join(subdirname, subfilename),
                              'language': category,
                              'filename': subfilename})
                else:
                    _extname = splitext(filename)[1]
                    path = join(dir_name, filename)
                    interpreter = (
                        cls.interpreter_from_shebang(open(path).read())
                        if exists(path) else None
                    )
                    if _extname == '':
                        raise '%s is missing an extension, maybe it ' \
                              'belongs in filenames/subdir' % path
                    func({'path': path,
                          'language': category,
                          'interpreter': interpreter,
                          'extname': _extname})

    @classmethod
    def data(cls):
        """
        Public: Build Classifier from all samples.

        Returns trained Classifier.
        """
        db = {'extnames': defaultdict(list),
              'filenames': defaultdict(list),
              'interpreters': defaultdict(list)}

        def _learn(sample):
            _extname = sample.get('extname')
            _filename = sample.get('filename')
            _interpreter = sample.get('interpreter')
            _langname = sample['language']

            if _extname:
                if _extname not in db['extnames'][_langname]:
                    db['extnames'][_langname].append(_extname)
                    db['extnames'][_langname].sort()

            if _filename:
                db['filenames'][_langname].append(_filename)
                db['filenames'][_langname].sort()

            if _interpreter:
                if not _langname in db['interpreters']:
                    db['interpreters'][_langname] = []
                db['interpreters'][_langname].append(_interpreter)
                db['interpreters'][_langname].sort()

            data = open(sample['path']).read()
            Classifier.train(db, _langname, data)

        cls.each(_learn)

        db['md5'] = MD5.hexdigest(db)
        return db

    @staticmethod
    def interpreter_from_shebang(data):
        """
        Used to retrieve the interpreter from the shebang line of a file's
        data.
        """
        script = None
        lines = data.split('\n')

        if lines and lines[0].startswith('#!'):
            shebang = lines[0]
            shebang = shebang.replace('#! ', '#!')
            tokens = shebang.split(' ')
            pieces = tokens[0].split('/')

            if len(pieces) > 1:
                script = pieces[-1]
            else:
                script = tokens[0][2:]

            script = tokens[1] if script == 'env' else script

            # "python2.6" -> "python"
            version = re.search('((?:\d+\.?)+)', script)
            if version:
                script = script.replace(version.group(0), '')

            # Check for multiline shebang hacks that call `exec`
            if script == 'sh':
                exec_lines = lines[0:5]
                for exec_line in exec_lines:
                    match = re.match(r'exec (\w+).+\$0.+\$@', exec_line)
                    if match:
                        script = match.group(1)
                        break

        return script
