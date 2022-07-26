from pathlib import Path
from typing import Union
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    age: int


class TextStorage():

    def __init__(self, file, obj):
        self.file = file
        self.__fields__ = list(obj.__annotations__.keys())
        self.__type__ = list(obj.__annotations__.values())
        filepath = Path.cwd() / file
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if not filepath.exists():
            with filepath.open('w') as f:
                f.write(f'table={obj.__name__}\n')
                f.write(f'fields={",".join([flds for flds in self.__fields__])}\n')
                f.write(f'type={",".join([typ.__name__ for typ in self.__type__])}\n')
                f.write('------------------------------------\n')
    
    def _check_existing_fields(self,fields,create=True):
        key_set = set(fields.keys())
        field_set = set(self.__fields__)
        if create:
            if len(field_set.intersection(key_set)) != len(field_set):
                diff = field_set - key_set
                raise KeyError(f'Missing keys {list(diff)}')
        if len(key_set) > len(field_set):
            diff = key_set - field_set
            raise KeyError(
                f'keys = {list(diff)} should not exist. Existing fields = {field_set}')
        

    def create(self, obj:Union[User,dict]):
        if isinstance(obj, User):
            record = obj.__dict__
        else:
            record = obj
        self._check_existing_fields(record)
        with open(self.file, 'r') as f:
            id = int(record.get('id'))
            for lines in f.readlines():
                cols = lines.split(',')
                if cols[0].isnumeric():
                    if id == int(cols[0]):
                        raise KeyError(f'id={id} already exists')
                        
        with open(self.file, 'a') as f:   
            res = [str(value) for value in record.values()]
            input = ','.join(r for r in res)
            f.write(f'{input}\n')
        print(f'{obj} created')


    def __str__(self):
        return self.obj



if __name__ == "__main__":
    t = TextStorage("user_record.txt", User)
    u1 = User(1000, "Ram", 20)
    u2 = User(1001, "Ze", 21)
    u3 = User(1002, "Ze", 22)
    u4 = User(1003, "Shyam", 20)
    users = [u1,u2,u3,u4]
    for u in users:
        t.create(u)