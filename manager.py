#!/usr/bin/env python3

import traceback
import signal
import asyncio
import aioamqp
import aiofiles
from helper_functions import *


"""
    RabbitMQ Manager reads asynchronously using asyncio library file of SQL's
    And puts each sql as a task in MQ
"""

log, log_exc = init_log('manager.log', log_to_screen_err=True)
logging.info('---------------- Manager Started ----------------')


async def read_tasks():

    file_name = args.file
    message_count = 0
    async with aiofiles.open(file_name, mode='r') as f:
        while True:
            message = await f.readline()
            if not message:  # EOF
                if message_count != 0:
                    logging.info(f"Sent {message_count} messages - waiting")
                message_count = 0
                await asyncio.sleep(1)
            if str(message).strip():  # ignore blank lines
                message_count += 1
                yield message


async def new_task():

    try:
        transport, protocol = await aioamqp.connect(args.host_name, args.port)
    except aioamqp.AmqpClosedConnection:
        logging.error("Can't connect - connection closed")
        return

    channel = await protocol.channel()

    await channel.queue('task_queue', durable=True)
    while True:
        async for message in read_tasks():
            await channel.basic_publish(
                payload=message,
                exchange_name='',
                routing_key='task_queue',
                properties={
                    'delivery_mode': 2,
                },
            )
        # print(f" Sent {message}")

    await protocol.close()
    transport.close()


if __name__ == '__main__':

    #  first check if there is stop request
    my_pid_file = "/tmp/MQ_manager.pid"
    if len(sys.argv) > 1:
        if 'stop' in sys.argv[1].lower():
            check_pid(my_pid_file, action='stop', age_threshold='0')
            sys.exit(0)
    # write pid file
    check_pid(my_pid_file)

    parser = generate_argparser('manager')
    args = parser.parse_args()
    if args.version:
        print('RabbitMQ Manager version 1')
        print(args)
        sys.exit(0)

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(new_task())
        # loop.run_forever()
    except KeyboardInterrupt:
        print("Closing")

    except Exception as e:
        logging.error(traceback.format_exc())
        print('\n', sys.exc_info()[1])
        print("\n\tCheck log for more details\n")
        sys.exit(-1)
    finally:
        os.unlink(my_pid_file)
        loop.close()
