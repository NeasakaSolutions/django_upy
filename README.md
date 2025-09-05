.\entorno\Scripts\activate
npm run dev -- --host

Para activar mysql:
con administrador de tareas detener laragon y mysqld.exe

En powershell verifica que este libre el puerto, no debe de devolver nada:
netstat -ano | findstr 3306

win + r y escribir: services.msc

Busca MySQL80 y le das en iniciar