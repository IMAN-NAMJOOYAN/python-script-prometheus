# python-script-prometheus
**Monitoring metrics by python script and prometheus**

We used a simple Python script to monitor the number of metrics from the status of the host (Oracle Linux) in Prometheus. Finally, we displayed the values in Grafana.

![image](https://github.com/IMAN-NAMJOOYAN/python-script-prometheus/assets/16554389/671736bb-bfd3-494c-8d47-6e9257cb9627)


**Requirements:**
```
0- Prometheus Stack (installed on Kubernetes cluster)

https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack

1- Oracle Linux 8.5 (the target host is installed as a virtual machine outside the Kubernetes cluster)
2- Python 3.9
3- pip 3.9
4- psutil and prometheus_client libraries
```
**Steps:**

1- Installing Python 3.9
```
dnf install python39 -y
```
2- Installing pip
```
dnf install python39-pip.noarch -y
```
3- Installing required libraries
```
pip3.9 install psutil prometheus_client
```
4- Creating a Python script
```
You can use the py-metrics.py script file. 
```
5- Creating a service for the corresponding script
```
cat <<EOF> /etc/systemd/system/py-metrics.service
[Unit]
Description=Get Resource Metrics By Python
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3.9 /tmp/py-metrics.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now py-metrics.service

```

6- View metrics

![image](https://github.com/IMAN-NAMJOOYAN/python-script-prometheus/assets/16554389/b02ff2af-db4e-4446-bb61-f65d9b9e2054)

7- Creating  external service, endpoint and service monitor in Kubernetes in order to monitor metrics in Prometheus

You can use the py-extservice.yaml,py-extendpoint.yaml and py-svcmonitor.yaml manifest file.
```
kubectl apply -f py-extservice.yaml
kubectl apply -f py-extendpoint.yaml
kubectl apply -f py-svcmonitor.yaml
```
![image](https://github.com/IMAN-NAMJOOYAN/python-script-prometheus/assets/16554389/0d6b051e-82f4-4e0f-825a-66256bfd1b2f)


Note: In the py-extendpoint.yaml file, instead of the ip value, put the IP value of the desired host whose metrics are to be monitored.

8- Creating a dashboard in Grafana.

![image](https://github.com/IMAN-NAMJOOYAN/python-script-prometheus/assets/16554389/61b90efa-60db-456a-876e-59292560b17a)



