"""
    Implementation of the widget
"""

# -*- coding: utf-8 -*-

import zope.component
import zope.interface
import zope.schema
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from z3c.form import interfaces


from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form.widget import SequenceWidget, FieldWidget
from z3c.form.browser import widget
from z3c.form.i18n import MessageFactory as _

from zope.i18n import translate
from Products.CMFCore.utils import getToolByName



from z3c.form.term import CollectionTermsVocabulary

class IElectionsWidget(interfaces.ISequenceWidget):
    """Text lines widget."""



class ElectionsWidget(widget.HTMLSelectWidget, SequenceWidget):
    """ Widget for elections
    """
    zope.interface.implementsOnly(IElectionsWidget)
    klass = u'election-widget'
    size = 5
    multiple = u'multiple'
    items = ()
    selectedItems = ()
    notselectedItems = ()


    def scriptShowHide(self):

        return  'var opcion = \"\" \n \
$(document).ready(function(){ \n \
    $(\"#'+self.id+'-option-default\").hide(); \n \
    $(\"#'+self.id+'-option-collection\").hide();\n \
    $(\"#'+self.id+'-option-plaintext\").hide();\n \
\n \
    $(\'input:radio\').click(function(){\n \
        opcion = $(\'input:radio[name='+self.id+'option]:Checked\').val()\n \
        switch(opcion){\n \
            case \"'+self.id+'-option-default\":\n \
                $(\"#'+self.id+'-option-default\").show();\n \
                $(\"#'+self.id+'-option-collection\").hide();\n \
                $(\"#'+self.id+'-option-plaintext\").hide();\n \
                break; \n \
            case \"'+self.id+'-option-collection\":\n \
                $(\"#'+self.id+'-option-default\").hide();\n \
                $(\"#'+self.id+'-option-collection\").show();\n \
                $(\"#'+self.id+'-option-plaintext\").hide();\n \
                break;\n \
\
            case \"'+self.id+'-option-plaintext\": \n \
                $(\"#'+self.id+'-option-default\").hide();\n \
                $(\"#'+self.id+'-option-collection\").hide();\n \
                $(\"#'+self.id+'-option-plaintext\").show();\n \
                break; \n \
        }\n \
    }); \n \
\
});\n '


    

    def loadRadio(self):
	value = self.id + "-option-default"
        try:
            value = self.value[3]
            rstr = '$(document).ready(function(){ \
                        document.getElementById(\"'+value+'id\").checked=true; \
                        $(\"#'+value+'\").show(); \
                    });'
            return rstr            
        except:
            return ""



    def getItem(self, term, count=0):
        id = '%s-%i' % (self.id, count)
        content = term.value
        if zope.schema.interfaces.ITitledTokenizedTerm.providedBy(term):
            content = translate(
                term.title, context=self.request, default=term.title)
        return {'id':id, 'value':term.token, 'content':content}

    def updateTerms(self):
        if self.terms is None:
            factory = getUtility(IVocabularyFactory, 'plone.app.vocabularies.Users')
            vocabulary = factory(self.context)
            self.terms = CollectionTermsVocabulary(self.context, self.request, self.form, self.field, vocabulary, self)
        return self.terms


    def strtolist(self, str):
        ls = []
        if str == 'None':
	    return []
        for ele in str[1:-1].split(', '):
            if ele != "u''":
                ele = u'' + ele[2:-1]
                ls.append(ele)
        return ls

    def update(self):
        """See z3c.form.interfaces.IWidget."""

        super(ElectionsWidget, self).update()
        widget.addFieldClass(self)


        self.items = [
            self.getItem(term, count)
            for count, term in enumerate(self.terms)]
        try:
            
            self.selectedItems = [
                self.getItem(self.terms.getTermByToken(token), count)
                for count, token in enumerate(self.strtolist(self.value[0]))]
        except:
            self.selectedItems = []
        self.notselectedItems = self.deselect()
        datatosave = []
        datatosave.append(self.request.get(self.name + "default"))
        datatosave.append(self.request.get(self.name + "collection"))
        datatosave.append(self.request.get(self.name + "plaintext"))
        datatosave.append(self.request.get(self.id + "option"))
        self.request.set(self.name, datatosave)




      

    def deselect(self):
        selecteditems = []
        notselecteditems = []
        for selecteditem in self.selectedItems:
            selecteditems.append(selecteditem['content']) 
        for item in self.items:
            if not item['content'] in selecteditems:
                notselecteditems.append(item)
        return notselecteditems


    def isNomination(self):
        val = self.field.title == 'Nominations roll'
        return val



    def isSelected(self, term):
        return term.token in self.value


    def getText(self):
        try:
            return self.value[2]
        except:
            return ""

    def items2(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        res  = catalog.searchResults({'portal_type': 'Collection'})
        coll_data = []
	for coll in res:
	    coll_data.append(
                 {'token': coll.getObject(),'title':coll.getObject().title}    
            )

        items = []
        def addItem(idx, term, prefix=''):
            id = '%s-%s%i' % (self.id, prefix, idx)
            content = term['title']
            selected = False
            try:
                selected = content in self.strtolist(self.value[1])
            except:
                selected = False
            items.append(
                {'id': id, 'value': content, 'content': content,
                 'selected': selected})

        for idx, term in enumerate(coll_data):
            addItem(idx, term)
        return items

@zope.interface.implementer(interfaces.IFieldWidget)
def ElectionsFieldWidget(field, request):
    """ IFieldWidget factory for ElectionsWidget.
    """
    return FieldWidget(field, ElectionsWidget(request))
