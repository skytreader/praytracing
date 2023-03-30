import sys

def _derive_ppm_filename() -> str:
    my_filename: str = sys.argv[0].split("/")[-1]
    sans_extension: str = my_filename.rsplit(".", 1)[0]
    return "/tmp/%s.ppm" % sans_extension
