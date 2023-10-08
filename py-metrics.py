import psutil
from prometheus_client import make_wsgi_app, Gauge
from wsgiref.simple_server import make_server

disk_total = Gauge('disk_total_bytes', 'Total Disk Capacity', ['partition', 'mountpoint'])
disk_free = Gauge('disk_free_bytes', 'Free Disk Space', ['partition', 'mountpoint'])
disk_used = Gauge('disk_used_bytes', 'Used Disk Space', ['partition', 'mountpoint'])

cpu_usage = Gauge('cpu_usage_percent', 'CPU Usage Percent')
memory_total = Gauge('memory_total_bytes', 'Total Memory')
memory_used = Gauge('memory_used_bytes', 'Used Memory')
memory_free = Gauge('memory_free_bytes', 'Free Memory')

def collect_metrics(environ, start_response):
    partitions = psutil.disk_partitions(all=True)

    for partition in partitions:
        if partition.fstype == "xfs":
            partition_name = partition.device
            disk_info = psutil.disk_usage(partition.mountpoint)

            disk_total.labels(partition=partition_name, mountpoint=partition.mountpoint).set(disk_info.total)
            disk_free.labels(partition=partition_name, mountpoint=partition.mountpoint).set(disk_info.free)
            disk_used.labels(partition=partition_name, mountpoint=partition.mountpoint).set(disk_info.used)

    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_usage.set(cpu_percent)

    memory_info = psutil.virtual_memory()
    memory_total.set(memory_info.total)
    memory_used.set(memory_info.used)
    memory_free.set(memory_info.available)

    metrics_app = make_wsgi_app()
    return metrics_app(environ, start_response)

if __name__ == '__main__':
    httpd = make_server('0.0.0.0', 9918, collect_metrics)

    print("Listening on port 9918...")
    httpd.serve_forever()
