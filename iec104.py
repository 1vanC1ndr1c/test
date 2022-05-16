import sys

from hat import aio
import ssl
from hat.drivers import tcp
from hat.drivers.iec60870 import apci
from hat.drivers.iec60870 import iec104


def main():
    aio.run_asyncio(async_main())


async def async_main():
    ctx = ssl.SSLContext()
    ctx.load_cert_chain(certfile='bundle.pem')
    link = await apci.connect(addr=tcp.Address('192.168.0.191', 19998),
                              ssl_ctx=ctx)
    conn = iec104.Connection(link)
    msg = iec104.InterrogationMsg(is_test=False,
                                  originator_address=0,
                                  asdu_address=1,
                                  request=0,
                                  is_negative_confirm=False,
                                  cause=iec104.CommandReqCause.ACTIVATION)

    conn.send([msg])
    while True:
        recv = await conn.receive()
        print(recv)

    await conn.async_close()


if __name__ == '__main__':
    sys.exit(main())
