import sys
from hat import aio
from hat.drivers.iec60870 import iec104
from hat.drivers.iec60870 import apci
from hat.drivers import tcp


def main():
    aio.run_asyncio(async_main())


async def async_main():
    link = await apci.connect(addr=tcp.Address('127.0.0.1', 1234))
    conn = iec104.Connection(link)
    print('nesto')
    breakpoint()
    pass
    await conn.async_close()


if __name__ == '__main__':
    sys.exit(main())
