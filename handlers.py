import pkg_resources

# legacy imports
from MaKaC.services.implementation.base import ServiceBase
from MaKaC.plugins.base import PluginsHolder

#from indico.web.handlers import RHHtdocs
from MaKaC.webinterface.rh.conferenceModif import RHConferenceModifBase
from indico.ext.exporter.register import ExporterRegister

# indico imports
import indico.ext.exporter



class RHExporterView(RHConferenceModifBase):

    _register = ExporterRegister()

    def _checkProtection(self):
        pass

    def _checkParams(self, params):
        pass
        
    def _process(self):
        return "Base class method. Need to be implemented."
