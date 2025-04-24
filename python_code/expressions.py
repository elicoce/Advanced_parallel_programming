# ELISA COCEANI SM3201340

# Eccezione per quando si tenta di accedere a un elemento da uno stack vuoto
class EmptyStackException(Exception):
    pass
    
# Eccezione per quando si cerca di accedere ad una varibaile non presente nell'ambiente
class MissingVariableException(Exception):
    pass

# Eccezione per quando si cerca di chiamare una funzione non presente nell'ambiente
class MissingFunctionException(Exception):
    pass

# Eccezione lper quando si tenta di dividere per zero
class ZeroDivisionError(Exception):
    pass

# Eccezione per quando si tenta di accedere a un indice non valido di un array: indice non intero positivo
class InvalidIndexError(Exception):
    pass

# Eccezione per quando si tenta di creare una variabile già presente nell'ambiente
class VariableAlreadyExistsException(Exception):
    pass

# Eccezione per quando si incontra un'espressione non valida
class InvalidExpressionError(Exception):
    pass


class Stack:

    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.data == []:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[0:-1]
        return res

    def __str__(self):
        return " ".join([str(s) for s in self.data])
    
    # Metodo per calcolare quanti elememnti sono presenti nello stack
    def len(self):
        return len(self.data)


class Expression:
    """
    La classe Expression ha il compito di valutare le espressioni e convertire la stringa di testo fornita in un albero di espressioni.
    Vengono passati in input la stringa di testo contenente l'espressione (text) e
    il dizionario (dispactch) che contiene le operazioni implementate nel codice.
    Il metodo di classe from_program ritorna l'espressione valutata sotto forma di un unico oggetto della classe Expression.

    Viene utilizzato uno stack per tenere traccia delle espressioni valutate: 
    per ogni elemento dell'espressione fornita
    - viene aggiunta una costante o una variabile allo stack, a seconda dell'oggetto presente nell'espressione
    - quando si incontra un operatore (che sia matematico, booleano o di altro tipo)
    - si estraggono dallo stack gli elementi necessari per l'operazione
    - viene costruito un oggetto corrispondente all'operazione effettuata e inserito nello stack
    
    Al termine della valutazione nello stack rimane l'oggetto corrispondente all'espressione completa

    Gli argomenti delle operazioni non matematiche o booleane, come valloc, setq, setv e altre, vengono invertiti poiché 
    le operazioni stesse richiedono che gli argomenti siano nell'ordine in cui appaiono nella stringa di input.

    """
    def __init__(self):
        raise NotImplementedError()

    @classmethod
    def from_program(cls, text, dispatch):
    
        stack = Stack() 

        #per ogni elemento nell'espressione da valutare 
        for item in text.split():

            if item.isdigit(): #se è una costante viene creata una istanza della classe Constant e inserita nello stack
                stack.push( Constant(int(item)) )

            elif item in dispatch: #se è un operazione presente del dizionario

                # viene determinata l'arità dell'operatore
                arity = dispatch[item].arity

                if arity >0:
                    #viene verificato che ci siano abbastanza operatori nello stack per svolgere l'operazione
                    if stack.len() < arity:
                        raise ValueError(f"Non ci sono abbastanza operandi per l'operazione {item}")

                    #vengono estratti gli operatori necessari all'operaione
                    args = [stack.pop() for _ in range(arity)]
                    # se l'operatore estratto è una variabile viene preso il nome, altrimenti è una costante
                    args = [arg.name if isinstance(arg, Variable) else arg for arg in args]

                    # Inversione degli argomenti per le operazioni che lo richiedono
                    if not issubclass(dispatch[item],Operation):
                        args = args[::-1]

                    #viene creata un'istanza dell'operazione effettuata 
                    op_instance = dispatch[item](args)
                else:
                    op_instance = dispatch[item]()

                #l'operazione viene inserita nello stack
                stack.push(op_instance)

            else: #altrimenti è una variabile, viene creato un oggetto Variable e inserito nello stack
                stack.push(Variable(item))

        # al terimine della valutazione nello stack deve rimanere un oggetto contenente il risultato dell'espressione, altrimenti è avvenuto un errore 
        if stack.len() != 1:
            raise InvalidExpressionError("Espressione non valida")
        
        return stack.pop() #viene estratto il risultato 
    
    # il metodo evaluate è stato implementato nelle sottoclassi
    def evaluate(self, env):
        raise NotImplementedError()


