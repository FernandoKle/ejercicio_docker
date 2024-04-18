# By: Fernando Kleinubing
# https://aulavirtual.fio.unam.edu.ar/mod/assign/view.php?id=71502

import asyncio, ssl, certifi, logging, os, sys
import aiomqtt
from contextvars import ContextVar

logging.basicConfig(format='%(asctime)s: servicio_:mqtt (%(thread)s) - %(levelname)s -> %(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

class Datos():
    contador = 0

datos = Datos()

cola_1 = asyncio.Queue()
cola_2 = asyncio.Queue()

##################################################################################

async def incrementa():
    while True:
        logging.info("Incrementa contador")
        datos.contador += 1
        await asyncio.sleep(3)

##################################################################################

async def publica(client):
    while True:
        logging.info("Publicando datos...")
        await client.publish(os.environ['TOPICO_PUBLICA'], payload=datos.contador)
        await asyncio.sleep(5)

##################################################################################

async def escucha_1(client):
    while True:
        message = await cola_1.get()
        logging.info(os.environ['TOPICO_1'] + ": " + message.payload.decode("utf-8"))

##################################################################################

async def escucha_2(client):
    while True:
        message = await cola_2.get()
        logging.info(os.environ['TOPICO_2'] + ": " + message.payload.decode("utf-8"))

##################################################################################

async def distribuye(client):

    async for message in client.messages:

        if message.topic.matches(os.environ['TOPICO_1']):
            cola_1.put_nowait(message)

        elif message.topic.matches(os.environ['TOPICO_2']):
            cola_2.put_nowait(message)

################################# MAIN ###########################################

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
        
        await client.subscribe( os.environ['TOPICO_1'] )
        await client.subscribe( os.environ['TOPICO_2'] )
        
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task( publica(client)    )
            task2 = tg.create_task( distribuye(client) )
            task3 = tg.create_task( escucha_1(client)  )
            task4 = tg.create_task( escucha_2(client)  )
            task5 = tg.create_task( incrementa()       )

########################## END MAIN #########################################

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logging.info("Terminando ejecucion")
        sys.exit(0)
