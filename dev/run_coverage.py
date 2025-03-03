import io
from pathlib import Path
import shutil
import subprocess
import sys

THIS_DIR = Path(__file__).parent.resolve()
ROOT_DIR = (THIS_DIR / '..').resolve()
PY_SOURCE_DIR = ROOT_DIR / 'src'
PNB_MCL_PACKAGE_PATH = PY_SOURCE_DIR / 'pnb' / 'mcl'
TEST_PACKAGE_PATH = PNB_MCL_PACKAGE_PATH / 'test'

print(TEST_PACKAGE_PATH)

def main():
    subprocess.call([
        sys.executable,
        '-m',
        'coverage',
        'run',
        '--data-file',
        ROOT_DIR / '.coverage',
        '-m',
        'unittest',
        'discover',
        '-s',
        TEST_PACKAGE_PATH,
        '-p',
        '*.py',
      #  '-t', PY_SOURCE_DIR
        
        
        ])
    subprocess.call([
        sys.executable,
        '-m',
        'coverage',
        'html',
        '--data-file',
        ROOT_DIR / '.coverage',
        '--directory',
        ROOT_DIR / '.coverage-html'])
    
    
if __name__ == '__main__':
    main()
        


