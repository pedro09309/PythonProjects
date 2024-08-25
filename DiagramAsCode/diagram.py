# ----------------------- Example 1 -----------------------:
# from diagrams import Diagram
# from diagrams.aws.compute import EC2
# from diagrams.aws.database import RDS
# from diagrams.aws.network import ELB

# with Diagram("Grouped Workers", show=False, direction="TB"):
#     ELB("lb") >> [EC2("worker1"),
#                   EC2("worker2"),
#                   EC2("worker3"),
#                   EC2("worker4"),
#                   EC2("worker5")] >> RDS("events")
# ----------------------- Example 1 -----------------------:

# ----------------------- Example 2 -----------------------:
from diagrams import Cluster, Diagram
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram("Advanced Web Service with On-Premise", show=False):
    ingress = Nginx("ingress")

    metrics = Prometheus("metric")
    metrics << Grafana("monitoring")

    with Cluster("Service Cluster"):
        grpcsvc = [
            Server("grpc1"),
            Server("grpc2"),
            Server("grpc3")]

    with Cluster("Sessions HA"):
        primary = Redis("session")
        primary - Redis("replica") << metrics
        grpcsvc >> primary

    with Cluster("Database HA"):
        primary = PostgreSQL("users")
        primary - PostgreSQL("replica") << metrics
        grpcsvc >> primary

    aggregator = Fluentd("logging")
    aggregator >> Kafka("stream") >> Spark("analytics")

    ingress >> grpcsvc >> aggregator
# ----------------------- Example 2 -----------------------: