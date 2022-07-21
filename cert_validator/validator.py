import datetime
import os
import subprocess
import sys
import tempfile
import typing
from pathlib import Path

import cryptography.x509.base
from cryptography import x509


def outside_prereqs():
    # todo delete this function
    """
    Conf contains:
    - cert_path: certificate that is being validated,
    - authorized_names: certificates that can connect, None if not supported
    - root_ca_path: certificate of CA, None if self signed
    - provisioned_certs_dir: dir with public keys and certs bundled in
     .pem format; only used with self signed certs, else None. Dictated by the
     standard that storage of that kind needs to exist (line 939).
    """

    _default_conf = {
        'authorized_names': ['RTU_Cert'],
        'root_ca_path': Path(
            __file__).parent.resolve() / 'certs' / 'root_CA.pem',
        'provisioned_certs_dir': None
    }

    _default_conf2 = {
        'authorized_names': ['self_signed_cert'],
        'root_ca_path': None,
        'provisioned_certs_dir': (Path(__file__).parent.resolve() / 'certs')
    }

    conf = _default_conf2
    tmp_path = (Path(__file__).parent.resolve()
                / 'certs' / f'{conf["authorized_names"][0]}.pem')
    with open(tmp_path, 'rb') as file:
        cert_bytes = file.read()
    main(cert_bytes, conf)


def main(cert_bytes, conf):
    cert = x509.load_pem_x509_certificate(cert_bytes)
    root_ca_path = conf['root_ca_path']
    authorized_names = conf['authorized_names']
    provisioned_certs_dir = conf['provisioned_certs_dir']

    # 1. Verify the Subject Name of the certificate
    # (if the list of authorized remote stations is configured)
    name = verify_subject_name(cert, authorized_names)
    # 2. Verify the certificate digital signature.
    verify_digital_signature(name, cert_bytes, root_ca_path)

    # 3. Verify that the starting validity date.
    # 4. Verify that the certificate is not expired.
    verify_date_range(cert, name)
    breakpoint()
    # If the certificate is self-signed by device, additional operations
    # must be performed as listed below:
    if root_ca_path is None:
        # 5. Verify that the public key contained in
        # the certificate is provisioned on the local device.
        verify_provisioned_public_key(provisioned_certs_dir, cert, name)

    # If the Central Authority is supported and the certificate is signed by the Central Authority,
    # additional operations on the remote station’s certificate must be performed as listed below:
    pass


def verify_subject_name(cert: cryptography.x509.base.Certificate,
                        authorized_names: typing.List[str]) -> str:
    """
    Verifies subject name by checking if the certificate has a common name
    and if the common name is contained within names authorized to connect.
    Args:
        cert: certificate being verified
        authorized_names: list of authorized names

    Returns: name string, if the verification was successful
    Raises:
        Exception: if verification fails because the certificate does not have
        a common name or the name if not contained within authorized names

    """
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


def verify_digital_signature(cert_name: str,
                             cert_bytes: bytes,
                             root_ca_path: Path):
    """
    Verifies the digital signature of the certificate.
    If it is self-signed, own public key is used for verification.
    If CA is used, root CA public key is used for verification.
    Args:
        cert_name: name of the certificate being verified
        cert_bytes: certificate being verified, represented in bytes
        root_ca_path: path to the root CA file

   Raises:
        Exception: if verification fails

    """
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
        raise Exception(f'Certificate "{cert_name} signature failed"')


def verify_date_range(cert: cryptography.x509.base.Certificate,
                      cert_name: str):
    """
    Verifies whether the starting validity date permits the certificate to be
    used or if the certificate is expired.
    Args:
        cert: certificate being verified
        cert_name: name of the certificate being verified

    Raises:
        Exception: if the certificate cannot yet be used or if it is expired
    """
    if datetime.datetime.now() < cert.not_valid_before:
        raise Exception(f'Certificate "{cert_name}"  is not yet valid')

    if datetime.datetime.now() > cert.not_valid_after:
        raise Exception(f'Certificate "{cert_name}"  is no longer valid')


def verify_provisioned_public_key(provisioned_certs_dir: Path,
                                  cert: cryptography.x509.base.Certificate,
                                  cert_path: Path):
    # TODO
    # name = os.path.basename(cert_path)
    # prov_cert = _get_x509_cert(provisioned_certs_dir / name)

    # Verify that the public key contained in the certificate
    # is provisioned on the local device.
    # if prov_cert.public_key() != cert.public_key():
    #   raise Exception(f'Certificate "{cert_path}" '
    #                    f'is not provisioned locally')
    return


def _get_x509_cert(cert_path: Path) -> cryptography.x509.base.Certificate:
    with open(cert_path, 'rb') as file:
        cert = file.read()
        cert = x509.load_pem_x509_certificate(cert)
    return cert


if __name__ == '__main__':
    sys.exit(outside_prereqs())
