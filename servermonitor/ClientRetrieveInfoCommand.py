import json

import time

from ClientCommand import ClientCommand
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO
from scratchtocatrobat.tools.logger import log
from websocketserver.protocol.message.base.base_message import BaseMessage
from websocketserver.protocol.message.job import job_message

class ClientRetrieveInfoCommand(ClientCommand):
    def __init__(self, config_params):
        args = {ClientCommand.ArgumentType.JOB_ID: int(config_params.scractchprojectid)}
        ClientCommand.__init__(self, COMMAND_RETRIEVE_INFO, args)

    def execute(self, ws):
        while(True):
            data = self.to_json().encode('utf8')
            log.debug("RetrieveInfoCommand Sending {}".format(data))
            ws.send(data)
            result = ws.recv()

            log.info("RetrieveInfoCommand Response Received {}".format(result))
            json_result = json.JSONDecoder('utf8').decode(result)
            if self.isDone(json_result):
                break
            time.sleep(1)
        if ClientRetrieveInfoCommand.verify_response(json_result):
            log.info("Retrieve Info successful")
        else:
            log.error("Bad retrieve Info response")
        return json.JSONDecoder('utf8').decode(result)

    @staticmethod
    def verify_response( json_result):
        return json_result["type"] == BaseMessage.MessageType.INFO

        # TODO: more checks(if necessary) & make sure it is finished

    @staticmethod
    def get_download_url(response, job_id):

        print response
        if response["type"] == job_message.JobMessage.MessageType.JOB_CONVERSION_FINISHED:
            return response["data"]["url"]
        for jobinfo in response["data"]["jobsInfo"]:
            if jobinfo["jobID"] == job_id:
                url = jobinfo["downloadURL"]
                return url

    def isDone(self, json_result):
        if json_result["type"] == job_message.JobMessage.MessageType.JOB_PROGRESS:
            jobinfo = json_result["data"]
            if jobinfo["jobID"] == self.args[ClientCommand.ArgumentType.JOB_ID]:
                log.info("progress: " + str(jobinfo["progress"]) + "%")
            return False

        if json_result["type"] == job_message.JobMessage.MessageType.JOB_RUNNING:
            return False
        if json_result["type"] == job_message.JobMessage.MessageType.JOB_CONVERSION_FINISHED:
            return True
        log.error("unexpected message type: "+ str(json_result["type"]))
        raise NotImplemented
