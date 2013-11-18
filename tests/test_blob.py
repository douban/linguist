# -*- coding: utf-8 -*-

from os.path import realpath, dirname, join
from pygments.lexers import find_lexer_class
from framework import LinguistTestBase, main
from libs.file_blob import FileBlob
from libs.samples import Samples

DIR = dirname(dirname(realpath(__file__)))
SAMPLES_PATH = join(DIR, "samples")

colorize = """<div class="highlight"><pre><span class="k">module</span> <span class="nn">Foo</span>
<span class="k">end</span>
</pre></div>
"""

colorize_without_wrapper = """<span class="k">module</span> <span class="nn">Foo</span>
<span class="k">end</span>
"""


class TestFileBob(LinguistTestBase):

    def blob(self, name):
        if not name.startswith('/'):
            name = join(SAMPLES_PATH, name)
        return FileBlob(name, SAMPLES_PATH)

    def script_blob(self, name):
        blob = self.blob(name)
        blob.name = 'script'
        return blob

    def test_name(self):
        assert 'foo.rb' == self.blob('foo.rb').name

    def test_mime_type(self):
        assert 'application/postscript' == self.blob('Binary/octocat.ai').mime_type
        assert 'application/x-ruby' == self.blob("Ruby/grit.rb").mime_type
        assert "application/x-sh" == self.blob("Shell/script.sh").mime_type
        assert "application/xml" == self.blob("XML/bar.xml").mime_type
        assert "audio/ogg" == self.blob("Binary/foo.ogg").mime_type
        assert "text/plain" == self.blob("Text/README").mime_type

    def test_content_type(self):
        assert "application/pdf" == self.blob("Binary/foo.pdf").content_type
        assert "audio/ogg" == self.blob("Binary/foo.ogg").content_type
        assert "image/png" == self.blob("Binary/foo.png").content_type
        assert "text/plain; charset=iso-8859-2" == self.blob("Text/README").content_type

    def test_disposition(self):
        assert "attachment; filename=foo+bar.jar" == self.blob("Binary/foo bar.jar").disposition
        assert "attachment; filename=foo.bin" == self.blob("Binary/foo.bin").disposition
        assert "attachment; filename=linguist.gem" == self.blob("Binary/linguist.gem").disposition
        assert "attachment; filename=octocat.ai" == self.blob("Binary/octocat.ai").disposition
        assert "inline" == self.blob("Text/README").disposition
        assert "inline" == self.blob("Text/foo.txt").disposition
        assert "inline" == self.blob("Ruby/grit.rb").disposition
        assert "inline" == self. blob("Binary/octocat.png").disposition

    def test_data(self):
        assert "module Foo\nend\n" == self.blob("Ruby/foo.rb").data

    def test_lines(self):
        assert ["module Foo", "end", ""] == self.blob("Ruby/foo.rb").lines
        assert ["line 1", "line 2", ""] == self.blob("Text/mac.txt").lines

    def test_size(self):
        assert 15 == self.blob("Ruby/foo.rb").size

    def test_loc(self):
        assert 3 == self.blob("Ruby/foo.rb").loc

    def test_sloc(self):
        assert 2 == self.blob("Ruby/foo.rb").sloc

    def test_encoding(self):
        assert "ISO-8859-2" == self.blob("Text/README").encoding
        assert "ISO-8859-1" == self.blob("Text/dump.sql").encoding
        assert "UTF-8" == self.blob("Text/foo.txt").encoding
        assert None == self.blob("Binary/dog.o").encoding

    def test_binary(self):
        # Large blobs aren't loaded
        large_blob = self.blob("git.exe")
        large_blob._data = None
        assert large_blob.is_binary

        assert self.blob("Binary/git.deb").is_binary
        assert self.blob("Binary/git.exe").is_binary
        assert self.blob("Binary/hello.pbc").is_binary
        assert self.blob("Binary/linguist.gem").is_binary
        assert self.blob("Binary/octocat.ai").is_binary
        assert self.blob("Binary/octocat.png").is_binary
        assert self.blob("Binary/zip").is_binary
        assert not self.blob("Text/README").is_binary
        assert not self.blob("Text/file.txt").is_binary
        assert not self.blob("Ruby/foo.rb").is_binary
        assert not self.blob("Perl/script.pl").is_binary

    def test_text(self):
        assert self.blob("Text/README").is_text
        assert self.blob("Text/dump.sql").is_text
        assert self.blob("Text/file.json").is_text
        assert self.blob("Text/file.txt").is_text
        assert self.blob("Text/md").is_text
        assert self.blob("Shell/script.sh").is_text
        assert self.blob("Text/txt").is_text

    def test_image(self):
        assert self.blob("Binary/octocat.gif").is_image
        assert self.blob("Binary/octocat.jpeg").is_image
        assert self.blob("Binary/octocat.jpg").is_image
        assert self.blob("Binary/octocat.png").is_image
        assert not self.blob("Binary/octocat.ai").is_image
        assert not self.blob("Binary/octocat.psd").is_image

    def test_solid(self):
        assert self.blob("Binary/cube.stl").is_solid
        assert self.blob("Text/cube.stl").is_solid

    def test_viewable(self):
        assert self.blob("Text/README").is_viewable
        assert self.blob("Ruby/foo.rb").is_viewable
        assert self.blob("Perl/script.pl").is_viewable
        assert not self.blob("Binary/linguist.gem").is_viewable
        assert not self.blob("Binary/octocat.ai").is_viewable
        assert not self.blob("Binary/octocat.png").is_viewable

    def test_csv(self):
        assert self.blob("Text/cars.csv").is_csv

    def test_pdf(self):
        assert self.blob("Binary/foo.pdf").is_pdf

    def test_generated(self):
        assert not self.blob("Text/README").is_generated

        # Xcode project files
        assert self.blob("XML/MainMenu.xib").is_generated
        assert self.blob("Binary/MainMenu.nib").is_generated
        assert self.blob("XML/project.pbxproj").is_generated

        # Gemfile.locks
        assert self.blob("Gemfile.lock").is_generated

        # Generated .NET Docfiles
        assert self.blob("XML/net_docfile.xml").is_generated

        # Long line
        assert not self.blob("JavaScript/uglify.js").is_generated

        # Inlined JS, but mostly code
        assert not self.blob("JavaScript/json2_backbone.js").is_generated

        # Minified JS
        assert not self.blob("JavaScript/jquery-1.6.1.js").is_generated
        assert self.blob("JavaScript/jquery-1.6.1.min.js").is_generated
        assert self.blob("JavaScript/jquery-1.4.2.min.js").is_generated

        # CoffeeScript-is_generated JS
        # TODO

        # TypeScript-is_generated JS
        # TODO

        # PEG.js-is_generated parsers
        assert self.blob("JavaScript/parser.js").is_generated

        # These examples are too basic to tell
        assert not self.blob("JavaScript/empty.js").is_generated
        assert not self.blob("JavaScript/hello.js").is_generated

        assert self.blob("JavaScript/intro-old.js").is_generated
        assert self.blob("JavaScript/classes-old.js").is_generated

        assert self.blob("JavaScript/intro.js").is_generated
        assert self.blob("JavaScript/classes.js").is_generated

        # Protocol Buffer generated code
        assert self.blob("C++/protocol-buffer.pb.h").is_generated
        assert self.blob("C++/protocol-buffer.pb.cc").is_generated
        assert self.blob("Java/ProtocolBuffer.java").is_generated
        assert self.blob("Python/protocol_buffer_pb2.py").is_generated

        # Generated JNI
        assert self.blob("C/jni_layer.h").is_generated

        # Minified CSS
        assert not self.blob("CSS/bootstrap.css").is_generated
        assert self.blob("CSS/bootstrap.min.css").is_generated

    def test_vendored(self):
        assert not self.blob("Text/README").is_vendored
        assert not self.blob("ext/extconf.rb").is_vendored

        # Dependencies
        assert self.blob("dependencies/windows/headers/GL/glext.h").is_vendored

        # Node depedencies
        assert  self.blob("node_modules/coffee-script/lib/coffee-script.js").is_vendored

        # Rails vendor/
        assert  self.blob("vendor/plugins/will_paginate/lib/will_paginate.rb").is_vendored

        # 'thirdparty' directory
        assert self.blob("thirdparty/lib/main.c").is_vendored

        # C deps
        assert  self.blob("deps/http_parser/http_parser.c").is_vendored
        assert  self.blob("deps/v8/src/v8.h").is_vendored

        # Debian packaging
        assert  self.blob("debian/cron.d").is_vendored

        # Prototype
        assert not self.blob("public/javascripts/application.js").is_vendored
        assert  self.blob("public/javascripts/prototype.js").is_vendored
        assert  self.blob("public/javascripts/effects.js").is_vendored
        assert  self.blob("public/javascripts/controls.js").is_vendored
        assert  self.blob("public/javascripts/dragdrop.js").is_vendored

        # jQuery
        assert  self.blob("jquery.js").is_vendored
        assert  self.blob("public/javascripts/jquery.js").is_vendored
        assert  self.blob("public/javascripts/jquery.min.js").is_vendored
        assert  self.blob("public/javascripts/jquery-1.7.js").is_vendored
        assert  self.blob("public/javascripts/jquery-1.7.min.js").is_vendored
        assert  self.blob("public/javascripts/jquery-1.5.2.js").is_vendored
        assert  self.blob("public/javascripts/jquery-1.6.1.js").is_vendored
        assert  self.blob("public/javascripts/jquery-1.6.1.min.js").is_vendored
        assert  self.blob("public/javascripts/jquery-1.10.1.js").is_vendored
        assert  self.blob("public/javascripts/jquery-1.10.1.min.js").is_vendored
        assert not self.blob("public/javascripts/jquery.github.menu.js").is_vendored

        # jQuery UI
        assert self.blob("themes/ui-lightness/jquery-ui.css").is_vendored
        assert self.blob("themes/ui-lightness/jquery-ui-1.8.22.custom.css").is_vendored
        assert self.blob("themes/ui-lightness/jquery.ui.accordion.css").is_vendored
        assert self.blob("ui/i18n/jquery.ui.datepicker-ar.js").is_vendored
        assert self.blob("ui/i18n/jquery-ui-i18n.js").is_vendored
        assert self.blob("ui/jquery.effects.blind.js").is_vendored
        assert self.blob("ui/jquery-ui-1.8.22.custom.js").is_vendored
        assert self.blob("ui/jquery-ui-1.8.22.custom.min.js").is_vendored
        assert self.blob("ui/jquery-ui-1.8.22.js").is_vendored
        assert self.blob("ui/jquery-ui-1.8.js").is_vendored
        assert self.blob("ui/jquery-ui.min.js").is_vendored
        assert self.blob("ui/jquery.ui.accordion.js").is_vendored
        assert self.blob("ui/minified/jquery.effects.blind.min.js").is_vendored
        assert self.blob("ui/minified/jquery.ui.accordion.min.js").is_vendored

        # MooTools
        assert  self.blob("public/javascripts/mootools-core-1.3.2-full-compat.js").is_vendored
        assert  self.blob("public/javascripts/mootools-core-1.3.2-full-compat-yc.js").is_vendored

        # Dojo
        assert  self.blob("public/javascripts/dojo.js").is_vendored

        # MochiKit
        assert  self.blob("public/javascripts/MochiKit.js").is_vendored

        # YUI
        assert  self.blob("public/javascripts/yahoo-dom-event.js").is_vendored
        assert  self.blob("public/javascripts/yahoo-min.js").is_vendored
        assert  self.blob("public/javascripts/yuiloader-dom-event.js").is_vendored

        # WYS editors
        assert  self.blob("public/javascripts/ckeditor.js").is_vendored
        assert  self.blob("public/javascripts/tiny_mce.js").is_vendored
        assert  self.blob("public/javascripts/tiny_mce_popup.js").is_vendored
        assert  self.blob("public/javascripts/tiny_mce_src.js").is_vendored

        # Fabric
        assert  self.blob("fabfile.py").is_vendored

        # WAF
        assert  self.blob("waf").is_vendored

        # Visual Studio IntelliSense
        assert  self.blob("Scripts/jquery-1.7-vsdoc.js").is_vendored

        # Microsoft Ajax
        assert  self.blob("Scripts/MicrosoftAjax.debug.js").is_vendored
        assert  self.blob("Scripts/MicrosoftAjax.js").is_vendored
        assert  self.blob("Scripts/MicrosoftMvcAjax.debug.js").is_vendored
        assert  self.blob("Scripts/MicrosoftMvcAjax.js").is_vendored
        assert  self.blob("Scripts/MicrosoftMvcValidation.debug.js").is_vendored
        assert  self.blob("Scripts/MicrosoftMvcValidation.js").is_vendored

        # jQuery validation plugin (MS bundles this with asp.net mvc)
        assert  self.blob("Scripts/jquery.validate.js").is_vendored
        assert  self.blob("Scripts/jquery.validate.min.js").is_vendored
        assert  self.blob("Scripts/jquery.validate.unobtrusive.js").is_vendored
        assert  self.blob("Scripts/jquery.validate.unobtrusive.min.js").is_vendored
        assert  self.blob("Scripts/jquery.unobtrusive-ajax.js").is_vendored
        assert  self.blob("Scripts/jquery.unobtrusive-ajax.min.js").is_vendored

        # NuGet Packages
        assert  self.blob("packages/Modernizr.2.0.6/Content/Scripts/modernizr-2.0.6-development-only.js").is_vendored

        # Test fixtures
        assert self.blob("test/fixtures/random.rkt").is_vendored
        assert self.blob("Test/fixtures/random.rkt").is_vendored

        # Cordova/PhoneGap
        assert self.blob("cordova.js").is_vendored
        assert self.blob("cordova.min.js").is_vendored
        assert self.blob("cordova-2.1.0.js").is_vendored
        assert self.blob("cordova-2.1.0.min.js").is_vendored

        # Vagrant
        assert self.blob("Vagrantfile").is_vendored

    def test_language(self):
        def _check_lang(sample):
            blob = self.blob(sample['path'])
            assert blob.language, 'No language for %s' % sample['path']
            assert sample['language'] == blob.language.name, blob.name

        Samples.each(_check_lang)

    def test_lexer(self):
        assert find_lexer_class('Ruby') == self.blob("Ruby/foo.rb").lexer

    def test_colorize(self):
        assert colorize == self.blob("Ruby/foo.rb").colorize()

    def test_colorize_does_skip_minified_files(self):
        assert None == self.blob("JavaScript/jquery-1.6.1.min.js").colorize()

    # Pygments.rb was taking exceeding long on this particular file
    def test_colorize_doesnt_blow_up_with_files_with_high_ratio_of_long_lines(self):
        assert None == self.blob("JavaScript/steelseries-min.js").colorize()


if __name__ == '__main__':
    main()
