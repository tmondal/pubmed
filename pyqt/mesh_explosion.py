import os
import itertools
import json
import api

class DataForEachMeshTerm():
    def __init__(self, mesh_terms, query):
        self.mesh_terms = mesh_terms
        self.query = query
        # if self.mesh_terms and self.query:
        #     self.fetchMeshTermdata()

    def get_data_foldername(self,query):
        return "data_folder/" + query

    def get_search_term(self):
        return self.query

    def getMeshTermCombinations(self):
        # Preprocess terms
        terms = self.mesh_terms.split('OR')
        terms = [term.replace('(', '') for term in terms]
        terms = [term.replace(')', '') for term in terms]
        # Removing date from last term
        temp = terms[len(terms)-1].split('AND')
        terms[len(terms)-1] = temp[0] 
        terms = [term.strip() for term in terms]
        terms = ['('+term+')' if 'AND' in term else term for term in terms]

        combs = []

        for i in range(1, len(terms)+1):
            tmp = [list(x) for x in itertools.combinations(terms,i)]
            combs.extend(tmp)

        # print(combs)
        mesh_exps = []
        for comb in combs:
            s = ""
            # for x in range(0,len(comb)-1):
                # s+="("
            count = 0
            for term in comb:
                if count == 0:
                    s += term
                else:
                    s += " OR " + term
                count += 1
            mesh_exps.append(s)
        return mesh_exps

    def fetchMeshTermdata(self):
        _retmax = 400
        if self.mesh_terms:
            _terms = self.getMeshTermCombinations()
        else:
            print("No mesh term returned by PUBMED API..")
        if _terms and self.query:
            if not os.path.exists(self.get_data_foldername(self.get_search_term())):
                os.mkdir(self.get_data_foldername(self.get_search_term()))
            count = 0
            for term in _terms:
                count = count + 1
                _pmids, mtdummy = api.fetch_data(term,_retmax)
                # Get abs for all ids together
                ids = ""
                for pmid in _pmids:
                    ids += str(pmid) + ","
                data = api.get_abstract(ids)

                jObject = {}
                jObject['queryId'] = count
                jObject['query'] = term
                jObject['articleIds'] = ids
                jObject['abstracts'] = data

                with open(self.get_data_foldername(self.get_search_term())+"/"+str(count)+'.json', 'w') as outfile:
                    json.dump(jObject, outfile)

