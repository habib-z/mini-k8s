import pickle
from os import unlink
from os.path import exists
from typing import TypeVar, Generic, List
#T=TypeVar("T")
# def save(l:List[T],path):
#     with open(path, "wb") as fp:
#         pickle.dump(l, fp)
#
# def load(path)->List[T]:
#     with open(path, "rb") as fp:
#         return pickle.load(fp)

class DBList(list):
    def __init__(self,path):
        super(DBList, self).__init__()
        self.path=path

    def save(self)->None:
        with open(self.path, "wb") as fp:
            pickle.dump(self, fp)

    def load(self):
        with open(self.path, "rb") as fp:
            return pickle.load(fp)

    def unlink(self):
        if (exists(self.path)):
            unlink(self.path)

class DBDict(dict):
    def __init__(self,path):
        super(DBDict, self).__init__()
        self.path=path

    def save(self)->None:
        with open(self.path, "wb") as fp:
            pickle.dump(self, fp)

    def load(self):
        with open(self.path, "rb") as fp:
            return pickle.load(fp)

    def unlink(self):
        if (exists(self.path)):
            unlink(self.path)