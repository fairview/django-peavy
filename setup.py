from setuptools import setup

peavy = __import__('peavy')

with open('README.rst') as file:
    long_description = file.read()

setup(
    author='Fairview Computing LLC',
    author_email='john@fairviewcomputing.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Logging',
    ],
    description=peavy.__doc__,
    long_description=long_description,
    download_url='http://github.com/fairview/django-peavy/downloads',
    install_requires=[
        'Django>=1.3',
        'South>=0.7.3'
    ],
    license="MIT License",
    name='django-peavy',
    packages=[
        'peavy',
        'peavy.migrations',
        'peavy.templatetags',
    ],
    package_data={
        'peavy': [
            'README.rst',
            'LICENSE.txt',
            'templates/*/*.html',
           'static/*/*/*',
        ],
    },
    tests_require=[
        'Django>=1.3',
        'South==0.7.3',
        'psycopg2>=2.4.3',  # 2.4.2 causes trouble with Django 1.3(.1) unit tests
    ],
    test_suite='tests.main',
    url='http://github.com/fairview/django-peavy',
    version=peavy.get_version(),
    zip_safe=True,
)
