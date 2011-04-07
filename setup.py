from setuptools import setup, find_packages

f = open('README')
readme = f.read()
f.close()

setup(
    name='django-report-utils',
    version='0.1',
    description='A convoluted reporting library you should not use',
    author='Steve Yeago',
    author_email='subsume@gmail.com',
    url='http://github.com/subsume/django-report-utils/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
