#!/usr/bin/env python3

import logging
import logging.handlers
import psutil
import time
from logging.handlers import TimedRotatingFileHandler
import os, sys
import argparse


def init_log(log_file='rmq.log', log_to_screen_err=False, log_format_type='lineno'):

    log_file_no_ext = '.'.join(log_file.split('.')[:-1])
    log_file_exceptions = log_file_no_ext + '_errors.log'
    curr_dir = os.getcwd()
    # curr_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    log_file = os.path.join(curr_dir, log_file)
    exc_file = os.path.join(curr_dir, log_file_exceptions)
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    if log_format_type == 'simple':
        log_format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    else:
        log_format = '%(asctime)s %(levelname)-8s [ %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s'

    logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S', filename=os.devnull,
                    level=logging.ERROR)
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    handler = TimedRotatingFileHandler(log_file, when='midnight', utc=True, backupCount=60)
    # handler = RotatingFileHandler(log_file, maxBytes=1024*1024*80, backupCount=60)

    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    if not os.path.exists(os.path.dirname(exc_file)):
        os.makedirs(os.path.dirname(exc_file))
    log_exc = logging.FileHandler(exc_file, mode='a', encoding=None, delay=False)
    log_exc.setLevel(logging.ERROR)
    log_exc.setFormatter(formatter)
    log.addHandler(log_exc)

    if log_to_screen_err:
        log_to_screen_err = logging.StreamHandler(sys.stdout)
        log.addHandler(log_to_screen_err)
        log_to_screen_err.setLevel(logging.INFO)

    return log, log_exc


def generate_argparser(program_name):
    LICENSE = """
    It's free software
    """

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=LICENSE)
    parser.add_argument('-f', '--file', required=False, default='tasks_test.txt',
                        help="Path to SQL File with insert statements")
    parser.add_argument('-host', '--host_name', required=False, default='localhost',
                        help="RabbitMQ Host")
    parser.add_argument('-p', '--port', required=False, default='5672',
                        help="RabbitMQ Port")
    if program_name == 'worker':
        parser.add_argument('-chunks', '--chunks_2_report', required=False, default=10, type=int,
                            help="How many received messages to report")
        parser.add_argument('-errors', '--max_errors', required=False, default=5, type=int,
                            help="How many received messages to report")

        parser.add_argument('-sqlh', '--sql_host', required=False, default='localhost',
                            help="MySQL Host")
        parser.add_argument('-sqlp', '--sql_port', required=False, default='3306',
                            help="MySQL Port")
        parser.add_argument('-sqluser', '--sql_user', required=False, default='leo', type=str,
                            help="MySQL User")
        parser.add_argument('-sqlpass', '--sql_password', required=False, default='leopass', type=str,
                            help="MySQL Password")

    parser.add_argument('--version', '-v', action='store_true', help='Print version info and exit')

    return parser


def check_pid(pid_file, table_type='none', age_threshold='500', action='exit'):
    """
    Check if the same program is running
    In case the program is not running, will write pid file
    In case action is stop will terminate the program and exited.
    """
    pid = str(os.getpid())
    try:
        if os.path.isfile(pid_file):
            # check that old pid is running
            f = open(pid_file)
            old_pid = f.readlines()[0]
            if psutil.pid_exists(int(old_pid)):
                logging.info(
                    "PID file: {pfile} already exists, and running process found,  check file PID age".format(pfile=pid_file))
                # Check if pid_file is older than age_threshold ...
                # Time in seconds since epoch
                file_mod_time = round(os.stat(pid_file).st_mtime)
                now_sec = round(time.time())
                pid_file_age_minutes = int((now_sec - file_mod_time)/60)
                # logging.info('pid_file_age_minutes = %d ' % pid_file_age_minutes)
                if pid_file_age_minutes >= int(age_threshold):
                    logging.info('OLD PID FILE - %d minutes, that is more than age_threshold. Exit...' % pid_file_age_minutes)
                    if action == 'no_exit':
                        return 'exit'
                    elif action == 'exit':
                        sys.exit(0)
                    elif action == 'stop':
                        for proc in psutil.process_iter():
                            for cmdline in proc.cmdline():
                                if sys.argv[0] in cmdline:
                                    # logging.info(cmdline)
                                    if os.getpid() != proc.pid:
                                        logging.info('Kill old process %s' % proc.cmdline())
                                        proc.terminate()
                                        proc.kill()
                                        os.unlink(pid_file)
                                        sys.exit(0)
                        # write pid after removing
                        #     open(pid_file, 'w').write(pid)
                    sys.exit(-1)
                else:
                    # os.unlink(pid_file)pid_file_age_minutes
                    pass

            else:
                logging.warning(
                    "PID file: {pfile} already exists, but no running process found, file will be removed".format(
                        pfile=pid_file))
                os.unlink(pid_file)
            # write pid after removing
                open(pid_file, 'w').write(pid)
        elif not os.path.exists(pid_file):
            open(pid_file, 'w').write(pid)
    except Exception as e:
        return logging.warning(e)
    return 'no_exit'
