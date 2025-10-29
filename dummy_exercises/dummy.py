from typing import TypedDict, Annotated

class MyDict(TypedDict):
    name: str
    age: int

dict = MyDict(name="John", age=30)
dict[123] = 456
dict['city'] = "Los Angeles"
dict['key'] = "value"
dict['name']  = "Doe"
print(dict)

input("Press Enter to continue...")

x = Annotated[str, "hey", 123, {"key": "value"}]

# print(x.__annotations__())
print(x.__metadata__)