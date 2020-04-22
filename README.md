# hivehistory
Python tools for obtaining and processing account history of a hive account

[![Build Status](https://travis-ci.org/holgern/hivehistory.svg?branch=master)](https://travis-ci.org/holgern/hivehistory)
[![Build status](https://ci.appveyor.com/api/projects/status/xkfm06q0otydqxa1?svg=true)](https://ci.appveyor.com/project/holger80/hivehistory)

## Installation
```
pip install hivehistory
```


## Commands
All steem posts from an account can be stored as markdown files with
```
hivehistory posts holger80 .
```
When also all images should be stored, a second folder path can be given:
```
hivehistory posts holger80 . ./images
```
