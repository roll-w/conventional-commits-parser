# conventional-commits-parser

A simple parser for [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Usage

```
parser.py [-h] [--from FROM_REF] [--to TO_REF] [--output OUTPUT]
          [--output-format OUTPUT_FORMAT] [--repo REPO]
```

- `-h`, `--help`: Show the help message and exit.
- `--from FROM_REF`: The starting reference to parse the commits.
- `--to TO_REF`: The ending reference to parse the commits.
- `--output OUTPUT`: The output file to write the parsed commits.
- `--output-format OUTPUT_FORMAT`: The output format of the parsed commits.
  Currently, support `markdown`, `json`, `yaml`, and `csv`.
- `--repo REPO`: The repository to parse the commits. It can be a local path or a remote URL.

Example:

```shell
python parser.py --from v1.0.0 --to v1.1.0 --output CHANGELOG.md --output-format markdown --repo /path/to/repo
```

## License

```text
MIT License

Copyright (c) 2024 RollW

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```