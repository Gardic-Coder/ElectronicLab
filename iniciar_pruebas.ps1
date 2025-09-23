# Ruta al ejecutable de LocalXpose
$localxpose = "D:\LocalXpose\loclx.exe"  # Ajusta esta ruta si lo tienes en otro lugar

# Ruta al proyecto Django
$proyecto = "D:\VSC\ElectronicLab"  # Ajusta según tu estructura
$proyectoweb = "D:\VSC\ElectronicLab\ElectronicLabWeb"  # Ajusta según tu estructura

# Activar entorno virtual (si usas uno)
Set-Location $proyecto
.\ElectronicLab\Scripts\activate  # O el nombre de tu entorno

# Iniciar servidor Django en segundo plano
Set-Location $proyectoweb
Start-Process powershell -ArgumentList "python manage.py runserver" -WorkingDirectory $proyectoweb

Start-Sleep -Seconds 5  # Espera a que el servidor arranque

# Abrir túnel con LocalXpose
Start-Process powershell -ArgumentList "$localxpose tunnel http --to 127.0.0.1:8000"