"""
    Basically, if you have a dictionary like this:
    {"a": 1, 
     "b.c": 2, 
     "b.d": 3
    }
    
    This function turns that into this:
    {"a": 1,
     "b": {
       "c": 2,
       "d": 3
       }
    }
    
    This is used because form-encoded POST data is always flattened.
    It makes life much easier if that data becomes an actual dict.
"""
def unflatten(dictionary):
    resultDict = dict()
    for key, value in dictionary.iteritems():
        parts = key.split(".")
        d = resultDict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return resultDict

