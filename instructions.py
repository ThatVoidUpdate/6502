def FromHex(hexa: bytes) -> int:
    return int.from_bytes(hexa, byteorder="little")

def opcode_00(machineState: dict):
    pass

def opcode_01(machineState: dict):
    pass

def opcode_05(machineState: dict):
    pass

def opcode_06(machineState: dict):
    pass

def opcode_08(machineState: dict):
    pass

def opcode_09(machineState: dict):
    pass

def opcode_0a(machineState: dict):
    pass

def opcode_0d(machineState: dict):
    pass

def opcode_0e(machineState: dict):
    pass


def opcode_10(machineState: dict):
    pass

def opcode_11(machineState: dict):
    pass

def opcode_15(machineState: dict):
    pass

def opcode_16(machineState: dict):
    pass

def opcode_18(machineState: dict):
    pass

def opcode_19(machineState: dict):
    pass

def opcode_1d(machineState: dict):
    pass

def opcode_1e(machineState: dict):
    pass


def opcode_20(machineState: dict):
    pass

def opcode_21(machineState: dict):
    pass

def opcode_24(machineState: dict):
    pass

def opcode_25(machineState: dict):
    pass

def opcode_26(machineState: dict):
    pass

def opcode_28(machineState: dict):
    pass

def opcode_29(machineState: dict):
    pass

def opcode_2a(machineState: dict):
    pass

def opcode_2c(machineState: dict):
    pass

def opcode_2d(machineState: dict):
    pass

def opcode_2e(machineState: dict):
    pass


def opcode_30(machineState: dict):
    pass

def opcode_31(machineState: dict):
    pass

def opcode_35(machineState: dict):
    pass

def opcode_36(machineState: dict):
    pass

def opcode_38(machineState: dict):
    pass

def opcode_39(machineState: dict):
    pass

def opcode_3d(machineState: dict):
    pass

def opcode_3e(machineState: dict):
    pass


def opcode_40(machineState: dict):
    pass

def opcode_41(machineState: dict):
    pass

def opcode_45(machineState: dict):
    pass

def opcode_46(machineState: dict):
    pass

def opcode_48(machineState: dict):
    pass

def opcode_49(machineState: dict):
    pass

def opcode_4a(machineState: dict):
    pass

def opcode_4c(machineState: dict):
    pass

def opcode_4d(machineState: dict):
    pass

def opcode_4e(machineState: dict):
    pass


def opcode_50(machineState: dict):
    pass

def opcode_51(machineState: dict):
    pass

def opcode_55(machineState: dict):
    pass

def opcode_56(machineState: dict):
    pass

def opcode_58(machineState: dict):
    pass

def opcode_59(machineState: dict):
    pass

def opcode_5d(machineState: dict):
    pass

def opcode_5e(machineState: dict):
    pass


def opcode_60(machineState: dict):
    pass

def opcode_61(machineState: dict):
    pass

def opcode_65(machineState: dict):
    pass

def opcode_66(machineState: dict):
    pass

def opcode_68(machineState: dict):
    pass

def opcode_69(machineState: dict):
    pass

def opcode_6a(machineState: dict):
    pass

def opcode_6c(machineState: dict):
    pass

def opcode_6d(machineState: dict):
    pass

def opcode_6e(machineState: dict):
    pass


def opcode_70(machineState: dict):
    pass

def opcode_71(machineState: dict):
    pass

def opcode_75(machineState: dict):
    pass

def opcode_76(machineState: dict):
    pass

def opcode_78(machineState: dict):
    pass

def opcode_79(machineState: dict):
    pass

def opcode_7d(machineState: dict):
    pass

def opcode_7e(machineState: dict):
    pass


def opcode_81(machineState: dict):
    pass

def opcode_84(machineState: dict):
    pass

def opcode_85(machineState: dict):
    pass

def opcode_86(machineState: dict):
    pass

def opcode_88(machineState: dict):
    pass

def opcode_8a(machineState: dict):
    pass

def opcode_8c(machineState: dict):
    pass

def opcode_8d(machineState: dict):
    #STA ABS 3 4
    address = FromHex(machineState["ROM"][machineState["PC"]+1:machineState["PC"]+3])
    machineState["RAM"][address] = machineState["ACC"]
    machineState["PC"] += 3
    print(f"Wrote to ram at address {hex(address)}: {hex(machineState['ACC'])}")

