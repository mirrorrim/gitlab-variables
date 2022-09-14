from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class VariableType(str, Enum):
    env_var = "env_var"
    file = "file"

    def __str__(self):
        return self.value


class Variable(BaseModel):
    key: str
    value: str
    variable_type: Optional[VariableType] = None
    protected: Optional[bool] = None
    masked: Optional[bool] = None
    environment_scope: Optional[str] = None

    class Config:
        orm_mode = True


class GlVarsConfig(BaseModel):
    gitlab_url: str = Field(default="", alias="gitlab-url")
    gitlab_private_token: str = Field(alias="gitlab-private-token")
    gitlab_project_id: str = Field(alias="gitlab-project-id")
    variables: Union[list[Variable], dict[str, str]]

    class Config:
        allow_population_by_field_name = True

    def get_variables(self) -> list[Variable]:
        if isinstance(self.variables, list):
            return self.variables
        return [Variable(key=key, value=value) for key, value in self.variables.items()]
