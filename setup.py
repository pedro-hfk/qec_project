from setuptools import setup, find_packages

setup(
    name='qec_project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'qiskit',
        'qiskit-ibm-runtime',
        'matplotlib',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'run-3bit-qec=3bit_qec:main',
        ],
    },
    author='Pedro Henrique Ferron Kim',
    author_email='pedroh.kim00@gmail.com',
    description='A project for Quantum Error Correction using Qiskit and IBM Quantum backends.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pedro-hfk/qec_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
