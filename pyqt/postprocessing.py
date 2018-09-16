import os
import json
from mesh_explosion import DataForEachMeshTerm
import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt


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
        article = ""
        count = 0
        allabs = []
        alltitles = []
        i = 0
        while(i < len(data)):
            if count == (index+1)*4:
                break
            elif (data[i] == 'P' and data[i+1] == 'M' and data[i+2] == 'I' and data[i+3] == 'D'):
                c = 0
                while(c < 2):
                    if(data[i] == '\n'):
                        c += 1
                    i += 1
                    
                if count >= index*4:
                    allabs.append(self.getProcessedAbs(article))
                    alltitles.append(self.getTitleFromAbs(article))
                article = ""
                count += 1

            article += data[i]
            i += 1

        return alltitles,allabs
    def getProcessedAbs(self, article):
        abs = ""
        i = 0
        count = 0
        c = 0
        while (i < len(article)):
            if article[i] == '\n' and article[i+1] == '\n':
                count += 1
            if(count == 3):
                if(article[i+2] == 'A' and (article[i+3] == 'u' or article[i+3] == 'U') and (article[i+4] == 't' or article[i+4] == 'T') 
                and (article[i+5] == 'h' or article[i+5] == 'H') and (article[i+6] == 'o' or article[i+6] == 'O')):
                    count -= 1
                else:
                    i += 2
                    while(c < 2 and i < len(article)):
                        abs += article[i]
                        if(article[i] == '\n'):
                            c += 1
                        i += 1
                    break
            i += 1
        return abs        

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

    def term_tagging(self,optimized_terms):
       
        term_dict = {}
        for terms in optimized_terms:
            for term in terms:
                i = 0
                count=0
                st = ""
                while i<len(term):
                    if term[i] == '"':
                        count += 1
                        if count%2==0:
                            self.countoccurrences(term_dict,st) 
                        st = ""
                    else:
                        st += term[i]
                    i += 1

        print(term_dict)

        sorted_dict = sorted(term_dict.items(), key=operator.itemgetter(1),reverse=True)

        print(sorted_dict)

        return sorted_dict


    def countoccurrences(self,store,value):
        try:
            store[value] = store[value] + 1
        except KeyError as e:
            store[value] = 1
        return


    def gene_cloud(self,term_id,gene_file_name,search_term):
        print("Gene cloud called..")
        file_name = "data_folder/"+search_term+"/"+str(term_id)+'.json'
        f = open(file_name, 'r')
        json_object = json.load(f)
        f.close()

        data_abstract = json_object["abstracts"]

        content = data_abstract.replace('\n', ' ')
        content = content.replace('(', ' ')
        content = content.replace(')', ' ')
        content = content.replace('.', ' ')
        content = content.replace(',', ' ')
        content = content.lower()
        # print(content)

        data = content.split()

        filepointer = open(gene_file_name,'r')
        genefile = filepointer.read().lower().split('\n')

        gene_dict = {} 

        for gene in genefile:
            if gene:
                gene_dict[gene] = data.count(gene)+1.0

        
        wordcloud = WordCloud(width = 800, height = 800,
                                background_color ='white',
                                min_font_size = 10).fit_words(gene_dict)
        
        # plot the WordCloud image                       
        fig = plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.tight_layout(pad = 0)
        plt.axis("off")
        fig.canvas.set_window_title("Gene cloud")
        plt.show()