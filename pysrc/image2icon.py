import ctypes
import os
from pysrc.load_sidecar import get_lib_path


class Image2IconLib:
    FORMAT_ICNS = 0
    FORMAT_ICO = 1

    def __init__(self, get_lib: get_lib_path):
        lib_path = get_lib
        self.image2icon_lib = ctypes.CDLL(lib_path)

        self.image2icon_lib.ffi_create_iconset.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
        ]
        self.image2icon_lib.ffi_create_iconset.restype = ctypes.c_int

        self.image2icon_lib.ffi_convert_iconset.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        self.image2icon_lib.ffi_convert_iconset.restype = ctypes.c_int

        self.image2icon_lib.ffi_convert_image.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        self.image2icon_lib.ffi_convert_image.restype = ctypes.c_int

    def convert_image(self, input_path: str, output_path: str, format: int) -> int:
        result = self.image2icon_lib.ffi_convert_image(
            input_path.encode("utf-8"),
            output_path.encode("utf-8"),
            format,
        )
        return result

    def convert_iconset(self, folder_path: str, output_path: str, format: int) -> int:
        result = self.image2icon_lib.ffi_convert_iconset(
            folder_path.encode("utf-8"),
            output_path.encode("utf-8"),
            format,
        )
        return result

    def create_iconset(self, input_path: str, output_dir_path: str) -> int:
        output_dir_with_iconset = os.path.join(output_dir_path, "iconset")
        if not os.path.exists(output_dir_with_iconset):
            os.makedirs(output_dir_with_iconset)

        result = self.image2icon_lib.ffi_create_iconset(
            input_path.encode("utf-8"),
            output_dir_with_iconset.encode("utf-8"),
        )
        return result
