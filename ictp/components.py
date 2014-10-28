from MaKaC.webinterface.rh.conferenceModif import RHConferenceModifBase
from indico.ext.exporter.register import ExporterRegister

# indico imports
import indico.ext.exporter


from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
from repoze.catalog.query import *

from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone
import MaKaC.common.info as info
from MaKaC.conference import ConferenceHolder

from flask import Response


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
        
        query = Ge('endDate',today) & Any('category', ['2l131','2l132'])
        numdocs, results = catalog.query(query, sort_index='startDate', reverse=False, limit=250)
        results = [catalog.document_map.address_for_docid(result) for result in results]
        res = ''
        for obj in results:
            try:
                confId = str(obj).split("|")[0]
                conf = ch.getById(confId)
                # get Secretary email
                admins = conf.getAccessController().getModifierList()
                admins_email = []
                if admins: admins_email = [admin.getEmail() for admin in admins]
                
                res += self.getSMR(conf)+"$"+','.join(admins_email)+"$"+conf.getTitle()+"$"+conf.getEndDate().strftime("%Y-%m-%d")+"$\n"
            except:
                pass
        return res
        
                
        
class RHExporterIctpCsvView(RHConferenceModifBase):

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
        catalog = RepozeCatalog().catalog
        ch = ConferenceHolder()
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        today = timezone(localTimezone).localize(datetime.now())
        today6month = today + relativedelta(months=6)
        
        
        query = Ge('startDate',today) & Le('startDate',today6month) & Any('category', ['2l130','2l131','2l132'])
        numdocs, results = catalog.query(query, sort_index='startDate', reverse=False, limit=250)
        results = [catalog.document_map.address_for_docid(result) for result in results]
        res = ''
        for obj in results:
            try:
                confId = str(obj).split("|")[0]
                conf = ch.getById(confId)
                # get Secretary email
                admins = conf.getAccessController().getModifierList()
                admins_email = []
                if admins: admins_email = [admin.getEmail() for admin in admins]    
                # get expparts            
                expparts = ''.join([k for k in conf.getKeywords().split('\n') if k.find("expparts") != -1]).replace('expparts','')
                res += conf.getStartDate().strftime("%Y-%m-%d")+";"+conf.getEndDate().strftime("%Y-%m-%d")+";"+conf.getTitle()+";"+','.join(admins_email)+";"+expparts+"\n"
            except:
                pass

        response = Response(res,  mimetype='application/csv')
        response.headers['Content-Type'] = "text/csv"
        response.headers.add('Content-Disposition', 'inline', filename='export.csv')

        #return response
        return res