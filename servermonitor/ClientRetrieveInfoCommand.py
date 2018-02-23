from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO
from scratchtocatrobat.tools.logger import log


class ClientRetrieveInfoCommand(ClientCommand):
    def __init__(self):
        ClientCommand.__init__(self, COMMAND_RETRIEVE_INFO, {})

    def execute(self, ws):
        data = self.to_json().encode('utf8')
        log.info("RetrieveInfoCommand Sending {}".format(data))
        ws.send(data)
        result = ws.recv()
        log.info("RetrieveInfoCommand Response Received {}".format(result))
        return result
