""" SampleFilter

    This is a do-nothing plugin, just for the purpose
    of using tests
"""
import traceback


from qgis.core import Qgis, QgsMessageLog
from qgis.server import QgsServerInterface, QgsServerFilter

class SampleServer:
    """Plugin for QGIS server"""
    def __init__(self, serverIface: QgsServerInterface) -> None:
        QgsMessageLog.logMessage('SUCCESS - init', 'sample', Qgis.Info)
        try:
            serverIface.registerFilter(SampleFilter(serverIface), 0)
        except Exception as e:
            QgsMessageLog.logMessage('Error loading filter sample : {}'.format(e), 'sample', Qgis.Critical)
            raise


class SampleFilter(QgsServerFilter):

    def __init__(self, serverIface: QgsServerInterface) -> None:
        QgsMessageLog.logMessage('SampleFilter.init', 'sample', Qgis.Info)
        super().__init__(serverIface)

        self._iface = serverIface

    def responseComplete(self):
        handler = self._iface.requestHandler()
        # XXX Qgis may crash on unhandled exception
        try:
            # Check if needed params are passed
            # If not, do not change QGIS Server response
            params = handler.parameterMap()
            if params.get('SERVICE','').lower() != 'wms':
                return

            # Check if getprintatlas request. If not, just send the response
            if params.get('REQUEST','').lower() != 'getsample':
                return

            body = "Hello from sample"

            handler.clear()
            handler.setResponseHeader('Content-type', 'text/plain')
            handler.appendBody(body.encode('utf-8'))
            handler.setStatusCode(200)
        except:
            QgsMessageLog.logMessage(traceback.format_exc(), 'sample', Qgis.Critical)
            handler.setStatusCode(500)

