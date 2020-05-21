from .gateway import Gateway


class Model:
    gateway = Gateway()

    def __init__(self, server_id, name, number, added):
        self.server_id = server_id
        self.name = name
        self.number = number
        self.added = added

    @classmethod
    def serialize_model(cls):
        data = [str(cls.server_id), cls.name, str(cls.number), str(cls.added)]
        return data

    @classmethod
    def see_db(cls):
        raw_servers = cls.gateway.get_all_servers()

        servers = []
        for raw_server in raw_servers:
            server_model = cls(**raw_server)
            servers.append(server_model)

        return servers

    @classmethod
    def fill_db(cls, servers):
        cls.gateway.fill_db(servers)

    @classmethod
    def get_analytics(cls, hour=False, day=False, month=False):
        raw_servers = cls.gateway.get_analytics(hour=hour, day=day, month=month)

        servers = []
        for raw_server in raw_servers:
            server_model = cls(**raw_server)
            servers.append(server_model)
        return servers
