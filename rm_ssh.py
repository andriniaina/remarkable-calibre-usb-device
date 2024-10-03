#!/usr/bin/env python3

import sys
import uuid
import os
import time
import json
import shutil
import argparse
import uuid
import subprocess
import tempfile
import pathlib
import urllib.request
import re
import time


XOCHITL_BASE_FOLDER = "~/.local/share/remarkable/xochitl"
default_prepdir = tempfile.mkdtemp(prefix="resync-")

ssh_socketfile = "/tmp/remarkable-push.socket"
ssh_options = "-o BatchMode=yes"
ssh_socket_options = f" -S {ssh_socketfile}" if os.name != "nt" else ""


def xochitl_restart(ip):
    cmd = f'ssh {ssh_options} {ssh_socket_options} root@{ip} "systemctl restart xochitl"'
    subprocess.getoutput(cmd)


def mkdir(ip, visible_name, parent_id):
    file_id = str(uuid.uuid4())
    with tempfile.TemporaryDirectory() as tmp_folder:
        file_metadata = f"{file_id}.metadata"
        file_content = f"{file_id}.content"
        current_timestamp_str = str(int(time.time()))
        with open(pathlib.Path(tmp_folder, file_metadata), "w+") as fp:
            metadata_json = (
                '{"createdTime": "'
                + current_timestamp_str
                + '",    "lastModified": "'
                + current_timestamp_str
                + '",    "parent": "'
                + parent_id
                + '",    "pinned": false,    "type": "CollectionType",    "visibleName": "'
                + visible_name
                + '"}'
            )
            fp.write(metadata_json)
        with open(pathlib.Path(tmp_folder, file_content), "w+") as fp:
            content_json = """{"tags": [    ]}"""
            fp.write(content_json)

        cmd = f"scp -r {tmp_folder}/* root@{ip}:{XOCHITL_BASE_FOLDER}"
        result = subprocess.getoutput(cmd)
        print(result)
    return file_id
