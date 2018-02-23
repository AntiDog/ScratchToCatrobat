from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO


class ClientRetrieveInfoCommand(ClientCommand):
    def __init__(self, configParams):
        args = {ClientCommand.ArgumentType.JOB_ID : configParams.scractchProjectId}
        scheduleCommand = ClientCommand(COMMAND_RETRIEVE_INFO, args)
        ClientCommand.__init__(self, scheduleCommand, args)
