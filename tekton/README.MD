# Tekton

These pipelines are created to run the main.py file to provision the SONiC switch.
At the moment, it requires a manual execution of the pipeline by running the pipelineRun file.

You need a local cluster to test and run the Tekton code.
This can be solved by:

1. Installing Rancher and disable the built-in Kubernetes cluster
2. Install k3d

To run the k3d cluster

``` bash
k3d create cluster tekton-sonic
```

When the cluster is up, install tekton-pipelines.

``` bash
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

The git-clone task from hub.tekton.dev is used to clone the repo and can be installed from here.

``` bash
kubectl apply -f https://raw.githubusercontent.com/tektoncd/catalog/main/task/git-clone/0.9/git-clone.yaml
```

Install the python task and pipeline.

``` bash
kubectl apply -f tekton/task-provision-vlan-python.yaml
kubectl apply -f tekton/pipeline-provisioning-sonic.yaml
```

Last run the pipeline with.

``` bash
kubectl apply -f tekton/pipelineRun-provisioning-vlan.yaml
```
