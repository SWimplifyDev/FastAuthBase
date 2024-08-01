#!/bin/bash

# TO BE RUN ON UNIX/MACOS/GitBash-WINDOWS use "source script-name.sh" command to run on shell
##################################################################################################
# This script will set you up a fresh virtual enviroment of your version of python installed     #
# into your machine, if there is not already one with the DIR name of '.venv'. Virtual enviroment#
# will be activated and then it will look for requirements.txt to be installed on your virtual   #
# machine, if so you have the choice whether to install them or not.                             #
##################################################################################################

# Define DIR name for the virtual enviroment
VENV_DIR=".venv"
VSCODE_DIR=".vscode"
VSCODE_JSON_FILE="settings.json"
python_interpreter_path="$PWD/$VENV_DIR/bin/python"
json_content="{\"python.defaultInterpreterPath\": \"$python_interpreter_path\"}"

# Check if the virtual enviroment already exists on working DIR
if [ ! -d "$VENV_DIR" ]; then
    # Create a new virtual environment
    python3 -m venv $VENV_DIR
    echo "👍\033[1;32m Virtual environment '$VENV_DIR' created.\033[0m"
    if [ ! -d "$VSCODE_DIR" ]; then
        mkdir "$VSCODE_DIR"
        touch "$VSCODE_DIR/$VSCODE_JSON_FILE"
        echo "$json_content" > "$VSCODE_DIR/$VSCODE_JSON_FILE"
        echo "👍\033[1;32m '$VSCODE_DIR' folder with $VSCODE_JSON_FILE file created.\033[0m"
    fi
else
    echo -e "⚠️ \033[1;33m Virtual environment '$VENV_DIR' already exists.\033[0m"
fi

# Clear VIRTUAL_ENV varibale
unset VIRTUAL_ENV
# Activate virtual environment
source $VENV_DIR/bin/activate

# Check if the virtual environment is activated
if [[ "$VIRTUAL_ENV" = "$PWD/$VENV_DIR" ]]; then
    echo "👍\033[1;32m Virtual environment '$VENV_DIR' is activated.\033[0m"
else
    echo "🤦‍♂️\033[1;31m Virtual environment activation failed or not detected.\033[0m"
    exit 1
fi

# Check if there is a file with requirements for virtuall enviroment
if [ -f "requirements.txt" ]; then
    # Ask the user whether to install packages from requirements.txt
    echo -n "🤔 Do you want to install packages from requirements.txt? (y/n): "
    read answer
    # Check the user's response
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        pip install --upgrade pip
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            # pip freeze > requirements.txt
            echo "👍\033[1;32m All packages installed, you are ready to go!\033[0m"
        else    
            echo "🤦‍♂️\033[1;31m Failed to install packages from requirements.txt.\033[0m"
            return 1
        fi
    else
        echo "⚠️ \033[1;33m Skipping installation of packages from requirements.txt.\033[0m"
    fi
fi