class Variable(Expression):
    # Classe le cui istanze rappresentano variabili

    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        # Viene ritornato il valore assegnato alla varibile se questa è presente nell'ambiente
        # Altrimenti viene sollevata l'eccezzione MissingVariableException

        if self.name not in env:
            raise MissingVariableException(f"La variabile {self.name} non è presente nell'ambiente")
        else:
            return env[self.name]

    def __str__(self):
        return self.name


class Constant(Expression):
    # Classe le cui istanze rappresentano costanti

    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

    def __str__(self):
        return str(self.value)


class Operation(Expression):
    # Sottoclasse di Expression che gestiste le operazioni matematiche implementate in seguito
    # Ogni operazione necessita di argomenti (args), a seconda del numero di argomenti richiesto verranno implementate due sottoclassi: BinaryOp e UnaryOP

    def __init__(self, args):
        self.args = args

    def evaluate(self, env):
        #lista degli argomenti valutati
        evaluated_args = []

        for arg in self.args: # per ogni argomento

            # se questo è un espressione viene valutata
            if isinstance(arg, Expression):
                evaluated_args.append(arg.evaluate(env)) #e aggiunta alla lista degli argomenti valutati 
            
            elif isinstance(arg,str): #se è una stringa, dunque una variabile 
                if arg in env:
                    evaluated_args.append(env[arg]) #viene aggiunta alla lista se è già presente l'ambiente 
                else:
                    raise MissingVariableException(f"Manca il valore della variabile '{arg}")
            else:
                evaluated_args.append(arg) 
        
        return self.op(*evaluated_args) #ritorniamo il risultato di ogni argomento nella lista



class BinaryOp(Operation):
    # Sottoclasse di Operation che comprende le operazioni che richiedono due argomenti
    arity = 2

    def __init__(self, args):
        self.x=args[0]
        self.y=args[1]
        super().__init__([self.x, self.y])


class UnaryOp(Operation):
    # Sottoclasse di Operation che comprende le operazioni che richiedono un solo argomento
    arity = 1
    def __init__(self,args):
        self.x=args[0]
        super().__init__([self.x])



class Addition(BinaryOp):
    # Vengono implementati un metodo op che ritorna il risultato dell'operazione e un metodo __str__  

    def op(self, x, y):
        return x + y
    
    def __str__(self):
        return f"(+ {self.x} {self.y})"


class Subtraction(BinaryOp):
    # Vengono implementati un metodo op che ritorna il risultato dell'operazione e un metodo __str__ 

    def op(self, x, y):
        return x - y 
    
    def __str__(self):
        return f"(- {self.x} {self.y})"


class Division(BinaryOp):
    # Vengono implementati un metodo op che ritorna il risultato dell'operazione e un metodo __str__ 

    def op(self, x, y):
        if y==0:
            raise ZeroDivisionError("Non è possibile dividere per zero")
        else:
            return x / y
        
    def __str__(self):
        return f"(/ {self.x} {self.y})"


class Multiplication(BinaryOp):
    # Vengono implementati un metodo op che ritorna il risultato dell'operazione e un metodo __str__ 

    def op(self, x, y):
        return x * y
    
    def __str__(self):
        return f"(* {self.x} {self.y})"


class Power(BinaryOp):
    # Vengono implementati un metodo op che ritorna il risultato dell'operazione e un metodo __str__ 

    def op( self, x, y):
        return x ** y
    
    def __str__(self):
        return f"(** {self.x} {self.y})"


class Modulus(BinaryOp):
    # Vengono implementati un metodo op che ritorna il risultato dell'operazione e un metodo __str__ 

    def op(self, x, y):
        return x % y
    
    def __str__(self):
        return f"(% {self.x} {self.y})"


