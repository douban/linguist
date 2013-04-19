# -*- coding: utf-8 -*-

from pygments.lexers import find_lexer_class
from framework import LinguistTestBase, main
from libs.language import Language


colorize = """<div class="highlight"><pre><span class="k">def</span> <span class="nf">foo</span>
  <span class="s1">&#39;foo&#39;</span>
<span class="k">end</span>
</pre></div>
"""

class TestLanguage(LinguistTestBase):

    def test_lexer(self):
        assert find_lexer_class('ActionScript 3') == Language.find_by_name('ActionScript').lexer
        assert find_lexer_class('ActionScript 3') == Language.find_by_name('ActionScript').lexer
        assert find_lexer_class('Bash') == Language.find_by_name('Gentoo Ebuild').lexer
        assert find_lexer_class('Bash') == Language.find_by_name('Gentoo Eclass').lexer
        assert find_lexer_class('Bash') == Language.find_by_name('Shell').lexer
        assert find_lexer_class('C') == Language.find_by_name('OpenCL').lexer
        assert find_lexer_class('C') == Language.find_by_name('XS').lexer
        assert find_lexer_class('C++') == Language.find_by_name('C++').lexer
        assert find_lexer_class('Coldfusion HTML') == Language.find_by_name('ColdFusion').lexer
        assert find_lexer_class('Coq') == Language.find_by_name('Coq').lexer
        assert find_lexer_class('FSharp') == Language.find_by_name('F#').lexer
        assert find_lexer_class('FSharp') == Language.find_by_name('F#').lexer
        assert find_lexer_class('Fortran') == Language.find_by_name('FORTRAN').lexer
        assert find_lexer_class('Gherkin') == Language.find_by_name('Cucumber').lexer
        assert find_lexer_class('Groovy') == Language.find_by_name('Groovy').lexer
        assert find_lexer_class('HTML') == Language.find_by_name('HTML').lexer
        assert find_lexer_class('HTML+Django/Jinja') == Language.find_by_name('HTML+Django').lexer
        assert find_lexer_class('HTML+PHP') == Language.find_by_name('HTML+PHP').lexer
        assert find_lexer_class('HTTP') == Language.find_by_name('HTTP').lexer
        assert find_lexer_class('JSON') == Language.find_by_name('JSON').lexer
        assert find_lexer_class('Java') == Language.find_by_name('ChucK').lexer
        assert find_lexer_class('Java') == Language.find_by_name('Java').lexer
        assert find_lexer_class('JavaScript') == Language.find_by_name('JavaScript').lexer
        assert find_lexer_class('MOOCode') == Language.find_by_name('Moocode').lexer
        assert find_lexer_class('MuPAD') == Language.find_by_name('mupad').lexer
        assert find_lexer_class('NASM') == Language.find_by_name('Assembly').lexer
        assert find_lexer_class('OCaml') == Language.find_by_name('OCaml').lexer
        assert find_lexer_class('Ooc') == Language.find_by_name('ooc').lexer
        assert find_lexer_class('OpenEdge ABL') == Language.find_by_name('OpenEdge ABL').lexer
        assert find_lexer_class('REBOL') == Language.find_by_name('Rebol').lexer
        assert find_lexer_class('RHTML') == Language.find_by_name('HTML+ERB').lexer
        assert find_lexer_class('RHTML') == Language.find_by_name('RHTML').lexer
        assert find_lexer_class('Ruby') == Language.find_by_name('Mirah').lexer
        assert find_lexer_class('Ruby') == Language.find_by_name('Ruby').lexer
        assert find_lexer_class('S') == Language.find_by_name('R').lexer
        assert find_lexer_class('Scheme') == Language.find_by_name('Emacs Lisp').lexer
        assert find_lexer_class('Scheme') == Language.find_by_name('Nu').lexer
        assert find_lexer_class('Racket') == Language.find_by_name('Racket').lexer
        assert find_lexer_class('Scheme') == Language.find_by_name('Scheme').lexer
        assert find_lexer_class('Standard ML') == Language.find_by_name('Standard ML').lexer
        assert find_lexer_class('TeX') == Language.find_by_name('TeX').lexer
        #FIXME bug by pygments
        # assert find_lexer_class('Verilog') == Language.find_by_name('Verilog').lexer
        assert find_lexer_class('XSLT') == Language.find_by_name('XSLT').lexer
        assert find_lexer_class('aspx-vb') == Language.find_by_name('ASP').lexer
        assert find_lexer_class('haXe') == Language.find_by_name('Haxe').lexer
        assert find_lexer_class('reStructuredText') == Language.find_by_name('reStructuredText').lexer


    def test_find_by_alias(self):
        assert Language.find_by_name('ASP') == Language.find_by_alias('asp')
        assert Language.find_by_name('ASP') == Language.find_by_alias('aspx')
        assert Language.find_by_name('ASP') == Language.find_by_alias('aspx-vb')
        assert Language.find_by_name('ActionScript') == Language.find_by_alias('as3')
        assert Language.find_by_name('ApacheConf') == Language.find_by_alias('apache')
        assert Language.find_by_name('Assembly') == Language.find_by_alias('nasm')
        assert Language.find_by_name('Batchfile') == Language.find_by_alias('bat')
        assert Language.find_by_name('C#') == Language.find_by_alias('c#')
        assert Language.find_by_name('C#') == Language.find_by_alias('csharp')
        assert Language.find_by_name('C') == Language.find_by_alias('c')
        assert Language.find_by_name('C++') == Language.find_by_alias('c++')
        assert Language.find_by_name('C++') == Language.find_by_alias('cpp')
        assert Language.find_by_name('CoffeeScript') == Language.find_by_alias('coffee')
        assert Language.find_by_name('CoffeeScript') == Language.find_by_alias('coffee-script')
        assert Language.find_by_name('ColdFusion') == Language.find_by_alias('cfm')
        assert Language.find_by_name('Common Lisp') == Language.find_by_alias('common-lisp')
        assert Language.find_by_name('Common Lisp') == Language.find_by_alias('lisp')
        assert Language.find_by_name('Darcs Patch') == Language.find_by_alias('dpatch')
        assert Language.find_by_name('Dart') == Language.find_by_alias('dart')
        assert Language.find_by_name('Emacs Lisp') == Language.find_by_alias('elisp')
        assert Language.find_by_name('Emacs Lisp') == Language.find_by_alias('emacs')
        assert Language.find_by_name('Emacs Lisp') == Language.find_by_alias('emacs-lisp')
        assert Language.find_by_name('Gettext Catalog') == Language.find_by_alias('pot')
        assert Language.find_by_name('HTML') == Language.find_by_alias('html')
        assert Language.find_by_name('HTML') == Language.find_by_alias('xhtml')
        assert Language.find_by_name('HTML+ERB') == Language.find_by_alias('html+erb')
        assert Language.find_by_name('HTML+ERB') == Language.find_by_alias('erb')
        assert Language.find_by_name('IRC log') == Language.find_by_alias('irc')
        assert Language.find_by_name('JSON') == Language.find_by_alias('json')
        assert Language.find_by_name('Java Server Pages') == Language.find_by_alias('jsp')
        assert Language.find_by_name('Java') == Language.find_by_alias('java')
        assert Language.find_by_name('JavaScript') == Language.find_by_alias('javascript')
        assert Language.find_by_name('JavaScript') == Language.find_by_alias('js')
        assert Language.find_by_name('Literate Haskell') == Language.find_by_alias('lhs')
        assert Language.find_by_name('Literate Haskell') == Language.find_by_alias('literate-haskell')
        assert Language.find_by_name('Objective-C') == Language.find_by_alias('objc')
        assert Language.find_by_name('OpenEdge ABL') == Language.find_by_alias('openedge')
        assert Language.find_by_name('OpenEdge ABL') == Language.find_by_alias('progress')
        assert Language.find_by_name('OpenEdge ABL') == Language.find_by_alias('abl')
        assert Language.find_by_name('Parrot Internal Representation') == Language.find_by_alias('pir')
        assert Language.find_by_name('PowerShell') == Language.find_by_alias('posh')
        assert Language.find_by_name('Puppet') == Language.find_by_alias('puppet')
        assert Language.find_by_name('Pure Data') == Language.find_by_alias('pure-data')
        assert Language.find_by_name('Raw token data') == Language.find_by_alias('raw')
        assert Language.find_by_name('Ruby') == Language.find_by_alias('rb')
        assert Language.find_by_name('Ruby') == Language.find_by_alias('ruby')
        assert Language.find_by_name('Scheme') == Language.find_by_alias('scheme')
        assert Language.find_by_name('Shell') == Language.find_by_alias('bash')
        assert Language.find_by_name('Shell') == Language.find_by_alias('sh')
        assert Language.find_by_name('Shell') == Language.find_by_alias('shell')
        assert Language.find_by_name('Shell') == Language.find_by_alias('zsh')
        assert Language.find_by_name('TeX') == Language.find_by_alias('tex')
        assert Language.find_by_name('TypeScript') == Language.find_by_alias('ts')
        assert Language.find_by_name('VimL') == Language.find_by_alias('vim')
        assert Language.find_by_name('VimL') == Language.find_by_alias('viml')
        assert Language.find_by_name('reStructuredText') == Language.find_by_alias('rst')
        assert Language.find_by_name('YAML') == Language.find_by_alias('yml')

    def test_groups(self):
        # Test a couple identity cases
        assert Language.find_by_name('Perl') == Language.find_by_name('Perl').group
        assert Language.find_by_name('Python') == Language.find_by_name('Python').group
        assert Language.find_by_name('Ruby') == Language.find_by_name('Ruby').group

        # Test a few special groups
        assert Language.find_by_name('Assembly') == Language.find_by_name('GAS').group
        assert Language.find_by_name('C') == Language.find_by_name('OpenCL').group
        assert Language.find_by_name('Haskell') == Language.find_by_name('Literate Haskell').group
        assert Language.find_by_name('Java') == Language.find_by_name('Java Server Pages').group
        assert Language.find_by_name('Python') == Language.find_by_name('Cython').group
        assert Language.find_by_name('Python') == Language.find_by_name('NumPy').group
        assert Language.find_by_name('Shell') == Language.find_by_name('Batchfile').group
        assert Language.find_by_name('Shell') == Language.find_by_name('Gentoo Ebuild').group
        assert Language.find_by_name('Shell') == Language.find_by_name('Gentoo Eclass').group
        assert Language.find_by_name('Shell') == Language.find_by_name('Tcsh').group

        # Ensure everyone has a group
        for language in Language.all():
            assert language.group, "%s has no group" % language


    def test_search_term(self):
        assert 'perl' == Language.find_by_name('Perl').search_term
        assert 'python' == Language.find_by_name('Python').search_term
        assert 'ruby' == Language.find_by_name('Ruby').search_term
        assert 'common-lisp' == Language.find_by_name('Common Lisp').search_term
        assert 'html+erb' == Language.find_by_name('HTML+ERB').search_term
        assert 'max/msp' == Language.find_by_name('Max').search_term
        assert 'puppet' == Language.find_by_name('Puppet').search_term
        assert 'pure-data' == Language.find_by_name('Pure Data').search_term

        assert 'aspx-vb' == Language.find_by_name('ASP').search_term
        assert 'as3' == Language.find_by_name('ActionScript').search_term
        assert 'nasm' == Language.find_by_name('Assembly').search_term
        assert 'bat' == Language.find_by_name('Batchfile').search_term
        assert 'csharp' == Language.find_by_name('C#').search_term
        assert 'cpp' == Language.find_by_name('C++').search_term
        assert 'cfm' == Language.find_by_name('ColdFusion').search_term
        assert 'dpatch' == Language.find_by_name('Darcs Patch').search_term
        assert 'ocaml' == Language.find_by_name('F#').search_term
        assert 'pot' == Language.find_by_name('Gettext Catalog').search_term
        assert 'irc' == Language.find_by_name('IRC log').search_term
        assert 'lhs' == Language.find_by_name('Literate Haskell').search_term
        assert 'ruby' == Language.find_by_name('Mirah').search_term
        assert 'raw' == Language.find_by_name('Raw token data').search_term
        assert 'bash' == Language.find_by_name('Shell').search_term
        assert 'vim' == Language.find_by_name('VimL').search_term
        assert 'jsp' == Language.find_by_name('Java Server Pages').search_term
        assert 'rst' == Language.find_by_name('reStructuredText').search_term

    def test_popular(self):
        assert Language.find_by_name('Ruby').is_popular
        assert Language.find_by_name('Perl').is_popular
        assert Language.find_by_name('Python').is_popular
        assert Language.find_by_name('Assembly').is_unpopular
        assert Language.find_by_name('Brainfuck').is_unpopular

    def test_programming(self):
        assert 'programming' == Language.find_by_name('JavaScript').type
        assert 'programming' == Language.find_by_name('Perl').type
        assert 'programming' == Language.find_by_name('PowerShell').type
        assert 'programming' == Language.find_by_name('Python').type
        assert 'programming' == Language.find_by_name('Ruby').type
        assert 'programming' == Language.find_by_name('TypeScript').type

    def test_markup(self):
        assert 'markup' == Language.find_by_name('HTML').type
        assert 'markup' == Language.find_by_name('YAML').type

    def test_other(self):
        assert None == Language.find_by_name('Brainfuck').type
        assert None == Language.find_by_name('Makefile').type

    def test_searchable(self):
        assert True == Language.find_by_name('Ruby').is_searchable
        assert False == Language.find_by_name('Gettext Catalog').is_searchable
        assert False == Language.find_by_name('SQL').is_searchable

    def test_find_by_name(self):
        assert Language.find_by_name('Ruby') == Language.name_index['Ruby']

    def test_find_all_by_name(self):
        for language in Language.all():
            assert language == Language.find_by_name(language.name)
            assert language == Language.name_index[language.name]

    def test_find_all_by_alias(self):
        for language in Language.all():
            for name in language.aliases:
                assert language == Language.find_by_alias(name)

    def test_find_by_filename(self):
        assert [Language.find_by_name('Shell')] == Language.find_by_filename('PKGBUILD')
        assert [Language.find_by_name('Ruby')] == Language.find_by_filename('foo.rb')
        assert [Language.find_by_name('Ruby')] == Language.find_by_filename('foo/bar.rb')
        assert [Language.find_by_name('Ruby')] == Language.find_by_filename('Rakefile')
        assert [Language.find_by_name('Ruby')] == Language.find_by_filename('PKGBUILD.rb')
        assert Language.find_by_name('ApacheConf') == Language.find_by_filename('httpd.conf')[0]
        assert [Language.find_by_name('ApacheConf')] == Language.find_by_filename('.htaccess')
        assert Language.find_by_name('Nginx') == Language.find_by_filename('nginx.conf')[0]
        assert ['C', 'C++', 'Objective-C'] == sorted(map(lambda l: l.name, Language.find_by_filename('foo.h')))
        assert [] == Language.find_by_filename('rb')
        assert [] == Language.find_by_filename('.rb')
        assert [] == Language.find_by_filename('.nkt')
        assert [Language.find_by_name('Shell')] == Language.find_by_filename('.bashrc')
        assert [Language.find_by_name('Shell')] == Language.find_by_filename('bash_profile')
        assert [Language.find_by_name('Shell')] == Language.find_by_filename('.zshrc')

    def test_find(self):
        assert 'Ruby' == Language.find_by_name('Ruby').name
        assert 'Ruby' == Language.find_by_name('ruby').name
        assert 'C++' == Language.find_by_name('C++').name
        assert 'C++' == Language.find_by_name('c++').name
        assert 'C++' == Language.find_by_name('cpp').name
        assert 'C#' == Language.find_by_name('C#').name
        assert 'C#' == Language.find_by_name('c#').name
        assert 'C#' == Language.find_by_name('csharp').name
        assert None == Language.find_by_name('defunkt')

    def test_name(self):
        assert 'Perl' == Language.name_index['Perl'].name
        assert 'Python' == Language.name_index['Python'].name
        assert 'Ruby' ==  Language.name_index['Ruby'].name

    def test_escaped_name(self):
        assert 'C', Language.find_by_name('C').escaped_name
        assert 'C%23', Language.find_by_name('C#').escaped_name
        assert 'C%2B%2B', Language.find_by_name('C++').escaped_name
        assert 'Objective-C', Language.find_by_name('Objective-C').escaped_name
        assert 'Common%20Lisp', Language.find_by_name('Common Lisp').escaped_name

    def test_error_without_name(self):
        self.assertRaises(KeyError, Language, {})

    def test_color(self):
        assert '#701516' == Language.find_by_name('Ruby').color
        assert '#3581ba' == Language.find_by_name('Python').color
        assert '#f15501' == Language.find_by_name('JavaScript').color
        assert '#31859c' == Language.find_by_name('TypeScript').color

    def test_ace_mode(self):
        assert 'c_cpp' == Language.find_by_name('C++').ace_mode
        assert 'coffee' == Language.find_by_name('CoffeeScript').ace_mode
        assert 'csharp' == Language.find_by_name('C#').ace_mode
        assert 'css' == Language.find_by_name('CSS').ace_mode
        assert 'javascript' == Language.find_by_name('JavaScript').ace_mode

    def test_ace_modes(self):
        assert Language.find_by_name('Ruby') in Language.ace_modes()
        assert Language.find_by_name('FORTRAN') not in Language.ace_modes()

    def test_wrap(self):
        assert False == Language.find_by_name('C').wrap
        assert True == Language.find_by_name('Markdown').wrap

    def test_extensions(self):
        assert '.pl' in Language.find_by_name('Perl').extensions
        assert '.py' in Language.find_by_name('Python').extensions
        assert '.rb' in Language.find_by_name('Ruby').extensions

    def test_primary_extension(self):
        assert '.pl' == Language.find_by_name('Perl').primary_extension
        assert '.py' == Language.find_by_name('Python').primary_extension
        assert '.rb' == Language.find_by_name('Ruby').primary_extension
        assert '.js' == Language.find_by_name('JavaScript').primary_extension
        assert '.coffee' == Language.find_by_name('CoffeeScript').primary_extension
        assert '.t' == Language.find_by_name('Turing').primary_extension
        assert '.ts' == Language.find_by_name('TypeScript').primary_extension

        # This is a nasty requirement, but theres some code in GitHub that
        # expects this. Really want to drop this.
        for language in Language.all():
          assert language.primary_extension, "%s has no primary extension" % language

    def test_eql(self):
        assert Language.find_by_name('Ruby') == Language.find_by_name('Ruby')
        assert Language.find_by_name('Ruby') != Language.find_by_name('Python')

    def test_colorize(self):
        assert colorize == Language.find_by_name('Ruby').colorize("def foo\n  'foo'\nend\n")


if __name__ == '__main__':
    main()
