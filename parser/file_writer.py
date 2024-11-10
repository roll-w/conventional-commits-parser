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
from enum import Enum

from parser.commitlog import CommitInfo


@dataclass
class WriterConfig:
    # Mapping from commit type to display name
    typ_mapping: dict[str, str]
    # TODO: not implemented yet
    group_by_scope: bool

    # Ignore these commit types when writing commits
    ignore_typs: list[str]

    # Display name for breaking changes
    break_change_mark: str


DEFAULT_CONFIG = WriterConfig(
    typ_mapping={
        'feat': 'Features',
        'fix': 'Bug Fixes',
        'refactor': 'Refactors',
        'perf': 'Performance Improvements',
        'docs': 'Documentation',
        'style': 'Styles',
        'test': 'Tests',
        'chore': 'Chores',
        'revert': 'Reverts'
    },
    group_by_scope=False,
    ignore_typs=[],
    break_change_mark='Breaking Changes'
)

RAW_CONFIG = WriterConfig(
    typ_mapping={},
    group_by_scope=False,
    ignore_typs=[],
    break_change_mark='Breaking Changes'
)


class CommitFileWriter:
    def __init__(self, file_path: str, config: WriterConfig = DEFAULT_CONFIG):
        self.file_path = file_path
        self.config = config

    def write(self, commits: list[CommitInfo]):
        pass


class FileFormat(Enum):
    MARKDOWN = 'markdown'
    JSON = 'json'
    YAML = 'yaml'
    CSV = 'csv'
    RAW = 'raw'


class FileWriterFactory:
    @staticmethod
    def from_format(form: str) -> FileFormat:
        return FileFormat(form)

    @staticmethod
    def create_writer(file_format: FileFormat, file_path: str,
                      config: WriterConfig = DEFAULT_CONFIG) -> CommitFileWriter:
        if file_format == FileFormat.MARKDOWN:
            return MarkdownCommitFileWriter(file_path, config)
        elif file_format == FileFormat.JSON:
            return JsonCommitFileWriter(file_path, config)
        elif file_format == FileFormat.YAML:
            return YamlCommitFileWriter(file_path, config)
        elif file_format == FileFormat.CSV:
            return CsvCommitFileWriter(file_path, config)
        elif file_format == FileFormat.RAW:
            return RawCommitFileWriter(file_path, config)
        else:
            raise ValueError(f'Unsupported file format {file_format}')


class MarkdownCommitFileWriter(CommitFileWriter):

    def __init__(self, file_path: str, config: WriterConfig = DEFAULT_CONFIG):
        super(MarkdownCommitFileWriter, self).__init__(file_path, config)

    def prepare_data(self, commits: list[CommitInfo]) -> str:
        typ_mapping = self.config.typ_mapping
        grouped_commits = {
            typ: [
                commit for commit in commits if commit.typ == typ
            ] for typ in set(commit.typ for commit in commits)
        }
        result = '## Changelog\n'
        result += '\n'.join(
            f'### {typ_mapping.get(typ, typ)}\n' +
            '\n'.join(
                f'- {commit.scope + ": " if commit.scope else ""}{commit.title} by {commit.author}'
                for commit in commits
            ) + '\n'
            for typ, commits in grouped_commits.items()
        )
        return result

    def write(self, commits: list[CommitInfo]):
        with open(self.file_path, 'w') as file:
            file.write(self.prepare_data(commits))


class JsonCommitFileWriter(CommitFileWriter):
    """
    write commits into JSON format like:
    ```
    [
        {
            "type": "feat",
            "scope": "scope",
            "title": "title",
            "message": "message",
            "author": "author",
            "committer": "committer@example.com",
            "commit_time": "2000-01-01T00:00:00Z",
            "hash": "hash",
            "break_change": false
        }
    ]
    ```
    """

    def __init__(self, file_path: str, config: WriterConfig = DEFAULT_CONFIG):
        super(JsonCommitFileWriter, self).__init__(file_path, config)

    def prepare_data(self, commits: list[CommitInfo]) -> str:
        import json
        typ_mapping = self.config.typ_mapping
        return json.dumps([
            {
                "type": typ_mapping.get(commit.typ, commit.typ),
                "scope": commit.scope,
                "title": commit.title,
                "message": commit.message,
                "author": commit.author,
                "committer": commit.committer,
                "commit_time": commit.commit_time,
                "hash": commit.hash,
                "break_change": commit.break_change
            }
            for commit in commits
            if commit.typ not in self.config.ignore_typs
        ], ensure_ascii=False, indent=4)

    def write(self, commits: list[CommitInfo]):
        with open(self.file_path, 'w') as file:
            file.write(self.prepare_data(commits))


class YamlCommitFileWriter(CommitFileWriter):
    """
    write commits into YAML format like:
    ```
    - type: feat
      scope: scope
      title: title
      message: message
      author: author
      committer:
      commit_time: 2000-01-01T00:00:00Z
      hash: hash
      break_change: false
    ```
    """

    def __init__(self, file_path: str, config: WriterConfig = DEFAULT_CONFIG):
        super(YamlCommitFileWriter, self).__init__(file_path, config)

    def prepare_data(self, commits: list[CommitInfo]) -> str:
        import yaml
        typ_mapping = self.config.typ_mapping
        return yaml.dump([
            {
                "type": typ_mapping.get(commit.typ, commit.typ),
                "scope": commit.scope,
                "title": commit.title,
                "message": commit.message,
                "author": commit.author,
                "committer": commit.committer,
                "commit_time": commit.commit_time,
                "hash": commit.hash,
                "break_change": commit.break_change
            }
            for commit in commits
            if commit.typ not in self.config.ignore_typs
        ], allow_unicode=True)

    def write(self, commits: list[CommitInfo]):
        with open(self.file_path, 'w') as file:
            file.write(self.prepare_data(commits))


class CsvCommitFileWriter(CommitFileWriter):
    """
    write commits into CSV format like:
    ```
    type,scope,title,message,author,committer,commit_time,hash,break_change
    feat,scope,title,message,author,committer,2000-01-01T00:00:00Z,hash,false
    ```
    """

    def __init__(self, file_path: str, config: WriterConfig = DEFAULT_CONFIG):
        super(CsvCommitFileWriter, self).__init__(file_path, config)

    def prepare_data(self, commits: list[CommitInfo]) -> str:
        import csv
        import io
        typ_mapping = self.config.typ_mapping
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            "type", "scope", "title", "message", "author", "committer", "commit_time", "hash", "break_change"
        ])
        writer.writerows([
            [
                typ_mapping.get(commit.typ, commit.typ),
                commit.scope,
                commit.title,
                commit.message,
                commit.author,
                commit.committer,
                commit.commit_time,
                commit.hash,
                commit.break_change
            ]
            for commit in commits
            if commit.typ not in self.config.ignore_typs
        ])
        return output.getvalue()

    def write(self, commits: list[CommitInfo]):
        with open(self.file_path, 'w') as file:
            file.write(self.prepare_data(commits))


class RawCommitFileWriter(CommitFileWriter):

    def __init__(self, file_path: str, config: WriterConfig = DEFAULT_CONFIG):
        super(RawCommitFileWriter, self).__init__(file_path, config)

    def write(self, commits: list[CommitInfo]):
        with open(self.file_path, 'w') as file:
            file.write('\n'.join(
                commit.__dict__.__str__() for commit in commits
                if commit.typ not in self.config.ignore_typs)
            )
