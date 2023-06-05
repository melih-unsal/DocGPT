from sentence_transformers import SentenceTransformer, CrossEncoder, util
from src.utils import toTextList
from tqdm import trange

class Embeddings:
    def __init__(self, model_name='all-MiniLM-L6-v2', threshold=0.3):
        self.model = SentenceTransformer(model_name)
        self.top_k = 32  #Number of passages we want to retrieve with the bi-encoder
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')    
        self.docs_embeddings = None
    
    def encode(self, prompt):
       if isinstance(prompt, str):
           return self.model.encode(prompt, convert_to_tensor=True).reshape((1,-1))
       return self.model.encode(prompt, convert_to_tensor=True, show_progress_bar=True)

    def setDocs(self, path):
        self.docs = toTextList(path)
        self.docs_embeddings = self.encode(self.docs).cuda()
    
    def getClosests(self,question, top=2):
        q_embeddings = self.encode(question).cuda()
        hits = util.semantic_search(q_embeddings, self.docs_embeddings, top_k=self.top_k)[0]
        ##### Re-Ranking #####
        # Now, score all retrieved passages with the cross_encoder
        cross_inp = [[question, self.docs[hit['corpus_id']]] for hit in hits]
        cross_scores = self.cross_encoder.predict(cross_inp)

        # Sort results by the cross-encoder scores
        for idx in trange(len(cross_scores)):
            hits[idx]['cross-score'] = cross_scores[idx]

        # Output of top-5 hits from bi-encoder
        """print("\n-------------------------\n")
        print(f"Top-{top} Bi-Encoder Retrieval hits")"""
        hits = sorted(hits, key=lambda x: x['score'], reverse=True)
        returning_docs = []
        for hit in hits[0:top]:
            #print("\t{:.3f}\t{}".format(hit['score'], self.docs[hit['corpus_id']].replace("\n", " ")))
            returning_docs.append(self.docs[hit['corpus_id']])
        return returning_docs
    
if __name__ == "__main__":
    x = ["Hi, my name is Melih. "]*10000
    model = Embeddings()
    emb = model.encode(x)
    print(emb.shape)