from pysrc.load_sidecar import get_lib_path
from pysrc.image2icon import Image2IconLib
from pysrc.gui import ConverterGui


def run_gui():
    get_lib = get_lib_path(is_static=False)
    lib = Image2IconLib(get_lib)
    app = ConverterGui(lib)
    app.run()


if __name__ == "__main__":
    run_gui()
