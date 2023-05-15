def _ieee754_to_decimal(packet: str) -> int:
    """
    Conversation of 32 bits IEEE 745 numbers to decimal.
    To write numbers in IEEE 754 standard or reconstruct, you must know 3 parameters:
    # S - sign bit (31 bit);
    # E - offset exponenta (30-23 bits);
    # M - fraction of mantissa (22-0 bits)
    This is an integers, wrote in number of IEEE 754 in binary
    The formula to conversation from IEEE 754 to decimal number single precision:
    F = (-1)^S * 2^(E-127) * (1+M/2^23)
    :param packet: str, payload from Eksis thermoanemome, 4 byres ASCII symbols string
    :return: dec_number - int, decimal value, converted from IEEE 754 standard
    """
    if isinstance(packet, str):
        pack = packet
        bits_string = "{0:08b}".format(int(pack, 16))  # convert ASCII symbols string to binary value
        len_bits_string = len(bits_string)
        # we need to get 32 bit binary string, but in result of converting we can get 31 or less bit binary string,
        # because, when MSB in "0", it's not writen for some reasons, so we add lost "0" at the beginning
        if len_bits_string < 32:
            while len_bits_string < 32:
                bits_string = "0" + bits_string
                len_bits_string = len(bits_string)
        sign = int(bits_string[0])  # sign, 1 bit (31)
        exp = int(bits_string[1:9], 2)  # exponent, 8 bits (30-23)
        mant = int(bits_string[9:], 2)  # fraction of mantissa, 23 bits (22-0)

        dec_number = ((-1) ** sign) * (2 ** (exp - 127)) * (1 + (mant / 2 ** 23))
        return dec_number
    else:
        raise TypeError


def _calculate_checksum256(command: str) -> str:
    """

    :param command:
    :return:
    """
    if isinstance(command, str):
        cmd = command
        sum_of_ascii_vals = 0
        checksum = 0
        len_of_pack = len(cmd)
        for ascii_val in cmd[0:len_of_pack]:
            sum_of_ascii_vals += ord(ascii_val)
        checksum = (sum_of_ascii_vals ^ 256) & 0xff
        checksum_hex = hex(checksum).upper()[2:]
        return checksum_hex
    else:
        raise TypeError


def _compare_checksum256(packet: bytes) -> bool:
    """

    :param packet:
    :return:
    """
    if isinstance(packet, bytes):
        pack = packet.decode()
        read_checksum = int(f'{pack[-3]}{pack[-2]}', 16)
        pack = pack[:-3]
        sum_of_ascii_vals = 0
        checksum = 0
        len_of_pack = len(pack)
        for ascii_val in pack[0:len_of_pack]:
            sum_of_ascii_vals += ord(ascii_val)
        checksum = (sum_of_ascii_vals ^ 256) & 0xff
        if checksum == read_checksum:
            return True
        else:
            return False
    else:
        raise TypeError


def _format_packet(command: str, checksum: str) -> bytes:
    """
    Format packet
    :param command:
    :param checksum:
    :return:
    """
    if isinstance(command, str) and isinstance(checksum, str):
        cmd_str = command
        ch_str = checksum
        cmd_b = bytes(cmd_str, 'ascii')
        ch_b = bytes(ch_str, 'ascii')
        tr_b = b'\r'
        pack = cmd_b + ch_b + tr_b
        return pack
    else:
        raise TypeError
