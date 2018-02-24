import json

from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO
from scratchtocatrobat.tools.logger import log
from websocketserver.protocol.message.base.base_message import BaseMessage


class ClientScheduleJobCommand(ClientCommand):
    def __init__(self, config_params):
        args = {ClientCommand.ArgumentType.JOB_ID: config_params.scractchprojectid}
        ClientCommand.__init__(self, COMMAND_RETRIEVE_INFO, args)

    def execute(self, ws):
        data = self.to_json().encode('utf8')
        log.debug("ScheduleJobCommand Sending {}".format(data))
        ws.send(data)
        response = ws.recv()
        log.debug("ScheduleJobCommand Response Received {}".format(response))
        if ClientScheduleJobCommand.verify_response(response):
            log.info("ScheduleJobCommand successful")
        else:
            log.error("Bad ScheduleJobCommand response")


    def verify_response( encoded_response):
        response = json.JSONDecoder('utf8').decode(encoded_response)
        return response["type"] == BaseMessage.MessageType.INFO
    verify_response = staticmethod(verify_response)
