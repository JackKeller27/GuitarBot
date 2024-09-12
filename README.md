# GuitarBot
## Robotic Musicianship Lab at the Georgia Institute of Technology
### Advisor: Dr. Gil Weinberg
---
Project repo for GuitarBot.

**Contributors:** Amit Rogel, Marcus Parker, Jack Keller, **add contributors here**.

## Environment Setup
1. Clone this repository.
2. Install Python 3.9.18 [here](https://www.python.org/downloads/) (make sure to scroll down to the specific release version).
3. Install Conda [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). While **Miniconda** is recommended, either of the Miniconda or Anaconda distributions are fine. Conda is a virtual environment and package manager for Python.
4. Once Conda is installed, open terminal in the cloned GuitarBot directory.
5. Run `conda env create -f environment/environment.yml` to create a new Conda environment for the project. It will automatically be named *guitarbot_env*.
6. To verify that the environment was installed correctly, run `conda env list`. You should see *guitarbot_env* as one of the options listed.
7. Run `conda activate guitarbot_env` to activate the new environment.
8. Note that if you're running the project from an IDE, you will need to select your new environment as the Python interpreter. See VSCode example below:
![VSCode interpreter selection](environment/screenshots/python_interpreter_selection.png)
![VSCode conda configuration](environment/screenshots/conda_configuration.png)

You're all set! Run the **UI/main.py** script to start the GuitarBot UI.

### To Update Environment Configuration:
1. Navigate to the **GuitarBot/environment** directory.
2. If not already activated, run `conda activate guitarbot_env` to activate the guitarbot environment.
3. Run `conda env export > environment.yml` to export the guitarbot environment to a new environment.yml file. Make sure to replace the existing environment.yml file.

## Documentation
See https://github.com/JackKeller27/GuitarBot/wiki.

Contains documentation on the project along with a future improvements page.

## Existing Bugs
See https://github.com/JackKeller27/GuitarBot/issues.

Contains details regarding existing bugs/issues within the project.
