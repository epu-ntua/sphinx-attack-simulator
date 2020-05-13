# Sphinx Behaviour & Attack Simulator - ABS
This is the git repository for the ABS  module of the Sphinx project

# Installation Guide

## Prerequisites

Step 1:  Download and install latest python3 - https://www.python.org/downloads/
Step 2:  Download and install Pycharm IDE - https://www.jetbrains.com/pycharm/
         (Alternatively to step 2 you can just go on with git and a conda or a
         virtual environment and then install the requirements.txt file)

## Installing the ABS Flask 
From Pycharms' starting screen

* Check out from Version Control ->Git
*  Copy the url "https://sphinx-repo.intracom-telecom.com/sphinx-project/attack-and-behaviour-simulators/behaviour-attack-simulator.git" url into "Git Repository URL"
*  Press test and enter gitlab credentials if needed
*  Clone
*  Create new virtual environment (File -> Settings -> Project -> Project Intepreter => icon -> Add local -> ok)
*  Install requirements from requirements.txt (Go to requirements.txt -> Press install on pop up)

Current Database used is Sqlite but it isn't included in github due to size so
in fresh installs always recreate database 
# Running the ABS module
`flask db migrate` (Shouldn't be needed)
`flask db upgrade` (Necessary to recreate db)
`flask run`