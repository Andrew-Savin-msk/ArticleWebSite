from setuptools import setup, find_packages

setup(
    name='NewsSite', 
    version='0.1.0', 
    author='Andew',  
    author_email='4andreysavin@gmail.com', 
    description='A simple Flask web application.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    url='https://github.com/Andrew-Savin-msk',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[
        'blinker==1.7.0',
        'click==8.1.7',
        'colorama==0.4.6',
        'Flask==3.0.2',
        'Flask-Login==0.6.3',
        'Flask-SQLAlchemy==3.1.1',
        'greenlet==3.0.3',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.3',
        'MarkupSafe==2.1.5',
        'SQLAlchemy==2.0.27',
        'typing_extensions==4.9.0',
        'Werkzeug==3.0.1',
    ],
)