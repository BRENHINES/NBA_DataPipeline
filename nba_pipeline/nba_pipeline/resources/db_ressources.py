from dagster import ConfigurableResource
import psycopg2

class PostgresResource(ConfigurableResource):
    host: str = "localhost"
    port: int = 5432
    user: str = "nbauser"
    password: str = "nbapass"
    dbname: str = "nba_base"

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.dbname
        )
