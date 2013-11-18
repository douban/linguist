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
        assert find_lexer_class('ActionScript 3') == Language['ActionScript'].lexer
        assert find_lexer_class('Bash') == Language['Gentoo Ebuild'].lexer
        assert find_lexer_class('Bash') == Language['Gentoo Eclass'].lexer
        assert find_lexer_class('Bash') == Language['Shell'].lexer
        assert find_lexer_class('C') == Language['OpenCL'].lexer
        assert find_lexer_class('C') == Language['XS'].lexer
        assert find_lexer_class('C++') == Language['C++'].lexer
        assert find_lexer_class('Coldfusion HTML') == Language['ColdFusion'].lexer
        assert find_lexer_class('Coq') == Language['Coq'].lexer
        assert find_lexer_class('FSharp') == Language['F#'].lexer
        assert find_lexer_class('FSharp') == Language['F#'].lexer
        assert find_lexer_class('Fortran') == Language['FORTRAN'].lexer
        assert find_lexer_class('Gherkin') == Language['Cucumber'].lexer
        assert find_lexer_class('Groovy') == Language['Groovy'].lexer
        assert find_lexer_class('HTML') == Language['HTML'].lexer
        assert find_lexer_class('HTML+Django/Jinja') == Language['HTML+Django'].lexer
        assert find_lexer_class('HTML+PHP') == Language['HTML+PHP'].lexer
        assert find_lexer_class('HTTP') == Language['HTTP'].lexer
        assert find_lexer_class('JSON') == Language['JSON'].lexer
        assert find_lexer_class('Java') == Language['ChucK'].lexer
        assert find_lexer_class('Java') == Language['Java'].lexer
        assert find_lexer_class('JavaScript') == Language['JavaScript'].lexer
        assert find_lexer_class('MOOCode') == Language['Moocode'].lexer
        assert find_lexer_class('MuPAD') == Language['mupad'].lexer
        assert find_lexer_class('NASM') == Language['Assembly'].lexer
        assert find_lexer_class('OCaml') == Language['OCaml'].lexer
        assert find_lexer_class('Ooc') == Language['ooc'].lexer
        assert find_lexer_class('OpenEdge ABL') == Language['OpenEdge ABL'].lexer
        assert find_lexer_class('REBOL') == Language['Rebol'].lexer
        assert find_lexer_class('RHTML') == Language['HTML+ERB'].lexer
        assert find_lexer_class('RHTML') == Language['RHTML'].lexer
        assert find_lexer_class('Ruby') == Language['Mirah'].lexer
        assert find_lexer_class('Ruby') == Language['Ruby'].lexer
        assert find_lexer_class('S') == Language['R'].lexer
        assert find_lexer_class('Scheme') == Language['Emacs Lisp'].lexer
        assert find_lexer_class('Scheme') == Language['Nu'].lexer
        assert find_lexer_class('Racket') == Language['Racket'].lexer
        assert find_lexer_class('Scheme') == Language['Scheme'].lexer
        assert find_lexer_class('Standard ML') == Language['Standard ML'].lexer
        assert find_lexer_class('TeX') == Language['TeX'].lexer
        assert find_lexer_class('verilog') == Language['Verilog'].lexer
        assert find_lexer_class('XSLT') == Language['XSLT'].lexer
        assert find_lexer_class('aspx-vb') == Language['ASP'].lexer
        # assert find_lexer_class('haXe') == Language['Haxe'].lexer
        assert find_lexer_class('reStructuredText') == Language['reStructuredText'].lexer

    def test_find_by_alias(self):
        assert Language['ASP'] == Language.find_by_alias('asp')
        assert Language['ASP'] == Language.find_by_alias('aspx')
        assert Language['ASP'] == Language.find_by_alias('aspx-vb')
        assert Language['ActionScript'] == Language.find_by_alias('as3')
        assert Language['ApacheConf'] == Language.find_by_alias('apache')
        assert Language['Assembly'] == Language.find_by_alias('nasm')
        assert Language['Batchfile'] == Language.find_by_alias('bat')
        assert Language['C#'] == Language.find_by_alias('c#')
        assert Language['C#'] == Language.find_by_alias('csharp')
        assert Language['C'] == Language.find_by_alias('c')
        assert Language['C++'] == Language.find_by_alias('c++')
        assert Language['C++'] == Language.find_by_alias('cpp')
        assert Language['CoffeeScript'] == Language.find_by_alias('coffee')
        assert Language['CoffeeScript'] == Language.find_by_alias('coffee-script')
        assert Language['ColdFusion'] == Language.find_by_alias('cfm')
        assert Language['Common Lisp'] == Language.find_by_alias('common-lisp')
        assert Language['Common Lisp'] == Language.find_by_alias('lisp')
        assert Language['Darcs Patch'] == Language.find_by_alias('dpatch')
        assert Language['Dart'] == Language.find_by_alias('dart')
        assert Language['Emacs Lisp'] == Language.find_by_alias('elisp')
        assert Language['Emacs Lisp'] == Language.find_by_alias('emacs')
        assert Language['Emacs Lisp'] == Language.find_by_alias('emacs-lisp')
        assert Language['Gettext Catalog'] == Language.find_by_alias('pot')
        assert Language['HTML'] == Language.find_by_alias('html')
        assert Language['HTML'] == Language.find_by_alias('xhtml')
        assert Language['HTML+ERB'] == Language.find_by_alias('html+erb')
        assert Language['HTML+ERB'] == Language.find_by_alias('erb')
        assert Language['IRC log'] == Language.find_by_alias('irc')
        assert Language['JSON'] == Language.find_by_alias('json')
        assert Language['Java Server Pages'] == Language.find_by_alias('jsp')
        assert Language['Java'] == Language.find_by_alias('java')
        assert Language['JavaScript'] == Language.find_by_alias('javascript')
        assert Language['JavaScript'] == Language.find_by_alias('js')
        assert Language['Literate Haskell'] == Language.find_by_alias('lhs')
        assert Language['Literate Haskell'] == Language.find_by_alias('literate-haskell')
        assert Language['Objective-C'] == Language.find_by_alias('objc')
        assert Language['OpenEdge ABL'] == Language.find_by_alias('openedge')
        assert Language['OpenEdge ABL'] == Language.find_by_alias('progress')
        assert Language['OpenEdge ABL'] == Language.find_by_alias('abl')
        assert Language['Parrot Internal Representation'] == Language.find_by_alias('pir')
        assert Language['PowerShell'] == Language.find_by_alias('posh')
        assert Language['Puppet'] == Language.find_by_alias('puppet')
        assert Language['Pure Data'] == Language.find_by_alias('pure-data')
        assert Language['Raw token data'] == Language.find_by_alias('raw')
        assert Language['Ruby'] == Language.find_by_alias('rb')
        assert Language['Ruby'] == Language.find_by_alias('ruby')
        assert Language['Scheme'] == Language.find_by_alias('scheme')
        assert Language['Shell'] == Language.find_by_alias('bash')
        assert Language['Shell'] == Language.find_by_alias('sh')
        assert Language['Shell'] == Language.find_by_alias('shell')
        assert Language['Shell'] == Language.find_by_alias('zsh')
        assert Language['TeX'] == Language.find_by_alias('tex')
        assert Language['TypeScript'] == Language.find_by_alias('ts')
        assert Language['VimL'] == Language.find_by_alias('vim')
        assert Language['VimL'] == Language.find_by_alias('viml')
        assert Language['reStructuredText'] == Language.find_by_alias('rst')
        assert Language['YAML'] == Language.find_by_alias('yml')

    def test_groups(self):
        # Test a couple identity cases
        assert Language['Perl'] == Language['Perl'].group
        assert Language['Python'] == Language['Python'].group
        assert Language['Ruby'] == Language['Ruby'].group

        # Test a few special groups
        assert Language['Assembly'] == Language['GAS'].group
        assert Language['C'] == Language['OpenCL'].group
        assert Language['Haskell'] == Language['Literate Haskell'].group
        assert Language['Java'] == Language['Java Server Pages'].group
        assert Language['Python'] == Language['Cython'].group
        assert Language['Python'] == Language['NumPy'].group
        assert Language['Shell'] == Language['Batchfile'].group
        assert Language['Shell'] == Language['Gentoo Ebuild'].group
        assert Language['Shell'] == Language['Gentoo Eclass'].group
        assert Language['Shell'] == Language['Tcsh'].group

        # Ensure everyone has a group
        for language in Language.all():
            assert language.group, "%s has no group" % language

    def test_search_term(self):
        assert 'perl' == Language['Perl'].search_term
        assert 'python' == Language['Python'].search_term
        assert 'ruby' == Language['Ruby'].search_term
        assert 'common-lisp' == Language['Common Lisp'].search_term
        assert 'html+erb' == Language['HTML+ERB'].search_term
        assert 'max/msp' == Language['Max'].search_term
        assert 'puppet' == Language['Puppet'].search_term
        assert 'pure-data' == Language['Pure Data'].search_term

        assert 'aspx-vb' == Language['ASP'].search_term
        assert 'as3' == Language['ActionScript'].search_term
        assert 'nasm' == Language['Assembly'].search_term
        assert 'bat' == Language['Batchfile'].search_term
        assert 'csharp' == Language['C#'].search_term
        assert 'cpp' == Language['C++'].search_term
        assert 'cfm' == Language['ColdFusion'].search_term
        assert 'dpatch' == Language['Darcs Patch'].search_term
        assert 'fsharp' == Language['F#'].search_term
        assert 'pot' == Language['Gettext Catalog'].search_term
        assert 'irc' == Language['IRC log'].search_term
        assert 'lhs' == Language['Literate Haskell'].search_term
        assert 'ruby' == Language['Mirah'].search_term
        assert 'raw' == Language['Raw token data'].search_term
        assert 'bash' == Language['Shell'].search_term
        assert 'vim' == Language['VimL'].search_term
        assert 'jsp' == Language['Java Server Pages'].search_term
        assert 'rst' == Language['reStructuredText'].search_term

    def test_popular(self):
        assert Language['Ruby'].is_popular
        assert Language['Perl'].is_popular
        assert Language['Python'].is_popular
        assert Language['Assembly'].is_unpopular
        assert Language['Brainfuck'].is_unpopular

    def test_programming(self):
        assert 'programming' == Language['JavaScript'].type
        assert 'programming' == Language['Perl'].type
        assert 'programming' == Language['PowerShell'].type
        assert 'programming' == Language['Python'].type
        assert 'programming' == Language['Ruby'].type
        assert 'programming' == Language['TypeScript'].type

    def test_markup(self):
        assert 'markup' == Language['HTML'].type

    def test_data(self):
        assert 'data' == Language['YAML'].type

    def test_other(self):
        assert None == Language['Brainfuck'].type
        assert None == Language['Makefile'].type

    def test_searchable(self):
        assert True == Language['Ruby'].is_searchable
        assert False == Language['Gettext Catalog'].is_searchable
        assert False == Language['SQL'].is_searchable

    def test_find_by_name(self):
        assert Language['Ruby'] == Language.name_index['Ruby']

    def test_find_all_by_name(self):
        for language in Language.all():
            assert language == Language[language.name]
            assert language == Language.name_index[language.name]

    def test_find_all_by_alias(self):
        for language in Language.all():
            for name in language.aliases:
                assert language == Language.find_by_alias(name)

    def test_find_by_filename(self):
        assert [Language['Shell']] == Language.find_by_filename('PKGBUILD')
        assert [Language['Ruby']] == Language.find_by_filename('foo.rb')
        assert [Language['Ruby']] == Language.find_by_filename('foo/bar.rb')
        assert [Language['Ruby']] == Language.find_by_filename('Rakefile')
        assert [Language['Ruby']] == Language.find_by_filename('PKGBUILD.rb')
        assert Language['ApacheConf'] == Language.find_by_filename('httpd.conf')[0]
        assert [Language['ApacheConf']] == Language.find_by_filename('.htaccess')
        assert Language['Nginx'] == Language.find_by_filename('nginx.conf')[0]
        assert ['C', 'C++', 'Objective-C'] == sorted(map(lambda l: l.name, Language.find_by_filename('foo.h')))
        assert [] == Language.find_by_filename('rb')
        assert [] == Language.find_by_filename('.rb')
        assert [] == Language.find_by_filename('.nkt')
        assert [Language['Shell']] == Language.find_by_filename('.bashrc')
        assert [Language['Shell']] == Language.find_by_filename('bash_profile')
        assert [Language['Shell']] == Language.find_by_filename('.zshrc')
        assert [Language['Clojure']] == Language.find_by_filename('riemann.config')
        assert [Language['HTML+Django']] == Language.find_by_filename('index.jinja')

    def test_find(self):
        assert 'Ruby' == Language['Ruby'].name
        assert 'Ruby' == Language['ruby'].name
        assert 'C++' == Language['C++'].name
        assert 'C++' == Language['c++'].name
        assert 'C++' == Language['cpp'].name
        assert 'C#' == Language['C#'].name
        assert 'C#' == Language['c#'].name
        assert 'C#' == Language['csharp'].name
        assert None == Language['defunkt']

    def test_name(self):
        assert 'Perl' == Language.name_index['Perl'].name
        assert 'Python' == Language.name_index['Python'].name
        assert 'Ruby' == Language.name_index['Ruby'].name

    def test_escaped_name(self):
        assert 'C' == Language['C'].escaped_name
        assert 'C%23' == Language['C#'].escaped_name
        assert 'C%2B%2B' == Language['C++'].escaped_name
        assert 'Objective-C' == Language['Objective-C'].escaped_name
        assert 'Common%20Lisp' == Language['Common Lisp'].escaped_name

    def test_error_without_name(self):
        self.assertRaises(KeyError, Language, {})

    def test_color(self):
        assert '#701516' == Language['Ruby'].color
        assert '#3581ba' == Language['Python'].color
        assert '#f15501' == Language['JavaScript'].color
        assert '#31859c' == Language['TypeScript'].color

    def test_colors(self):
        Language['Ruby'] in Language.colors()
        Language['Python'] in Language.colors()

    def test_ace_mode(self):
        assert 'c_cpp' == Language['C++'].ace_mode
        assert 'coffee' == Language['CoffeeScript'].ace_mode
        assert 'csharp' == Language['C#'].ace_mode
        assert 'css' == Language['CSS'].ace_mode
        assert 'javascript' == Language['JavaScript'].ace_mode

    def test_ace_modes(self):
        assert Language['Ruby'] in Language.ace_modes()
        assert Language['FORTRAN'] not in Language.ace_modes()

    def test_wrap(self):
        assert False == Language['C'].wrap
        assert True == Language['Markdown'].wrap

    def test_extensions(self):
        assert '.pl' in Language['Perl'].extensions
        assert '.py' in Language['Python'].extensions
        assert '.rb' in Language['Ruby'].extensions

    def test_primary_extension(self):
        assert '.pl' == Language['Perl'].primary_extension
        assert '.py' == Language['Python'].primary_extension
        assert '.rb' == Language['Ruby'].primary_extension
        assert '.js' == Language['JavaScript'].primary_extension
        assert '.coffee' == Language['CoffeeScript'].primary_extension
        assert '.t' == Language['Turing'].primary_extension
        assert '.ts' == Language['TypeScript'].primary_extension

        # This is a nasty requirement, but theres some code in GitHub that
        # expects this. Really want to drop this.
        for language in Language.all():
            assert language.primary_extension, "%s has no primary extension" % language

    def test_eql(self):
        assert Language['Ruby'] == Language['Ruby']
        assert Language['Ruby'] != Language['Python']

    def test_colorize(self):
        assert colorize == Language['Ruby'].colorize("def foo\n  'foo'\nend\n")


if __name__ == '__main__':
    main()
