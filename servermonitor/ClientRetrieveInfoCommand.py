import json

from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO
from scratchtocatrobat.tools.logger import log
from websocketserver.protocol.message.base.base_message import BaseMessage

class ClientRetrieveInfoCommand(ClientCommand):
    def __init__(self):
        ClientCommand.__init__(self, COMMAND_RETRIEVE_INFO, {})

    def execute(self, ws):
        data = self.to_json().encode('utf8')
        log.debug("RetrieveInfoCommand Sending {}".format(data))
        ws.send(data)
        result = ws.recv()
        log.debug("RetrieveInfoCommand Response Received {}".format(result))

        if ClientRetrieveInfoCommand.verify_response(result):
            log.info("Retrieve Info successful")
        else:
            log.error("Bad retrieve Info response")
        return

    def verify_response( encoded_response):
        response = json.JSONDecoder('utf8').decode(encoded_response)
        # TODO: more checks(if necessary) & make sure it is finished
        return response["type"] == BaseMessage.MessageType.INFO
    verify_response = staticmethod(verify_response)