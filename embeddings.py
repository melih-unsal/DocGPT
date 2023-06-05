from sentence_transformers import SentenceTransformer, util
import numpy as np

class Embeddings:
    def __init__(self, model_name='all-MiniLM-L6-v2', threshold=0.3):
        self.model = SentenceTransformer(model_name)
        self.model.max_seq_length = 1000
        dim = self.model.encode("").shape[0]
        self.threshold = threshold
        self.embeddings_list = np.zeros((0,dim))
    
    def get(self, prompt):
       return self.model.encode(prompt).reshape((1,-1))
    
    def add(self, embeddings):
        self.embeddings_list = np.concatenate((self.embeddings_list,embeddings))

    def getCloseIndices(self,prompt):
        if self.embeddings_list.shape[0] == 0:
            return [],[]
        indices = []
        embeddings = self.get(prompt)
        print("embeddings:",embeddings.shape)
        similarities = 1 - embeddings @ self.embeddings_list.T
        print("similarities:",similarities)
        indices = np.argwhere(similarities > self.threshold).flatten()
        return np.unique(indices), similarities[0]
    
if __name__ == "__main__":
    x = "a"*1000
    model = Embeddings()
    t = model.model.tokenize(x)
    print(t["input_ids"].shape)
    emb = model.get(x)
    print(emb.shape)