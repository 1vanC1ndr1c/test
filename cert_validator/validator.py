import datetime
import os
import subprocess
import tempfile
import typing
from pathlib import Path

import cryptography.x509.base
from cryptography import x509

"""
Conf contains:
- cert_path: certificate that is being validated,
- authorized_names: certificate (subject names) that can connect, 
    None if not supported
- root_ca_path: certificate of CA, None if self signed
- provisioned_certs_dir: dir with public keys and certs bundled in
 .pem format; only used with self signed certs, else None. Dictated by the
 standard that storage of that kind needs to exist (line 939).
"""


def verify(cert_bytes, conf):
    """
    Certificate verification procedure as defined in IEC 62351-5 2021

    """
    cert = x509.load_pem_x509_certificate(cert_bytes)
    root_ca_path = conf['root_ca_path']
    authorized_names = conf['authorized_names']
    provisioned_certs_dir = conf['provisioned_certs_dir']

    # 1. Verify the Subject Name of the certificate
    # (if the list of authorized remote stations is configured)
    cert_cn = _verify_subject_name(cert, authorized_names)
    # 2. Verify the certificate digital signature.
    _verify_digital_signature(cert_cn, cert_bytes, root_ca_path)

    # 3. Verify that the starting validity date.
    # 4. Verify that the certificate is not expired.
    _verify_date_range(cert, cert_cn)

    self_signed = root_ca_path is None
    # If the certificate is self-signed by device, additional operations
    # must be performed as listed below:
    if self_signed is None:
        # 5. Verify that the public key contained in
        # the certificate is provisioned on the local device.
        _verify_provisioned_public_key(provisioned_certs_dir,
                                       cert_bytes,
                                       cert_cn)

    # If the Central Authority is supported and the certificate
    # is signed by the Central Authority, additional operations on the remote
    # station’s certificate must be performed as listed below:
    else:
        # 5. Verify that the certificate was  issued by a recognized
        # Central Authority. (done by checking signature)
        # 6. Verify that the certificate is
        # not revoked by the Central Authority.
        verify_crl(cert_bytes)
        # If RBAC and the Area of Responsibility (AoR) are supported,
        # verify that the AoR text strings in the remote station’s certificate
        # matches at least one such string in the local station’s certificate
        # TODO


def _verify_subject_name(cert, authorized_names):
    name = cert.subject
    name = name.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    if authorized_names and len(name) == 0:
        raise Exception(
            f'Certificate with serial number:"{cert.serial_number}" '
            'does not have a common name but authorized names are supported. '
            'Therefore, the certificate must have a common name.')

    name = name[0].value
    if authorized_names and name not in authorized_names:
        raise Exception(f'Certificate "{name}" is not authorized to connect')

    return name


def _verify_digital_signature(cert_cn: str,
                              cert_bytes: bytes,
                              root_ca_path: Path):
    self_signed = root_ca_path is None

    with tempfile.NamedTemporaryFile() as cert_file:
        cert_file.write(cert_bytes)
        cert_file.seek(0)

        if self_signed:
            verification_process = subprocess.Popen([
                'openssl', 'verify', '-CAfile',
                cert_file.name, cert_file.name],
                stdout=subprocess.PIPE)

        else:
            verification_process = subprocess.Popen([
                'openssl', 'verify', '-CAfile',
                str(root_ca_path), cert_file.name],
                stdout=subprocess.PIPE)

        resp = verification_process.communicate()[0].decode()

    resp = resp[resp.index(':') + 2:].strip()
    if resp != 'OK':
        raise Exception(f'Certificate "{cert_cn} signature failed"')


def _verify_date_range(cert: cryptography.x509.base.Certificate,
                       cert_cn: str):
    if datetime.datetime.now() < cert.not_valid_before:
        raise Exception(f'Certificate "{cert_cn}"  is not yet valid')

    if datetime.datetime.now() > cert.not_valid_after:
        raise Exception(f'Certificate "{cert_cn}"  is no longer valid')


def _verify_provisioned_public_key(provisioned_certs_dir: Path,
                                   cert_bytes: bytes,
                                   cert_cn: str):
    pem_files = [provisioned_certs_dir / str(file)
                 for file in os.listdir(provisioned_certs_dir)
                 if (provisioned_certs_dir / str(file)).suffix == '.pem']

    if not pem_files:
        raise Exception(f'No .pem certificates found '
                        f'at given location ({provisioned_certs_dir})')

    with tempfile.NamedTemporaryFile() as cert_file:
        cert_file.write(cert_bytes)
        cert_file.seek(0)
        cert_pub_key = _get_public_key_from_cert(cert_file.name)

    for pem_file_path in pem_files:
        file_pub_key = _get_public_key_from_cert(str(pem_file_path))

        if cert_pub_key == file_pub_key:
            return

    raise Exception(f'Certificate for {cert_cn} is not provisioned'
                    f'on the local device')


def verify_crl(cert_bytes):
    pass


def _get_public_key_from_cert(file_path: str):
    public_key_process = subprocess.Popen([
        'openssl', 'x509', '-pubkey', '-noout', '-in', file_path],
        stdout=subprocess.PIPE)
    public_key = public_key_process.communicate()[0]
    return public_key


def _get_x509_cert(cert_path: Path) -> cryptography.x509.base.Certificate:
    with open(cert_path, 'rb') as file:
        cert = file.read()
        cert = x509.load_pem_x509_certificate(cert)
    return cert
