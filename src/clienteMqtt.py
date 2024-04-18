# By: Fernando Kleinubing
# https://aulavirtual.fio.unam.edu.ar/mod/assign/view.php?id=71502

import asyncio, ssl, certifi, logging, os, sys
import aiomqtt
from contextvars import ContextVar

logging.basicConfig(format='%(asctime)s: servicio_:mqtt (%(thread)s) - %(levelname)s -> %(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')


async def main():

    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

    client = aiomqtt.Client(
        os.environ['SERVIDOR'],
        port=8883,
        tls_context=tls_context,
        )

    #await client.conect()
    await client.subscribe( os.environ['TOPICO_1'] )

    async for message in client.messages:
        logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Terminando ejecucion")
        sys.exit(0)