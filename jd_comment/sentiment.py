from snownlp import SnowNLP
import numpy


data = []
filename = 'comment.txt'
with open(filename) as f:
    mytext = f.read()
s = SnowNLP(mytext)
for sentences in s.sentences:
    data.append(SnowNLP(sentences).sentiments)

print(numpy.mean(data))
