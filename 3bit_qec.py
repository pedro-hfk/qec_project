from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2
from qiskit.visualization import plot_histogram
from qiskit_aer.primitives import Estimator
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import sys
from collections import Counter


def generate_3bit_qec_circuit():

    qr = QuantumRegister(5)                                    # 3 data qubits + 2 ancilla qubits
    cr = ClassicalRegister(3, name='result_register')          # To store the final result
    syndrome = ClassicalRegister(2, name='syndrome_register')  # To store the error syndrome

    # Concatenating the registers
    qc = QuantumCircuit(qr, cr, syndrome) 

    # Quantum entanglement between the data qubits (CNOT gates)
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])

    # Extracting the error syndrome using ancilla qubits
    # First ancilla qubit qr[3]: parity between qubit 0 and qubit 1
    # Second ancilla qubit qr[4]: parity between qubit 1 and qubit 2
    qc.cx(qr[0], qr[3])
    qc.cx(qr[1], qr[3])
    qc.cx(qr[1], qr[4])
    qc.cx(qr[2], qr[4])

    return qc, qr, cr, syndrome

def correct_3bit_error(qc, qr, cr, syndrome):

    # Measuring the error syndrome
    qc.measure(qr[3], syndrome[0])
    qc.measure(qr[4], syndrome[1])

    # Error correction based on the syndrome
    with qc.if_test((syndrome, 1)):            # If the syndrome is 01
        qc.x(qr[2])                            # Correct qubit 2

    with qc.if_test((syndrome, 2)):            # If the syndrome is 10
        qc.x(qr[1])                            # Correct qubit 1

    with qc.if_test((syndrome, 3)):            # If the syndrome is 11
        qc.x(qr[0])                            # Correct qubit 0
    
    # Measuring the final data qubits
    qc.measure(qr[0], cr[0])
    qc.measure(qr[1], cr[1])
    qc.measure(qr[2], cr[2])

    return qc

def main(ibm_token, ibm_backend_name):
    qc, qr, cr, syndrome = generate_3bit_qec_circuit()
    qc = correct_3bit_error(qc, qr, cr, syndrome)


    service = QiskitRuntimeService(channel='ibm_quantum',
                                token=ibm_token)

    backend = service.backend(name=ibm_backend_name)
    compiled_circuit = transpile(qc, backend=backend)

    try:
        with Session(service=service, backend=backend) as session:
            sampler = SamplerV2(session=session)
            result = sampler.run([compiled_circuit]).result()
            job_id = result.job_id

    except Exception as e:
        print(f"An error occurred: {e}")

    print(f'Job ID: {job_id}')
    return job_id

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("Usage: python 3bit_qec.py <IBM_BACKEND>")
        sys.exit(1)

    load_dotenv()
    ibm_token = os.getenv('IBM_TOKEN')

    ibm_backend_name = sys.argv[1]

    job_id = main(ibm_token, ibm_backend_name)

    if job_id:
        service = QiskitRuntimeService(channel='ibm_quantum', token=ibm_token)
        job = service.job(job_id)
        job_result = job.result()

        pub_result0 = job_result[0].data['result_register'].get_counts()
        pub_result1 = job_result[0].data['syndrome_register'].get_counts()

        # Plotting the histograms in separate subplots
        fig, axs = plt.subplots(2, 1, figsize=(10, 8))

        # Plot for result_register
        axs[0].bar(pub_result0.keys(), pub_result0.values(), color='blue')
        axs[0].set_title('Result Register Counts')
        axs[0].set_xlabel('Bitstring')
        axs[0].set_ylabel('Count')

        # Plot for syndrome_register
        axs[1].bar(pub_result1.keys(), pub_result1.values(), color='red')
        axs[1].set_title('Syndrome Register Counts')
        axs[1].set_xlabel('Bitstring')
        axs[1].set_ylabel('Count')

        # Main title for the figure
        fig.suptitle('Quantum Error Correction Results')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Save the plot
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)
        plt.savefig(f"{images_dir}/3bit_qec_result_{job_id}.png")

        print(f"The result from job {job_id} has been saved in the 'images' directory.")

        plt.show()