def opcode_8e(machineState: dict):
    pass


def opcode_90(machineState: dict):
    pass

def opcode_91(machineState: dict):
    pass

def opcode_94(machineState: dict):
    pass

def opcode_95(machineState: dict):
    pass

def opcode_96(machineState: dict):
    pass

def opcode_98(machineState: dict):
    pass

def opcode_99(machineState: dict):
    pass

def opcode_9a(machineState: dict):
    pass

def opcode_9d(machineState: dict):
    pass


def opcode_a0(machineState: dict):
    pass

def opcode_a1(machineState: dict):
    pass

def opcode_a2(machineState: dict):
    pass

def opcode_a4(machineState: dict):
    pass

def opcode_a5(machineState: dict):
    pass

def opcode_a6(machineState: dict):
    pass

def opcode_a8(machineState: dict):
    pass

def opcode_a9(machineState: dict):
    # LDA IMM 2 2
    machineState["ACC"] = machineState["ROM"][machineState["PC"]+1]
    machineState["PC"] += 2

def opcode_aa(machineState: dict):
    pass

def opcode_ac(machineState: dict):
    pass

def opcode_ad(machineState: dict):
    pass

def opcode_ae(machineState: dict):
    pass


def opcode_b0(machineState: dict):
    pass

def opcode_b1(machineState: dict):
    pass

def opcode_b4(machineState: dict):
    pass

def opcode_b5(machineState: dict):
    pass

def opcode_b6(machineState: dict):
    pass

def opcode_b8(machineState: dict):
    pass

def opcode_b9(machineState: dict):
    pass

def opcode_ba(machineState: dict):
    pass

def opcode_bc(machineState: dict):
    pass

def opcode_bd(machineState: dict):
    pass

def opcode_be(machineState: dict):
    pass


def opcode_c0(machineState: dict):
    pass

def opcode_c1(machineState: dict):
    pass

def opcode_c4(machineState: dict):
    pass

def opcode_c5(machineState: dict):
    pass

def opcode_c6(machineState: dict):
    pass

def opcode_c8(machineState: dict):
    pass

def opcode_c9(machineState: dict):
    pass

def opcode_ca(machineState: dict):
    pass

def opcode_cc(machineState: dict):
    pass

def opcode_cd(machineState: dict):
    pass

def opcode_ce(machineState: dict):
    pass


def opcode_d0(machineState: dict):
    pass

def opcode_d1(machineState: dict):
    pass

def opcode_d5(machineState: dict):
    pass

def opcode_d6(machineState: dict):
    pass

def opcode_d8(machineState: dict):
    pass

def opcode_d9(machineState: dict):
    pass

def opcode_dd(machineState: dict):
    pass

def opcode_de(machineState: dict):
    pass


def opcode_e0(machineState: dict):
    pass

def opcode_e1(machineState: dict):
    pass

def opcode_e4(machineState: dict):
    pass

def opcode_e5(machineState: dict):
    pass

def opcode_e6(machineState: dict):
    pass

def opcode_e8(machineState: dict):
    pass

def opcode_e9(machineState: dict):
    pass

def opcode_ea(machineState: dict):
    #NOP implied 1 2
    return

def opcode_ec(machineState: dict):
    pass

def opcode_ed(machineState: dict):
    pass

def opcode_ee(machineState: dict):
    pass


def opcode_f0(machineState: dict):
    pass

def opcode_f1(machineState: dict):
    pass

def opcode_f5(machineState: dict):
    pass

def opcode_f6(machineState: dict):
    pass

def opcode_f8(machineState: dict):
    pass

def opcode_f9(machineState: dict):
    pass

def opcode_fd(machineState: dict):
    pass

def opcode_fe(machineState: dict):
    pass

