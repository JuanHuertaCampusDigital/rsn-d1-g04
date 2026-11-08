# Saica DAT · 5162 · 210 h

Caso didáctico ficticio. Solo datos sintéticos. Los comandos no se ejecutan al abrir este kit.

1. Descomprime `kit` y abre el terminal en esa carpeta. Bash/Linux es la ruta de referencia; AWS CLI también funciona en PowerShell, pero no pegues sintaxis Bash en PowerShell. Para SQL usa psql desde el cliente privado preparado por el docente.
2. Usa la cuenta, rol, región y presupuesto del centro. `aws sts get-caller-identity` confirma la identidad; no pegues credenciales en ficheros. Edita y carga scripts/entorno.example.sh; sus marcadores no son valores ya comprobados.
3. Python 3.11 o superior: crea un venv e instala requirements.txt. El centro prepara las dependencias antes de las ventanas; no se presupone Internet desde clientes privados.
4. Ejecuta `python scripts/generar_muestras.py`. El resultado normal tiene 120 eventos válidos. `telemetria_con_errores.csv` añade dos registros deliberadamente inválidos.
5. Revisa cada plantilla y su change set antes de desplegar. Las subredes, grupos de seguridad de clientes, roles de Glue/DataSync y el dominio son entradas del contrato con Redes/docente.
6. Cada servicio cloud, copia, snapshot, clave, log, dirección o transferencia puede tener coste. Los ejemplos de capacidad no prometen Free Tier. Revisa disponibilidad real, cuota y tarifa con fecha.

## Rutas
- infra/: RDS PostgreSQL privado/cifrado, DynamoDB, lake/Glue/Athena y EFS original.
- sql/: esquema sintético PostgreSQL, permisos y pruebas, consultas y comparación de índices.
- scripts/: datos sintéticos, manifiesto SHA-256, ETL, espejo sin borrado y sincronización bidireccional con conflictos.
- glue/: ETL Python shell para muestras S3; lo ejecuta un rol con permisos mínimos facilitado por el docente.
- evidence/: registros y contratos de origen/destino, CE, coste y recuperación.

## Uso de los servicios y límites
RDS y EFS reutilizan la VPC y los clientes de Redes. DynamoDB/S3 son servicios regionales, no servidores dentro de una subred. DataSync realiza transferencias; no es un motor general de resolución de conflictos. El ejercicio bidireccional incluye una política explícita y un diario de hashes.

La práctica offline D22 prepara el procedimiento físico y distingue demostración local de servicio del proveedor. Snowball Edge está restringido a clientes existentes desde el 7/11/2025 según AWS; el centro debe verificar una opción realmente disponible. No se declara DAT-CE5d acreditado por una simple simulación.

## Cierre
Exporta evidencias saneadas antes de retirar recursos. No borres VPC, dominio, roles o destinos compartidos. RDS conserva snapshots al borrar el stack; DynamoDB y los buckets se retienen. Inventaría esos recursos retenidos y programa su retirada autorizada: borrar el stack no significa coste cero.
