def tokenize(doc):
   return [token for token in simple_preprocess(doc) if token not in STOPWORDS]


