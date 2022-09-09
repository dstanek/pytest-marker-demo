# pytest Marker Demo
A small demo of interesting ways to use pytest markers

Included are two different demos that attack the problem described below in slightly different ways.
The first is just a straightforward fixture, and the other is a "plugin" with a command line argument.

## Backstory
At HPE, we use [pytest]() to test our microservices. We have functional
tests that need to access multiple microservice APIs. We also have numerous
versions of each API. So we want to:

1. Specify which tests work with which APIs
2. Allow versions to be specified when running tests (e.g., latest, pick a random supported version)
3. Utilize the functionality of pytest where possible

We do not want to:

1. Make it difficult to know what tests support what versions
2. Make it difficult to add new tests

## tldr; Running the tests

To run each test once with the lastest supported API version:

```bash
$ poetry run pytest tests -v
```

- or -

```bash
$ poetry run pytest tests -v --demo-strategy latest
```

To run each test once using a random supported API version:

```bash
$ poetry run pytest tests -v --demo-strategy random
```

To run the cartesian product of supported API versions:

```bash
$ poetry run pytest tests -v --demo-strategy cartesian
```

## tldr; Reading the tests

A new magic marker is used to specify what versions a test supports.

## TODOs

* Add the ability to specify versions like: "run v2alpha1 or greater"
* Maybe create an actual plugin from this code
* Clean up the API typing...
