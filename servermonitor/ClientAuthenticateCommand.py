from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_AUTHENTICATE


class ClientAuthenticateCommand(ClientCommand):
    def __init__(self, configParams):
        args = {ClientCommand.ArgumentType.CLIENT_ID : int(configParams.clientId)}
        authenticationCommand = ClientCommand(COMMAND_AUTHENTICATE, args)
        ClientCommand.__init__(self, authenticationCommand, args)
