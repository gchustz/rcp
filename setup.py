# WARNING: SETUP.PY MODIFIED FOR USE WITH CATKIN BUILD
# DO NOT RUN PYTHON SETUP.PY INSTALL ON THIS FILE

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup


def readme():
    with open('README.md') as f:
        return f.read()


setup_args = generate_distutils_setup(
    name='rcp',
    version='0.0.1',
    description='A rospy based package to read compute system performance',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Communications'
    ],
    url='http://github.com/gchustz/rcp',
    author='George Chustz',
    author_email='george.chustz@gmail.com',
    license='GNU GPL v3',
    packages=['compute_performance'],
    package_dir={'': 'src'},
    requires=['psutil', 'attrs']
)

setup(**setup_args)
