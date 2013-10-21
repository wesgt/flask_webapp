import sys
import os
import shutil
from os import path
from flask_webapp import __version__

PROMPT_PREFIX = '> '

if sys.version_info < (3, 3, 2):
    print('Error, need python version : 3.3.2')
    sys.exit(1)


def mkdir_p(dir):
    if path.isdir(dir):
        return
    os.makedirs(dir)


class ValidationError(Exception):

    """Raised for validation errors."""


def is_path(x):
    if path.exists(x) and not path.isdir(x):
        raise ValidationError("Please enter a valid path name.")
    return x


def nonempty(x):
    if not x:
        raise ValidationError("Please enter some text.")
    return x


def boolean(x):
    if x.upper() not in ('Y', 'YES', 'N', 'NO'):
        raise ValidationError("Please enter either 'y' or 'n'.")
    return x.upper() in ('Y', 'YES')


def do_prompt(d, key, text, default=None, validator=nonempty):
    while True:
        if default:
            prompt = PROMPT_PREFIX + '{0} [{1}]: '.format(text, default)
        else:
            prompt = PROMPT_PREFIX + text + ': '

        x = input(prompt).strip()
        if default and not x:
            x = default

        try:
            x = validator(x)
        except ValidationError as err:
            print('* {0}'.format(str(err)))
            continue
        break
    d[key] = x


def ask_user(d):
    print('Welcome to the Webapp {0} quickstart utility.'.format(__version__))

    # check webapp root path
    if 'path' in d:
        print('Selected root path: {0}'.format(d['path']))
    else:
        print('Enter the root path for webapp.')
        do_prompt(d, 'path', 'Root path for the webapp', '.', is_path)

    if 'open_iap' not in d:
        print('Open In-App Purchases (Y/N).')
        do_prompt(d, 'open_iap', 'Open In-App Purchases', 'N', boolean)
    pass

    if 'push_notification' not in d:
        print('Open push notification (Y/N).')
        do_prompt(d, 'open_iap', 'Open push notification', 'N', boolean)
    pass


def generate(d, overwrite=True, silent=False):

    webapp_root_path = d['path'].lower()

    if not path.isdir(webapp_root_path):
        mkdir_p(webapp_root_path)

    webapp_tests_path = path.join(webapp_root_path, 'tests')
    webapp_app_path = path.join(webapp_root_path, 'webapp')

    mkdir_p(webapp_tests_path)
    mkdir_p(webapp_app_path)

    def write_file(fpath, content, newline=None):
        if overwrite or not path.isfile(fpath):
            print('Creating file {0}.'.format(fpath))
            with open(fpath, 'wt', encoding='utf-8', newline=newline) as f:
                f.write(content)
        else:
            print('File {0} already exists, skipping.'.format(fpath))

    here = path.dirname(path.abspath(__file__))
    shutil.copyfile(path.join(here, 'webapp_test_all.py'),
                    path.join(webapp_root_path, 'webapp_test_all.py'))

    shutil.copyfile(path.join(here, 'webapp_main.py'),
                    path.join(webapp_root_path, 'webapp_main.py'))

    shutil.copyfile(path.join(here, 'webapp/__init__.py'),
                    path.join(webapp_root_path, 'webapp/__init__.py'))

    config_content = 'DEBUG = True\n' + "SERVER_IP = '172.18.102.104'\n" + \
        'SERVER_PORT = 80\n' + "LOG_PATH = 'log/webapp.log'\n" + \
        "SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT1346'\n"

    write_file(
        path.join(webapp_root_path, 'webapp/config.cfg'), config_content)

    print()
    print('Finished: An new webapp has been created.')
    pass


def main(argv=sys.argv):
    d = {}

    if len(argv) > 3:
        print('Usage: webapp-quickstart [root]')
        sys.exit(1)
    elif len(argv) == 2:
        d['path'] = argv[1]
    try:
        ask_user(d)
    except (KeyboardInterrupt, EOFError):
        print()
        print('[Interrupted.]')
        return

    generate(d)
