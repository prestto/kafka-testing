#!/bin/bash
cecho() {
    LB='\033[1;36m' # Light Blue
    LG='\033[1;32m' # Light Green
    YE='\033[1;33m' # Yellow

    # print normally if no second arg added
    if [[ $2 == "" ]]; then
        echo $1
        return
    fi

    case $1 in
    BL)
        printf "$LB%s\033[0m\n" "$2" # Light Cyan
        ;;
    GR)
        printf "$LG%s\033[0m\n" "$2" # Light green
        ;;
    YE)
        printf "$YE%s\033[0m\n" "$2" # Light green
        ;;
    normal | *)
        echo $2 # Light Purple
        ;;
    esac
}

function run_install {
    cecho "BL" "Installing system dependancy: Colima..."
    brew install colima
    cecho "BL" "Colima installed."
    
    cecho "BL" "Installing system dependancy: Docker..."
    brew install docker
    cecho "BL" "Docker installed."

    cecho "BL" "Installing system dependancy: Minikube..."
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
    sudo install minikube-darwin-amd64 /usr/local/bin/minikube
    cecho "BL" "Minikube installed."

    cecho "BL" "Installing system dependancy: Tilt..."
    curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
    cecho "BL" "Tilt installed."
}

function run_migrate {
    cecho "BL" "Migrating..."
    cd app_core/
    python src/manage.py migrate
    cecho "BL" "Migrated..."
}

function run_clean {
    run_down
    cecho "BL" "Killing minikube..."
    minikube delete -p event-testing
    cecho "BL" "Minikube killed..."
}

function run_start_minikube {
    cecho "BL" "Starting minikube..."
    minikube start -p event-testing --memory=7800
    cecho "BL" "Minikube started..."
}

function run_tilt {
    cecho "BL" "Tilting..."
    tilt up --context event-testing
    cecho "BL" "Finished Tilting..."
}

function run_down {
    cecho "BL" "DeTilting..."
    tilt down --context event-testing
    cecho "BL" "Finished DeTilting..."
}

function run_dev {
    run_start_minikube
    run_tilt
}

function run_local_celery_task {
    # Expects 2 args: service (app_core or app_peripheral) and a message to send.
    if [ "$#" -ne 2 ]; then
        echo "Error: Two arguments are required - service and message."
        return 1
    fi

    service="$1"
    message="$2"

    case "$service" in
        app_core)
            port=8001
            ;;
        app_peripheral)
            port=8002
            ;;
        *)
            echo "Error: Unsupported service. Supported values are 'app_core' and 'app_peripheral'."
            return 1
            ;;
    esac

    cecho "BL" "Running local celery task on app_core..."
    # echo "curl -X POST -H "Content-Type: application/json" -d "{\"body\": \"$1\"}" http://localhost:8001/local-celery-task"
    echo   "curl -X POST -H \"Content-Type: application/json\" -d \"{\"body\": \"$message\"}\" http://localhost:$port/local-celery-task"
    curl -X POST -H "Content-Type: application/json" -d "{\"body\": \"$message\"}" "http://localhost:$port/local-celery-task"
    
    echo ""
    cecho "BL" "Finished running local celery task..."
}

function show_help {
    cecho "BL" "Help: $0 <ACTION>"
    cecho "BL" "Parameters :"
    cecho "BL" " - ACTION values :"
    cecho "BL" "   * install                               - Install system deps."
    cecho "BL" "   * dev                                   - Run the dev server."
    cecho "BL" "   * migrate                               - Run migrate."
    cecho "BL" "   * start_minikube                        - Run minikube with profile event-testing."
    cecho "BL" "   * tilt                                  - Run Tilt to deploy resources to minikube."
    cecho "BL" "   * clean                                 - Stop Tilt and kill minikube."
    cecho "BL" "   * local_celery_task [service, message]  - Execute a celery task on a service (no IPC)."
    cecho "BL" "                                             eg ./run.sh local_celery_task app_peripheral message"
}


if [[ "$1" == "" ]]; then
    cecho "YE" "No arguments provided."
    show_help
    exit 1
fi

case "$1" in
install)
    run_install
    ;;
dev)
    run_dev
    ;;
migrate)
    run_migrate
    ;;
start_minikube)
    run_start_minikube
    ;;
tilt)
    run_tilt
    ;;
down)
    run_down
    ;;
clean)
    run_clean
    ;;
local_celery_task)
    run_local_celery_task $2 $3
    ;;
*)
    show_help
    ;;
esac