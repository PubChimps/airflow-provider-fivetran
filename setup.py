from setuptools import find_packages, setup

setup(
    name='airflow-provider-fivetran',
    description='A Fivetran provider for Apache Airflow',
    long_description="Initiate syncs from sources to destinations via Fivetran connectors, then monitor the process to trigger further data transformations with other Airflow tasks.",
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    version='0.0.1',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['apache-airflow~=1.10'],
    setup_requires=['setuptools', 'wheel'],
    extras_require={},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Monitoring',
    ],
    author='Developer Relations Team, Fivetran',
    author_email='devrel@fivetrean.com',
    url='http://fivetram.com/',
    python_requires='~=3.6',
)
