from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthenticator
from service.settings import config

def get_creds(self):
    return {'username': f"{config.DB_USER}", 'password': f"{config.DB_PASS}"}

def get_session():
    cluster = Cluster([f"{config.DB_HOST}"], auth_provider=get_creds)
    session = cluster.connect()
    session.execute(f"create keyspace {config.KEYSPACE} with replication={ 'class': 'SimpleStrategy', 'replication_factor' : 3};")
    return session