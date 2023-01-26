from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import hashlib


CONNECT = '10.232.29.140:9092'
USERNAME = 'admin'
PASSWORD = 'test1234'
GROUP = 'app-B'

sourceTopicName = "queue-B"
resultTopicName = "result-B"

ALGORITHM = 'sha512'


def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def make_hash(data):
    h = hashlib.new(ALGORITHM)
    h.update(data.encode('utf8')) 
    result = h.hexdigest()
    return result

consumer = KafkaConsumer(sourceTopicName,
                        bootstrap_servers=CONNECT,
                        auto_offset_reset='earliest',
                        group_id=GROUP,
                        security_protocol='SASL_PLAINTEXT',
                        sasl_mechanism='PLAIN',
                        sasl_plain_username=USERNAME,
                        sasl_plain_password=PASSWORD)

producer = KafkaProducer(bootstrap_servers=[CONNECT], 
                        # key_serializer=key_serializer,
                        value_serializer=json_serializer,
                        security_protocol='SASL_PLAINTEXT',
                        sasl_mechanism='PLAIN',
                        sasl_plain_username=USERNAME,
                        sasl_plain_password=PASSWORD)

if __name__ == '__main__':
    print("Start processing data from topic: %s" % sourceTopicName)

    for msg in consumer:
        data = json.loads(msg.value)
        print("Data read: {}".format(data))
        
        result = make_hash(data)

        producer.send(resultTopicName, value=result)