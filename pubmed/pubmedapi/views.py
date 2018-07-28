from sklearn.feature_extraction.text import CountVectorizer
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


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

            # api call
            url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&reldate=60&datetype=edat&retmax=1&retmode=json'
            res = requests.get(url.format(query)).json()
            idlist = res['esearchresult']['idlist']
            # print(idlist)
            for id in idlist:
                print(id)
                abstracturl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={}&retmode=text&rettype=abstract'
                idabstract = requests.get(abstracturl.format(id))
                # print(idabstract.text)
                vectorizer = CountVectorizer()
                x = vectorizer.fit_transform(idabstract)
                print(x.toarray())

            
            
            # send data to template
            args = {'form': form,'data': query}
            return render(request,'pubmedapi/index.html',args)
        else:
            return render(request,'pubmedapi/index.html',{'form': form})