switch_table = {
    0x00: opcode_00,
    0x01: opcode_01,
    0x05: opcode_05,
    0x06: opcode_06,
    0x08: opcode_08,
    0x09: opcode_09,
    0x0a: opcode_0a,
    0x0d: opcode_0d,
    0x0e: opcode_0e,

    0x10: opcode_10,
    0x11: opcode_11,
    0x15: opcode_15,
    0x16: opcode_16,
    0x18: opcode_18,
    0x19: opcode_19,
    0x1d: opcode_1d,
    0x1e: opcode_1e,

    0x20: opcode_20,
    0x21: opcode_21,
    0x24: opcode_24,
    0x25: opcode_25,
    0x26: opcode_26,
    0x28: opcode_28,
    0x29: opcode_29,
    0x2a: opcode_2a,
    0x2c: opcode_2c,
    0x2d: opcode_2d,
    0x2e: opcode_2e,

    0x30: opcode_30,
    0x31: opcode_31,
    0x35: opcode_35,
    0x36: opcode_36,
    0x38: opcode_38,
    0x39: opcode_39,
    0x3d: opcode_3d,
    0x3e: opcode_3e,

    0x40: opcode_40,
    0x41: opcode_41,
    0x45: opcode_45,
    0x46: opcode_46,
    0x48: opcode_48,
    0x49: opcode_49,
    0x4a: opcode_4a,
    0x4c: opcode_4c,
    0x4d: opcode_4d,
    0x4e: opcode_4e,

    0x50: opcode_50,
    0x51: opcode_51,
    0x55: opcode_55,
    0x56: opcode_56,
    0x58: opcode_58,
    0x59: opcode_59,
    0x5d: opcode_5d,
    0x5e: opcode_5e,

    0x60: opcode_60,
    0x61: opcode_61,
    0x65: opcode_65,
    0x66: opcode_66,
    0x68: opcode_68,
    0x69: opcode_69,
    0x6a: opcode_6a,
    0x6c: opcode_6c,
    0x6d: opcode_6d,
    0x6e: opcode_6e,

    0x70: opcode_70,
    0x71: opcode_71,
    0x75: opcode_75,
    0x76: opcode_76,
    0x78: opcode_78,
    0x79: opcode_79,
    0x7d: opcode_7d,
    0x7e: opcode_7e,
        
    0x81: opcode_81,
    0x84: opcode_84,
    0x85: opcode_85,
    0x86: opcode_86,
    0x88: opcode_88,
    0x8a: opcode_8a,
    0x8c: opcode_8c,
    0x8d: opcode_8d,
    0x8e: opcode_8e,

    0x90: opcode_90,
    0x91: opcode_91,
    0x94: opcode_94,
    0x95: opcode_95,
    0x96: opcode_96,
    0x98: opcode_98,
    0x99: opcode_99,
    0x9a: opcode_9a,
    0x9d: opcode_9d,

    0xa0: opcode_a0,
    0xa1: opcode_a1,
    0xa2: opcode_a2,
    0xa4: opcode_a4,
    0xa5: opcode_a5,
    0xa6: opcode_a6,
    0xa8: opcode_a8,
    0xa9: opcode_a9,
    0xaa: opcode_aa,
    0xac: opcode_ac,
    0xad: opcode_ad,
    0xae: opcode_ae,

    0xb0: opcode_b0,
    0xb1: opcode_b1,
    0xb4: opcode_b4,
    0xb5: opcode_b5,
    0xb6: opcode_b6,
    0xb8: opcode_b8,
    0xb9: opcode_b9,
    0xba: opcode_ba,
    0xbc: opcode_bc,
    0xbd: opcode_bd,
    0xbe: opcode_be,

    0xc0: opcode_c0,
    0xc1: opcode_c1,
    0xc4: opcode_c4,
    0xc5: opcode_c5,
    0xc6: opcode_c6,
    0xc8: opcode_c8,
    0xc9: opcode_c9,
    0xca: opcode_ca,
    0xcc: opcode_cc,
    0xcd: opcode_cd,
    0xce: opcode_ce,

    0xd0: opcode_d0,
    0xd1: opcode_d1,
    0xd5: opcode_d5,
    0xd6: opcode_d6,
    0xd8: opcode_d8,
    0xd9: opcode_d9,
    0xdd: opcode_dd,
    0xde: opcode_de,

    0xe0: opcode_e0,
    0xe1: opcode_e1,
    0xe4: opcode_e4,
    0xe5: opcode_e5,
    0xe6: opcode_e6,
    0xe8: opcode_e8,
    0xe9: opcode_e9,
    0xea: opcode_ea,
    0xec: opcode_ec,
    0xed: opcode_ed,
    0xee: opcode_ee,

    0xf0: opcode_f0,
    0xf1: opcode_f1,
    0xf5: opcode_f5,
    0xf6: opcode_f6,
    0xf8: opcode_f8,
    0xf9: opcode_f9,
    0xfd: opcode_fd,
    0xfe: opcode_fe
}