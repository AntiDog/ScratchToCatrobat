from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_AUTHENTICATE
from scratchtocatrobat.tools.logger import log


class ClientAuthenticateCommand(ClientCommand):
    def __init__(self, config_params):
        args = {ClientCommand.ArgumentType.CLIENT_ID: int(config_params.clientId)}
        ClientCommand.__init__(self, COMMAND_AUTHENTICATE, args)

    def execute(self, ws):
        data = self.to_json().encode('utf8')
        log.info("AuthenticateCommand Sending {}".format(data))
        ws.send(data)
        result = ws.recv()
        log.info("AuthenticateCommand Response Received {}".format(result))
        return result