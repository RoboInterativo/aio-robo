CREATE USER robo WITH PASSWORD 'Sample';
DROP DATABASE IF EXISTS robo;
CREATE DATABASE robo;
ALTER DATABASE robo OWNER TO robo;
GRANT ALL PRIVILEGES ON DATABASE robo TO robo;
