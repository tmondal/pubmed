from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.cluster import KMeans
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import numpy as np


from pubmedapi.forms import QueryForm

# Create your views here.

class IndexView(View):

    def get(self,request):
        form = QueryForm()
        return render(request,'pubmedapi/index.html',{'form': form})

    def post(self,request):
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            print(query)
            
            http_proxy = "http://subha174101025:subha000@202.141.80.22:3128"
            https_proxy = "https://subha174101025:subha000@202.141.80.22:3128"
            ftp_proxy = "ftp://subha174101025:subha000@202.141.80.22:3128"

            proxy_dict = {
                "http"  :   http_proxy,
                "https" :   https_proxy,
                "ftp"   :   ftp_proxy
            }

            with open('/home/subha/gene_dict.txt','r') as f:
                genes = f.read().splitlines()
            
            # genes = ['the','a','of','in']
            # api call
            n=100
            url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&api_key=947c1845e9a006cd589f251e11def613e308&term={}&reldate=60&datetype=edat&retmax={}&retmode=json'
            res = requests.get(url.format(query,n)).json()

            # # api call with proxy
            # url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&api_key=947c1845e9a006cd589f251e11def613e308&term={}&reldate=60&datetype=edat&retmax=1&retmode=json'
            # res = requests.get(url.format(query),proxies=proxy_dict).json()

            abstract = []
            idlist = res['esearchresult']['idlist']
            # print(idlist)
            for id in idlist:
                print(id)
                abstracturl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&api_key=947c1845e9a006cd589f251e11def613e308&id={}&retmode=text&rettype=abstract'
                idabstract = requests.get(abstracturl.format(id))
                # print(idabstract.text)
                abstract.append(idabstract.text)
                # print(abstract)
                # if 'Barcelona' in abstract:
                    # print('blahhhhhhhhhhhhhhh')
                # vectorizer = CountVectorizer()
                # x = vectorizer.fit_transform(idabstract)
                # print(x.toarray())
            
            # create the transform
            vectorizer = TfidfVectorizer(vocabulary=genes)
            # # tokenize and build vocabulay
            # vectorizer.fit(abstract)
            # # summarize
            # print(vectorizer.vocabulary_)
            # print(vectorizer.idf_)

            vector = vectorizer.fit_transform(abstract)

            # print(vector.shape)
            # print(vector.toarray())

            # No of Clusters
            clus_no = 10
            #apply kmeans to cluster row vectors
            kmeans = KMeans(n_clusters=clus_no,init='k-means++',random_state=0).fit(vector)
            
            scores = np.zeros(clus_no)
            total = np.zeros(clus_no)
            flag = np.zeros((clus_no,len(genes)))
            X=kmeans.labels_

            print(X)

            for i in range(0,len(X)):
                total[X[i]] = total[X[i]]+len(abstract[i].split())
                # print('document:%d and cluster:%d'%(i,X[i]))
                # print(len(abstract[i].split()))
                for j in range(0,len(genes)):
                    if flag[X[i]][j]==0 and genes[j] in abstract[i]:
                        flag[X[i]][j]=1
                        scores[X[i]] = scores[X[i]]+1

            for i in range(0,scores.size):
                print(scores[i])
                print(total[i])
                scores[i] = scores[i]/total[i]

            print(scores)
            

            
            
            # send data to template
            args = {'form': form,'data': query}
            return render(request,'pubmedapi/index.html',args)
        else:
            return render(request,'pubmedapi/index.html',{'form': form})
