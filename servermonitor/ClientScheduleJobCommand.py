from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO
from scratchtocatrobat.tools.logger import log


class ClientScheduleJobCommand(ClientCommand):
    def __init__(self, config_params):
        args = {ClientCommand.ArgumentType.JOB_ID: config_params.scractchProjectId}
        ClientCommand.__init__(self, COMMAND_RETRIEVE_INFO, args)

    def execute(self, ws):
        data = self.to_json().encode('utf8')
        log.info("ScheduleJobCommand Sending {}".format(data))
        ws.send(data)
        result = ws.recv()
        log.info("ScheduleJobCommand Response Received {}".format(result))
        return result
