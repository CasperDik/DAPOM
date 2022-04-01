import pandas as pd

a = {"a": {"lats": [1,2], "longs": [4,5]}, "b": {"lats": [2,3], "longs": [4,5]}}
print(min(a, key=a.get))