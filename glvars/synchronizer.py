from gitlab import Gitlab
from gitlab.v4.objects import Project
from rich import print

from glvars.schemas import GlVarsConfig, Variable


class VariableSynchronizer:
    def __init__(self, config: GlVarsConfig):
        self.config = config

        self._client = None
        self._project = None

    @property
    def client(self) -> Gitlab:
        if self._client is None:
            self._client = Gitlab(private_token=self.config.gitlab_private_token)
        return self._client

    @property
    def project(self) -> Project:
        if self._project is None:
            self._project = self.client.projects.get(self.config.gitlab_project_id)
        return self._project

    def sync(self):
        existing_variables = self.list_variables()
        existing, to_create, to_update, to_delete = self.get_changes(
            existing_variables, self.config.get_variables()
        )

        if not any([to_create, to_update, to_delete]):
            print("[green]Variables are up-to-date.[/green]")

        for var in to_create:
            self.create_variable(var)
            print(f"{var.key} created.")

        for var in to_update:
            self.update_variable(var)
            print(f"{var.key} updated.")

        for var in to_delete:
            self.delete_variable(var)
            print(f"{var.key} deleted.")

    def list_variables(self):
        variables = self.project.variables.list(all=True)
        return [Variable.from_orm(var) for var in variables]

    def create_variable(self, var: Variable) -> Variable:
        created_var = self.project.variables.create(
            var.dict(exclude_none=True, exclude_unset=True)
        )
        return Variable.from_orm(created_var)

    def update_variable(self, var: Variable) -> Variable:
        updated_var = self.project.variables.update(
            var.key, var.dict(exclude={"key"}, exclude_none=True, exclude_unset=True)
        )
        return Variable(**updated_var)

    def delete_variable(self, var: Variable) -> None:
        self.project.variables.delete(var.key)

    def get_changes(
        self, existing: list[Variable], expected: list[Variable]
    ) -> tuple[list[Variable], list[Variable], list[Variable], list[Variable]]:
        """Get exising, to create, to update, to delete variables."""
        existing_dict = {var.key: var for var in existing}
        already_exists = []
        to_create = []
        to_update = []

        for var in expected:
            existing_var = existing_dict.pop(var.key, None)
            if not existing_var:
                to_create.append(var)
            elif self._var_has_changes(var, existing_var):
                to_update.append(var)
            else:
                already_exists.append(var)

        to_delete = list(existing_dict.values())

        return already_exists, to_create, to_update, to_delete

    def _var_has_changes(self, expected: Variable, exiting: Variable) -> bool:
        expected_dict = expected.dict(
            exclude={"key"}, exclude_unset=True, exclude_defaults=True
        )
        existing_dict = exiting.dict()
        for key, value in expected_dict.items():
            if value != existing_dict[key]:
                return True
        return False


class SynchronizerError(Exception):
    pass
