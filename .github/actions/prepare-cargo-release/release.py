"""Prepare one signed release revision for all downstream validation jobs."""

import base64
import json
import os
import pathlib
import re
import subprocess
import tomllib


def version_tuple(value):
    if not re.fullmatch(r'\d+\.\d+\.\d+', value):
        raise ValueError(f'Expected stable semantic version, got {value!r}')
    return tuple(map(int, value.split('.')))


def next_version(current, latest, messages):
    current_tuple = version_tuple(current)
    if latest is None or current_tuple > version_tuple(latest):
        return current
    if current_tuple < version_tuple(latest):
        raise ValueError('Manifest version is behind the latest release tag')
    level = 0
    for message in messages:
        header = message.splitlines()[0]
        if re.match(r'\w+(?:\([^\n]+\))?!:', header) or re.search(r'^BREAKING[ -]CHANGE:', message, re.M):
            level = max(level, 3)
        elif re.match(r'feat(?:\([^\n]+\))?:', header):
            level = max(level, 2)
        elif not re.match(r'(?:docs|style|ci)(?:\([^\n]+\))?:|chore\(release\):', header):
            level = max(level, 1)
    major, minor, patch = current_tuple
    return {0: None, 1: f'{major}.{minor}.{patch + 1}',
            2: f'{major}.{minor + 1}.0', 3: f'{major + 1}.0.0'}[level]


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def output(**values):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
        for key, value in values.items():
            stream.write(f'{key}={value}\n')


def prepare():
    source = run('git', 'rev-parse', 'HEAD')
    if os.environ['GITHUB_REF'] != 'refs/heads/main':
        output(revision=source, release='false', version='')
        return
    remote = run('git', 'ls-remote', 'origin', 'refs/heads/main').split()[0]
    if source != remote:
        subprocess.run(['git', 'fetch', 'origin', remote], check=True)
        parent = run('git', 'rev-parse', f'{remote}^')
        message = run('git', 'log', '-1', '--format=%B', remote)
        if parent == source and message.startswith('chore(release): prepare ') and f'Release source: {source}' in message:
            # Resume the exact version commit prepared by an earlier attempt.
            subprocess.run(['git', 'checkout', '--detach', remote], check=True)
            source = remote
        else:
            # A newer main run includes these changes; never publish a stale base.
            output(revision=source, release='false', version='')
            return
    manifest = tomllib.loads(pathlib.Path('Cargo.toml').read_text())
    package = manifest.get('workspace', {}).get('package', manifest['package'])
    current = package['version']
    tags = [tag for tag in run('git', 'tag', '--merged', 'HEAD', '--list', 'v*').splitlines()
            if re.fullmatch(r'v\d+\.\d+\.\d+', tag)]
    tag = max(tags, key=lambda item: version_tuple(item[1:])) if tags else None
    revisions = f'{tag}..HEAD' if tag else 'HEAD'
    messages = [message.strip() for message in run('git', 'log', '--format=%B%x00', revisions).split('\0') if message.strip()]
    version = next_version(current, tag[1:] if tag else None, messages)
    if version is None:
        pending = False
        if tag and run('git', 'rev-parse', f'{tag}^{{commit}}') == source:
            result = subprocess.run(['gh', 'api', f'repos/{os.environ["GITHUB_REPOSITORY"]}/releases/tags/{tag}'],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                pending = json.loads(result.stdout)['draft']
            elif 'HTTP 404' in result.stderr:
                pending = True
            else:
                raise RuntimeError(result.stderr)
        output(revision=source, release=str(pending).lower(), version=current)
        return
    if version == current:
        output(revision=source, release='true', version=version)
        return
    subprocess.run(['cargo', 'version-info', 'bump', '--version', version, '--no-commit'], check=True)
    paths = run('git', 'diff', '--name-only').splitlines()
    if 'Cargo.toml' not in paths:
        raise RuntimeError('Version bump did not update Cargo.toml')
    additions = [{'path': path, 'contents': base64.b64encode(pathlib.Path(path).read_bytes()).decode()}
                 for path in paths]
    payload = {
        'query': 'mutation($input: CreateCommitOnBranchInput!) { createCommitOnBranch(input: $input) { commit { oid } } }',
        'variables': {'input': {
            'branch': {'repositoryNameWithOwner': os.environ['GITHUB_REPOSITORY'], 'branchName': 'main'},
            'expectedHeadOid': source,
            'message': {'headline': f'chore(release): prepare {version}', 'body': f'Release source: {source}'},
            'fileChanges': {'additions': additions},
        }},
    }
    result = subprocess.run(['gh', 'api', 'graphql', '--input', '-'], input=json.dumps(payload),
                            capture_output=True, text=True, check=True)
    response = json.loads(result.stdout)
    if response.get('errors'):
        raise RuntimeError(response['errors'])
    revision = response['data']['createCommitOnBranch']['commit']['oid']
    output(revision=revision, release='true', version=version)


if __name__ == '__main__':
    prepare()
