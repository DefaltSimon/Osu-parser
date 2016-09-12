## Osu-parser
Helps you get data from osu! (currently only about users, beatmaps "coming soon")  


###Installing  
To install, simply execute `python setup.py install`.  
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
