"""Apply OS resource limits in a single-threaded child, then exec the scraper."""

import os
import resource
import sys


def main() -> None:
    if len(sys.argv) < 5:
        raise SystemExit(64)
    file_limit = int(sys.argv[1])
    memory_limit = int(sys.argv[2])
    cpu_limit = int(sys.argv[3])
    command = sys.argv[4:]
    resource.setrlimit(resource.RLIMIT_FSIZE, (file_limit, file_limit))
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
    os.execvpe(command[0], command, os.environ)


if __name__ == "__main__":
    main()
