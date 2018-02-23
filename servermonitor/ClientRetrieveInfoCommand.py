from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO


class ClientRetrieveInfoCommand(ClientCommand):
    def __init__(self):
        ClientCommand.__init__(self, COMMAND_RETRIEVE_INFO, {})
