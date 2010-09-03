import sys
import os

def build_possible_paths():
    """ Returns a list of possible paths where App Engine SDK could be

    First look within the project for a local copy, then look for where the Mac
    OS SDK installs it.
    """
    dir_path = os.path.abspath(os.path.dirname(__file__))
    app_dir = os.path.dirname(os.path.dirname(dir_path))
    paths = [os.path.join(app_dir, '.google_appengine'),
            '/usr/local/google_appengine',
            '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine']
    # Then if on windows, look for where the Windows SDK installed it.
    for path in os.environ.get('PATH', '').replace(';', ':').split(':'):
        path = path.rstrip(os.sep)
        if path.endswith('google_appengine'):
            paths.append(path)
    try:
        from win32com.shell import shell
        from win32com.shell import shellcon
        id_list = shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_PROGRAM_FILES)
        program_files = shell.SHGetPathFromIDList(id_list)
        paths.append(os.path.join(program_files, 'Google','google_appengine'))
    except ImportError, e:
        # Not windows.
        pass
    return paths


def gae_sdk_path():
    """ Returns the App Engine SDK Path """
    paths = build_possible_paths()
    # Loop through all possible paths and look for the SDK dir.
    sdk_path = None
    for possible_path in paths:
        possible_path = os.path.realpath(possible_path)
        if os.path.exists(possible_path):
            sdk_path = possible_path
            break
    if sdk_path is None:
        # The SDK could not be found in any known location.
        sys.stderr.write('The Google App Engine SDK could not be found!\n'
              'Visit http://code.google.com/p/app-engine-patch/'
              ' for installation instructions.\n')
        sys.exit(1)
    return sdk_path

def add_gae_sdk_path():
    """ Try to import the appengine code from the system path. """
    try:
        from google.appengine.api import apiproxy_stub_map
    except ImportError, e:
        # Hack to fix reports of import errors on Ubuntu 9.10.
        if 'google' in sys.modules:
            del sys.modules['google']
        sys.path = [gae_sdk_path()] + sys.path
