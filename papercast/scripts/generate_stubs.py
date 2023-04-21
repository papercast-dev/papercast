from pathlib import Path
import subprocess
import warnings
import shutil
import pkg_resources


def find_papercast() -> str:
    package = pkg_resources.get_distribution("papercast")
    return package.location


def move_stubs(output_dir):
    for stub_folder in output_dir.glob("*"):
        if stub_folder.is_dir():
            folder_files = list(stub_folder.glob("**/*.pyi"))
            if len(folder_files) == 0:
                warnings.warn(
                    f"Expected one file in {stub_folder}, found {folder_files}, skipping"
                )
                continue

            if not len(folder_files) == 1:
                raise ValueError(
                    f"Expected one file in {stub_folder}, found {folder_files}"
                )

            file = folder_files[0]

            file.rename(output_dir / f"{stub_folder.name}.pyi")

            shutil.rmtree(stub_folder)

            outpath = output_dir / "__init__.pyi"

            content = f"from .{stub_folder.name} import *"

            if not (outpath).exists():
                outpath.write_text(content)

            elif content in outpath.read_text():
                print(
                    f"Skipping {stub_folder.name} import in __init__.pyi, already exists"
                )

            else:
                outpath.write_text(outpath.read_text() + "\n" + content)


def generate_stubs():
    papercast_dir = find_papercast() + "/papercast"
    packages = [
        package
        for package in pkg_resources.working_set
        if "papercast-" in package.project_name
    ]
    for package in packages:
        for module_name in package.get_metadata_lines("top_level.txt"):
            for k, v in package.get_entry_map().items():
                if module_name in str(v):
                    plugin_type = k.split(".")[-1]
                    if plugin_type == "types":
                        plugin_type_output = "types_plugins"
                    else:
                        plugin_type_output = plugin_type
                    module_name_for_stubs = f"{module_name}.{plugin_type}"
                    print(f"Generating stubs for {module_name_for_stubs}...")
                    output_dir = Path(papercast_dir) / f"{plugin_type_output}/stubs"
                    cmd = [
                        "stubgen",
                        "-o",
                        str(output_dir / f"{module_name}_{plugin_type}"),
                        "--export-less",
                        "-m",
                        module_name_for_stubs,
                    ]
                    print(" ".join(cmd))
                    subprocess.run(
                        cmd,
                        check=True,
                    )

    for plugin_type in ["publishers", "subscribers", "processors", "types_plugins"]:
        print(f"Moving stubs for {plugin_type}...")
        output_dir = Path(papercast_dir) / f"{plugin_type}/stubs"
        move_stubs(output_dir)
