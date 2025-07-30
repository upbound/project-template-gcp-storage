# project-template-gcp-storage

This template can be used to initialize a new project using `provider-gcp`. By
default it comes with an `XStorageBucket` XRD and a matching composition
function which creates a GCP Storage bucket. It also creates the corresponding
unit and e2e tests.

## Usage

To use this template, run the following command:

```shell
up project init -t upbound/project-template-gcp-storage --language=kcl <project-name>
```

This template supports the following languages:

- `kcl`
- `go`
- `python`
- `go-templating`
