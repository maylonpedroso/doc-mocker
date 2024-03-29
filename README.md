# Document Image Mocker

**Warning:** This project is completely experimental – do not use in real-world projects.

This tool is intended to generate images of fake documents using content seeders.
It can be extended with plugins to add extra processing or content to the resulting images.

## Usage
Running `doc-mocker -h` will display the following help

```
usage: doc-mocker [-h] [-n NUMBER_OF_PAGES] [-t {A4}] [-s PAGE_SEEDER]
                  [-o OUTPUT_PATH] [-l {debug,info,warn,error,critical}]
                  {generate}

positional arguments:
  {generate}            command to run

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER_OF_PAGES, --number-of-pages NUMBER_OF_PAGES
                        number of pages to generate (default: 1)
  -t {A4}, --page-type {A4}
                        page type (default: A4)
  -s PAGE_SEEDER, --page-seeder PAGE_SEEDER
                        choices: {basic, wikipedia[:keyword]}
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        output path (default: current path)
  -l {debug,info,warn,error,critical}, --logging {debug,info,warn,error,critical}
                        Logging level (default e: error)
```

## Contributing

Every contribution is welcome.

Be sure your code is [PEP-8](https://www.python.org/dev/peps/pep-0008/) compliant.
Use [black](https://black.readthedocs.io/en/stable/) to fix your formatting before committing changes.
```bash
black main.py doc_mocker --line-length=100
```
Optional: Install flake8 pre-commit hook to check your code before committing.
```bash
flake8 --install-hook git
git config --bool flake8.strict true
```

### Create a plugin
Plugins are auto-discovered if created as modules in the sub-package `doc_mocker.plugins`
using the [namespace packages](https://packaging.python.org/guides/creating-and-discovering-plugins/#using-namespace-packages)
convention.

Check the [noise plugin](https://github.com/maylonpedroso/doc-mocker-noise-plugin)
to get an idea on the required structure.

### Run tests

```bash
python -m pytest
```

## Credits

View the full list of [contributors](https://github.com/maylonpedroso/doc-mocker/graphs/contributors). [MIT](LICENSE) licensed. 