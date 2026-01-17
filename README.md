# Odoo-Developer-Foundation
## 📚 Enlaces Importantes

### Odoo
- **Apps Oficiales:** https://apps.odoo.com/apps
- **Repositorio Odoo 17 (core):** https://github.com/odoo/odoo/tree/17.0
- **Documentación Odoo 17 (ES):** https://www.odoo.com/documentation/17.0/es/administration/odoo_sh/first_module.html

### Docker + Odoo
- **Imagen oficial Odoo (Docker Hub):** https://hub.docker.com/_/odoo/
- **Repositorio Docker oficial Odoo 17:** https://github.com/odoo/docker/tree/cee8710442112aad57f34f797459df1ab1d5ef6a/17.0
- **Instalación Docker Engine en Debian:** https://docs.docker.com/engine/install/debian/

### Repositorios Propios
- **Odoo Developer Foundation:** https://github.com/AlexFlyer/Odoo-Developer-Foundation

### Herramientas
- **Extensión Chrome – Odoo Debug:** https://chromewebstore.google.com/detail/odoo-debug/hmdmhilocobgohohpdpolmibjklfgkbi

---

## 🧠 Comandos Docker Estandarizados

### Levantamiento
```bash
docker compose up -d
```

### Estado y Visibilidad
```bash
docker ps
docker ps --all
```

### Logs
```bash
docker compose logs -f <container_name>
```

### Control de Contenedores
```bash
docker stop <container_name>
docker start <container_name>
docker restart <container_name>
docker attach <container_name>
```

### Permisos (host)
```bash
chown -R 101:101 data/
```
