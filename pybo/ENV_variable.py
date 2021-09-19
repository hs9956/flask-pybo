import os

def ENV_set(dic=None, **kwargs):
    if str(type(dic))=="<class 'dict'>":
        for name, value in dic.items():
            os.environ[name] = value
    else:
        for name, value in kwargs.items():
            os.environ[name]=value