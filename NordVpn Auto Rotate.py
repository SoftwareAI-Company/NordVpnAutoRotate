import subprocess

try:
    subprocess.run(["Dependenc/Python/pythonw", "Dependenc/update.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar o script de atualização: {e}")