class Reciprocal(UnaryOp):
    # Vengono implementati un metodo op che ritorna il risultato dell'operazione e un metodo __str__ 

    def op(self, x):
        if x==0:
            raise ZeroDivisionError("Non è possibile dividere per zero")
        else: 
            return 1 / x
    
    def __str__(self):
        return f"(1/ {self.x})"


class AbsoluteValue(UnaryOp):
    # Vengono implementati un metodo op che ritorna il risultato dell'operazione e un metodo __str__ 

    def op(self, x):
        return abs(x)
    
    def __str__(self):
        return f"(abs {self.x})"
    

class Grater(BinaryOp):
    # Vengono implementati un metodo op che ritorna un valore booleano, e un metodo __str__ 

    def op(self, x, y):
        return x > y
    
    def __str__(self):
        return f"(> {self.x} {self.y})"
    

class GraterEq(BinaryOp):
    # Vengono implementati un metodo op che ritorna un valore booleano, e un metodo __str__ 

    def op(self, x, y):
        return x >= y
    
    def __str__(self):
        return f"(>= {self.x} {self.y})"
    

class Equal(BinaryOp):
    # Vengono implementati un metodo op che ritorna un valore booleano, e un metodo __str__ 

    def op(self, x, y):
        return x == y 
    
    def __str__(self):
        return f"(= {self.x},{self.y})"
    

class NotEqual(BinaryOp):
    # Vengono implementati un metodo op che ritorna un valore booleano, e un metodo __str__ 

    def op(self, x, y):
        return  x != y
    
    def __str__(self):
        return f"(!= {self.x},{self.y})"
    

class Less(BinaryOp):
    # Vengono implementati un metodo op che ritorna un valore booleano, e un metodo __str__ 

    def op(self, x, y):
        return  x < y
    
    def __str__(self):
        return f"(< {self.x},{self.y})"
    

class LessEq(BinaryOp):
    # Vengono implementati un metodo op che ritorna un valore booleano, e un metodo __str__ 

    def op(self, x, y):
        return x <= y
    
    def __str__(self):
        return f"(<= {self.x},{self.y})"
    

class Alloc(Expression):
    # Alloca una variabile e le assegna il valore zero di default
    # L'attributo arity comune a tutte le istanze rappresenta il numero di argomenti, in questo caso si può quindi allocare una sola variabile 

    arity = 1

    def __init__(self, args):
        self.var = args[0] #variabile da allocare

    def evaluate(self, env):
    
        env[self.var] = 0  #nell'ambiente ora sarà presente la variabile self.var con valore zero
        
        
    def __str__(self):
        return f"alloc({self.var})"

    

class Valloc(Expression): 
    # Viene allocato un array x di n elementi tutti con il valore di default zero
    arity = 2

    def __init__(self,args):
        self.n = args[0]  # dimensione dell'array
        self.x = args[1]  # nome dell'array

    def evaluate(self,env):
    
        # se n è il risultato di un espressione, questa viene valutata
        n = self.n.evaluate(env)
        
        # il valore n deve essere un numero intero positivo poichè rappresenta la dimensione dell'array
        if not isinstance(n, int) or n < 0:
            raise InvalidIndexError(f" La dimensione dell'array {n} deve essere un numero intero positivo")
        
        env[self.x] = [0] * n
        

    def __str__(self):
        return f"valloc({self.n} {self.x})"


class Setq(Expression):
    # Imposta il valore della variabile x al risultato dell'espressione expr
    arity = 2

    def __init__(self,args):
        self.expr = args[0]  #espressione
        self.x = args[1]     #variabile

    def evaluate(self,env):

        # si valuta l'espressione, viene considerato anche il caso in cui expr è un valore costante
        value = self.expr.evaluate(env) if isinstance(self.expr, Expression) else self.expr

        # la variabile x deve essere già presente nell'ambiente
        if self.x not in env:
            raise MissingVariableException(f" La variabile {self.x} non è presente nell'ambiente")
        
        env[self.x] = value

        # viene ritornato il valore della variabile x
        return env[self.x]

    def __str__(self):
        return f"setq ({self.expr} {self.x})"


