#!c:\users\akhil\desktop\miri_app\miri_app\miri\scripts\python3.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'xhtml2pdf==0.2.5','console_scripts','pisa'
__requires__ = 'xhtml2pdf==0.2.5'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('xhtml2pdf==0.2.5', 'console_scripts', 'pisa')()
    )
