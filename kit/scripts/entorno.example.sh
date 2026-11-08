# Copia a entorno.sh, sustituye los valores y carga con source. No guardar secretos.
export AWS_REGION=eu-south-2
export TEAM=g03
export VPC_ID=VPC_REAL
export PRIVATE_A=SUBNET_PRIVADA_A_REAL
export PRIVATE_B=SUBNET_PRIVADA_B_REAL
export APP_SG=SG_CLIENTE_REAL
export DAT_BUCKET=BUCKET_DAT_REAL
export LAKE_BUCKET=BUCKET_LAKE_REAL
export RESULT_BUCKET=BUCKET_RESULTADOS_REAL
export TABLE=TABLA_DYNAMO_REAL
export DB_ID=INSTANCIA_RDS_REAL
export PGHOST=ENDPOINT_RDS_REAL
export PGPORT=5432
export PGDATABASE=saica
export PGUSER=saica_admin
export PGSSLMODE=verify-full
export PGSSLROOTCERT="$PWD/certs/global-bundle.pem"
# La contraseña se introduce mediante psql -W o .pgpass protegido (0600), no en este fichero.
