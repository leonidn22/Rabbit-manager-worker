# Rabbit-manager-worker

This is the excersise to create:
1. manager reads continuosly file of sql inserts and puts it into RabbitMQ queue
2. worker recieves messages from RabbitMQ and executes SQL's in MySQL DB

The work done using Python3 asyncio library.
It requires at minimum python3.5

It's possible to run with ampersand “&” to fork manager and worker.
In this case to stop the programs use "stop" as parameter like: python3.7 manager.py stop

.....
