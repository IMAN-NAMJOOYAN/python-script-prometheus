# python-script-prometheus
**Monitoring metrics by python script and prometheus**

We used a simple Python script to monitor the number of metrics from the status of the host (Oracle Linux) in Prometheus. Finally, we displayed the values in Grafana.

**Requirements:**
```
0- Prometheus Stack (installed on Kubernetes cluster)
1- Oracle Linux 8.x (the target host is installed as a virtual machine outside the Kubernetes cluster)
2- Python 3.8
3- pip 3.8
4- psutil and prometheus_client libraries
```
**Steps:**
1- Installing Python 3.8
```
dnf install python38 -y
```
2- Installing pip
```
dnf install python38-pip.noarch -y
```
3- Installing required libraries
```
pip3.8 install psutil prometheus_client
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
ExecStart=/usr/bin/python3.8 /tmp/py-metrics.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now py-metrics.service

```

6- View metrics
7- Creating monitor service in Kubernetes in order to monitor metrics in Prometheus
8- Creating a dashboard in Grafana
