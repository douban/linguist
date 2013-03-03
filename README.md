linguist
========

Language Savant 

## Generated

```python
from libs.generated import Generated
# Generated.is_generated(file_name, file_data or get_file_data_func)
# => False or True
Generated.is_generated('test.js', 'js file content')
Generated.is_generated('test.xib', open('test.xib').read)
```

## Language

```python
from libs.language import Language
# Language.detect(file_name, file_data or get_file_data_func, file_mode=None)
# => <Language name:Language> or None
Language.detect('a.py', 'from datetime import datetime\nprint datetime.now()')
```

## Classifier

```python
from libs.samples import DATA
from libs.classifier import Classifier
# db   - Hash of classifer tokens database.
# data - Array of tokens or String data to analyze.
# languages - Array of language name Strings to restrict to.
# Classifier.classify(db, data, languages=[])
# => [('Python', 0.52), ('Ruby', 0.22), ..]
Classifier.classify(DATA, 'def a; end')
```
