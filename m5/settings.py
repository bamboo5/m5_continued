""" Settings for the m5 package. """


from os import getenv
from os.path import join, abspath, expanduser
from sys import modules


USER_BASE_DIR = join(expanduser('~'), '.m5', )
PROJECT_DIR = abspath(__file__ + '/../..')
ASSETS_DIR = join(PROJECT_DIR, 'assets')
PACKAGE_DIR = join(PROJECT_DIR, 'm5')
INSTANCE_DIR = join(PROJECT_DIR, 'instance')
TEST_JOBS_DIR = join(ASSETS_DIR, 'test_jobs')
MOCK_DIRNAME = 'mock_user'

# Assets files
MASK_FILEPATH = join(ASSETS_DIR, 'mask.png')
SHP_FILEPATH = join(ASSETS_DIR, 'berlin_postleitzahlen.shp')
DBF_FILEPATH = join(ASSETS_DIR, 'berlin_postleitzahlen.dbf')


# Wordcloud parameters
WORD_BLACKLIST = {'strasse', 'allee', 'platz', 'a', 'b', 'c', 'd'}
WORD_SOURCE = 'street'
MAX_WORDS = 200
HORIZONTAL_WORDS = 0.8

# URLs to the company server
LOGIN_URL = 'http://bamboo-mec.de/ll.php5'
LOGOUT_URL = 'http://bamboo-mec.de/index.php5'
JOB_URL = 'http://bamboo-mec.de/ll_detail.php5'
SUMMARY_URL = 'http://bamboo-mec.de/ll.php5'

# String constants
LOGGING_FORMAT = '[M5] [%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] %(message)s'
JOB_QUERY_URL = 'http://bamboo-mec.de/ll_detail.php5?status=delivered&uuid={uuid}&datum={date}'
FAILURE_REPORT = '{date}-{uuid}: Failed to scrape {field}.'
JOB_FILENAME = '{date}-uuid-{uuid}.html'
FILE_DATE_FORMAT = '%d-%m-%Y'
URL_DATE_FORMAT = '%d.%m.%Y'
LOG_FORMAT = '[%(asctime)s] [%(module)s] %(message)s'

# Formatting
FILL = '.'
CENTER = '^'
LEAP = '\n\n'
SKIP = '\n'
STEP = ''
SEPERATOR = '-'*30

# Readability
LOGGED_IN = 'erfolgreich'
REDIRECT = 302
EXIT = {'logout': '1'}
UUID = slice(-12, -5)

# Matplotlib settings
PLOT_FONTSIZE = 14
FIGURE_SIZE = (18, 12)
FIGURE_STYLE = 'default'
FIGURE_FONT = 'Droid Sans'
BACKGROUND_ALPHA = 0.0

# Environment variables
USERNAME = getenv('BAMBOO_USERNAME')
PASSWORD = getenv('BAMBOO_PASSWORD')
CREDENTIALS_WARNING = 'Please export BAMBOO_USERNAME and BAMBOO_PASSWORD'


def show_settings():
    """ Echo all settings. """

    print('Current m5 settings:', end=LEAP)
    objects = dir(modules[__name__])
    parameters = [x for x in objects if x.isupper()]

    for p in parameters:
        value = getattr(modules[__name__], p)
        print('{item} = {value!r}'.format(item=p.rjust(20, ' '), value=value))


if __name__ == '__main__':
    show_settings()