class Setv(Expression):
    # L'operazione Setv necessita di tre argomenti: espressione expr, posizione n, array x
    # Assegna alla posizione n-esima dell'array x la valutazione dell'apressione expr
    arity = 3

    def __init__(self, args):
        self.expr = args[0]  # espressione
        self.n = args[1]      # posizione n
        self.x = args[2]      # array 

    def evaluate(self, env):

        # viene considerato anche il caso in cui n sia un espressione e necessita di essere valutata
        if isinstance(self.n,Expression):
            n = self.n.evaluate(env)

        # se n è una varibile, viene recuperato il suo valore
        elif isinstance(self.n, str):
            if self.n in env:
                n = env[self.n]
            else:
                raise MissingVariableException(f"La variabile {self.n} non è presente nell'ambiente")
            
        # altrimenti n è un valore costante
        else:
            n = self.n

        # il valore n deve essere un numero intero positivo poichè rappresenta la dimensione dell'array
        if not isinstance(n, int) or n < 0:
            raise InvalidIndexError(f" La dimensione dell'array {n} deve essere un numero intero positivo")
        
        var = str(self.x)

        # l'array x deve già essere presente nell'ambiente 
        if var not in env:
            raise MissingVariableException(f"L'array {self.x} non è presente nell'ambiente")
        
        # se si sta provando ad accedere ad una posizione dell'array che non esiste viene sollevata un'eccezzione
        if n >= len(env[var]):
            raise IndexError("Errore: si sta provando ad accedere ad un indice che non esiste")
        
        # valutazione dell'espressione
        value = self.expr.evaluate(env) 
        
        env[var][n] = value 

        # viene ritornato il valore dall'array nella posizione n
        return value  
    
    def __str__(self):
        return f"setv({self.expr},{self.n},{self.x})"


class Prog(Expression):
    """ 
    La classe Prog è una classe generale per implementare le operazioni prog2, prog3, prog4 che valutano le 2,3,4 espressioni precedenti
    e ritornano il risultato della prima espressione.
    Il metodo evaluate, poichè viene ereditato da Prog2, Prog3 e Prog4, viene implementato solo in questa classe.
    
    Le sottoclassi sono indicate nel dizionario delle operazioni e saranno queste ad essere presenti nelle espressioni.
    """
    def __init__(self, args):
        self.args = args

    def evaluate(self, env):

        # vengono valutate le espressioni in ordine inverso e restituita la prima 
        for expr in self.args[::-1]:
            result = expr.evaluate(env)
        return result
    
    def __str__(self):
        return f"{type(self).__name__}({', '.join(map(str, self.args))})"


class Prog2(Prog):
    # Eredita i metodi da Prog
    arity = 2

    def __init__(self,args):
        super().__init__(args)


class Prog3(Prog):
    # Eredita i metodi da Prog
    arity = 3

    def __init__(self,args):
        super().__init__(args)


class Prog4(Prog):
    # Eredita i metodi da Prog
    arity = 4

    def __init__(self,args):
        super().__init__(args)


class If(Expression):
    # Operazione di controllo if-else
    arity = 3

    def __init__(self, args):
        self.false = args[0]  # espressione associata al ramo falso 
        self.true = args[1]   # espressione associata al ramo vero
        self.cond = args[2]   # condizione da valutare 

    def evaluate(self,env):

        # valutare la condizione dell'if
        if isinstance(self.cond, Expression):
            condition = self.cond.evaluate(env)

        # se cond è una variabile viene considerato il suo valore 
        elif isinstance(self.cond, str):
            if self.cond in env:
                condition = env[self.cond]
            else:
                raise MissingVariableException(f"La varibaile {self.cond} non è presente nell'ambiente")
        else:
            condition = self.cond 

        # se la condizone è vera, valuta l'espressione nel ramo vero, altrimenti valta quella nel ramo falso 
        if condition is True:
            return self.true.evaluate(env) if isinstance(self.true, Expression) else self.true
        else: 
            return self.false.evaluate(env) if isinstance(self.false, Expression) else self.false
        
    def __str__(self):
        return f"if ({self.false} {self.true} {self.cond})"


