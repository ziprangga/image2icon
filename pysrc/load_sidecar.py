import os
import sys
import platform


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def get_lib_path(is_static=False):
    system = platform.system()
    ext = {
        "Darwin": ".dylib",
        "Linux": ".so",
        "Windows": ".dll",
    }.get(system)

    if not ext:
        raise RuntimeError(f"Unsupported platform: {system}")

    if is_static:
        ext = ".a"

    candidates = {}

    if getattr(sys, "frozen", False):
        root = resource_path(os.path.join("image2icon", f"libimage2icon{ext}"))
        if os.path.exists(root):
            candidates["bundled"] = root
    else:
        root = resource_path(os.path.join("build", "rust_target"))
        for build_type in ("release", "debug"):
            for variant in ("universal2", "aarch64", "x86_64"):
                path = os.path.join(root, build_type, variant, f"libimage2icon{ext}")
                if os.path.exists(path):
                    candidates[variant] = path
                    break

    if not candidates:
        raise FileNotFoundError(
            "Could not locate compiled Rust library in expected paths."
        )

    if len(candidates) == 1:
        return next(iter(candidates.values()))

    if "universal2" in candidates:
        return candidates["universal2"]

    raise RuntimeError(
        f"Multiple Rust builds found ({', '.join(candidates)}), and no universal2 fallback."
    )
