"""Opt-in Python open guard; importing this module installs no hooks.

Derive the complete held path/object alias set from authenticated metadata
before calling add_root(). Install separately in every Python consumer process.
This is an observation/control for cooperative quiescent execution, not a
sandbox against native code, subprocesses, or hostile concurrent path changes.
Denials are never positive consumer qualification, even if the consumer catches
PermissionError and returns zero. The ledger contains path/descriptor metadata,
never protected contents. Native Git processing is outside the Python guard.
"""
from pathlib import Path
import os


class HeldBodyGuard:
    def __init__(self):
        self.paths = set()
        self.inodes = set()
        self.object_roots = set()
        self.events = []
        self._original_os_open = os.open
        self._installed = False

    @property
    def denials(self):
        return len(self.events)

    def add_root(self, root, held_paths, *, protect_git_objects=True):
        root = Path(root).absolute()
        if not root.is_dir() or root.is_symlink():
            raise RuntimeError('Held guard requires an ordinary root directory')
        if protect_git_objects:
            self.object_roots.add(str((root / '.git/objects').resolve()))
        for relative in held_paths:
            if not isinstance(relative, str) or not relative or relative.startswith('/') or any(
                    part in ('', '.', '..') for part in relative.split('/')):
                raise RuntimeError('Unsafe held metadata path')
            target = root
            for part in relative.split('/'):
                target = target / part
                if target.is_symlink():
                    raise RuntimeError('Symlink in held metadata path')
            self.paths.add(str(target.resolve()))
            if target.exists():
                info = target.stat()
                self.inodes.add((info.st_dev, info.st_ino))

    def add(self, root, held_rows):
        self.add_root(root, [row['path'] for row in held_rows])

    def inspect(self, value, dir_fd=None):
        if not isinstance(value, (int, str, bytes, os.PathLike)):
            return
        name = None
        forbidden = False
        try:
            if isinstance(value, int):
                info = os.fstat(value)
            else:
                name = os.fsdecode(value)
                if dir_fd is not None and not os.path.isabs(name):
                    name = os.path.join(os.readlink('/proc/self/fd/' + str(dir_fd)), name)
                name = os.path.realpath(name)
                forbidden = name in self.paths or any(
                    name == root or name.startswith(root + '/') for root in self.object_roots)
                info = os.stat(name)
            forbidden = forbidden or (info.st_dev, info.st_ino) in self.inodes
        except OSError:
            pass
        if forbidden:
            self.events.append({'path': name, 'descriptor': value if isinstance(value, int) else None})
            raise PermissionError('HELD_BODY_PYTHON_OPEN_DENIED')

    def audit(self, event, args):
        if event == 'open' and args:
            self.inspect(args[0])

    def install(self):
        if self._installed:
            raise RuntimeError('Held guard already installed')
        import sys
        def guarded_os_open(path, flags, mode=0o777, *, dir_fd=None):
            self.inspect(path, dir_fd)
            return self._original_os_open(path, flags, mode, dir_fd=dir_fd)
        sys.addaudithook(self.audit)
        os.open = guarded_os_open
        self._installed = True
