import httplib
import traceback
import os
import websocket
import zipfile

from scratchtocatrobat.tools.logger import setup_logging
from scratchtocatrobat.tools.logger import log
from scratchtocatrobat.tools.helpers import _setup_configuration
from ClientRetrieveInfoCommand import ClientRetrieveInfoCommand
from ClientAuthenticateCommand import ClientAuthenticateCommand
from ClientScheduleJobCommand import ClientScheduleJobCommand

configpath = "config/default.ini"
config = None

class ConfigFileParams:
    def __init__(self, conversionurl, clientid, scractchprojectid, webapirul, downloadurl, code_xml_hash):
        self.conversionurl = conversionurl
        self.clientid = int(clientid)
        self.scractchprojectid = int(scractchprojectid)
        self.webapirul = webapirul
        self.downloadurl = downloadurl
        self.code_xml_hash = int(code_xml_hash)
    conversionurl = None
    clientid = None
    scractchprojectid = None
    webapirul = None
    code_xml_hash = None


def readConfig():
    config = _setup_configuration(configpath)
    webapirul = config.config_parser.get("Scratch2CatrobatConverter", "webapiurl")
    conversionurl = config.config_parser.get("Scratch2CatrobatConverter", "conversionurl")
    clientid = config.config_parser.get("Scratch2CatrobatConverter", "clientid")
    scractchprojectid = config.config_parser.get("Scratch2CatrobatConverter", "scratchprojectid")
    downloadurl = config.config_parser.get("Scratch2CatrobatConverter", "downloadurl")
    code_xml_hash = config.config_parser.get("Scratch2CatrobatConverter", "code_xml_hash")
    return ConfigFileParams(conversionurl, clientid, scractchprojectid, webapirul, downloadurl, code_xml_hash)


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
        command = ClientRetrieveInfoCommand(config_params)
        return command.execute(ws)

    def download_project():
        print(config_params.downloadurl + download_path)
        conn = httplib.HTTPConnection(config_params.downloadurl)
        conn.request("GET", download_path)
        r1 = conn.getresponse()
        status = r1.status
        if status == 200:
            log.info("Download Project Http status OK")
            return r1.read()
        else:
            log.error("Download Project Http status not OK, status is:" + str(status))

        pass

    def validate_ziped_project():
        if not os.path.isdir("tmp/"):
            os.makedirs("tmp/")
        file = open("tmp/project.zip","wb")
        file.write(ziped_project)
        file.close()
        myzip = zipfile.ZipFile("tmp/project.zip")
        xml_file_path = myzip.extract("code.xml","tmp/")
        file = open(xml_file_path,"r")
        xml_file_content = file.read()
        file.close()
        if hash(xml_file_content) == config_params.code_xml_hash: # hash() doesn't work for some reason
            log.info("Project hash OK")
        else:
            log.error("Project hash unexpected, has: " + str(hash(xml_file_content))
                      + " but should be: " + str(config_params.code_xml_hash))
        os.remove("tmp/project.zip")
        os.remove("tmp/code.xml")

    ws = None
    try:
        ws = websocket.create_connection(config_params.conversionurl)
        authenticate()
        start_conversion()
        result = retrieve_info()
        download_path = ClientRetrieveInfoCommand.get_download_url(result, config_params.scractchprojectid)
        ziped_project = download_project()
        validate_ziped_project()
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
