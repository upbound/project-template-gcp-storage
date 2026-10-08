# {{.ProjectName}}

This project was initialized using the `{{.TemplateName}}` template (version
{{.TemplateVersion}}). Update this README with information about what the
project contains and an example of how to use it.

## Installation

TODO

## Examples

TODO

## Testing

TODO

## Python editor support

If this project uses Python functions or tests, `up` builds them in a
container, so a local Python install (3.11-3.13) is only needed for editor
features. To resolve imports from the generated `models` package, run
`up project build`, then create a virtual environment in each function or test
directory:

```shell
cd functions/<function-name>
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e ../../.up/python
```

**Note:** `pip install -e .` installs a non-editable copy of the models package, so
re-run `pip install -e ../../.up/python` whenever `up` regenerates the models (after
you add dependencies or change XRDs) for your editor to pick up the changes.
