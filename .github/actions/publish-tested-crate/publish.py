"""Publish a crate, verifying revision identity when resuming a partial release."""

import json
import os
import pathlib
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.error
import urllib.request


def request(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'legra-release-workflow'}), timeout=60)


def verify_revision(info, revision):
    if info.get('git', {}).get('sha1') != revision:
        raise ValueError('Published crate belongs to a different or unknown source revision')


def main():
    crate, version, revision = (os.environ[key] for key in ['RELEASE_CRATE', 'RELEASE_VERSION', 'RELEASE_REVISION'])
    if not re.fullmatch(r'[A-Za-z0-9_-]+', crate) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid crate name or version')
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() != revision:
        raise ValueError('Publication checkout differs from validated revision')
    endpoint = f'https://crates.io/api/v1/crates/{crate}/{version}'
    try:
        with request(endpoint) as response:
            json.load(response)
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        subprocess.run(['cargo', 'publish', '--locked', '--allow-dirty', '--package', crate], check=True)
        return
    with tempfile.TemporaryDirectory(prefix='verify-published-crate-') as folder:
        archive_path = pathlib.Path(folder) / 'package.crate'
        with request(endpoint + '/download') as response, archive_path.open('wb') as archive:
            shutil.copyfileobj(response, archive, length=64 * 1024)
        with tarfile.open(archive_path) as archive:
            member = archive.extractfile(f'{crate}-{version}/.cargo_vcs_info.json')
            if member is None:
                raise ValueError('Published crate lacks source revision evidence')
            verify_revision(json.load(member), revision)
    print(f'{crate} {version} already published from validated revision {revision}')


if __name__ == '__main__':
    main()
