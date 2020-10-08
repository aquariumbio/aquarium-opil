from setuptools import setup, find_packages

readme = open('README.md').read()
requirements_list = [pkg for pkg in open('requirements.txt').readlines()]

setup(
    name='aquarium-opil',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=requirements_list,

    author='Ben Keller',
    author_email='bjkeller@uw.edu',
    description='Package for exposing Aquarium workflows as OPIL',
    license='MIT',
    long_description=readme,
    url='https://aquariumbio.bio',
    project_urls={
        'Source Code': 'https://github.com/aquariumbio/aquarium-opil'
    }
)