# EEA Python Script for Data Extraction and Processing

[![GitHub license](https://img.shields.io/badge/license-GNU-blue.svg)](https://raw.githubusercontent.com/nikoshet/spark-cherry-shuffle-service/master/LICENSE)

## Table of Contents

+ [About](#about)
+ [Getting Started](#getting_started)
    + [Prerequisites](#prerequisites)
    + [Available Ansible Playbooks](#playbooks)
    + [Configuration](#configuration)
+ [Execution Options](#execution_options)	
+ [Available Workloads](#available_workloads)	
+ [Deployment](#deployment)
+ [Built With](#built_with)
+ [License](#license)

## About <a name = "about"></a>


## Getting Started <a name = "getting_started"></a>

The following instructions will help you run this project on a Kubernetes cluster. The already implemented Ansible playbooks will help speed up this procedure.

### Prerequisites <a name = "prerequisites"></a>

As mentioned above, you will need to install the correct versions of Python, Apache Spark, Kubernetes (kubeadm, kubelet, kubectl), Docker, Java, Scala and Ansible to all the hosts in the available cluster.
Firstly, install Ansible to all nodes as follows:
```
sudo apt install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install ansible

```
In order to install the rest of the software required with Ansible, first configure the info of the `/ansible/inventory/hosts` file based on your cluster. Then execute the following:
```

```

The above commands will configure the Kubernetes cluster. More specifically:
- [X] Disable Swap on each node
- [X] Add IPs to path /etc/hosts on each node
- [X] Enable Passwordless SSH netween nodes
- [X] Install Java, Python, Scala, Docker, kubeadm, kubelet, kubectl and enable Kubernetes Services
- [X] Initialize Kubernetes Cluster from Master node
- [X] Install Calico CNI Network Add-on
- [X] Join Worker nodes with kubernetes master
- [X] Install Python Docker module and Log into Docker Hub to store and retrieve Docker images
- [X] Add monitoring packages for Kubernetes (i.e., prometheus-operator)
- [X] Label Kubernetes nodes accordingly, create namespace, start Kubernetes Services for Spark and Prometheus to scrape Spark metrics

### Available Ansible Playbooks <a name = "playbooks"></a>
There have also been implemented other Ansible Playbooks in the `/ansible/playbooks` folder that do the following:
- 
- 
- 
- 
- 
- 
- 

### Configuration <a name = "configuration"></a>


## Execution Options <a name = "execution_options"></a>
To simplify the deployment of a Spark Cluster and a Spark workload as a Kubernetes Job with different parameters, the aforementioned script is used, and the flags it accepts are the following:
```

```
## Available Workloads <a name = "available_workloads"></a>

## Deployment <a name = "deployment"></a>
To deploy a Spark Cluster with differently configured workloads, you need to deploy the implemented Spark Metadata Service, the Spark Master, Workers, Cherry shuffle services and finally the Driver job. Example command:
```
kubectl delete deploy spark-metadata-service spark-worker spark-cherry-shuffle-service -n spark \
&& kubectl delete job spark-driver -n spark \
&& sleep 1m \
&& kubectl create -f ./kubernetes/spark-metadata-service/spark-metadata-service-deployment.yaml --namespace=spark \
&& sleep 1m \
&& kubectl create -f ./kubernetes/spark-cherry-shuffle-service/spark-cherry-shuffle-service-deployment.yaml --namespace=spark \
&& kubectl create -f ./kubernetes/spark-worker/spark-worker-deployment.yaml --namespace=spark \
&& kubectl scale deployments/spark-worker --replicas=10 --namespace=spark \
&& kubectl scale deployments/spark-cherry-shuffle-service --replicas=10 --namespace=spark \
&& sleep 1m \
&& kubectl create -f ./kubernetes/spark-driver/spark-driver-job.yaml --namespace=spark
```

Example commands with flags for the `spark-driver.sh` script to execute different workloads (need to be modified in the `/kubernetes/spark-driver/spark-driver-job.yaml` file):
```
 
```

## Built With <a name = "built_with"></a>


## License <a name = "license"></a>
This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.
