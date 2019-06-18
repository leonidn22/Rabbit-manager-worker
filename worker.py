#!/usr/bin/env python3

import traceback
import asyncio
import aioamqp
from mysql_pool import mysql_insert
from helper_functions import *


"""
    RabbitMQ Worker read from SQL's from queue and perform it in MySQL
    
    To purge queue: sudo rabbitmqctl purge_queue task_queue
"""

log, log_exc = init_log('worker.log',log_to_screen_err=False)
logging.info('---------------- Worker Started ----------------')
message_count = 0
message_sql_errors_count = 0


async def callback(channel, message, envelope, properties):

    global message_count, message_sql_errors_count
    if message_count % args.chunks_2_report == 0:
        print(f"  Received total message_count={message_count}; total error sql messages={message_sql_errors_count} ")
              # , flush=True)
    message_count += 1
    ret_code = await mysql_insert(loop, message)
    # In case of SQL Error Write it to log
    if ret_code != 'Done':
        message_sql_errors_count += 1
        if message_sql_errors_count >= args.max_errors:
            print("-------------------                               ---------------------")
            print("------------------- Reached the Max Errors - EXIT ---------------------")
            print("-------------------                               ---------------------")
            logging.exception("Reached the Max Errors")
            asyncio.get_event_loop().stop()
        logging.exception(ret_code)
    #
    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)


async def worker():
    print(f'loop { loop.is_running()}')
    try:
        transport, protocol = await aioamqp.connect('localhost', 5672)
    except aioamqp.AmqpClosedConnection:
        print("closed connections")
        return

    channel = await protocol.channel()

    await channel.queue(queue_name='task_queue', durable=True)
    await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
    await channel.basic_consume(callback, queue_name='task_queue')


if __name__ == '__main__':

    #  first check if there is stop request
    my_pid_file = "/tmp/MQ_worker.pid"
    if len(sys.argv) > 1:
        if 'stop' in sys.argv[1].lower():
            check_pid(my_pid_file, action='stop', age_threshold='0')
            sys.exit(0)
    # write pid file
    check_pid(my_pid_file)

    parser = generate_argparser('worker')
    args = parser.parse_args()
    if args.version:
        print('RabbitMQ Worker version 1')
        print(args)
        sys.exit(0)
    print(args)
    try:
        loop = asyncio.get_event_loop()
        # asyncio.ensure_future(worker())
        loop.run_until_complete(worker())
        loop.run_forever()
        # while True:
        #     loop.run_until_complete(worker())
        #     if message_count > 0:
        #         logging.info(f"Received {message_count} messages - waiting")
        #         message_count = 0
        #     time.sleep(1)
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

