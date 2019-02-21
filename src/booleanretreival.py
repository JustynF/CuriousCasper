from bitmap import BitMap
import json
import collections
from stemmer import stemmer


class BooleanModel:
    def __init__(self, inv_index):
        with open('./src/output/corpus.json') as corpus:
            docs = json.load(corpus)
        self.all_doc_id = {document['docId'] for document in docs}
        self.inverted_index = inv_index
        self.operators = ["AND","OR","NOT"]
        self.query_operators = []
        self.queries = []

        
    def process_query(self,query):
        query = query.replace('(', '( ')
        query = query.replace(')', ' )')
        query = query.split(' ')

        
        
        postfix_queue = collections.deque(self.query_to_postfix(query))
        with open("./src/output/dictionary.json") as dictionary:
            dict = json.load(dictionary)


        while postfix_queue:
            token = postfix_queue.popleft()
            if token in self.operators:
                self.query_operators.append(token)
            else:
                    if "*" in token:
                        ngram = self.create_ngram_model(token,self.inverted_index)
                        print(ngram)
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
        ngrams = [token[i:i+2]for i in range(1,len(token) - 1,2)]

        print(ngrams)
        ngrams.append(token[0])
        print(ngrams)
        ngrams.append(token[-1])

        ngrams = [''.join(n for n in ngram if n not in '*') for ngram in ngrams]
        print(ngrams)

        return {ngram: [word for word in index.keys() if ngram in index] for ngram in ngrams}





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

