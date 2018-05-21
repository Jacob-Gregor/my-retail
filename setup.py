from setuptools import find_packages, setup


setup(
    name='myretail_service',
    version='0.5.0',
    description='',
    long_description='',
    author='Jacob Gregor',
    author_email='gregorj9974@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'myretail_service=myretail_service.dev.main:main',
        ],
    },
    install_requires=['mock', 'redis', 'flake8', 'tox', 'pytest-cov', 'flask']
)
