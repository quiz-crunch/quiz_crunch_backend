from typing import Optional, Any

from pydantic import BaseModel
import inflection


def camel_to_snake(obj: Any):
    """
    驼峰命名转下划线命名
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        data = {inflection.underscore(key): camel_to_snake(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        data = [camel_to_snake(item) for item in obj]
    else:
        data = obj
    return data


def snake_to_camel(obj: Any):
    """
    下划线命名转驼峰命名
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        data = {inflection.camelize(key, False): snake_to_camel(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        data = [snake_to_camel(item) for item in obj]
    else:
        data = obj
    return data


class BasisModel(BaseModel):
    convert_names: bool = True

    def __init__(self, **data):
        super().__init__(**camel_to_snake(data))

    def model_dump(self, *args, **kwargs):
        convert_names = self.convert_names
        data = self._convert_model_to_dict(self)
        if convert_names:
            return snake_to_camel(data)
        return data

    def _convert_model_to_dict(self, obj):
        if isinstance(obj, BaseModel):
            data_dict = {}
            for field_name in obj.model_fields:
                if field_name != "convert_names":
                    field_value = getattr(obj, field_name)
                    data_dict[field_name] = self._convert_model_to_dict(field_value)
            return data_dict
        elif isinstance(obj, list):
            return [self._convert_model_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            data_dict = {}
            for key, value in obj.items():
                if key != "convert_names":
                    data_dict[key] = self._convert_model_to_dict(value)
            return data_dict
        else:
            return obj


class BasicModel(BasisModel):
    id: Optional[str] = None
