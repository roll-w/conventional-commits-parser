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

from dataclasses import dataclass

import git


@dataclass
class CommitInfo:
    typ: str
    scope: str
    title: str
    message: str
    author: str
    committer: str
    commit_time: str
    hash: str
    break_change: bool


def collect_commits(repo: git.Repo, ref1: str, ref2: str) -> list[CommitInfo]:
    commits = []
    for commit in repo.iter_commits(ref1 + '..' + ref2):
        commits.append(parse_commit(commit))
    return commits


@dataclass
class CommitMessage:
    typ: str
    scope: str
    title: str
    message: str
    break_change: bool = False


def parse_commit_message(commit: git.Commit) -> CommitMessage:
    msg = commit.message
    break_change = False
    if ':' not in msg:
        return CommitMessage('', '', msg, msg, break_change)
    type_scope = msg.split(':')[0]
    if '(' in type_scope and ')' in type_scope:
        typ, scope = type_scope.split('(')[0], type_scope.split('(')[1].split(')')[0]
    else:
        typ, scope = type_scope, ''

    if typ.endswith('!'):
        break_change = True
        typ = typ[:-1]

    title = msg.split(':')[1].strip()
    if '\n' in title:
        title = title.split('\n')[0]

    # Collect the rest part as the message, and remove leading/trailing whitespaces
    message = '\n'.join(msg.split('\n')[1:]).strip()
    return CommitMessage(typ, scope, title, message, break_change)


def parse_commit(commit: git.Commit) -> CommitInfo:
    msg = parse_commit_message(commit)
    return CommitInfo(
        msg.typ, msg.scope, msg.title,
        msg.message,
        commit.author.name,
        commit.author.email,
        commit.committed_datetime.isoformat(),
        commit.hexsha,
        msg.break_change
    )
