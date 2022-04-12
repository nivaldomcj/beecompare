# Beecrowd User Compare

## Description

This is a simple python script to compare/get the difference of solved problems (accepted problems) between 2 users of Beecrowd.
The result of the comparison is written in 2 CSV files, comparing user A vs user B solved problems (and vice-versa).

## Dependencies

- Python 3.6+
- requests 2.18+
- beautifulsoup4

## How to use

Get the users ID who's you will compare and simply pass as command-line arguments. Example:

```
$ python compare.py 64393 68813
```

In this example, it will generate 2 CSV files, containing the difference between accepted solutions from user #64393 vs #68813 (and from #68813 vs #64393).
Both CSV files contain the Problem Code (ID), Name and Description Link for each problem solved by the user.
