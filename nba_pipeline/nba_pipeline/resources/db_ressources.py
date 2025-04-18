from dagster import ConfigurableResource
import psycopg2

class PostgresResource(ConfigurableResource):
    host: str
    port: int
    user: str
    password: str
    dbname: str

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.dbname
        )
