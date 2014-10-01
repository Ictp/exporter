from MaKaC.webinterface.rh.conferenceModif import RHConferenceModifBase
from indico.ext.exporter.register import ExporterRegister

# indico imports
import indico.ext.exporter


from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
from repoze.catalog.query import *

from datetime import datetime
from pytz import timezone
import MaKaC.common.info as info
from MaKaC.conference import ConferenceHolder



class RHExporterIctpView(RHConferenceModifBase):

    _register = ExporterRegister()

    def _checkProtection(self):
        pass

    def _checkParams(self, params):
        pass

    def getSMR(self, conf):
        for k in conf.getKeywords().split('\n'):
            if k.find('smr') != -1:
                smr = k.replace('smr','').replace('None','')
                return smr
        return ''
        
    def _process(self):
        #return "Ictp EXPORTER"
        # This is cozy hook for custom code.
        catalog = RepozeCatalog().catalog
        ch = ConferenceHolder()
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        today = timezone(localTimezone).localize(datetime.now())
        
        query = Ge('endDate',today) 
        numdocs, results = catalog.query(query, sort_index='startDate', reverse=False, limit=250)
        results = [catalog.document_map.address_for_docid(result) for result in results]
        res = ''
        for obj in results:
            #try:
            if 1:
                confId = str(obj).split("|")[0]
                conf = ch.getById(confId)
                # get Secretary email
                admins = conf.getAccessController().getModifierList()
                admins_email = []
                if admins: admins_email = [admin.getEmail() for admin in admins]
                
                res += self.getSMR(conf)+"$"+','.join(admins_email)+"$"+conf.getTitle()+"$"+conf.getEndDate().strftime("%Y-%m-%d")+"$\n"
            #except:
            #    pass
        return res
        
