# Awesome selfhosted services sorted by stars

Copy of [awesome-selfhosted](https://github.com/awesome-selfhosted) repository,
but with projects sorted by GitHub stars.

The data is from [awesome-selfhosted-data](https://github.com/awesome-selfhosted/awesome-selfhosted-data).

## How it works

Continuous integration ([GitHub actions](https://github.com/features/actions)) runs everyday.
Each run triggers the execution of [`app/main.py` script](app/main.py) which:

1. Fetches [awesome-selfhosted-data](https://github.com/awesome-selfhosted/awesome-selfhosted-data)
2. Parses the data from it
3. Generate an `HTML` file from [`app/templates.html` template](app/template.html)
   using [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) and put in the [`web` folder](web)

Then, the CI deploys the `web` folder in `gh-pages` branches, which updates the website hosted on
[GitHub pages](https://pages.github.com/).

## Contributing

To contribute to the list of awesome self-hosted softwares, see
[contributing section of awesome-selfhosted-data](https://github.com/awesome-selfhosted/awesome-selfhosted-data/blob/master/CONTRIBUTING.md)

To contribute to this repository, feel free to open PRs, all the contributions are welcome.
