# project-template-starter

A starting point for creating Upbound project templates which can be used with `up
project init`. See [upbound/project-template-aws-s3] for a working example.

[upbound/project-template-aws-s3]: https://github.com/upbound/project-template-aws-s3

To get started:

1. Modify the `template.yaml` file with a new name, description and supported
   languages.
1. Update the `template/upbound.yaml` to describe the example once it has been
   initialized.
1. Update the `template/README.md` to be about the initialized project - the
   resources it contains and the commands it supports.
1. Add any resources to `templates/[apis|examples|functions|tests]`, using the
   guide below, which will be initialized alongside the template.
1. Update this `README.md` to be about your example!

## Templated directories

When initializing a project, the `up project init` command requires the user to
specify a language and a test language. These languages determine which files
are created for the user - allowing you to create examples that work for
multiple languages.

Use the `rename.directories` option in the `template.yaml` file to determine
which files should be used for a given language.

### Example

Assuming your example supports both `kcl` and `python` languages. And looks like
this:

```shell
template
├── apis
│   ├── xstoragebucket-kcl
│   │   ├── composition.yaml
│   │   └── definition.yaml
│   └── xstoragebucket-python
│       ├── composition.yaml
│       └── definition.yaml
├── examples
│   ├── xstoragebuckets-kcl
│   │   └── example.yaml
│   └── xstoragebuckets-python
│       └── example.yaml
├── functions
│   ├── compose-bucket-kcl
│   │   ├── kcl.mod
│   │   ├── kcl.mod.lock
│   │   ├── main.k
│   │   └── model -> ../../.up/kcl/models
│   └── compose-bucket-python
│       ├── main.py
│       ├── model -> ../../.up/python/models
│       └── requirements.txt
├── LICENSE
├── README.md
├── tests
│   ├── test-xstoragebucket-kcl
│   │   ├── kcl.mod
│   │   ├── kcl.mod.lock
│   │   ├── main.k
│   │   └── model -> ../../.up/kcl/models
│   └── test-xstoragebucket-python
│       ├── main.py
│       ├── model -> ../../.up/python/models
│       └── requirements.txt
└── upbound.yaml
```

You can configure your `template.yaml` to rename directories assuming the
language is in the suffix of the directories, like so:

```yaml
languages:
- kcl
- python

rename:
  directories:
    - pattern: "*-python"
      replacement: "*"
      languages: ["python"]
    - pattern: "*-kcl"
      replacement: "*"
      languages: ["kcl"]
```

Then, when a user initializes their project with one of the supported languages,
like `up project init -e <your example> --language python <project-name>`, the
directories will be renamed using the pattern defined in the `replacement`. For
the example above, the initialized project will have the following structure:

```shell
<project-name>
├── apis
│   └── xstoragebucket
│       ├── composition.yaml
│       └── definition.yaml
├── examples
│   └── xstoragebuckets
│       └── example.yaml
├── functions
│   └── compose-bucket
│       ├── main.py
│       ├── model -> ../../.up/python/models
│       └── requirements.txt
├── LICENSE
├── README.md
├── tests
│   └── test-xstoragebucket
│       ├── main.py
│       ├── model -> ../../.up/python/models
│       └── requirements.txt
└── upbound.yaml
```

## Templated files

When initializing the project, `up` can optionally run each file through the Go
`text/template` engine. All files suffixed with `.template` will be processed as
a template, and created with the suffix removed. You can also specify other
files to be processed as templates in the `template.yaml` file using
`files.<filename>.template = true`.

The variables made available to the templates are:

- `Language` - the language specified by the user.
- `ProjectName` - the name of the initialized project.
- `ExampleName` - the name of the example used to initialize the project.
- `ExampleVersion` - the version of the example (as specified in `template.yaml`)
- `Values` - an arbitrary map of values configured as provided by the example or
  the user (like Helm values).

### Values

Users can pass values as key-value pairs to be used with templated files, using the
`--values` argument with `up project init`. You can specify default values for
these keys in the `template.yaml` file like so:

```yaml
values:
  Author: "platform-admin"
  Team: "platform"
```

Then in your template files you can access these values using
`{{.Values.author}}`.
