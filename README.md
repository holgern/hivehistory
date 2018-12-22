# steemhistory
Python tools for obtaining and processing account history of a steem account

[![Build Status](https://travis-ci.org/holgern/steemhistory.svg?branch=master)](https://travis-ci.org/holgern/steemhistory)
[![Build status](https://ci.appveyor.com/api/projects/status/xkfm06q0otydqxa1?svg=true)](https://ci.appveyor.com/project/holger80/steemhistory)

## Installation
```
pip install steemhistory
```


## Commands
All steem posts from an account can be stored as markdown files with
```
steemhistory posts holger80 .
```
When also all images should be stored, a second folder path can be given:
```
steemhistory posts holger80 . ./images
```
