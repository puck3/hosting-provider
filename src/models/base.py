from typing import Any


class BaseModel:
    __id: int

    def dict(self) -> dict[str, Any]:
        result = {}
        for attr_name, attr_value in self.__dict__.items():
            if attr_name.startswith("__"):
                continue

            elif attr_name.startswith("_"):
                result[attr_name[1:]] = attr_value

            else:
                result[attr_name] = attr_value

        return result

    def get_id(self) -> int:
        return self.__id

    def _set_id(self, new_id: int) -> None:
        self.__id = new_id
