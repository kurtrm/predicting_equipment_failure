# Predicting Equipment Failure
---
### Description
Version: *0.0*

* For an overview of the project, see the [overview](https://github.com/kurtrm/predicting_equipment_failure/blob/master/overview.md) markdown file.
* The final deployment dashboard can be seen [here](http://transformers.kurtrm.com).

### Authors
---
* [Kurt Maurer](kurtrm.com)

### Dependencies
---
* numpy
* pytz
* pandas
* flask
* psycopg2
* numpy
* googlemaps
* sklearn
* scipy

### Getting Started
---
##### *Prerequisites*
* [python (3.6+)](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/)
* [git](https://git-scm.com/)

##### *Installation*
First, clone the project repo from Github. Then, change directories into the cloned repository. To accomplish this, execute these commands:

`$ git clone https://github.com/kurtrm/predicting_equipment_failure.git`

`$ cd predicting_equipment_failure`

Now that you have cloned your repo and changed directories into the project, create a virtual environment named "ENV", and install the project requirements into your VE.
(Or your preferred environment manager.)

`$ python3 -m venv ENV`

`$ source ENV/bin/activate`

`$ pip install -r requirements.txt`

### Test Suite
---
##### *Running Tests*
This application uses [pytest](https://docs.pytest.org/en/latest/) as a testing suite. To run tests, run:

Until a config file is made, execute the following:
``$ cd src``

``$ pytest ../tests/test.py``

To view test coverage, add ``--cov`` to the above command.

##### *Test Files*
The testing files for this project are:

| File Name | Description |
|:---:|:---:|
| `./tests/test.py` | Test this. |

### Development Tools
---
* *python* - programming language
* *flask* - web framework
* *psycopg2* - DB management system

### License
---
This project is licensed under MIT License - see the LICENSE.md file for details.
### Acknowledgements
---

*This README was generated using [writeme.](https://github.com/chelseadole/write-me)*
