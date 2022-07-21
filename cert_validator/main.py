import sys
from pathlib import Path

import validator


def do_validation_with_fake_data():
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
        'provisioned_certs_dir': None}

    _default_conf2 = {
        'authorized_names': ['self_signed_cert'],
        'root_ca_path': None,
        'provisioned_certs_dir': (Path(__file__).parent.resolve() / 'certs')}

    conf = _default_conf

    tmp_path = (Path(__file__).parent.resolve()
                / 'certs' / f'{conf["authorized_names"][0]}.pem')
    with open(tmp_path, 'rb') as file:
        cert_bytes = file.read()

    validator.verify(cert_bytes, conf)


if __name__ == '__main__':
    sys.exit(do_validation_with_fake_data())
