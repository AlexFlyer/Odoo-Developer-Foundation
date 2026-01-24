# Odoo-Developer-Foundation
## 📚 Enlaces Importantes

### Odoo
- **Apps Oficiales:** https://apps.odoo.com/apps
- **Repositorio Odoo 17 (core):** https://github.com/odoo/odoo/tree/17.0
- **Documentación Odoo 17 (ES):** https://www.odoo.com/documentation/17.0/es/administration/odoo_sh/first_module.html
- **Documentación Odoo 17 Modelos:** https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/03_basicmodel.html
- **Documentación Odoo 17 Vistas:** https://www.odoo.com/documentation/17.0/es/developer/tutorials/server_framework_101/06_basicviews.html
- **Documentación Odoo 17 Widgets:** https://www.odoo.com/documentation/17.0/applications/studio/fields.html#simple-fields


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

### Entrar a Contenedores
```bash
docker exec -ti <container_name> bash
```
### actualizar Modulo desde BD
```bash
psql -U odoo -d db_name
UPDATE ir_module_module SET state = 'to upgrade' WHERE name = 'module_name';
```
