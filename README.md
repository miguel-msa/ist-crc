# IST - Network Science

## Repository General Description

`agent.py`: 
- describes an agent that is also a node in the lattice
- includes all the state and functionalities of an agent

`utils.py`:
- includes initialization, util/helper, and debugging functions

`common.py`:
- contains parameters shared throughout the code

`simmulation.py`
- the project's building blocks together resulting in the run of a simulation, from initializations and logic, to the final results

## Requirements

If you do not want to use a virtual environment, you are free to manage the project package requirements as you wish.

If you wish to use venv, follow the steps below: these steps are for windows, adapt as needed if you have an unix based systems.

### Requirements:

(pip install globally)

-   [virtualenv](https://pypi.org/project/virtualenv/) - to create/manage virtualenv
-   [ipykernel](https://pypi.org/project/ipykernel/) - to run jupyter notebooks w/ venv

### Setup Steps:

1. Start virtualenv

```bash
virtualenv venv
```

2. Get into _venv_ (windows step, unix systems is different)

```bash
./venv/Scripts/activate
```

Do not forget to select the (venv) python interpreter in your IDE

4. Install libs (into venv!)

```bash
cd venv

# install in venv the required packages
pip intall -r ..\requirements.txt
```

Networkx contains some dependencies, e.g., numpy, scipy that the requirements.txt version of networkx does not include, take that into account and install `networkx[default]` instead if you wish, or install dependencies manually ad hoc.
For more details refer to [doc: networkx install](https://networkx.org/documentation/stable/install.html)

## License

### Code License

The code in this repository is licensed under the MIT License. You are free to use, modify, and distribute the code as long as proper attribution is given to the original author. See the [LICENSE](LICENSE) file for more details.
