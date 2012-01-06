import os
from setuptools import setup
from setuptools import find_packages
from liasis import __version__


if sys.version < '2.7':
    print 'Requires Python 2.7 or greater'
    sys.exit(1)

setup(name='liasis',
      version=__version__,
      url='http://syslog.tv/liasis',
      author="Kura",
      author_email="kura@deviling.net",
      description="An asynchronous Python-powered HTTP daemon that serves RST or HTML websites",
      long_description = file(
          os.path.join(
              os.path.dirname(__file__),
              'README.rst'
          )
      ).read(),
      license='BSD',
      platforms=['linux'],
      packages=['liasis',],
      install_requires=[
          'eventlet==0.9.16',
          ],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
    zip_safe = False,
)
