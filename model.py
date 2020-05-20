from gateway import Gateway


class Model:
    gateway = Gateway()

    def __init__(self, server_id, name, number):
        self.name = name
        self.number = number
        self.server_id = server_id

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
