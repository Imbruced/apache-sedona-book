from prefect.filesystems import LocalFileSystem

LocalFileSystem(basepath="/opt/prefect/data").save("sedona-block", overwrite=True)