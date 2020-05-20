from .db import session_scope, Server
from datetime import datetime, timedelta


class Gateway:
    def get_all_servers(self):
        with session_scope() as session:
            raw_servers = session.query(Server)

            raw_servers_dict = []

            if raw_servers:
                for raw_server in raw_servers:
                    raw_dict = raw_server.__dict__
                    del raw_dict['_sa_instance_state']

                    raw_servers_dict.append(raw_dict)
            return raw_servers_dict

    def fill_db(self, servers):
        with session_scope() as session:
            for key in servers.keys():
                server = session.query(Server).filter(Server.name == key).first()

                if server:
                    server.number = servers[key]
                else:
                    session.add(Server(name=key, number=servers[key], added=datetime.now()))

    def get_analytics(self, hour=False, day=False, month=False):
        if hour:
            comparator = datetime.now() - timedelta(hours=1)
        elif day:
            comparator = datetime.now() - timedelta(days=1)
        else:
            comparator = datetime.now() - timedelta(days=30)
        with session_scope() as session:
            raw_servers = session.query(Server).filter(Server.added >= comparator).all()

            raw_servers_dict = []

            if raw_servers:
                for raw_server in raw_servers:
                    raw_dict = raw_server.__dict__
                    del raw_dict['_sa_instance_state']

                    raw_servers_dict.append(raw_dict)
            return raw_servers_dict
