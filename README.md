# asenetcky digital twin

![PyPI version](https://img.shields.io/pypi/v/asenetcky-digital-twin.svg)

Python Boilerplate contains all the boilerplate you need to create a Python package.

* Created by **[Alexander J. Senetcky](https://asenetcky.dev)**
  * GitHub: https://github.com/asenetcky
  * PyPI: https://pypi.org/user/asenetcky/
* PyPI package: https://pypi.org/project/asenetcky-digital-twin/
* Free software: MIT License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://asenetcky.github.io/asenetcky_digital_twin/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/asenetcky-digital-twin.git
cd asenetcky-digital-twin

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `asenetcky_digital_twin`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

asenetcky digital twin was created in 2026 by Alexander J. Senetcky.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
