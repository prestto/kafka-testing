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

function run_dev {
    cecho "BL" "Running dev server..."
    cd app_core/
    python src/manage.py runserver
    cecho "BL" "Dev server stopped..."
}

function show_help {
    cecho "BL" "Help: $0 <ACTION>"
    cecho "BL" "Parameters :"
    cecho "BL" " - ACTION values :"
    cecho "BL" "   * install                            - Install system deps."
    cecho "BL" "   * dev                                - Run the dev server."
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
*)
    show_help
    ;;
esac