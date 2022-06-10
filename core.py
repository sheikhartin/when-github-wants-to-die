#!/usr/bin/env python

from typing import Optional

import requests
import git


def _get_account_info(id: str) -> Optional[dict]:
    """Gets account info from GitHub by ID."""
    resp = requests.get(f'https://api.github.com/users/{id}')
    if resp.status_code == 200:
        return resp.json()
    return None


def _get_all_repos_metadata(id: str) -> str:
    """Gets all repositories metadata such as name, description, etc."""
    resp = requests.get(f'https://api.github.com/users/{id}/repos?per_page=100&sort=stars')  # Top 100 repositories is enough
    return [(repo['name'], repo['description'], repo['default_branch']) for repo in resp.json()]


def download_repo(id: str, repo_name: str, branch: Optional[str] = None,
                  path: Optional[str] = None) -> None:
    """Downloads a repository from a account."""
    git.Repo.clone_from(f'https://github.com/{id}/{repo_name}.git',
                        path if path is not None else repo_name, branch=branch)


def download_all_repos(id: str) -> None:
    """Downloads all repositories from a account."""
    all_repos_metadata = _get_all_repos_metadata(id)
    for repo_name, description, default_branch in all_repos_metadata:
        print(f'Downloading {repo_name}... {description}')
        # print(f'Repository: {repo_name}')
        # print(f'Description: {description}')
        download_repo(id, repo_name, default_branch)
        print()


if __name__ == '__main__':
    import argparse
    import sys
    import os

    parser = argparse.ArgumentParser(description='Download repositories from GitHub for worrying situations.')
    parser.add_argument('id', help='The ID of the account what could be a user or organization')
    parser.add_argument('-r', '--repositories', nargs='+', help='The name of the repositories to download')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress output')
    args = parser.parse_args()

    if args.quiet:
        sys.stdout = open(os.devnull, 'w')

    account_info = _get_account_info(args.id)
    if account_info is None:
        print(f'Could not find account {args.id}!')
        sys.exit(1)
    print(f'Account found!')
    print(f'Name: {account_info["name"]}')
    print(f'Bio: {account_info["bio"]}')
    print(f'Email: {account_info["email"]}')
    print(f'Twitter: {account_info["twitter_username"]}')
    print(f'Blog: {account_info["blog"]}')
    print(f'Location: {account_info["location"]}\n')

    if args.repositories:
        for repo in args.repositories:
            name, *branch = repo.split('@')
            print(f'Downloading {name}...')
            download_repo(args.id, name, branch[0] if branch else None)
    else:
        print(f'Downloading all repositories for {args.id}...')
        download_all_repos(args.id)

    print('All done! ;)')
