import setuptools
from setuptools_protobuf import Protobuf

setuptools.setup(
        name="protein_file_format",
        version="0.1.0",
        setup_requires=['setuptools-protobuf'],
        protobufs=[Protobuf('protein.proto')],
)
