# Deploy all the resources in minikube/everything.yaml
# https://docs.tilt.dev/tiltfile_concepts#execution-model
k8s_yaml('minikube/everything.yaml')

# Forward port 8000 from the deployment named 'app-core-deployment'
# to port 8001 locally.
# https://docs.tilt.dev/tiltfile_concepts#kubernetes-workloads
k8s_resource('app-core-deployment', port_forwards=8001)

# Define a Docker build based on:
# docker build -t event_testing/app_core:latest -f app_core/Dockerfile app_core
# https://docs.tilt.dev/tiltfile_concepts#build
docker_build(
    'event_testing/app_core:latest',
    context="app_core",
    dockerfile="./app_core/Dockerfile"
)
