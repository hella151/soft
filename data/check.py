import asyncio
import subprocess
from typing import Optional
from supabase import create_client, Client
from data.log import logger
import platform
import socket
import datetime

url = "https://lnrasyfhnygucfiduwbt.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxucmFzeWZobnlndWNmaWR1d2J0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYwMjM3OTksImV4cCI6MjA3MTU5OTc5OX0.7biADifrQhCq5wf_HgHbVtpFLAZ-D50dBTyGfA0lUSk"
supabase: Client = create_client(url, key)

active_task: Optional[asyncio.Task] = None
is_running: bool = False
chats_vz = [-1002029765485]

def get_motherboard_info():
    system = platform.system()
    if system == "Windows":
        try:
            import wmi
            c = wmi.WMI()
            for board in c.Win32_BaseBoard():
                return {'serial': board.SerialNumber}
        except ImportError:
            return {'serial': 'N/A'}
    elif system == "Linux":
        try:
            result = subprocess.run(['sudo', 'dmidecode', '-t', 'baseboard'],
                                    capture_output=True, text=True, timeout=10)
            output = result.stdout
            serial = 'N/A'
            for line in output.split('\n'):
                if 'Serial Number:' in line:
                    serial = line.split(':')[1].strip()
                    break
            return {'serial': serial}
        except:
            return {'serial': 'N/A'}
    else:
        return {'serial': 'N/A'}


def licensia_check():
    try:
        info = get_motherboard_info()
        serial = str(info.get('serial', 'N/A'))
        ip_address = socket.gethostbyname(socket.gethostname())

        response = supabase.table("dino").select("*").eq("serial", serial).execute()

        if not response.data:
            stopped_at_utc = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
            supabase.table("dino").insert({
                "serial": serial,
                "ip": ip_address,
                "stopped_at": stopped_at_utc.isoformat()
            }).execute()
            
            return "Устройство зарегистрировано"
        else:
            response = supabase.table("dino").select("*").eq("serial", serial).eq("approve", True).execute()
            if not response.data:

                return "Ждите подтверждения"
            else:
                response = supabase.table("dino").select("stopped_at").eq("serial", serial).execute()
                if datetime.datetime.now(datetime.timezone.utc) >= datetime.datetime.fromisoformat(
                        response.data[0].get("stopped_at")):

                    return "Продлите подписку"
                else:
                    return True

    except Exception as e:
        logger.warning(f"Ошибка при проверке лицензии: {e}")
        logger.debug("Запуск приложения без проверки лицензии")
        return True
