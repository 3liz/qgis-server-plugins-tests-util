"""
Sample Qgis server plugin
"""


# Server Plugin only
def serverClassFactory(serverIface: 'QgsServerInterface' ) -> 'SampleServer':
    """Load sampleServer class
    """
    from .sampleServer import SampleServer
    return SampleServer(serverIface)

