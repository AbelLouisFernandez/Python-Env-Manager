import os
import subprocess


def generate_graph(env_path):
    env_path+="\\Lib\\site-packages"
    try:
        # Step 1: Generate DOT file
        with open("tree.dot", "w") as dot_file:
            subprocess.run(
                ['pipdeptree', '--path', env_path, '--graph-output', 'dot'],
                check=True,
                stdout=dot_file,
                stderr=subprocess.STDOUT
            )

        # Step 2: Convert to PNG using Graphviz
        subprocess.run(
            ['dot', '-Tpng', 'tree.dot', '-o', 'tree.png'],
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"pipdeptree failed:\n{e}")



def list_packages(env_path):
    python_exe = os.path.join(env_path, 'Scripts', 'python.exe')

    if not os.path.exists(python_exe):
        return "python.exe not found in the selected environment."

    try:
        result = subprocess.run(
            [python_exe, '-m', 'pip', 'freeze'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running pip freeze:\n{e.stderr or str(e)}"
    except Exception as ex:
        return f"Unexpected error:\n{str(ex)}"


def find_virtualenvs(root_dirs):
    envs = []
    for root in root_dirs:
        for dirpath, dirnames, filenames in os.walk(root):
            if 'pyvenv.cfg' in filenames:
                envs.append(dirpath)
    return envs