#!/bin/bash
PROJECT_NAME="$(pwd | awk '{split($0,a,"/"); print a[length(a)-1]}')"
ENV_NAME="env_${PROJECT_NAME}"
PYTHON_PATH=$(ls /c/Users/*/AppData/Local/Programs/Python/Python*/python.exe | tail -1)
echo "Using Project Name: $PROJECT_NAME"
echo "Using virtual environment: $ENV_NAME"
echo "Using Python path: $PYTHON_PATH"
# ls "$ENV_NAME/Scripts/activate"
if [[ -d "$ENV_NAME" ]]; then

    source "$ENV_NAME/Scripts/activate"
    cd ..
    find ./ -name "projeto_*.py" -exec streamlit run {} \; > log_application.log 

else
    echo "Virtual environment $ENV_NAME does not exist. Please create it first."
fi
