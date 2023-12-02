"""
Script to parse raw awesome-selfhoster data
and generate files
"""

import os
import shutil
import subprocess
from typing import Any, List
import jinja2
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    """Main entrypoint"""
    fetch_data()
    softwares = parse_yaml_files(
        list_dir(os.path.join("awesome-selfhosted-data", "software"))
    )
    tagToSoftware = sortTagToSoftware(softwares)
    generate(softwares=sorted(list(tagToSoftware.items())))


def fetch_data():
    """Fetch the data from awesome-selfhosted-data"""
    shutil.rmtree("awesome-selfhosted-data", ignore_errors=True)
    subprocess.run((
        "git", "clone", "--depth=1", "https://github.com/awesome-selfhosted/awesome-selfhosted-data"
    ))


def list_dir(directory_path: str) -> List[str]:
    """Return the paths to each file in given directory"""
    return [os.path.join(directory_path, file) for file in os.listdir(directory_path)]


def parse_yaml_files(files: List[str]):
    """Parse a list of yaml files"""
    return [parse_yaml_file(file) for file in files]


def parse_yaml_file(filepath: str) -> Any:
    """Parse a Yaml file"""
    with open(filepath, "r", encoding="utf-8") as fis:
        data = yaml.safe_load(fis)
    return data


def generate(**data):
    """Generate the HTML file"""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(BASE_DIR),
        autoescape=jinja2.select_autoescape()
    )
    template = env.get_template("template.html")
    result = template.render(**data)
    with open(
        os.path.join(BASE_DIR, "..", "web", "index.html"), "w", encoding="utf-8"
    ) as fos:
        fos.write(result)


def sortTagToSoftware(softwares: List[dict]):
    """Sort the softwares by tag"""
    tagToSoftware = {}
    for software in softwares:
        for tag in software["tags"]:
            prev = tagToSoftware.get(tag)
            if prev is None:
                tagToSoftware[tag] = [software]
            else:
                prev.append(software)
    sortedResult = {}
    for tag in sorted(tagToSoftware.keys()):
        software_list = tagToSoftware[tag]
        sortedResult[tag] = sorted(software_list, key=lambda software: -software.get('stargazers_count', -1))
    return sortedResult


if __name__ == "__main__":
    main()
