Linguist
========
[![Build Status](https://travis-ci.org/liluo/linguist.png)](https://travis-ci.org/liluo/linguist)

Language Savant, Python clone of [github/linguist](https://github.com/github/linguist/).

## Installation

PIP
```bash
pip install linguist
```

Easy_install
```bash
easy_install linguist
```

## Features

#### Language detection

Linguist defines the list of all languages known in a [yaml file](https://github.com/liluo/linguist/blob/master/linguist/libs/languages.yml). In order for a file to be highlighted, a language and lexer must be defined there.

Most languages are detected by their file extension. This is the fastest and most common situation.

For disambiguating between files with common extensions, we use a [Bayesian classifier](https://github.com/liluo/linguist/blob/master/linguist/libs/classifier.py). For an example, this helps us tell the difference between `.h` files which could be either C, C++, or Obj-C.

For testing, there is a simple FileBlob API:

```python
from linguist.libs.file_blob import FileBlob

FileBlob('test.py').language.name #=> 'Python'

FileBlob('test_file').language.name #=> 'Python'
```

See [linguist/libs/language.py](https://github.com/liluo/linguist/blob/master/linguist/libs/language.py) and [lib/linguist/languages.yml](https://github.com/liluo/linguist/blob/master/linguist/libs/languages.yml).


#### Syntax Highlighting

The actual syntax highlighting is handled by [pygments](https://bitbucket.org/birkenfeld/pygments-main). It also provides a Lexer abstraction that determines which highlighter should be used on a file.

#### Stats

The Language Graph you see on every repository is built by aggregating the languages of all repo's blobs.

The repository stats API can be used on a directory:

```python
from linguist.libs.repository import Repository

project = Repository.from_directory(".")

project.language.name #=> 'Python'

project.languages #=> defaultdict(<type 'int'>, {<Language name:Python>: 53446, <Language name:JavaScript>: 1991})

for lang, count in projects.languages.iteritems():
    print lang.name, count
#=> Python, 53446
#=> JavaScript, 1991
```

These stats are also printed out by the binary. Try running `pylinguist [dir_path|file_path]`:

```bash
$ pylinguist ~/douban/proj/code/
60.8% JavaScript
39.1% Python
0.1% Shell

$ pylinguist static/js/lib/jquery.min.js
static/js/lib/jquery.min.js: 2 lines (2 sloc)
  type: Text
  language: JavaScript
  appears to be generated source code
  appears to be a vendored file

$ pylinguist config.py
config.py: 34 lines (23 sloc)
  type: Text
  language: Python
```

#### Ignore vendored files

Checking other code into your git repo is a common practice. But this often inflates your project's language stats and may even cause your project to be labeled as another language. We are able to identify some of these files and directories and exclude them.

```python
from linguist.libs.file_blob import FileBlob

FileBlob('static/js/jquery-2.0.0.min.js').is_vendored #=> True
```

See [BlobHelper#is_vendored](https://github.com/liluo/linguist/blob/master/linguist/libs/blob_helper.py#L279) and [linguist/libs/vendor.yml](https://github.com/liluo/linguist/blob/master/linguist/libs/vendor.yml).

#### Generated file detection

```python
from linguist.libs.file_blob import FileBlob

FileBlob('jquery-2.0.0.min.js').is_generated #=> True
FileBlob('app.coffee').is_generated #=> True
```

See [Generated#is_generated](https://github.com/liluo/linguist/blob/master/linguist/libs/generated.py).


## Contributing

```bash
* Fork the repository.
* Create a topic branch.
* Implement your feature or bug fix.
* Add, commit, and push your changes.
* Submit a pull request.
```

#### Testing

```bash
cd tests/
python run.py
```

## Changelog

__v0.1.1 [2014-11-03]__
* Updated require Pygments

__v0.1.0 [2013-11-19]__
* Better performance, create && require scanner
* Sync the latest version of github/linguist
* Using MIME Types, create && require mime
* Compatible github custom lexers, create && require pygments-github-lexers

__v0.0.3 [2013-05-20]__
* Bugfix: ignore dir if dir.startswith('.')

__v0.0.2 [2013-04-25]__
* Added script `pylinguist`
* Disable detech unknown ext file
* Bugfix count blob sloc
* Added some unittest

__v0.0.1 [2013-04-22]__
* Release v0.0.1
