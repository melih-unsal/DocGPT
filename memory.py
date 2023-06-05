import faiss
from embeddings import Embeddings
import numpy as np
from utils import MEMORY_NEED_PROMPT, SUMMARY_ENOUGH_CHECK_PROMPT, SUMMARIZATION_PROMPT, HISTORY_BASED_PROMPT

class MemoryManager:
    def __init__(self, model) -> None:
        self.embeddings_model = Embeddings(model_name="all-mpnet-base-v2")
        self.model = model
        self.history = []
        self.history_embeddings = []
        self.similarity_thr = 0.4
        self.relevance_coef = 1
        self.recency_coef = 0.3
        self.history_limit = 3
        self.index = faiss.IndexFlatIP(384)

    @property
    def getHistorySize(self):
        return len(self.history)
    
    def getEmbeddings(self, prompt):
        return self.embeddings_model.get(prompt)
    
    @property
    def getRecency(self):
        indices = self.getHistorySize - 1 - np.arange(self.getHistorySize)
        recency = np.exp(indices)/sum(np.exp(indices))
        return recency
    
    def getPrompt(self, prompt):
        print("history:",len(self.history))
        I, S = self.embeddings_model.getCloseIndices(prompt)
        scores = []
        for index in I:
            score = self.relevance_coef * S[index] + self.recency_coef * self.getRecency[index]
            print("score:",score,"sentence:",self.history[index])
            scores.append((int(index), int(score)))
        scores = sorted(scores, key=lambda x: x[1],reverse=True)
        limit = min(self.history_limit,len(scores))
        indices = [score[0] for score in scores[:limit]]
        resulting_prompt = ""
        for index in indices:
            resulting_prompt += self.history[index] + "\n"
        return resulting_prompt
    
    def getRole(self):
        return "User:" if len(self.history) % 2 == 0 else "Assistant:"
    
    def addPrompt(self,prompt):
        embeddings = self.getEmbeddings(prompt)
        role = self.getRole()
        self.history.append(role+prompt)
        self.embeddings_model.add(embeddings)

    def isMemoryNeeded(self,content):
        prompt = MEMORY_NEED_PROMPT.format(user_input = content)
        completion = self.model.get_completion_without_history(prompt)
        return "(A)" in completion
    
    def isSummaryEnough(self,content):
        prompt = SUMMARY_ENOUGH_CHECK_PROMPT.format(user_input = content)
        completion = self.model.get_completion_without_history(prompt)
        return "(A)" in completion
    
    def summarize(self, user_prompt, completion):
        prompt = SUMMARIZATION_PROMPT.format(user_input = user_prompt, system_response= completion)
        return self.model.get_completion_without_history(prompt)

    def completionWithHistory(self,history_of_related_turn, previous_user_input, previous_system_response, current_user_input):
        prompt = HISTORY_BASED_PROMPT.format(history_of_related_turn = history_of_related_turn, 
                                             previous_user_input= previous_user_input,
                                             previous_system_response= previous_system_response,
                                             current_user_input= current_user_input)
        return self.model.get_completion_without_history(prompt)

    def getCompletion(self, prompt):
        history_of_related_turn = self.getPrompt(prompt)
        print("history_of_related_turn:",history_of_related_turn)
        last_user_index = self.getHistorySize -1 - (self.getHistorySize-1) % 2            
        last_assistant_index = self.getHistorySize -1 - self.getHistorySize % 2
        previous_user_input = "" if last_user_index < 0 else self.history[last_user_index]
        previous_system_response = "" if last_assistant_index < 0 else self.history[last_assistant_index]
        self.addPrompt(prompt)
        completion =  self.completionWithHistory(history_of_related_turn, previous_user_input, previous_system_response, prompt)
        self.addPrompt(completion)
        return completion