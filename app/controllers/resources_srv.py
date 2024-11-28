import paramiko
from fastapi import HTTPException

# Función genérica para ejecutar comandos remotos
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

def get_server_info(host: str, username: str, password: str, port: int = 55220):
    try:
        # Comandos para obtener información del sistema
        commands = {
            "cpu": "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'",
            "memory": "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'",
            "storage": "df -h --total | grep 'total' | awk '{print $5}'",
            "top_processes": "ps aux --sort=-%cpu | head -n 5",
            "failed_services": "systemctl --failed --no-pager | grep -E '(failed|inactive)'"
        }

        # Ejecutar comandos con el puerto correcto
        cpu_usage = execute_ssh_command(host, username, password, commands["cpu"], port)
        memory_usage = execute_ssh_command(host, username, password, commands["memory"], port)
        storage_usage = execute_ssh_command(host, username, password, commands["storage"], port)
        top_processes = execute_ssh_command(host, username, password, commands["top_processes"], port)
        failed_services = execute_ssh_command(host, username, password, commands["failed_services"], port)

        return {
            "cpu_usage": f"{cpu_usage}%",
            "memory_usage": memory_usage,
            "storage_usage": storage_usage,
            "top_processes": top_processes.splitlines(),
            "failed_services": failed_services.splitlines()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
