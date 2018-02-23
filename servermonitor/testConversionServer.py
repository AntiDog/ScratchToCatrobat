import httplib
import traceback
import websocket

from scratchtocatrobat.tools.logger import setup_logging
from scratchtocatrobat.tools.logger import log
from scratchtocatrobat.tools.helpers import _setup_configuration
from ClientRetrieveInfoCommand import ClientRetrieveInfoCommand
from ClientAuthenticateCommand import ClientAuthenticateCommand
from ClientScheduleJobCommand import ClientScheduleJobCommand

configpath = "config/default.ini"
config = None

class ConfigFileParams:
    def __init__(self, conversionurl, clientId, scractchProjectId, webapirul):
        self.conversionurl = conversionurl
        self.clientId = clientId
        self.scractchProjectId = scractchProjectId
        self.webapirul = webapirul
    conversionurl = None
    clientId = None
    scractchProjectId = None
    webapirul = None

def readConfig():
    config = _setup_configuration(configpath)
    webapirul = config.config_parser.get("Scratch2CatrobatConverter", "webapiurl") #http://scratch2.catrob.at/
    conversionurl = config.config_parser.get("Scratch2CatrobatConverter", "conversionurl") #http://scratch2.catrob.at/convertersocket
    clientId = config.config_parser.get("Scratch2CatrobatConverter", "clientid")
    scractchProjectId = config.config_parser.get("Scratch2CatrobatConverter", "scratchprojectid")
    return ConfigFileParams(conversionurl, clientId, scractchProjectId, webapirul)

def main():
    setup_logging()
    config_params = readConfig()
    test_web_api(config_params.webapirul)
    test_conversion(config_params)


def test_web_api(webapirul):
    conn = None
    try:
        conn = httplib.HTTPConnection(webapirul)
        conn.request("GET", "/")
        r1 = conn.getresponse()
        status = r1.status
        if status == 200:
            log.info("WebApi is up and running")
        else:
            log.error("WebApi Http status not OK, status is:" + str(status))
    except:
        log.error("Could not connect to WebApi:\n" + traceback.format_exc())
    try:
        conn.close()
    except AttributeError:
        pass
    return


def test_conversion(configParams):
    def authenticate():
        log.info("Starting Authentication")
        command = ClientAuthenticateCommand(configParams)
        command.execute(ws)

    def start_conversion():
        log.info("Starting Conversion")
        command = ClientScheduleJobCommand(configParams)
        command.execute(ws)

    def retrieve_info():
        log.info("Starting retrieveInfo")
        command = ClientRetrieveInfoCommand()
        command.execute(ws)

    ws = None
    try:
        ws = websocket.create_connection(configParams.conversionurl)
        authenticate()
        start_conversion()
        retrieve_info()
        ws.close()
    except:
        log.error("Exception while Conversion: "+traceback.format_exc())
    try:
        ws.close()
    except AttributeError:
        pass


if __name__ == '__main__':
    main()
