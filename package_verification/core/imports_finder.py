import re
from pathlib import Path


class ImportsFinder:
    def __init__(self) -> None:
        pass

    def get_imports(self, file):
        with open(file, "r") as f:
            lines = f.readlines()
            imports = []
            for line in lines:
                if re.match(r"import ", line):
                    module = line.split()[1]
                    imports.append(module)
                elif re.match(r"from ", line):
                    module = line.split()[1]
                    if "." in module:
                        module = module.split(".")[-1]
                    imports.append(module)

        return imports

    def get_all_imports(self, root_path: Path):
        imports = []
        for file in root_path.rglob("*.py"):
            file_imports = self.get_imports(file)
            for import_ in file_imports:
                if import_ not in imports:
                    imports.append(import_)

        python_imports = self._is_import_a_file(imports, root_path)
        return python_imports

    def _is_import_a_file(self, imports: list, root_path: Path):
        file_names = [file.stem for file in root_path.rglob("*.py")]
        python_imports = []
        for import_ in imports:
            if import_ not in file_names:
                python_imports.append(import_)
        return python_imports
