from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer
import json


# CONNECT = '10.232.29.140:9092'
CONNECT = 'kafka.kafka.svc:9094'
USERNAME = 'admin'
PASSWORD = 'test1234'


def create_topic(name, partitions, replicas):
    admin_client = KafkaAdminClient(
                                    bootstrap_servers=CONNECT, 
                                    # client_id='test',
                                    security_protocol='SASL_PLAINTEXT',
                                    sasl_mechanism='PLAIN',
                                    sasl_plain_username=USERNAME,
                                    sasl_plain_password=PASSWORD
        )

    topic_list = []
    topic_list.append(NewTopic(name=name, num_partitions=partitions, replication_factor=replicas))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)


def topic_list():
    admin_client = KafkaAdminClient(bootstrap_servers=CONNECT, 
                                    security_protocol='SASL_PLAINTEXT',
                                    sasl_mechanism='PLAIN',
                                    sasl_plain_username=USERNAME,
                                    sasl_plain_password=PASSWORD)

    topic_list = admin_client.list_topics()

    full_list = []

    for topic in topic_list:
        tmp_list = []
        name = [f'{topic}']
        describe = admin_client.describe_topics(name)
        tmp = describe[0]['partitions']
        partitions = len(tmp)
        replicas = len(tmp[0]['replicas'])
        tmp_list.append(topic)
        tmp_list.append(partitions)
        tmp_list.append(replicas)
        full_list.append(tmp_list)

    return full_list


def topics():
    admin_client = KafkaAdminClient(bootstrap_servers=CONNECT, 
                                    security_protocol='SASL_PLAINTEXT',
                                    sasl_mechanism='PLAIN',
                                    sasl_plain_username=USERNAME,
                                    sasl_plain_password=PASSWORD)

    topic_list = admin_client.list_topics()
    final_list = []

    for topic in topic_list:
        tmp_tuple = (topic, topic)
        final_list.append(tmp_tuple)

    return final_list


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def produce(topic, message):
    producer = KafkaProducer(bootstrap_servers=[CONNECT], 
                            value_serializer=json_serializer,
                            security_protocol='SASL_PLAINTEXT',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username=USERNAME,
                            sasl_plain_password=PASSWORD)

    producer.send(topic, value=message)