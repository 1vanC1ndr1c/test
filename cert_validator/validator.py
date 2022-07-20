import datetime
import subprocess
import sys
import typing
from pathlib import Path
import os
import cryptography.x509.base
from cryptography import x509

"""
Conf contains:
- cert_path: certificate that is being validated,
- authorized_names: certificates that can connect, None if not supported
- root_ca_path: certificate of CA, None if self signed
- provisioned_certificates_dir: dir with public keys and certs bundled in 
 .pem format; only used with self signed certs, else None. Dictated by the
 standard that storage of that kind needs to exist (line 939).
"""

_default_conf = {
    'cert_path': Path(__file__).parent.resolve() / 'certs' / 'RTU_Cert.pem',
    'authorized_names': ['192.168.0.29', 'RTU_Cert'],
    'root_ca_path': Path(__file__).parent.resolve() / 'certs' / 'root_CA.pem',
    'provisioned_certificates_dir': None
}

_default_conf2 = {
    'cert_path': (Path(__file__).parent.resolve()
                  / 'certs'
                  / 'self_signed_cert.pem'),
    'authorized_names': ['192.168.0.29', 'RTU_Cert', 'self_signed_cert'],
    'root_ca_path': None,
    'provisioned_certificates_dir': (Path(__file__).parent.resolve() / 'certs')
}


def main(conf):
    cert_path = conf['cert_path']
    root_ca_path = conf['root_ca_path']
    authorized_names = conf['authorized_names']
    provisioned_certificates_dir = conf['provisioned_certificates_dir']
    self_signed = root_ca_path is None

    cert = get_x509_cert(cert_path)

    verify_subject_name(cert, authorized_names, cert_path)
    verify_digital_signature(self_signed, cert_path, root_ca_path)
    verify_date_range(cert, cert_path)

    # If the certificate is self-signed by device, additional operations
    # must be performed as listed below:
    if self_signed:
        verify_provisioned_public_key(
            provisioned_certificates_dir, cert, cert_path)

    # If the Central Authority is supported and the certificate is signed by the Central Authority,
    # additional operations on the remote station’s certificate must be performed as listed below:
    breakpoint()
    pass


if __name__ == '__main__':
    sys.exit(main(_default_conf))


def get_x509_cert(cert_path: Path) -> cryptography.x509.base.Certificate:
    with open(cert_path, 'rb') as file:
        cert = file.read()
        cert = x509.load_pem_x509_certificate(cert)
    return cert


def verify_subject_name(cert: cryptography.x509.base.Certificate,
                        authorized_names: typing.List[str],
                        cert_path: Path):
    """
    Verify the Subject Name of the certificate,
    if the list of authorized remote stations is configured,
    :param cert: Cerificate being verified
    :param authorized_names: list of authorized names
    :param cert_path: path to the certificate
    """

    name = cert.subject
    name = name.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    if authorized_names and len(name) == 0:
        raise Exception(f'Certificate "{cert_path}" does not have a '
                        'common name but authorized names are supported. '
                        'Therefore, the certificate needs a common name.')
    name = name[0].value
    if authorized_names and name not in authorized_names:
        raise Exception(f'Certificate "{cert_path}" is not authorized '
                        f'for connections')


# TODO
def verify_digital_signature(self_signed: bool,
                             cert_path: Path,
                             root_ca_path: Path):
    # Verify the certificate digital signature (self signed)
    if self_signed:
        verification_process = subprocess.Popen(
            ['openssl', 'verify', '-verbose', '-CAfile',
             str(cert_path), str(cert_path)], stdout=subprocess.PIPE)

    # Verify the certificate digital signature (CA signed)
    else:
        verification_process = subprocess.Popen(
            ['openssl', 'verify', '-verbose', '-CAfile',
             str(root_ca_path), str(cert_path)], stdout=subprocess.PIPE)

    resp = verification_process.communicate()[0].decode()
    resp = resp[resp.index(':') + 2:].strip()

    if resp != 'OK':
        raise Exception(f'Certificate "{cert_path}" '
                        f'is not signed by "{root_ca_path}"')


def verify_date_range(cert: cryptography.x509.base.Certificate,
                      cert_path: Path):
    #  Verify starting validity date permits the certificate to be used.
    if datetime.datetime.now() < cert.not_valid_before:
        raise Exception(f'Certificate "{cert_path}"  is not yet valid')

    # Verify that the certificate is not expired.
    if datetime.datetime.now() > cert.not_valid_after:
        raise Exception(f'Certificate "{cert_path}"  is no longer valid')


def verify_provisioned_public_key(provisioned_certificates_dir: Path,
                                  cert: cryptography.x509.base.Certificate,
                                  cert_path: Path):
    name = os.path.basename(cert_path)
    prov_cert = get_x509_cert(provisioned_certificates_dir / name)

    # Verify that the public key contained in the certificate
    # is provisioned on the local device.
    if prov_cert.public_key() != cert.public_key():
        raise Exception(f'Certificate "{cert_path}" '
                        f'is not provisioned locally')
