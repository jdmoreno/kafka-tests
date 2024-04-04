from confluent_kafka import Producer

# mybroker1 = '127.0.0.1:9192,127.0.0.1:9292,127.0.0.1:9392'
# config = {'bootstrap.servers': 'localhost:9192,localhost:9292,localhost:9392'}
config = {'bootstrap.servers': 'localhost:9182,localhost:9183,localhost:9184'}

p = Producer(config)
some_data_source = ['one', 'two', 'three']

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


for data in some_data_source:
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message. The delivery report callback will
    # be triggered from the call to poll() above, or flush() below, when the
    # message has been successfully delivered or failed permanently.
    p.produce('mytopic', data.encode('utf-8'), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()