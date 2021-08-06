#!/usr/bin/env python

import json
import urllib.request
import shutil
import subprocess


repos = {
    "sharkdp/bat": "https://github.com/sharkdp/bat/releases/download/vLATEST_TAG/bat-vLATEST_TAG-x86_64-unknown-linux-gnu.tar.gz",
    "ogham/exa": "https://github.com/ogham/exa/releases/download/vLATEST_TAG/exa-linux-x86_64-vLATEST_TAG.zip",
    "sharkdp/fd": "https://github.com/sharkdp/fd/releases/download/vLATEST_TAG/fd-vLATEST_TAG-x86_64-unknown-linux-gnu.tar.gz",
    "dalance/procs": "https://github.com/dalance/procs/releases/download/vLATEST_TAG/procs-vLATEST_TAG-x86_64-lnx.zip",
}

current_versions = {}

for r in repos:
    print(r)
    url = f"https://api.github.com/repos/{r}/releases/latest"
    f = urllib.request.urlopen(url)
    tag_name = json.loads(f.read().decode("utf-8"))["tag_name"]
    tag_name = tag_name.removeprefix("v")
    current_versions[r] = tag_name
    artifact_url = repos.get(r)
    artifact_url = artifact_url.replace("LATEST_TAG", tag_name)
    print(artifact_url)

    file_name = r.replace("/", "-")
    if artifact_url.endswith("zip"):
        file_name = file_name + ".zip"
    else:
        file_name = file_name + ".tgz"

    with urllib.request.urlopen(artifact_url) as response, open(
        file_name, "wb"
    ) as out_file:
        shutil.copyfileobj(response, out_file)

        if artifact_url.endswith("zip"):
            shutil.unpack_archive(file_name, r.replace("/", "-"))
        else:
            shutil.unpack_archive(file_name)

subprocess.run(
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
