from app.libs.execute_command import execute_ssh_command
from fastapi import HTTPException

def get_server_info(host: str, username: str, password: str, port: int = 55220):
    # Comandos para obtener información del sistema
    commands = {
        "cpu": "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'",
        "memory": "free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2 }'",
        "disks": "df -h | awk 'NR>1 {print $1, $2, $3, $4, $5, $6}'",  # Obtener detalles de todos los discos
        "top_processes": "ps aux --sort=-%cpu | head -n 5",
        "failed_services": "systemctl --failed --no-pager | grep -E '(failed|inactive)'",
        "uptime": "uptime -p",
        "network": "ip -s link",
        "connections": "netstat -tuln",
        "swap": "free -m | grep Swap | awk '{print $3 \"/\" $2}'",
        "errors": "journalctl -p 3 -b",
    }

    def safe_execute(command_key):
        """Ejecutar un comando de forma segura y manejar errores individuales."""
        try:
            return execute_ssh_command(host, username, password, commands[command_key], port)
        except Exception as cmd_error:
            return f"Error ejecutando '{command_key}': {str(cmd_error)}"

    try:
        # Ejecutar comandos y manejar resultados
        cpu_usage = safe_execute("cpu")
        memory_usage = safe_execute("memory")
        disks_info = safe_execute("disks")
        top_processes = safe_execute("top_processes")
        failed_services = safe_execute("failed_services")
        uptime = safe_execute("uptime")
        network = safe_execute("network")
        connections = safe_execute("connections")
        swap_usage = safe_execute("swap")
        errors = safe_execute("errors")

        # Procesar información de discos y filtrar solo los importantes
        disk_list = [
            {
                "filesystem": line.split()[0],
                "size": line.split()[1],
                "used": line.split()[2],
                "available": line.split()[3],
                "usage": line.split()[4],
                "mount_point": line.split()[5]
            }
            for line in disks_info.splitlines()
            if not any(skip in line.split()[0] for skip in ["tmpfs", "overlay", "loop"])  # Excluir discos temporales
        ]

        # Ordenar los discos por uso descendente (más utilizados primero)
        disk_list = sorted(disk_list, key=lambda d: int(d["usage"].strip('%')), reverse=True)

        # Seleccionar los más importantes (e.g., los tres más usados)
        important_disks = disk_list[:3]

        # Formatear resultados
        return {
            "cpu_usage": f"{cpu_usage.strip()}%",  # Asegurar que los valores sean limpios
            "memory_usage": f"{memory_usage.strip()}%",
            "important_disks": important_disks,
            "top_processes": top_processes.splitlines(),
            "failed_services": failed_services.splitlines(),
            "uptime": uptime.strip(),
            "network": network.splitlines(),
            "connections": connections.splitlines(),
            "swap_usage": swap_usage.strip(),
            "errors": errors.splitlines(),
        }
    except Exception as e:
        # Manejar errores generales con detalles para depuración
        raise HTTPException(status_code=500, detail=f"Error al obtener información del servidor: {str(e)}")