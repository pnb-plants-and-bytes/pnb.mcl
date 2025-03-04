#!/usr/bin/env/python
"""
sphinx-execute-code module for execute_code directive
To use this module, add: extensions.append('sphinx_execute_code')

Available options:

        'linenos': directives.flag,
        'output_language': directives.unchanged,
        'hide_code': directives.flag,
        'hide_headers': directives.flag,
        'filename': directives.path,
        'hide_filename': directives.flag,

Usage:

.. example_code:
   :linenos:
   :hide_code:

   print 'Execute this python code'

   See Readme.rst for documentation details
"""
import sys
import os
from docutils.parsers.rst import Directive, directives
from docutils import nodes
from io import StringIO

from sphinx.directives.code import CodeBlock

# execute_code function thanks to Stackoverflow code post from hekevintran
# https://stackoverflow.com/questions/701802/how-do-i-execute-a-string-containing-python-code-in-python

__author__ = 'jp.senior@gmail.com'
__docformat__ = 'restructuredtext'
__version__ = '0.2a2'


SCOPE_BY_NAME = {}

class Scope:
    def __init__(self):
        self.globals = {}
        self.locals = {}
        self.linenr = 1
        
        
CODE = ''


class ExecuteCode(Directive):
    """ Sphinx class for execute_code directive
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 5

    option_spec = {
        'linenos': directives.flag,
        'output_language': directives.unchanged,  # Runs specified pygments lexer on output data
        'hide_code': directives.flag,
        'hide_headers': directives.flag,
        'filename': directives.path,
        'hide_filename': directives.flag,
        'scope': directives.unchanged,
    }

    @classmethod
    def execute_code(cls, code, locals_, globals_):
        """ Executes supplied code as pure python and returns a list of stdout, stderr

        Args:
            code (string): Python code to execute

        Results:
            (list): stdout, stderr of executed python code

        Raises:
            ExecutionError when supplied python is incorrect

        Examples:
            >>> execute_code('print "foobar"')
            'foobar'
        """

        output = StringIO()
        err = StringIO()

        sys.stdout = output
        sys.stderr = err

        try:
            # pylint: disable=exec-used
            exec(code, locals_, globals_)
        # If the code is invalid, just skip the block - any actual code errors
        # will be raised properly
        except TypeError:
            pass
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        results = list()
        results.append(output.getvalue())
        results.append(err.getvalue())
        results = ''.join(results)

        return results

    def run(self):
        """ Executes python code for an RST document, taking input from content or from a filename

        :return:
        """
        language = self.options.get('language') or 'python'
        output_language = self.options.get('output_language') or 'none'
        filename = self.options.get('filename')
        code = ''

        if not filename:
            code = '\n'.join(self.content)
            
        global CODE
            
        CODE = CODE + '\n' + code
        
      #  print('##########')
      #  print(CODE)
      #  print('##########')
        
        
            
        if filename:
            try:
                with open(filename, 'r') as code_file:
                    code = code_file.read()
                    self.warning('code is %s' % code)
            except (IOError, OSError) as err:
                # Raise warning instead of a code block
                error = 'Error opening file: %s, working folder: %s' % (err, os.getcwd())
                self.warning(error)
                return [nodes.warning(error, error)]
        fragments = []
        in_fragment = False

        for row in code.splitlines():
            if in_fragment:
                if row and row[0] == ' ':
                    fragments[-1] += '\n' + row
                else:
                    fragments.append(row)
                    
                        
            else:
                fragments.append(row)
                if row and row[0] != '#':
                    in_fragment = True
                    
                    
        scope_name = self.options.get('scope')
        if scope_name:
            scope = SCOPE_BY_NAME.setdefault(scope_name, Scope())
        else:
            scope = Scope()

        fragments_and_outputs = []
   
        for fragment in fragments:
            if fragments_and_outputs and not fragments_and_outputs[-1][1]:
                fragments_and_outputs[-1][0] += '\n' + fragment
            else:
                fragments_and_outputs.append([fragment, None])
                                             
            code_results = self.execute_code(fragment, scope.locals, scope.globals)
            if code_results:
                fragments_and_outputs[-1][1] = code_results
                
                
        output = []
                
        for fragment, fragment_output in fragments_and_outputs:
           
            input_code = nodes.literal_block(fragment, fragment)
            extra_args = input_code['highlight_args'] = {}
            input_code['language'] = language
            if 'linenos' in self.options: 
                input_code['linenos'] = True
                extra_args['linenostart'] = scope.linenr 
            if not 'hide_headers' in self.options:
                suffix = ''
                if not 'hide_filename' in self.options:
                    suffix = '' if filename is None else str(filename)
                if suffix:
                    output.append(nodes.caption(
                        text='Code %s' % suffix))
            output.append(input_code)
            
            scope.linenr += fragment.count('\n') + 1
            
            if fragment_output:
                
                
                fragment_output = '↳  ' + '\n   '.join(fragment_output.splitlines())
                
                
                output_code = nodes.literal_block(fragment_output, fragment_output)
                #extra_args = input_code['highlight_args'] = {}
                output_code['language'] = output_language
                # if 'linenos' in self.options: 
               #     input_code['linenos'] = True
               #     extra_args['linenostart'] = lineno_start 
               # if not 'hide_headers' in self.options:
               #     suffix = ''
               #     if not 'hide_filename' in self.options:
               #         suffix = '' if filename is None else str(filename)
                #    if suffix:
               #         output.append(nodes.caption(
               #             text='Code %s' % suffix))
               
 
                output.append(output_code)
                
            
        return output

                
        
            
            
            
            

            

        

        # Show the example code
        if not 'hide_code' in self.options:
            input_code = nodes.literal_block(code, code)

            input_code['language'] = language
            input_code['linenos'] = 'linenos' in self.options
            if not 'hide_headers' in self.options:
                suffix = ''
                if not 'hide_filename' in self.options:
                    suffix = '' if filename is None else str(filename)
                output.append(nodes.caption(
                    text='Code %s' % suffix))
            output.append(input_code)

        # Show the code results
        if not 'hide_headers' in self.options:
            output.append(nodes.caption(text='Results'))
        code_results = self.execute_code(code)
        code_results = nodes.literal_block(code_results, code_results)

        code_results['linenos'] = 'linenos' in self.options
        code_results['language'] = output_language
        output.append(code_results)
        return output

def setup(app):
    """ Register sphinx_execute_code directive with Sphinx """
    app.add_directive('execute_code', ExecuteCode)
    return {'version': __version__}
