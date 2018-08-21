import os
import api
from mesh_explosion import DataForEachMeshTerm


class GoldenCorpus():

    def __init__(self,query,filepath):
        self.query = query
        self.filepath = filepath
        self.rel_docs = []
        self.mesh_terms = []

    def get_corpus_folder(self,query):
        return "golden_corpus/" + query
        
    def get_mesh_terms(self):
        return self.mesh_terms
    
    def get_rel_docs_pmid(self):
        return self.rel_docs

    def preprocess(self,abstract):
        content = abstract.replace('\n', ' ')
        content = content.replace('(', ' ')
        content = content.replace(')', ' ')
        content = content.replace('.', ' ')
        content = content.replace(',', ' ')
        content = ' '.join(content.split())
        content = content.lower()
        # print(content)
        return content

    def checkRelevence(self,abstract, genes):
        abs = self.preprocess(abstract)
        for gene in genes:
            if gene and gene+" " in abs:
                return True,gene
        return False,""

    def fetchData(self):
        print("fetchdata called..")
        _pmids, self.mesh_terms = api.fetch_data(self.query,10000)
        print("pmid:----------------------------------> ",len(_pmids))
        self.saveGoldenCorpus(_pmids)


    def saveGoldenCorpus(self, _pmids):
        print("save golden corpus called..")
        _genefile = []
        if not os.path.exists(self.get_corpus_folder(self.query)):
            os.mkdir(self.get_corpus_folder(self.query))
            #  Download abs as a group of 200
            if len(_pmids):
                slist = []
                count = 0
                doccount = 1

                total_parts = int(len(_pmids)/200)
                for cid in _pmids:
                    if count < 200:
                        slist.append(cid)
                        count+=1
                        continue
                    else:
                        ids = ""
                        for pmid in slist:
                            ids += str(pmid) + ","
                        print("Downloading part " + str(doccount) + " of " + str(total_parts))
                        data = api.get_abstract(ids)
                        slist = []
                        count = 0
                        doccount+=1
                        self.split_abstracts(self.query, data)

                if count > 0:
                    ids = ""
                    for pmid in slist:
                        ids += str(pmid) + ","
                    data = api.get_abstract(ids)
                    self.split_abstracts(self.query, data)
            else:
                print("No data found!")
        # check relevance and populate get rel_Docset
        print("Relevant docs creating.......")
        if os.path.exists(self.filepath):
            _filepointer = open(self.filepath,'r')
            _genefile = _filepointer.read().split('\n')
            abstracts_folder_name = self.get_corpus_folder(self.query)
            for file in os.listdir(abstracts_folder_name):
                rf = open(abstracts_folder_name+"/"+file, 'r')
                content = self.preprocess(rf.read())
                result,gene = self.checkRelevence(content,_genefile)
                count = 0
                if result:
                    count += 1
                    # print count
                    print("file: ",file)
                    print("gene found: -- > ", gene)
                    self.rel_docs.append(int(file))
            print("len: ",len(self.rel_docs))
            print("corpus done..")
        else:
            print("Genefile not found...")

    def split_abstracts(self,query, data):
        # if not os.path.exists(self.get_corpus_folder(query)):
        #     os.mkdir(self.get_corpus_folder(query))
        lines = data.split('\n')
        article = ""
        count = 0
        for line in lines:
            dummy = line[:-1]
            dummy = dummy.replace('[', ':')
            dummy = dummy.replace(']', ':')
            value = dummy.split(':')
            if(value[0] == "PMID"):
                pmid_value = value[1].replace(' ', '')
                wf = open(self.get_corpus_folder(query) + "/" + pmid_value, 'w')
                article += line
                wf.write(article)
                wf.close()
                article = ""
                count += 1
            else:
                article += line