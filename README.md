# Rabbit-manager-worker

This is the excersise to create:
1. manager reads continuosly file of sql inserts and puts it into RabbitMQ queue
2. worker recieves messages from RabbitMQ and executes SQL's in MySQL DB

The work done using Python3 asyncio library.
It requires at minimum python3.5

It's possible to run with ampersand “&” to fork manager and worker.
In this case to stop the programs use "stop" as parameter like: python3.7 manager.py stop

.....
Here is usage of the programs:
<pre>
usage: manager.py [-h] [-f FILE] [-host HOST_NAME] [-p PORT] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to SQL File with insert statements (default:
                        tasks_test.txt)
  -host HOST_NAME, --host_name HOST_NAME
                        RabbitMQ Host (default: localhost)
  -p PORT, --port PORT  RabbitMQ Port (default: 5672)
  --version, -v         Print version info and exit (default: False)


usage: worker.py [-h] [-f FILE] [-host HOST_NAME] [-p PORT]
                 [-chunks CHUNKS_2_REPORT] [-errors MAX_ERRORS]
                 [-sqlh SQL_HOST] [-sqlp SQL_PORT] [-sqluser SQL_USER]
                 [-sqlpass SQL_PASSWORD] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to SQL File with insert statements (default:
                        tasks_test.txt)
  -host HOST_NAME, --host_name HOST_NAME
                        RabbitMQ Host (default: localhost)
  -p PORT, --port PORT  RabbitMQ Port (default: 5672)
  -chunks CHUNKS_2_REPORT, --chunks_2_report CHUNKS_2_REPORT
                        How many received messages to report (default: 10)
  -errors MAX_ERRORS, --max_errors MAX_ERRORS
                        How many received messages to report (default: 5)
  -sqlh SQL_HOST, --sql_host SQL_HOST
                        MySQL Host (default: localhost)
  -sqlp SQL_PORT, --sql_port SQL_PORT
                        MySQL Port (default: 3306)
  -sqluser SQL_USER, --sql_user SQL_USER
                        MySQL User (default: leo)
  -sqlpass SQL_PASSWORD, --sql_password SQL_PASSWORD
                        MySQL Password (default: leopass)
  --version, -v         Print version info and exit (default: False)
</pre>
