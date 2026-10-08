# project-template-gcp-storage

This template can be used to initialize a new project using `provider-gcp`. By
default it comes with a namespaced `StorageBucket` XRD (Crossplane v2,
`apiextensions.crossplane.io/v2`) and a matching composition function which
creates a GCP Storage bucket using the provider's namespaced (`.m.upbound.io`)
resources. It also creates the corresponding unit and e2e tests.

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
