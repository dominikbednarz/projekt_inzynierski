from kubernetes.client.rest import ApiException
from kubernetes import client, config
import kubernetes.client
import requests
import time


NAMESPACE = 'kafka'


def check_prom(topic):
    url = 'http://prometheus.monitoring.svc:9090/api/v1/query'
    response = requests.get(url, params={'query': 'sum(rate(kafka_server_brokertopicmetrics_messagesin_total{topic="%s"}[1m]))' % topic})
    data = response.json()
    data_result = data['data']['result'][0]['value'][1]
    final = float(data_result)
    return final


def scale(replicas, name, namespace):
    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config()
        except config.ConfigException:
            raise Exception("[ERROR] Problem with connection to K8s cluster")

    api = client.AppsV1Api()
    spec = kubernetes.client.V1ScaleSpec()
    spec.replicas = replicas
    body = kubernetes.client.V1Scale(spec=spec)

    try:
        api.patch_namespaced_deployment_scale(name, namespace, body=body)
        return "[INFO] Successfully scaled %s to %s replicas" % (name, replicas)
    except ApiException as e:
        return "[ERROR] Exception when calling AppsV1Api->patch_namespaced_deployment_scale: %s\n" % e


prevStateA = 1
prevStateB = 1


if __name__ == "__main__":
    while True:
        valueA = check_prom('queue-A')
        valueB = check_prom('queue-B')

        if(valueA == 0 or valueB == 0):
            podsA = 1
            podsB = 1
        else:
            if(valueA > 1.5*valueB):
                podsA = 2
                podsB = 1  
            elif(valueA > 2.5*valueB):
                podsA = 3
                podsB = 1
            elif(valueB > 1.5*valueA):
                podsA = 1
                podsB = 2
            elif(valueB > 2.5*valueA):
                podsA = 1
                podsB = 3
            else:
                podsA = 1
                podsB = 1 

        if(podsA != prevStateA):
            scaleA = scale(podsA, 'app-a', NAMESPACE)
            print(scaleA)
            prevStateA = podsA
        if(podsB != prevStateB):    
            scaleB = scale(podsB, 'app-b', NAMESPACE)
            print(scaleB)
            prevStateB = podsB

        time.sleep(60)