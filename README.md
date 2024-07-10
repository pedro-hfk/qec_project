# Quantum Error Correction Project

This project demonstrates different Quantum Error Correction algorithms using Qiskit and IBM Quantum backends.

For version 0.1.0:

* 3-bit Error Correction Code

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/pedro-hfk/qec_project.git
    cd qec_project
    ```

2. Create a `.env` file from the example provided and add your IBM Quantum token (read the Usage section for help):
    ```sh
    cp .env.example .env
    ```

3. Install the package:
    ```sh
    pip install .
    ```

## Usage

#### IBM Quantum Platform

1. If you have not yet created a IBM Quantum Platform account, access https://quantum.ibm.com/

2. Access the Dashboard page (https://quantum.ibm.com/) and copy your unique IBM Token in order to put it in the .env file

3. Access the Compute resources page (https://quantum.ibm.com/services/resources) and choose which backend you would like to use to run the code on

4. After each time you run any algorithm, you are able to access the Jobs page (https://quantum.ibm.com/jobs) to check the status of your job request

#### Executing

Run the script of the algorithm of your choice with the IBM backend name:

1. 3-bit Correction Code
```sh
run-3bit-qec <ibm_backend_name>
```