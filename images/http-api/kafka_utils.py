from kafka import KafkaProducer, KafkaConsumer
import json


CONNECT = '10.232.29.140:9092'
USERNAME = 'admin'
PASSWORD = 'test1234'
GROUP = 'http-api'


def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def key_serializer(data):
    return data.encode("utf-8")


def produce(request_json):
    producer = KafkaProducer(bootstrap_servers=[CONNECT], 
                            value_serializer=json_serializer,
                            security_protocol='SASL_PLAINTEXT',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username=USERNAME,
                            sasl_plain_password=PASSWORD)

    request = json.loads(request_json)

    topic = request["topic"]
    key = request["key"]
    msg = request["message"]

    producer.send(topic, value=msg, key=key)
    return "Successful"


def consume(request_json):
    request = json.loads(request_json)

    topic = request["topic"]

    consumer = KafkaConsumer(topic,
                            bootstrap_servers=CONNECT,
                            auto_offset_reset='earliest',
                            group_id=GROUP,
                            security_protocol='SASL_PLAINTEXT',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username=USERNAME,
                            sasl_plain_password=PASSWORD)

    for msg in consumer:
        data = json.loads(msg.value)
        consumer.close()

    return data
