## Osu-parser
![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)  
Helps you get data from osu! (currently only about users, beatmaps "coming soon")  


###Installing  
To install, you've got two options:  

1. `pip install git+https://github.com/DefaltSimon/Osu-parser@master`  
2. download the source code and execute `python setup.py install`.  

Additionally, you must also download **PhantomJS** for your os from [here](http://phantomjs.org/download.html)  
  
###Usage  
A simple example:  
```python
import osu_parser

path = "[path to your PhantomJS]"

osu = osu_parser.OsuParser(selenium_path=path)
user = osu.get_user_by_name("DefaltSimon")

print(user.level, user.play_count)
```
