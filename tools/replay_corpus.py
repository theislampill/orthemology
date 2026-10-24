"""Named adapter; original frozen runner executes only in a verified reconstructed context."""
import sys
from replay import main

if __name__ == "__main__":
    raise SystemExit(main(['case', *sys.argv[1:]]))
