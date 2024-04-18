# By: Fernando Kleinubing
# https://aulavirtual.fio.unam.edu.ar/mod/assign/view.php?id=71502

import asyncio, ssl, certifi, logging, os, sys
import aiomqtt
from contextvars import ContextVar

WorkerName = ContextVar('worker_name')

logging.basicConfig(format='%(asctime)s: servicio_mqtt (%(worker_name)s) - %(levelname)s -> %(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

class WorkerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        kwargs.setdefault('extra', {})['worker_name'] = WorkerName.get()
        return msg, kwargs

logger = WorkerAdapter(logging.getLogger(__name__), None)

async def main():
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

    async with aiomqtt.Client(
        os.environ['SERVIDOR'],
        port=8883,
        tls_context=tls_context,
    ) as client:
        await client.subscribe(os.environ['TOPICO_1'])
        async for message in client.messages:
            logger.info(str(message.topic) + ": " + message.payload.decode("utf-8"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Terminando ejecucion")
        sys.exit(0)