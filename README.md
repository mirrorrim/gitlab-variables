# gitlab-variables
CLI utility for managing variables in Gitlab

Default path for config file is $PWD/.glvars.yml

# Installation

```shell
pip install glvars
```

## Config example

### Simplified

```yaml
gitlab-url: https://gitlab.example.com  # The URL of the GitLab server (defaults to https://gitlab.com)
gitlab-private-token: glpat-12345678901234567890  # The user private token with access to API, required
gitlab-project-id: namespace/project_name  # The ID of a project or URL-encoded NAMESPACE/PROJECT_NAME of the project
variables:
  USERNAME: admin
  PASSWORD: Sup3rs3crE7
```

### Full

```yaml
gitlab-url: https://gitlab.example.com  # The URL of the GitLab server (defaults to https://gitlab.com)
gitlab-private-token: glpat-12345678901234567890  # required, private gitlab token with access to API
gitlab-project-id: namespace/project_name  # The ID of a project or URL-encoded NAMESPACE/PROJECT_NAME of the project
variables:
  - key: USERNAME  # The key of a variable; must have no more than 255 characters; only A-Z, a-z, 0-9, and _ are allowed
    value: admin  # The value of a variable
    variable_type: env_var  # The type of a variable. Available types are: env_var (default) and file
    protected: false  # Whether the variable is protected. Default: false
    masked: false  # Whether the variable is masked. Default: false
    environment_scope: *  # The environment_scope of the variable. Default: *
  - key: PASSWORD
    value: Sup3rs3crE7
    masked: true
```
