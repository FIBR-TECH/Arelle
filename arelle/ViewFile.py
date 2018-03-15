'''
Created on Oct 9, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
'''
import  re #, sys, csv, io, json
#from lxml import etree
#from decimal import Decimal
from arelle.FileSource import FileNamedStringIO
#if sys.version[0] >= '3':
#    csvOpenMode = 'w'
#    csvOpenNewline = ''
#else:
#    csvOpenMode = 'wb' # for 2.7
#    csvOpenNewline = None
#from openpyxl import Workbook, cell
#from openpyxl.styles import Font, PatternFill, Border, Alignment, Color, fills, Side

NOOUT = 0
CSV   = 1
XLSX  = 2
HTML  = 3
XML   = 4
JSON  = 5
TYPENAMES = ["NOOUT", "CSV", "XLSX", "HTML", "XML", "JSON"] # null means no output
nonNameCharPattern =  re.compile(r"[^\w\-\.:]")

class View:
    # note that cssExtras override any css entries provided by this module if they have the same name
    def __init__(self, modelXbrl, outfile, rootElementName, lang=None, style="table", cssExtras=""):
        self.modelXbrl = modelXbrl
        self.lang = lang
        self.type = JSON
        self.outfile = outfile
        if style == "rendering": # for rendering, preserve root element name
            self.rootElementName = rootElementName
        else: # root element is formed from words in title or description
            self.rootElementName = rootElementName[0].lower() + nonNameCharPattern.sub("", rootElementName.title())[1:]
        self.numHdrCols = 0
        self.treeCols = 0  # set to number of tree columns for auto-tree-columns
        if modelXbrl:
            if not lang: 
                self.lang = modelXbrl.modelManager.defaultLang

        
        self.entries = []
        self.entryLevels = [self.entries]
        self.jsonObject = {self.rootElementName: self.entries}
            
    def setColWidths(self, colWidths):
        # widths in monospace character counts (as with xlsx files)
        if self.type == XLSX:
            for iCol, colWidth in enumerate(colWidths):
                colLetter = chr( ord("A") + iCol )
                self.xlsxWs.column_dimensions[colLetter].width = colWidth  
        
    def setColWrapText(self, colColWrapText):
        # list with True for columns to be word wrapped in every row including heading
        if self.type == XLSX:
            self.xlsxColWrapText = colColWrapText
        
    def addRow(self, cols, asHeader=False, treeIndent=0, colSpan=1, xmlRowElementName=None, xmlRowEltAttr=None, xmlRowText=None, xmlCol0skipElt=False, xmlColElementNames=None, lastColSpan=None):
        if asHeader and len(cols) > self.numHdrCols:
            self.numHdrCols = len(cols)



        if asHeader:
            # save column element names
            self.xmlRowElementName = xmlRowElementName
            self.columnEltNames = [col[0].lower() + nonNameCharPattern.sub('', col[1:])
                                   for col in cols]
        else:
            if treeIndent < len(self.entryLevels) and self.entryLevels[treeIndent] is not None:
                entries = self.entryLevels[treeIndent]
            else:
                # problem, error message? unexpected indent
                entries = self.entryLevels[0] 
            entry = []
            if xmlRowElementName:
                entry.append(xmlRowElementName)
            elif self.xmlRowElementName:
                entry.append(self.xmlRowElementName)
            if xmlRowEltAttr:
                entry.append(xmlRowEltAttr)
            else:
                entry.append({})
            entries.append(entry)
            if treeIndent + 1 >= len(self.entryLevels): # extend levels as needed
                for extraColIndex in range(len(self.entryLevels) - 1, treeIndent + 1):
                    self.entryLevels.append(None)
            self.entryLevels[treeIndent + 1] = entry
            if not xmlColElementNames: xmlColElementNames = self.columnEltNames
            if len(cols) == 1 and not xmlCol0skipElt:
                entry.append(xmlRowText if xmlRowText else cols[0])
            else:
                content = {}
                entry.append(content)
                for i, col in enumerate(cols):
                    if (i != 0 or not xmlCol0skipElt) and col and i < len(xmlColElementNames):
                            elementName = xmlColElementNames[i]
                            if elementName == "dimensions":
                                value = dict((str(cols[i]),str(cols[i+1])) for i in range(i, len(cols), 2))
                            else:
                                value = str(col)
                            content[elementName] = value
#        if asHeader and lastColSpan: 
#            self.numHdrCols += lastColSpan - 1
                                
    def close(self, noWrite=False):
#        print('viefile Type : ' + str(self.type))
        if self.type == CSV:
            if not isinstance(self.outfile, FileNamedStringIO):
                self.csvFile.close()
        elif self.type == XLSX:
            self.xlsxWb.save(self.outfile)
        elif self.type != NOOUT and not noWrite:
            fileType = TYPENAMES[self.type]
            try:
#                from arelle import XmlUtil
#                if isinstance(self.outfile, FileNamedStringIO):
#                    fh = self.outfile
#                else:
#                    fh = open(self.outfile, "w", encoding="utf-8")
#                if self.type == JSON:
                return(self.jsonObject)
#                    print('We are printing something' + str(self.jsonObject))
#                    
#                    fh.write(json.dumps(self.jsonObject, ensure_ascii=False))
#                else:
#                    XmlUtil.writexml(fh, self.xmlDoc, encoding="utf-8",
#                                     xmlcharrefreplace= (self.type == HTML) )
#                if not isinstance(self.outfile, FileNamedStringIO):
#                    fh.close()
#                self.modelXbrl.info("info", _("Saved output %(type)s to %(file)s"), file=self.outfile, type=fileType)
            except (IOError, EnvironmentError) as err:
                self.modelXbrl.exception("arelle:htmlIOError", _("Failed to save output %(type)s to %(file)s: \s%(error)s"), file=self.outfile, type=fileType, error=err)
        self.modelXbrl = None
#        if self.type == HTML:
#            self.tblElt = None
#        elif self.type == XML:
#            self.docEltLevels = None

        self.__dict__.clear() # dereference everything after closing document