class While(Expression):
    # Implementazione del costrutto while 
    arity = 2

    def __init__(self, args):
        self.expr = args[0]  # espressione 
        self.cond = args[1]  # condizione del while

    def evaluate(self, env):
        
        # valuta l'espressione finchè la condizione rimane vera
        while self.cond.evaluate(env):
            self.expr.evaluate(env)

    def __str__(self):
        return f"while ({self.expr} {self.cond}) "
        

class For(Expression):
    # Implementazione del ciclo for che valuta l'espressione expr con il valore i, da start a end-1 con incrementi di uno
    arity = 4 

    def __init__(self, args):
        self.expr = args[0]   # espressione 
        self.end = args[1]    # fine ciclo
        self.start = args[2]  # inizio ciclo
        self.i = args[3]      # variabile i

    def evaluate(self, env):
        # valuta start e end come espressioni o come variabili 
        start = self.start.evaluate(env) if isinstance(self.start, Expression) else self.start
        end = self.end.evaluate(env) if isinstance(self.end, Expression) else self.end
       
        # ciclo for da start a end (escluso)
        for i in range(start, end):
            env[str(self.i)] = i     # assegna il valore dell'indice alla variabile di controllo
            self.expr.evaluate(env)  # esegui l'espressione all'interno del ciclo

    def __str__(self):
        return f"for({self.expr}, from {self.start} to {self.end}, {self.i})"

        
class DefSub(Exception):
    # Con questa operazione si possono definire delle subroutine
    arity = 2

    def __init__(self, args):
        self.expr = args[0] # espressione 
        self.var = args[1]  # variabile

    def evaluate(self, env):
        # l'espressione viene associata alla variabile e non viene valutata
        env[str(self.var)] = self.expr

    def __str__(self):
        return f"defsub({self.expr} {self.var})"
    

class Call(Expression):
    # Valuta l'espressione associata a f definita tramite defsub
    arity = 1

    def __init__(self,args):
        self.f = args[0] 

    def evaluate(self,env):
        # la funzione deve essere già definita
        if self.f not in env:
            raise MissingFunctionException(f"La funzione {self.f} non è presente nell'ambiente")
        
        # valuta l'espressione associata alla funzione 
        expression = env[str(self.f)]
        return expression.evaluate(env)

    def __str__(self):
        return f"call ({self.f})"


class Print(Expression):
    # Valuta l'espressione expr e stampa il risultato, inoltre ritorna il valore dell'espressione
    arity = 1

    def __init__(self,args):
        self.expr = args[0]

    def evaluate(self, env):

        # gestiamo ogni caso di expr: che sia un'espressione,una variabile o una costante
        if isinstance(self.expr, Expression):
            result = self.expr.evaluate(env)
        elif isinstance(self.expr, str): 
            if self.expr in env:
                result = env[self.expr]
            else:
                raise MissingVariableException(f"Valore mancante per la variabile '{self.expr}'")
        else:
            result = self.expr  # gestisci i valori costanti

        # stampa e ritorna il risultato
        print(result)
        return result
    
    def __str__(self):
        return f"print({self.expr})"
    

class Nop(Expression):
    # Non svolge nessuna operazione 
    arity=0

    def __init__(self):
        pass

    def evaluate(self, env):
        return None
    
    def __str__(self):
        return "nop"

# Dizionario delle operazioni
d = {"+": Addition, "*": Multiplication, "**": Power, "-": Subtraction, "/": Division,
     "%": Modulus, "1/": Reciprocal, "abs": AbsoluteValue,
     ">": Grater,">=": GraterEq, "=": Equal,"!=": NotEqual, "<": Less, "<=": LessEq,
     "alloc": Alloc, "valloc": Valloc, "setq": Setq, "setv": Setv,
     "prog2": Prog2, "prog3": Prog3, "prog4":Prog4,
     "if": If,"while": While, "for": For,
     "desub": DefSub, "call": Call, "print": Print, "nop":Nop}


example =  "0 2 -"
e = Expression.from_program(example, d)

print(e)
res = e.evaluate({})
print(res)
