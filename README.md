# Rabbit-manager-worker

This is the excersise to create:
1. manager reads continuosly file of sql inserts and put it into RabbitMQ queue
2. worker recieves messages from RabbitMQ and perform SQl's in MySQL DB

The work done using Python3 asyncio library.
It requires at minimum python3.5
