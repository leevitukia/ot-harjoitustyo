## How to run the program
- Clone the repo
- cd to the root directory
- Install the project's dependencies by running ```poetry install --no-root```, this *should* also create a virtual environment
- Run ```poetry shell``` to activate the virtual environment. You may have to run ```poetry self add poetry-plugin-shell``` before you can use ```poetry shell```
- Run ```python src/index.py``` or ```poetry run invoke start``` to start the program. Use the first option if you're on Windows since the latter only works on UNIX based operating systems afaik