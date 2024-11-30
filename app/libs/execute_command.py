import paramiko
from fastapi import HTTPException

def execute_ssh_command(host, username, password, command, port=55220):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Agregamos el parámetro 'port=55220' para usar el puerto SSH correcto
        ssh.connect(hostname=host, username=username, password=password, port=port)

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        ssh.close()
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar al servidor: {str(e)}")