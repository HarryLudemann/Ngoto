# Ngoto
[![](https://github.com/HarryLudemann/Ngoto/workflows/pytests/badge.svg)]()
[![Maintainability](https://api.codeclimate.com/v1/badges/08e4dc1f109aaa6c4f75/maintainability)](https://codeclimate.com/github/HarryLudemann/Ngoto/maintainability)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f50d18ce111d4faf99ff411b5129e920)](https://www.codacy.com/gh/HarryLudemann/Ngoto/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=HarryLudemann/Ngoto&amp;utm_campaign=Badge_Grade)
![Supported Python versions](https://img.shields.io/badge/python-3.8+-blue.svg)
[![version-1.3](https://img.shields.io/badge/version-0.0.33-blue)](https://github.com/Datalux/Osintgram/releases/tag/1.3)
![platforms](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-blue)


## Warning :warning:

<p align="center"><b>This tool is solely for educational purposes. Developer will not be responsible for any misuse of the tool</b></p>    

## Example:
### 1. Install Module
Using pip or pip3, install the 'ngoto' module.
```
pip install ngoto
```
### 2. Example Code
The following code is a example on how to create each of three event types,  as well as start the tool.
```python
from ngoto import plugin, command, task, Ngoto


class Basic():
    @plugin(name='Tester', desc='Tester Plugin', folder='Random')
    def tester(self, logger):
        logger.info(f'Plugin ran', program='Test')

    @command(name='test', aliases=['t'], desc='Tests command')
    def test(self, logger, options):
        logger.info(f'Command ran', program='Test')

    @task(name='TaskTest', desc="Tests task creation", delay=3, id='test')
    def testing(self):
        self.logger.info(f'Task logger test ran', program='Test')
        return 'Task ran'


ngoto = Ngoto()
ngoto.load_cogs([Basic()])
ngoto.start()
```

## Development
#### 1. Clone Repo:
```
git clone https://github.com/HarryLudemann/Ngoto
```

#### 2. Install Required Modules:
Move into downloaded Ngoto folder then pip/pip3 install requirements:
```
pip install -r requirements.txt
```

#### 3. Run
Start script by running python/python3 main.py script:
```
python main.py
```
Which will bring you to the following:

![](.github/LaunchScreen.png)
