#!/usr/bin/env python

import json
import urllib.request
import shutil
import subprocess


def run_and_log(args):
    print(f"running command {args}")
    subprocess.run(args)


repos = {
    "sharkdp/bat": "https://github.com/sharkdp/bat/releases/download/vLATEST_TAG/bat-vLATEST_TAG-x86_64-unknown-linux-gnu.tar.gz",
    "ogham/exa": "https://github.com/ogham/exa/releases/download/vLATEST_TAG/exa-linux-x86_64-vLATEST_TAG.zip",
    "sharkdp/fd": "https://github.com/sharkdp/fd/releases/download/vLATEST_TAG/fd-vLATEST_TAG-x86_64-unknown-linux-gnu.tar.gz",
    "dalance/procs": "https://github.com/dalance/procs/releases/download/vLATEST_TAG/procs-vLATEST_TAG-x86_64-lnx.zip",
}

current_versions = {}

for r in repos:
    print(f"get latest version for {r}")
    url = f"https://api.github.com/repos/{r}/releases/latest"
    f = urllib.request.urlopen(url)
    tag_name = json.loads(f.read().decode("utf-8"))["tag_name"]
    tag_name = tag_name.removeprefix("v")
    current_versions[r] = tag_name

    artifact_url = repos.get(r)
    artifact_url = artifact_url.replace("LATEST_TAG", tag_name)
    print(f"download artifact from {artifact_url}")
    base_name = r.replace("/", "-")
    file_name = f"{base_name}.zip" if artifact_url.endswith("zip") else f"{base_name}.tgz"
    print(f"saving file as {file_name}")

    with urllib.request.urlopen(artifact_url) as response, open(
        file_name, "wb"
    ) as out_file:
        shutil.copyfileobj(response, out_file)

        # The tarballs create a nested directory when extracted using "extract_dir" option, so leave it out for now
        if artifact_url.endswith("zip"):
            shutil.unpack_archive(file_name, base_name)
        else:
            shutil.unpack_archive(file_name)

run_and_log(
    [
        "docker",
        "build",
        "--tag",
        "modern-unix",
        "--build-arg",
        f'BAT_VERSION={current_versions["sharkdp/bat"]}',
        "--build-arg",
        f'FD_VERSION={current_versions["sharkdp/fd"]}',
        ".",
    ]
)
