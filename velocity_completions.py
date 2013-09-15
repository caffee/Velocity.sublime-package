# -*- coding: utf8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2012 Lee <lee.github@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sublime
import sublime_plugin

# Modify from HTML completions
# Provide completions that match just after typing an hash
class DirectivesCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within Velocity
        if not view.match_selector(locations[0], "source.vm"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '#':
            return []

        return ([
            ("parse(variable)\tDirective", "parse(\\$${1:val})"),
            ("parse(string)\tDirective", "parse(\"${1}.vm\")"),

            ("set(variable)\tDirective", "set(\\$${1:ref} = \\$${2:val})"),
            (u"set(string '…')\tDirective", "set(\\$${1:ref} = '${2}')"),
            (u"set(string \"…\")\tDirective", "set(\\$${1:ref} = \"${2}\")"),
            ("set(number)\tDirective", "set(\\$${1:ref} = ${2:0})"),
            ("set(range)\tDirective", "set(\\$${1:ref} = [${2:0}..${3:2}])"),
            ("set(arraylist)\tDirective", "set(\\$${1:ref} = [${2}])"),
            ("set(map)\tDirective", "set(\\$${1:ref} = {${2} : ${3}})"),

            ("foreach(reference)\tDirective", "foreach(\\$${1:item} in \\$${2:items})\n\t${3}\n#end"),
            ("foreach(arraylist)\tDirective", "foreach(\\$${1:item} in [${2}])\n\t${3}\n#end"),
            ("foreach(range)\tDirective", "foreach(\\$${1:item} in [${2:0}..${3:2}])\n\t${4}\n#end"),

            ("if\tDirective", "if(\\$${1:var}) ${2} #end"),
            (u"if …\tDirective", "if(\\$${1:var})\n\t${2}\n${3}"),
            (u"elseif …\tDirective", "elseif(\\$${1:var})\n\t${2}\n${3}"),
            ("elseif\tDirective", "elseif(\\$${1:var})\n\t${2}\n#end"),
            ("else\tDirective", "else\n\t${1}\n#end"),

            ("macro(name)\tDirective", "macro(${1:name})\n\t${2}\n#end"),
            ("macro(name arg)\tDirective", "macro(${1:name} \\$${2:arg})\n\t${3}\n#end"),

            ("include(variable)\tDirective", "include(\\$${1:val})"),
            ("include(string)\tDirective", "include(\"${1}\")")
        ], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)