import httplib
from scratchtocatrobat.tools.logger import setup_logging
from scratchtocatrobat.tools.logger import log
from scratchtocatrobat.tools.helpers import _setup_configuration
import traceback
import websocket
from websocketserver.protocol.command.command import COMMAND_AUTHENTICATE
from websocketserver.protocol.command.command import COMMAND_RETRIEVE_INFO
from websocketserver.protocol.command.command import COMMAND_SCHEDULE_JOB

configpath = "config/default.ini"

def main():
    config = _setup_configuration(configpath)
    setup_logging()
    webapirul = config.config_parser.get("Scratch2CatrobatConverter", "webapiurl") #http://scratch2.catrob.at/
    testWebApi(webapirul)
    conversionurl = config.config_parser.get("Scratch2CatrobatConverter", "conversionurl") #http://scratch2.catrob.at/convertersocket
    testConversion(conversionurl)


def testWebApi(url):
    conn = None
    try:
        conn = httplib.HTTPConnection(url)
        conn.request("GET","/")
        r1 = conn.getresponse()
        status = r1.status
        if status == 200:
            log.info("WebApi is up and running")
        else:
            log.error("WebApi Http status not OK, status is:" + str(status))
    except:
        log.error("Could not connect to WebApi:\n" + traceback.format_exc())
    finally:
        try:
           conn.close()
        except:
            pass
    return


def testConversion(conversionurl):
    ws = websocket.WebSocket()
    ws.connect(conversionurl)
    ws.send(COMMAND_AUTHENTICATE)
    ws.send(COMMAND_SCHEDULE_JOB)
    pass


if __name__ == '__main__':
    main()
