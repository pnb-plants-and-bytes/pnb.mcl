import io
from pathlib import Path
import shutil
import subprocess
import sys

THIS_DIR = Path(__file__).parent.resolve()
ROOT_DIR = (THIS_DIR / '..').resolve()
PY_SOURCE_DIR = ROOT_DIR / 'src'
DOC_DIR = ROOT_DIR / 'doc'
DOC_SOURCE_DIR = DOC_DIR / 'source'
API_DOC_SOURCE_DIR = DOC_SOURCE_DIR / 'api'

DOC_BUILD_DIR = ROOT_DIR / '.doc'


SCRIPTS_DIR = Path(sys.executable).parent.resolve()
SPHINX_APIDOC_PATH = SCRIPTS_DIR / 'sphinx-apidoc'
SPHINX_BUILD_PATH = SCRIPTS_DIR / 'sphinx-build'


def make_api_doc():

    try:
        shutil.rmtree(API_DOC_SOURCE_DIR)
    except FileNotFoundError:
        pass

    subprocess.call([
        SPHINX_APIDOC_PATH,
        '-e',
        '-d', '1',
        '--implicit-namespaces',
        '-o', API_DOC_SOURCE_DIR,
        'pnb'],
        cwd=PY_SOURCE_DIR)

    toplevel_filenames = []

    for path in list(API_DOC_SOURCE_DIR.iterdir()):
        filename = path.name
        if (filename in ['modules.rst', 'pnb.rst', 'pnb.mcl.rst']
                or filename.startswith('pnb.mcl.io')
                or filename.startswith('pnb.mcl.test')
                or filename.startswith('pnb.mcl.utils')):
            path.unlink()
            continue
        if filename.count('.') == 3:
            toplevel_filenames.append(filename)
            rst_lines = path.read_text(encoding='utf-8').splitlines()
            assert rst_lines[5] == 'Submodules', repr(rst_lines[5])
            assert rst_lines[6] == '----------', repr(rst_lines[6])
            rst_lines[5] = 'Modules'
            rst_lines[6] = '-------'

            assert rst_lines[8] == '.. toctree::', repr(rst_lines[8])
            assert rst_lines[9] == '   :maxdepth: 1', repr(rst_lines[9])
            assert rst_lines[10] == '', repr(rst_lines[10])

            if filename == 'pnb.mcl.io.rst':
                # TOFIX:
                # Not sure why this happens...
                # pnb.mcl.io refers to itself as one of its modules?!?
                assert rst_lines[11] == '   pnb.mcl.io', repr(rst_lines[11])
                rst_lines.pop(11)

            row_nr = 11
            while True:
                try:
                    row = rst_lines[row_nr]
                except IndexError:
                    break
                if not row.strip():
                    break
                assert row.startswith('   '), repr(row)
                row = row [3:]
                assert row == row.strip()
                rst_lines[row_nr] = f'   {row} <{row}.rst>'
                row_nr += 1

            path.write_text('\n'.join(rst_lines), encoding='utf-8')


def build_html():

    try:
        shutil.rmtree(DOC_BUILD_DIR)
    except FileNotFoundError:
        pass

    sphinx_process = subprocess.Popen([
        SPHINX_BUILD_PATH, '-M', 'html', DOC_SOURCE_DIR, DOC_BUILD_DIR],
        stderr=subprocess.PIPE)

    for line in io.TextIOWrapper(sphinx_process.stderr, encoding='utf-8'):
        # TODO: capture in output, fix in html
        # if 'WARNING: duplicate object description of pnb.mcl.' in line:
        #     continue
        sys.stderr.write(line)



def clean_html():
    for html_path in (DOC_BUILD_DIR / 'html' ).glob('**/*.html'):
        html_code = html_path.read_bytes()
        for html_cleaner in [
               add_legal_stuff]:
            html_code = html_cleaner(html_path, html_code)
        html_path.write_bytes(html_code)

    # Quick hack to reduce font size in generated API doc.
    furo_extensions_css_path = DOC_BUILD_DIR / 'html' / '_static' / 'styles' / 'furo-extensions.css'
    furo_extensions_css = furo_extensions_css_path.read_bytes()
    furo_extensions_css += b'''
        dd p {
            font-size: 14.3px;
        }'''
    furo_extensions_css_path.write_bytes(furo_extensions_css)


def add_legal_stuff(html_path: str, html_code: bytes):
    insertion_point = b'<article role="main" id="furo-main-content">'
    assert html_code.count(insertion_point) == 1, html_path
    html_code = html_code.replace(
        insertion_point,
        insertion_point + b'''
            <p style="padding-top: 7px">
              <a class="reference internal" href="https://www.plants-and-bytes.de/en/legal-notice">
                <span class="pre">Legal Notice</span>
              </a>
              <a class="reference internal" href="https://www.plants-and-bytes.de/en/data-protection" style="padding-left: 15px">
                <span class="pre">Data Protection</span>
              </a>
            </p>''')
    return html_code


def main():
    make_api_doc()
    build_html()
    clean_html()


if __name__ == '__main__':
    main()
