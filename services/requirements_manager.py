import shutil
import pkg_resources


def write_to_package_file(all_packages, writing_pad):
    for _dir in writing_pad:
        with open(_dir, "w") as package_file:
            for _package, _version in all_packages.items():
                package_file.write(writing_pad[_dir](_package, _version))


def upate_toml_file():
    try:
        files = (
            "requirements/toml_part1.txt",
            "requirements/poetry.txt",
            "requirements/toml_part2.txt",
        )
        with open("pyproject.toml", "wb") as wfd:
            for f in files:
                with open(f, "rb") as fd:
                    shutil.copyfileobj(fd, wfd)
                    wfd.write(b"\n")
    except Exception as err:
        print(err)


def update_requirements():
    """
    Repackages requirements files, by making sure base file has no versions(newer versions of pip).
    """
    list_of_packages: list = [
        tuple(str(ws).split()) for ws in pkg_resources.working_set
    ]
    all_packages: dict = dict(sorted(list_of_packages, key=lambda x: (x[0].lower(), x)))
    packages_available: list = []
    try:
        base_requirements_dir: str = "requirements/base.txt"
        dev_requirements_dir: str = "requirements/development.txt"
        poetry_requirements_dir: str = "requirements/poetry.txt"
        writing_pad = {
            base_requirements_dir: lambda _package, _version: f"{_package}\n",
            dev_requirements_dir: lambda _package, _version: f"{_package}=={_version}\n",
            poetry_requirements_dir: lambda _package, _version: f'{_package} = "^{_version}"\n',
        }
        with open(base_requirements_dir, "r") as package_file:
            for _package in package_file:
                packages_available.append(_package.replace("\n", ""))

        if len(all_packages.items()) > len(packages_available):
            write_to_package_file(all_packages, writing_pad)
            upate_toml_file()
    except FileNotFoundError as err:
        print(f"Error {err}")
