import numpy
from snownlp import SnowNLP

data = []
filename = 'comment.txt'
with open(filename) as f:
    mytext = f.read()
s = SnowNLP(mytext)
for sentences in s.sentences:
    data.append(SnowNLP(sentences).sentiments)

print(numpy.mean(data))
