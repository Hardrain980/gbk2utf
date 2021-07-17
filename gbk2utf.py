import argparse
import os
import sys


class BackupFailException(Exception):
    pass


def convert(
    file: str,
    in_place: bool = False,
    backup_anyway: bool = False
) -> None:
    with open(file, 'rb') as fh:
        content = fh.read()

    content = content.decode('CP936').encode('utf-8')

    if not in_place:
        if os.path.exists(f"{file}.old") and not backup_anyway:
            raise BackupFailException()

        os.rename(file, f"{file}.old")

    with open(file, 'wb') as fh:
        fh.write(content)


arg_parser = argparse.ArgumentParser(
    description='Convert GBK coded file to UTF-8 coded.',
    allow_abbrev=False
)
arg_parser.add_argument(
    'files',
    metavar='files',
    type=str,
    nargs='+',
    help='file(s) to proceed',
)
arg_parser.add_argument(
    '-i', '--in-place',
    action='store_true',
    help='convert file in place, do not save backup.',
)
arg_parser.add_argument(
    '-b', '--backup-anyway',
    action='store_true',
    help='overwrite the existing backup file if it exists.',
)

args = vars(arg_parser.parse_args())

for file in list(args['files']):
    try:
        convert(
            file,
            in_place=bool(args['in_place']),
            backup_anyway=bool(args['backup_anyway'])
        )
    except BackupFailException:
        print(f'Failed: Could not save backup: "{file}"', file=sys.stderr)
    except FileNotFoundError:
        print(f'Failed: Not found: "{file}"', file=sys.stderr)
    except PermissionError:
        print(f'Failed: Permission denied: "{file}"', file=sys.stderr)
    except IsADirectoryError:
        print(f'Failed: Input is a directory: "{file}"', file=sys.stderr)
    except UnicodeDecodeError as e:
        print(f'Failed: Unable to decode as GBK: "{file}": {e}')
    else:
        print(f'Converted: "{file}"', file=sys.stderr)
    finally:
        pass
