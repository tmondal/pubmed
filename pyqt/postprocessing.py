import os
import json
from mesh_explosion import DataForEachMeshTerm


class PostProcessing():

    def __init__(self):
        pass

    def getTitleAbs(self,index,json_no,query):
        # open json
        dfet = DataForEachMeshTerm(None,None)
        data_folder_name = dfet.get_data_foldername(query)
        f = open(data_folder_name+"/"+str(json_no)+".json", 'r')
        json_object = json.load(f)
        f.close()
        abstracts = json_object["abstracts"]
        toptitles,topabs = self.split_abstracts(index,abstracts)
        return toptitles, topabs


    def split_abstracts(self,index,data):
        # lines = data.split('\n')
        article = ""
        count = 0
        allabs = []
        alltitles = []
        i = 0
        while(i < len(data)):
            if count == (index+1)*5:
                break
            elif (data[i] == 'P' and data[i+1] == 'M' and data[i+2] == 'I' and data[i+3] == 'D'):
                c = 0
                while(c < 2):
                    if(data[i] == '\n'):
                        c += 1
                    i += 1
                    
                if count >= index*5:
                    allabs.append(article)
                    alltitles.append(self.getTitleFromAbs(article))
                article = ""
                count += 1

            article += data[i]
            i += 1

        return alltitles,allabs

    def getTitleFromAbs(self, article):
        found = False
        nextfound = False
        title = ""
        i = 0
        while (i < len(article)):
            if not nextfound and found:
                title += article[i]
            if found:
                if article[i] == '\n' and article[i+1] == '\n':
                    nextfound = True
            if nextfound:
                break
            if not found:
                if article[i] == '\n' and article[i+1] == '\n':
                    found = True
                    i += 1
            i += 1
        return title