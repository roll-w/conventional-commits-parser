#  MIT License
#
#  Copyright (c) 2024 RollW
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import argparse
import os

import git

from parser.commitlog import collect_commits, CommitInfo
from parser.file_writer import FileWriterFactory, FileFormat, RAW_CONFIG


def pull_repo(repo_url: str) -> git.Repo:
    if os.path.exists(repo_url):
        print('Repo exists, skip cloning')
        path = repo_url
    else:
        print('Repo not exists, cloning to repo/')
        git.Repo.clone_from(repo_url, 'repo')
        print('Repo cloned successfully')
        path = 'repo'

    return git.Repo.init(path)


def get_ref_to_root(rep: git.Repo) -> str:
    first_commit = next(rep.iter_commits(rev='HEAD', max_parents=0))
    return first_commit.hexsha


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate changelog from git commits.',
                                     add_help=True, )
    parser.add_argument('--from', '-f', dest='from_ref', default='root',
                        help='Git ref from, default: root (the first commit). '
                             'Can be a commit hash, tag or any git ref')
    parser.add_argument('--to', '-t', dest='to_ref', default='HEAD',
                        help='Git ref to, default: HEAD. Can be a commit hash, tag or any git ref')
    parser.add_argument('--output', '-o', dest='output', default='CHANGELOG.md',
                        help='Output file name, default: CHANGELOG.md')
    parser.add_argument('--output-format', dest='output_format', default='markdown',
                        help='Output format, default: markdown, supports markdown, json, yaml, csv')
    parser.add_argument('--repo', '-r', dest='repo', default='.',
                        help='Target git repo, default: . (current directory).'
                             'Can be a local path or a git url to clone')
    # TODO: sort by date or scope
    # TODO: mapping read from config file or command line
    args = parser.parse_args()
    repo = pull_repo(args.repo)
    from_ref = args.from_ref
    if from_ref == 'root':
        from_ref = get_ref_to_root(repo)
    commits: list[CommitInfo] = collect_commits(repo, from_ref, args.to_ref)
    writer = FileWriterFactory.create_writer(
        FileFormat(args.output_format),
        args.output, config=RAW_CONFIG
    )
    writer.write(commits)
    print(f'Changelog generated to {args.output}')
    pass
