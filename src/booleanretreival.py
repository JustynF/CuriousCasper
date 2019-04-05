from bitmap import BitMap
import json
import collections
import nltk
from stemmer import stemmer



class BooleanModel:
    def __init__(self, inv_index):
        with open('src/output/corpus.json') as corpus:
            docs = json.load(corpus)
        self.all_doc_id = {document['docId'] for document in docs}
        with open("src/output/dictionary.json") as dictionary:
            self.dict = json.load(dictionary)

        self.inverted_index = inv_index
        self.operators = ["AND","OR","NOT"]
        self.query_operators = []
        self.queries = []

        
    def process_query(self,query):
        query = query.replace('(', '( ')
        query = query.replace(')', ' )')
        query = query.split(' ')



        postfix_queue = collections.deque(self.query_to_postfix(query))

        dict = self.dict

        while postfix_queue:
            token = postfix_queue.popleft()
            if token in self.operators:
                self.query_operators.append(token)
            else:
                    if "*" in token:
                        set_of_words = self.find_wildcard(token,self.handle_wildcard(token))
                        wildcard_query = ' OR '.join(set_of_words)
                        self.queries.append(self.process_query(wildcard_query))
                    else:
                        token = stemmer(token).encode("utf-8")
                        if token in dict:
                            self.queries.append(self.inverted_index[token])

        for operation in self.query_operators:
            if operation == 'AND':
                if len(self.queries)>=2:
                    current_queries = self.queries[:2]
                    self.queries = self.queries[2:]
                    p = current_queries[0]
                    q = current_queries[1]

                    self.queries.insert(0,self.intersection(p,q))
            elif operation == 'OR':
                if len(self.queries) >= 2:
                    current_queries = self.queries[:2]
                    self.queries = self.queries[2:]
                    p = current_queries[0]
                    q = current_queries[1]

                    self.queries.insert(0, self.union(p,q))
            elif operation == "NOT":
                if len(self.queries) >= 1:
                    current_queries = self.queries[:1]
                    self.queries = self.queries[1:]
                    p = current_queries[0]

                    self.queries.insert(0,self.all_doc_id-p)

        while len(self.queries)>1:
            current_queries = self.queries[:2]
            self.queries = self.queries[2:]
            p = current_queries[0]
            q = current_queries[1]

            self.queries.insert(0,self.intersection(p,q))

        return self.queries.pop() if len(self.queries)>0 else []

    def intersection(self,s1,s2):
       if len(s1)>len(s2):
           larger = set(s1)
           return  larger.intersection(s2)
       else:
        return set(s2).intersection(s1)

    def union(self,s1,s2):
        if len(s1) > len(s2):
            return set(s1).union(s2)
        else:
            return set(s2).union(s1)


    def create_ngram_model(self,token,index):
        ngrams = list(nltk.bigrams(token))

        ngrams = map(self.combineTuples,ngrams)

        ngram_model = {ngram: [i for i in index.keys() if ngram in i] for ngram in ngrams}

        return ngram_model

    def combineTuples(self,tuple):

        t1 = (str(tuple[0]) if str(tuple[0]) not in '*' else '')
        t2 = (str(tuple[1]) if str(tuple[1]) not in '*' else '')

        string_tuple = t1+t2

        return string_tuple

    def handle_wildcard(self,token):
        ngram = self.create_ngram_model(token, self.inverted_index)
        res = set()

        for _,arr in ngram.iteritems():
            if len(res) == 0:
                res.update(arr)
            else:
                res.intersection(arr)

        return list(res)



    def find_wildcard(self,token,set_of_words):
        result = []

        if token.startswith('*'):
            for word in set_of_words:
                if word.endswith(token[1:]):
                    result.append(word)

        elif token.endswith('*'):
            for word in set_of_words:
                if word.startswith(token[:len(token)-1]):
                    result.append(word)
        else:
            token_tuple = token.split('*')

            for index, split in enumerate(token_tuple):
                if index == 0:
                    for word in set_of_words:
                        if word.startswith(split):
                            result.append(word)
                elif index == len(split) - 1:
                    for word in set_of_words:
                        if word.endswith(split):
                            result.append(word)
                else:
                    for word in set_of_words:
                        if split in word:
                            result.append(word)
        return result





    def query_to_postfix(self,infix_query):
        # define precedences
        precedence = {}
        precedence['NOT'] = 3
        precedence['AND'] = 2
        precedence['OR'] = 1
        precedence['('] = 0
        precedence[')'] = 0

        # declare data strucures
        output = []
        operator_stack = []

        # while there are tokens to be read
        for token in infix_query:
            # if left bracket
            if (token == '('):
                operator_stack.append(token)
            elif (token == ')'):
                operator = operator_stack.pop()
                while operator != '(':
                    output.append(operator)
                    operator = operator_stack.pop()

            elif (token in precedence):
                if (operator_stack):
                    current_operator = operator_stack[-1]
                    while (operator_stack and precedence[current_operator] > precedence[token]):
                        output.append(operator_stack.pop())
                        if (operator_stack):
                            current_operator = operator_stack[-1]

                operator_stack.append(token)  # add token to stack

            else:
                output.append(token.lower())

        while (operator_stack):
            output.append(operator_stack.pop())

        return output

