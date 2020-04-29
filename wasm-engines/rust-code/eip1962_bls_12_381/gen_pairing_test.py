from py_ecc.fields import optimized_bls12_381_FQ12 as FQ12
from py_ecc.optimized_bls12_381 import (
    add,
    curve_order,
    final_exponentiate,
    G1,
    multiply,
    neg,
    pairing,
    Z1,
    Z2,
    G2,
)

def hex_to_rust_u8_array(hex_num):
    output = [] 

    assert len(hex_num) % 2 == 0, "invalid hex num length"

    for i in range(0, len(hex_num) - 1, 2):
        output.append("{}u8".format(int(hex_num[i:i+2], 16)))

    return ','.join(output)


# print a 48 byte field element in hex
# TODO endian safe?
def fp_to_hex(p):
    hex_repr = hex(int(p))[2:]
    if len(hex_repr) < 96:
        hex_repr = '0' * (96 - len(hex_repr)) + hex_repr

    return hex_repr

def g1_to_hex(p):
    return fp_to_hex(p[0]) + fp_to_hex(p[1])

def g2_to_hex(p):
    output = ''
    for i in range(3):
        for j in range(2):
            output += fp_to_hex(p[i].coeffs[j])

    return output

def g1_gen_hex():
    return g1_to_hex(G1)

def g2_gen_hex():
    return g2_to_hex(G2)

def websnark_test_case():
    p1A = G1
    p1B = G2

    p2A = multiply(p1A, 10) 
    p2B = multiply(p1B, 10)

    fp12A = pairing(p2B, p1A)
    fp12B = pairing(p1B, p2A)

    assert fp12A == fp12B

def signature_recovery_test_caes():
    pass

print("g1 is: ")
print(hex_to_rust_u8_array(g1_gen_hex()))
print("g2 is: ")
print(hex_to_rust_u8_array(g2_gen_hex()))
