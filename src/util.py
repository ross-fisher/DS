from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

def tokenize(doc):
   return [token for token in simple_preprocess(doc) if token not in STOPWORDS]


