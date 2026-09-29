import os
import zipfile

def package_project(zip_filename="InsurMinds_Apolice_360_Projeto_Final.zip"):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, zip_filename)
    artifacts_target = os.path.join(base_dir, "Projeto_Final_Artefatos", zip_filename)

    exclude_dirs = {"node_modules", ".git", "__pycache__", ".pytest_cache", ".venv", "venv"}
    exclude_files = {zip_filename, ".DS_Store"}

    with zipfile.ZipFile(target_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file in exclude_files or file.endswith(".pyc"):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname)

    import shutil
    shutil.copyfile(target_path, artifacts_target)
    print(f"Arquivo ZIP criado com sucesso: {target_path} ({os.path.getsize(target_path) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    package_project()
