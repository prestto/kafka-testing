# Deploy all the resources in minikube/everything.yaml
# https://docs.tilt.dev/tiltfile_concepts#execution-model
k8s_yaml('minikube/everything.yaml')

# Forward port 8000 from the deployment named 'app-core-deployment'
# to port 8001 locally.
# https://docs.tilt.dev/tiltfile_concepts#kubernetes-workloads
k8s_resource('app-core-deployment', port_forwards=8001)
k8s_resource('app-peripheral-deployment', port_forwards=8002)
k8s_resource('rabbitmq', port_forwards=[5672,15672])

# Define a Docker build based on:
# docker build -t event_testing/app_core:latest -f app_core/Dockerfile app_core
# https://docs.tilt.dev/tiltfile_concepts#build
docker_build(
    'event_testing/app_core:latest',
    context="app_core",
    dockerfile="./app_core/Dockerfile"
)
docker_build(
    'event_testing/app_peripheral:latest',
    context="app_peripheral",
    dockerfile="./app_peripheral/Dockerfile"
)
docker_build(
    'rabbitmq-with-management-command-enabled',
    context="rabbitmq",
    dockerfile="./rabbitmq/Dockerfile-rabbitmq"
)
docker_build(
    'celery-worker',
    context="app_core",
    dockerfile="./app_core/Dockerfile-celery-worker"
)
