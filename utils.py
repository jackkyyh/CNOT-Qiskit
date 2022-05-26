
import numpy as np
from qiskit import QuantumCircuit
# from qiskit import *
from qiskit import Aer, execute

backend = Aer.get_backend('unitary_simulator')

def add_row(A, op):    
    op = np.array(op)
    for i, j in op:
        A[j] = (A[i] + A[j]) % 2
    return A




def read_circ_qasm(file):
    with open(file, 'r') as f:
       lines = f.readlines()

    num_qubits = int(lines[0])
    circ = QuantumCircuit(num_qubits, 0)

    for line in lines[1:]:
        line = line.strip().split(' ')
        if(line[0] == 'CNOT'):
            gate, qu1, qu2 = line
            qu1, qu2 = int(qu1), int(qu2)
            circ.cnot(qu1, qu2)
        else:
            # continue
            gate, qu = line
            qu = int(qu)
            gate_map = {'X': circ.x, 'Y': circ.y, 'Z': circ.z,
                    'H': circ.h, 'T': circ.t, 'T+': circ.tdg,
                    'P': circ.s, 'P+': circ.sdg}
            gate_map[gate](qu)

    return circ


def read_circ_sarah(file):
    with open(file, 'r') as f:
       lines = f.readlines()

    num_qubits = 9
    circ = QuantumCircuit(num_qubits, 0)
    gate_map = {'X': circ.x, 'Y': circ.y, 'Z': circ.z,
        'H': circ.h, 'T': circ.t, 'T+': circ.tdg,
        'S': circ.s, 'S+': circ.sdg}

    for line in lines[6:]:
        line = line.strip().split('[')
        if(line[0] == 'CNOT'):
            qu1, qu2 = int(line[1][0])-1, int(line[1][3])-1
            circ.cnot(qu1, qu2)
        else:
            # continue
            gate, qu = line
            # print(line)
            qu = int(qu[0])-1
            gate_map[gate](qu)

    # circ.draw()
    return circ

def circ2u(circ):
    # circ.draw()
    job = execute(circ, backend)
    result = job.result()
    u = result.get_unitary(circ).data
    return u