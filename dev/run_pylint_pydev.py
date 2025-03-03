# Run Pylint from PyDev.
# 
# 1. Set message format such that Pylint will show the message symbols.
# 2. Select Pylint config file depending on "type" of *.py file to check:
#    "normal" source or unit test
# 3. Filter some messages.

import os.path
import pathlib
import re
import sys

from pylint import run_pylint

THIS_DIR = pathlib.Path(__file__).parent

after_msg_template = False
for nr, arg in list(enumerate(sys.argv)):
    if arg.startswith('--msg-template='):
        assert nr == len(sys.argv) - 2
        sys.argv[nr] = "--msg-template='{C}:{line:3d},{column:2d}: ({symbol}) {msg} ({symbol})'"
        after_msg_template = True
    elif after_msg_template:
        # '--msg-template' should be last kwargs; exactly 1 file paths should
        # follow.
        assert nr == len(sys.argv) - 1
        if '{sep}test{sep}'.format(sep=os.path.sep) in arg:
            rcfile = THIS_DIR / 'pylint_config_test.toml'
        else:
            rcfile = THIS_DIR / 'pylint_config_source.toml'
        sys.argv.insert(nr-1, f'--rcfile={rcfile}')
        

def filter_message(msg):
    if re.search(
            r'\(protected-access\) Access to a protected member _[^_].*[^_]_ '
                r'of a client class \(protected-access\)',
            msg):
        return ''
    
    return msg
      
        
class MessageFilter:
    
    def __init__(self, base_stream):
        self.base_stream = base_stream
        
    def write(self, args):
        msg = ''.join(args)
        assert '\n' not in msg.strip()
        self.base_stream.write(filter_message(msg))


sys.stdout = MessageFilter(sys.stdout)
sys.stderr = MessageFilter(sys.stderr)
try:
    sys.exit(run_pylint())
finally:
    sys.stdout = sys.stdout.base_stream
    sys.stderr = sys.stderr.base_stream
