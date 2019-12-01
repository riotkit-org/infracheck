
import psycopg2
import psycopg2.extras


class BasePostgreSQL:
    conn = None

    def __init__(self, host: str, dbname: str, port: int, username: str, password: str, connect_timeout: int):
        self.conn = psycopg2.connect(
            database=dbname,
            host=host,
            password=password,
            user=username,
            port=port,
            connect_timeout=connect_timeout
        )

    @staticmethod
    def create_instance(cls):
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            dbname=os.getenv('DB_NAME', ''),
            username=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            connect_timeout=int(os.getenv('DB_CONNECT_TIMEOUT', 10))
        )

    def query(self, qstr: str):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(qstr)

        return cur.fetchall()

    def validate_replication_row_exists(self, sql: str, expected_status: str, expected_user: str):
        out = self.query(sql)
        active_replications = len(out)
        has_no_access_to_at_least_one_row = False

        for row in out:
            status, conn_info = row

            if conn_info is None:
                has_no_access_to_at_least_one_row = True
                continue

            if status != expected_status and expected_user in conn_info:
                return False, 'Expected "%s" status for conn_info="%s", got "%s"' % (
                    expected_status, conn_info, status
                )

            if status == expected_status and expected_user in conn_info:
                return True, "%i replications active. The replication for '%s' user looks healthy" % (
                    active_replications, expected_user
                )

        if active_replications == 0:
            if has_no_access_to_at_least_one_row:
                return False, "no replications active: possibly connection user has no permissions to view this data"

            return False, "no replications active"

        return False, "%i replications active, but none found for user '%s'" % (active_replications, expected_user)
