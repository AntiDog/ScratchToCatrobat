import httplib
import json
import traceback
import os

import websocket
import zipfile
import logging
from SmtpUtility import SmtpUtility

from scratchtocatrobat.tools.logger import setup_logging
from scratchtocatrobat.tools.logger import log
from scratchtocatrobat.tools.helpers import _setup_configuration
from ClientRetrieveInfoCommand import ClientRetrieveInfoCommand
from ClientAuthenticateCommand import ClientAuthenticateCommand
from ClientScheduleJobCommand import ClientScheduleJobCommand

configpath = "config/default.ini"
smtp = None
class ConfigFileParams:
    def __init__(self): pass
    class Mailinfo(object):
        smtp_host = None
        smtp_port = None
        smtp_from = None
        smtp_pwd = None
        smtp_send_to = None
        def __init__(self): pass

        def to_json(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                              sort_keys=True, indent=4)

    conversionurl = None
    clientid = None
    scractchprojectid = None
    webapirul = None
    code_xml_hash = None
    mailinfo = Mailinfo()


def readConfig():
    global configpath
    config = _setup_configuration(configpath)
    config_params = ConfigFileParams()
    config_params.webapirul = config.config_parser.get("Scratch2CatrobatConverter", "webapiurl")
    config_params.conversionurl = config.config_parser.get("Scratch2CatrobatConverter", "conversionurl")
    config_params.clientid = config.config_parser.getint("Scratch2CatrobatConverter", "clientid")
    config_params.scractchprojectid = config.config_parser.getint("Scratch2CatrobatConverter", "scratchprojectid")
    config_params.downloadurl = config.config_parser.get("Scratch2CatrobatConverter", "downloadurl")
    config_params.code_xml_hash = config.config_parser.getint("Scratch2CatrobatConverter", "code_xml_hash")

    config_params.mailinfo.smtp_host = config.config_parser.get("MAIL", "smtp_host")
    config_params.mailinfo.smtp_from = config.config_parser.get("MAIL", "smtp_from")
    config_params.mailinfo.smtp_port = config.config_parser.get("MAIL", "smtp_port")
    config_params.mailinfo.smtp_pwd = config.config_parser.get("MAIL", "smtp_pwd")
    config_params.mailinfo.smtp_send_to = config.config_parser.get("MAIL", "smtp_send_to")[1:-1].split(",")

    return config_params

def main():
    setup_logging()
    _logger = logging.getLogger('websocket')
    _logger.addHandler(logging.NullHandler())
    config_params = readConfig()
    failure = False
    failure |= test_web_api(config_params.webapirul)
    failure |= test_conversion(config_params)
    #TODO: untested! Test this please!
    if failure | True:
        SmtpUtility.send(config_params.mailinfo, "Everything is OK. Was just joking.")


def test_web_api(webapirul):
    conn = None
    failed = True
    try:
        conn = httplib.HTTPConnection(webapirul)
        conn.request("GET", "/")
        r1 = conn.getresponse()
        status = r1.status
        if status == 200:
            log.info("WebApi is up and running")
            failed = False
        else:
            log.error("WebApi Http status not OK, status is:" + str(status))
    except:
        log.error("Could not connect to WebApi:\n" + traceback.format_exc())
    try:
        conn.close()
    except AttributeError:
        pass
    return failed


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
        failed = False
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
            failed = True
        os.remove("tmp/project.zip")
        os.remove("tmp/code.xml")
        return failed

    ws = None
    try:
        ws = websocket.create_connection(config_params.conversionurl)
        authenticate()
        start_conversion()
        result = retrieve_info()
        download_path = ClientRetrieveInfoCommand.get_download_url(result, config_params.scractchprojectid)
        #todo there is something worng here i guess? hash isn't always right :(
        ziped_project = download_project()
        failed = validate_ziped_project()
        #TODO check without force flag if cash works

    except:
        log.error("Exception while Conversion: " + traceback.format_exc())
        failed = True
    try:
        ws.close()
    except AttributeError:
        pass
    return failed


if __name__ == '__main__':
    main()
