"""
Script to parse raw awesome-selfhosted data
and generate files
"""

from datetime import datetime
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
    tag_to_software = sort_tag_to_software(softwares)
    generate(softwares=sorted(list(tag_to_software.items())))


def fetch_data():
    """Fetch the data from awesome-selfhosted-data"""
    shutil.rmtree("awesome-selfhosted-data", ignore_errors=True)
    subprocess.run(
        ("git", "clone", "--depth=1", "https://github.com/awesome-selfhosted/awesome-selfhosted-data")
    )


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
    result = template.render(now=datetime.now(), **data)
    with open(
        os.path.join(BASE_DIR, "..", "web", "index.html"), "w", encoding="utf-8"
    ) as fos:
        fos.write(result)


def sort_tag_to_software(softwares: List[dict]) -> dict:
    """Sort the softwares by tag"""
    tag_to_software = {}
    for software in softwares:
        for tag in software["tags"]:
            prev = tag_to_software.get(tag)
            if prev is None:
                tag_to_software[tag] = [software]
            else:
                prev.append(software)
    sorted_result = {}
    for tag in sorted(tag_to_software.keys()):
        software_list = tag_to_software[tag]
        sorted_result[tag] = sorted(
            software_list, key=lambda software: -software.get('stargazers_count', -1)
        )
    return sorted_result


if __name__ == "__main__":
    main()
