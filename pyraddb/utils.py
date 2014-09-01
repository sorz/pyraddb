import hashlib
import binascii


def nt_hash(s):
    """Calculate NT-Password."""
    hash = hashlib.new('md4', s.encode('utf-16le')).digest()
    return binascii.hexlify(hash).decode('ascii').upper()


