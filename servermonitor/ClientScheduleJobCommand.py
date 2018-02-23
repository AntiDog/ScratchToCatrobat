from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO


class ClientScheduleJobCommand(ClientCommand):
    def __init__(self, configParams):
        args = {ClientCommand.ArgumentType.JOB_ID : configParams.scractchProjectId}
        ClientCommand.__init__(self, COMMAND_RETRIEVE_INFO, args)
