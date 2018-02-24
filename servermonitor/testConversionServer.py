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
    def __init__(self, conversionurl, clientid, scractchprojectid, webapirul, downloadurl):
        self.conversionurl = conversionurl
        self.clientid = clientid
        self.scractchprojectid = scractchprojectid
        self.webapirul = webapirul
        self.downloadurl = downloadurl
    conversionurl = None
    clientid = None
    scractchprojectid = None
    webapirul = None


def readConfig():
    config = _setup_configuration(configpath)
    webapirul = config.config_parser.get("Scratch2CatrobatConverter", "webapiurl")
    conversionurl = config.config_parser.get("Scratch2CatrobatConverter", "conversionurl")
    clientid = config.config_parser.get("Scratch2CatrobatConverter", "clientid")
    scractchprojectid = config.config_parser.get("Scratch2CatrobatConverter", "scratchprojectid")
    downloadurl = config.config_parser.get("Scratch2CatrobatConverter", "downloadurl")
    return ConfigFileParams(conversionurl, clientid, scractchprojectid, webapirul, downloadurl)


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

def test_conversion(config_params):
    def authenticate():
        command = ClientAuthenticateCommand(config_params)
        command.execute(ws)

    def start_conversion():
        command = ClientScheduleJobCommand(config_params)
        command.execute(ws)

    def retrieve_info():
        command = ClientRetrieveInfoCommand()
        return command.execute(ws)

    def download_project(download_path):
        conn = httplib.HTTPConnection(config_params.downloadurl)
        conn.request("GET", download_path)
        print(config_params.downloadurl+download_path)
        r1 = conn.getresponse()
        status = r1.status
        if status == 200:
            log.info("Download Project Http status OK")
            return r1.read() #TODO: I don't think this works the way i think it does
        else:
            log.error("Download Project Http status not OK, status is:" + str(status))

        pass

    def validate_ziped_project(project):
        shouldbe = 6998348270307054976 #6998348270307054976
        if hash(project) == shouldbe: # hash() doesn't work for some reason
            log.info("Project hash OK")
        else:
            log.error("Project hash unexpected, has was: " + str(hash(project))
                      + " but should be: " + str(shouldbe))

    ws = None
    try:
        ws = websocket.create_connection(config_params.conversionurl)
        authenticate()
        start_conversion()
        result = retrieve_info()
        ziped_project = download_project(result["data"]["jobsInfo"][0]["downloadURL"])
        validate_ziped_project(ziped_project)
        #TODO: ensure validity of project (Not sure how, maybe hash value of the package?)
        ws.close()
    except:
        log.error("Exception while Conversion: " + traceback.format_exc())
    try:
        ws.close()
    except AttributeError:
        pass


if __name__ == '__main__':
    main()
