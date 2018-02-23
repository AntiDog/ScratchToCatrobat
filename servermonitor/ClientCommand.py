import json
from scratchtocatrobat.tools.logger import log


class ClientCommand(object):
    class ArgumentType(object):
        CLIENT_ID = "clientID"
        JOB_ID    = "jobID"
        FORCE     = "force"
        VERBOSE   = "verbose"

    def __init__(self, command, arguments):
        self.cmd = command
        self.args = arguments
    cmd = None
    args = None

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def execute(self, ws):
        ws.send(self.toJSON().encode('utf8'))
        result = ws.recv()
        log.info("Response Received {}".format(result))
