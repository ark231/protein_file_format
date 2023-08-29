import shutil
import os
from pathlib import Path
import sys
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

# https://stackoverflow.com/questions/27843481/python-project-using-protocol-buffers-deployment-issues

# Find the Protocol Compiler.
if "PROTOC" in os.environ and Path(os.environ["PROTOC"]).exists():
    protoc = os.environ["PROTOC"]
else:
    protoc = shutil.which("protoc")


def generate_proto(source):
    """Invokes the Protocol Compiler to generate a _pb2.py from the given
    .proto file.    Does nothing if the output already exists and is newer than
    the input."""

    output = Path(source.replace(".proto", "_pb2.py"))
    source = Path(source)

    if not output.exists() or (source.exists() and source.stat().st_mtime > output.stat().st_mtime):
        print(f"Generating {output}...")

        if not source.exists():
            print(f"Can't find required file: {source}\n", file=sys.stderr)
            sys.exit(-1)

        if protoc is None:
            print(
                "Protocol buffers compiler 'protoc' not installed or not found.\n",
                file=sys.stderr,
            )
            sys.exit(-1)

        protoc_command = [protoc, "-I.", "--python_out=.", source]
        if subprocess.call(protoc_command) != 0:
            sys.exit(-1)


# List of all .proto files
proto_src = ["src/protein/protein.proto"]


class build_py(_build_py):
    def run(self):
        for f in proto_src:
            generate_proto(f)
        _build_py.run(self)


setup(name="protein_file_format", version="0.1.0", cmdclass={"build_py": build_py}, install_requires=["protobuf"])
