## Osu-ds
![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)  
Lightweight module for getting user info from the osu! API.


### Installing  
To install this library do either of these things:  

1. `pip install git+https://github.com/DefaltSimon/osu-ds@master`  
2. download the source code and execute `python setup.py install`. 
  
### Usage  
A simple example:  
```python
import osu_ds

osu = osu_ds.Osu(api_key="somekey")
user = osu.get_user("DefaltSimon")

print(user.level, user.name)
```
