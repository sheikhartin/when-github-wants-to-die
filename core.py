#!/usr/bin/env python

import shutil
from pathlib import Path
from typing import Optional

import requests
import git
from git.exc import GitCommandError


def _validate_account(account: str) -> Optional[dict]:
    """Validates the account to make sure it exists."""
    resp = requests.get(f'https://api.github.com/users/{account}')
    if resp.status_code == 200:
        return resp.json()
    return None


def _build_path(*paths: str, delete_before: Optional[bool] = False) -> None:
    """Builds the path if it doesn't exist."""
    for path in paths:
        if delete_before:
            shutil.rmtree(path, ignore_errors=True)
        Path(path).mkdir(parents=True, exist_ok=True)


def clone_repository(account: str, repo: str, branch: Optional[str] = None) -> None:
    """Clones the repository."""
    _build_path(f'{account}/repos/{repo}', delete_before=True)
    try:
        git.Repo.clone_from(f'https://github.com/{account}/{repo}', f'{account}/repos/{repo}', branch=branch)
    except GitCommandError as e:
        print(f'Error occurred while cloning {account}/{repo}...')
        print(f'Details: {e}')
        shutil.rmtree(f'{account}/repos/{repo}', ignore_errors=True)


def clone_all_repositories(account: str) -> None:
    """Clones all repositories for the account."""
    resp = requests.get(f'https://api.github.com/users/{account}/repos')
    repo_names = [repo['name'] for repo in resp.json()]
    for repo in repo_names:
        print(f'Cloning {account}/{repo}...')
        clone_repository(account, repo)


def clone_gist(account: str, gist_id: str) -> None:
    """Clones the gist."""
    _build_path(f'{account}/gists/{gist_id}', delete_before=True)
    try:
        git.Repo.clone_from(f'https://gist.github.com/{account}/{gist_id}', f'{account}/gists/{gist_id}')
    except GitCommandError as e:
        print(f'Error occurred while cloning {account}/{gist_id}...')
        print(f'Details: {e}')
        shutil.rmtree(f'{account}/gists/{gist_id}', ignore_errors=True)


def clone_all_gists(account: str) -> None:
    """Clones all gists for the account."""
    resp = requests.get(f'https://api.github.com/users/{account}/gists')
    gist_ids = [gist['id'] for gist in resp.json()]
    for gist_id in gist_ids:
        print(f'Cloning {account}/{gist_id}...')
        clone_gist(account, gist_id)


if __name__ == '__main__':
    import argparse
    import sys
    import os

    parser = argparse.ArgumentParser(description='Clone any or even all repositories and gists for a GitHub account.')
    parser.add_argument('account', help='the github account to clone from')
    parser.add_argument('-r', '--repositories', nargs='+', help='the repositories to clone')
    parser.add_argument('-g', '--gists', nargs='+', help='the gists to clone')
    parser.add_argument('-q', '--quiet', action='store_true', help='suppress output')
    args = parser.parse_args()

    if args.quiet:
        sys.stdout = open(os.devnull, 'w')

    if not _validate_account(args.account):
        print(f'Account {args.account} does not exist...')
        sys.exit(1)
    print('Account exists...')

    if not args.repositories and not args.gists:
        print('Cloning all repositories and gists...')
        clone_all_repositories(args.account)
        clone_all_gists(args.account)
    if args.repositories:
        for repo in args.repositories:
            repo, *branch = repo.split('@')
            print(f'Cloning {args.account}/{repo} repository...')
            clone_repository(args.account, repo, branch=branch[0] if branch else None)
    if args.gists:
        for gist_id in args.gists:
            print(f'Cloning {args.account}/{gist_id} gist...')
            clone_gist(args.account, gist_id)

    print('The script has finished!')
