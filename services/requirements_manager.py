import pkg_resources


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
        with open(base_requirements_dir, "r") as package_file:
            for _package in package_file:
                packages_available.append(_package.replace("\n", ""))

        if len(all_packages.items()) > len(packages_available):
            with open(base_requirements_dir, "w") as package_file:
                for _package, _version in all_packages.items():
                    package_file.write(f"{_package}\n")
            with open(dev_requirements_dir, "w") as package_file:
                for _package, _version in all_packages.items():
                    package_file.write(f"{_package}=={_version}\n")
    except FileNotFoundError as err:
        print(f"Error {err}")
