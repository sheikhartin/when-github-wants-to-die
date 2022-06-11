#!/usr/bin/env python

import shutil
from typing import Optional

import requests
import git


def _get_account_info(username: str) -> Optional[dict]:
    """Gets account info from GitHub by username."""
    resp = requests.get(f'https://api.github.com/users/{username}')
    if resp.status_code == 200:
        return resp.json()
    return None


def _get_all_repos_metadata(username: str) -> list:
    """Gets all repositories metadata such as name, description and default branch."""
    resp = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100&sort=stars')  # https://docs.github.com/en/rest/search#search-repositories
    return [(repo['name'], repo['description'], repo['default_branch']) for repo in resp.json()]


def download_repo(username: str, repo_name: str, branch: Optional[str] = None,
                  path: Optional[str] = None) -> None:
    """Downloads a repository from a account."""
    shutil.rmtree(path if path is not None else repo_name, ignore_errors=True)
    git.Repo.clone_from(f'https://github.com/{username}/{repo_name}.git',
                        path if path is not None else repo_name, branch=branch)


def download_all_repos(username: str) -> None:
    """Downloads all repositories from a account."""
    all_repos_metadata = _get_all_repos_metadata(username)
    for repo_name, description, default_branch in all_repos_metadata:
        print(f'Downloading {repo_name}... {description}')
        # print(f'Repository: {repo_name}')
        # print(f'Description: {description}')
        download_repo(username, repo_name, default_branch)
        # print()


def _get_all_gists_metadata(username: str) -> list:
    """Gets all gists metadata such as ID, description and files."""
    resp = requests.get(f'https://api.github.com/users/{username}/gists?per_page=100')
    return [(gist['id'], gist['description'], gist['files']) for gist in resp.json()]


def download_gist(username: str, id: str, filename: str) -> None:
    """Downloads a gist from a account."""
    with requests.get(f'https://gist.github.com/{username}/{id}/raw/{filename}', stream=True) as r:
        # print('Status code:', r.status_code)
        # print('Response:', r.text)
        with open(filename, 'w') as f:
            f.write(r.text)


def download_all_gists(username: str) -> None:
    """Downloads all gists from a account."""
    all_gists_metadata = _get_all_gists_metadata(username)
    for gist_id, description, files in all_gists_metadata:
        print(f'Downloading {gist_id}... {description}')
        # print(f'Gist: {gist_id}')
        # print(f'Description: {description}')
        for filename, _ in files.items():
            download_gist(username, gist_id, filename)
        # print()


if __name__ == '__main__':
    import argparse
    import sys
    import os

    parser = argparse.ArgumentParser(description='Download repositories from GitHub for worrying situations.')
    parser.add_argument('username', help='The ID of the account what could be a user or organization')
    parser.add_argument('-r', '--repositories', nargs='+', help='The name of the repositories to download')
    parser.add_argument('-g', '--gists', nargs='+', help='The ID of the gists and the files to download')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress output')
    args = parser.parse_args()

    if args.quiet:
        sys.stdout = open(os.devnull, 'w')

    account_info = _get_account_info(args.username)
    if account_info is None:
        print(f'Could not find account {args.username}!')
        sys.exit(1)
    print(f'An account with ID `{args.username}` was found!')
    print(f'Name: {account_info["name"]}')
    print(f'Bio: {account_info["bio"] or "-"}')
    print(f'Email: {account_info["email"] or "-"}')
    print(f'Twitter: {account_info["twitter_username"] or "-"}')
    print(f'Blog: {account_info["blog"] or "-"}')
    print(f'Location: {account_info["location"] or "-"}\n')

    if not args.repositories and not args.gists:
        print(f'Downloading all repositories for {args.username}...')
        download_all_repos(args.username)
        print(f'\nDownloading all gists for {args.username}...')
        download_all_gists(args.username)
    if args.repositories:
        for repo in args.repositories:
            name, *branch = repo.split('@')
            print(f'Downloading {name}...')
            download_repo(args.username, name, branch[0] if branch else None)
    if args.gists:
        for gist in args.gists:
            gist_id, *filename = gist.split('@')
            print(f'Downloading {gist_id}...')
            download_gist(args.username, gist_id, filename[0] if filename else None)

    print('All done! ;)')
