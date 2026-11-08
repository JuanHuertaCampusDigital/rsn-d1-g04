-- Roles de grupo sin contraseña. Crear usuarios individuales por el canal del centro.
DO $$ BEGIN
 IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='dat_lector') THEN CREATE ROLE dat_lector NOLOGIN; END IF;
 IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='dat_operador') THEN CREATE ROLE dat_operador NOLOGIN; END IF;
END $$;
REVOKE ALL ON SCHEMA planta FROM PUBLIC;
GRANT USAGE ON SCHEMA planta TO dat_lector,dat_operador;
GRANT SELECT ON ALL TABLES IN SCHEMA planta TO dat_lector;
GRANT SELECT,INSERT,UPDATE ON ALL TABLES IN SCHEMA planta TO dat_operador;
GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA planta TO dat_operador;
-- Permite al creador ensayar SET ROLE; no se usa el administrador como cuenta de aplicación.
GRANT dat_lector,dat_operador TO CURRENT_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA planta GRANT SELECT ON TABLES TO dat_lector;
ALTER DEFAULT PRIVILEGES IN SCHEMA planta GRANT SELECT,INSERT,UPDATE ON TABLES TO dat_operador;
ALTER DEFAULT PRIVILEGES IN SCHEMA planta GRANT USAGE,SELECT ON SEQUENCES TO dat_operador;
