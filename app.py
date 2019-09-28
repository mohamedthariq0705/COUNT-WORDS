from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

import re
import linkGrabber
import ast


app = Flask(__name__,
            template_folder="template")


@app.route('/')
def customer():
    return render_template('web.html')
a=[]

@app.route('/success', methods=['POST'])
def print_data():
    if request.method == 'POST':
        result = request.form
        print(result)
        r = requests.get(result['url'])
        soup = BeautifulSoup(r.content, "html.parser")

        text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
        c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

        text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
        c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

        total = c_div + c_p
        list_most_common_words = total.most_common()

        ## print(result)
        #links = linkGrabber.Links(result['url'])
        #gb = links.find('href', 'text', pretty=False)
        ## gb= ast.literal_eval(str(gb))
        ## print(type( gb))
        newlist= []
        #for v in gb:
          #  newlist.append({"href":v["href"],"text":v["text"]})
        newlist = []
        for k, v in total.items():
            newlist.append({"word": k, "count":v})
        print(newlist)

        return render_template("result.html", result=result,gb=newlist)



if __name__ == '__main__':
    app.run(debug=True)
