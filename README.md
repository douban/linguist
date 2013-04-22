Linguist
========

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

Linguist defines the list of all languages known to GitHub in a [yaml file](https://github.com/liluo/linguist/blob/master/linguist/libs/languages.yml). In order for a file to be highlighted, a language and lexer must be defined there.

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

The actual syntax highlighting is handled by our Pygments wrapper, [pygments](https://bitbucket.org/birkenfeld/pygments-main). It also provides a Lexer abstraction that determines which highlighter should be used on a file.

We typically run on a pre-release version of Pygments, pygments.rb, to get early access to new lexers. The languages.yml file is a dump of the lexers we have available on our server.

#### Stats

The Language Graph you see on every repository is built by aggregating the languages of all repo's blobs.

The repository stats API can be used on a directory:

```python
from linguist.libs.repository import Repository

project = Repository.from_directory(".")

project.language.name #=> 'Python'

project.languages #=> defaultdict(<type 'int'>, {<Language name:Python>: 53446, <Language name:JavaScript>: 1991})

for lang, count in projects.iteritems():
    print lang.name, count
#=> Python, 53446
#=> JavaScript, 1991
```

#### Todo

These stats are also printed out by the binary. Try running `linguist` on itself.

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

__v0.0.1 [2013-04-22]__
* Release v0.0.1
