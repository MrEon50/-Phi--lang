import re
from typing import Any, Callable, List, Dict
from enum import Enum

# ==========================================
# PART 1: KERNEL V* - BRAIN
# ==========================================

class RuleType(Enum):
    HARD = "hard"
    SOFT = "soft"

class Rule:
    def __init__(self, name: str, kind: RuleType, logic_lambda: Callable):
        self.name = name
        self.kind = kind
        self.logic = logic_lambda
        self.active = True

class PhiContext:
    def __init__(self):
        self.generators = {} 
        self.rules = []
        
    def register_generator(self, name, obj):
        print(f"[G-Kernel] The structure was registered: {name}")
        self.generators[name] = obj
        
    def register_rule(self, rule: Rule):
        print(f"[R-Kernel] Rule registered: {rule.name} ({rule.kind.value})")
        self.rules.append(rule)

class Validator:
    def validate(self, func_name, func, args, ctx):
        print(f"\n--- [V*] Validation: {func_name} ---")
        # 1. Execution
        try:
            result = func(*args)
            print(f"    Result of the operation: {result}")
        except Exception as e:
            print(f"    CRITICAL ERROR: {e}")
            return False

        # 2. Checking the Rules
        for rule in ctx.rules:
            if not rule.active: 
                print(f"    (Rule '{rule.name}' is inactive - I skip it)")
                continue
            
            try:
                # Note: Here the Parser would normally convert the lambda to Python code.
                # For simplicity, we use predefined lambdas in the demo.
                is_ok = rule.logic(*args)
            except Exception:
                continue # The rule may not match the data type, we skip it

            if is_ok:
                print(f"    [OK] Rule '{rule.name}' fulfilled.")
            else:
                print(f"    [!] CONFLICT with the rule '{rule.name}'")
                if rule.kind == RuleType.HARD:
                    print("    [STOP] Violation of the HARD rule. I reject.")
                    return False
                else:
                    print(f"    [AUTO-FIX] The rule is SOFT. I'm turning it off for this case.")
                    rule.active = False
                    # Recursion - we check again with the rule disabled
                    return self.validate(func_name, func, args, ctx)
        
        print("--- [V*] STATUS: ACCEPT ---")
        return True

# ==========================================
# PART 2: PARSER - TEXT TRANSLATOR
# ==========================================

class PhiParser:
    """
    A simple parser that reads text in Phil-Lang format and calls the appropriate methods in the Kernel (Context).
    """
    def __init__(self, context: PhiContext):
        self.context = context

    def parse(self, source_code: str):
        lines = source_code.split('\n')
        print("\n>>> [PARSER] I'm starting to analyze the source code...")
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"): continue

            # 1. Parsing Generators (data Name)
            if line.startswith("data"):
                # Pattern: data Name ...
                match = re.search(r"data\s+(\w+)", line)
                if match:
                    name = match.group(1)
                    # In a real compiler we create the class dynamically here.
                    # In the demo we map a name to an existing Python class.
                    py_cls = globals().get(name) 
                    if py_cls:
                        self.context.register_generator(name, py_cls)
                    else:
                        print(f"    [Parser Warning] No implementation found for: {name}")

            # 2. Parsing Rules (axiom name : type (logic))
            elif line.startswith("axiom"):
                # Pattern: axiom name: soft/hard
                parts = line.split(":")
                if len(parts) >= 2:
                    header = parts[0].strip() # "axiom commutativity"
                    body = parts[1].strip()   # "soft (a*b == b*a)"
                    
                    rule_name = header.split()[1]
                    
                    rule_type = RuleType.HARD
                    if "soft" in body: rule_type = RuleType.SOFT
                    
                    # In the demo we need to "pin" the Python logic to the name from the text
                    logic = self._resolve_logic(rule_name)
                    
                    new_rule = Rule(rule_name, rule_type, logic)
                    self.context.register_rule(new_rule)

            # 3. Parsing Transformation (def name ...)
            elif line.startswith("def"):
                print(f"    [Parser] Function definition found: {line.split()[1]}")

        print(">>> [PARSER] Analysis completed. Kernel configured..\n")

    def _resolve_logic(self, name):
        """A helper method that maps names from a text file to Python lambdas."""
        if name == "commutativity":
            return lambda a, b: a * b == b * a
        if name == "identity":
            return lambda a: a == a
        return lambda *args: True

# ==========================================
# PART 3: MATHEMATICAL IMPLEMENTATION (G)
# ==========================================

class Matrix:
    def __init__(self, v): self.v = v
    def __repr__(self): return f"Mat{self.v}"
    def __mul__(self, other):
        # Simple multiplication for demo (non-commutative)
        return Matrix([[self.v[0][0] * other.v[0][0]]]) # Simplified
    def __eq__(self, other): return self.v == other.v

# ==========================================
# PART 4: MAIN PROGRAM (IDE SIMULATION)
# ==========================================

if __name__ == "__main__":
    # 1. We have a "text file" (simulation of what the programmer writes)
    source_code_phi = """
    // This is the code in Phil-lang
    
    // 1. Generators (Ontology)
    Data Matrix
    
    // 2. Rules (Logic) - Notice the keyword 'soft'
    axiom identity : hard ( a == a )
    axiom commutativity : soft ( a * b == b * a )
    
    // 3. Transformations
    def matrix_multiply : Matrix -> Matrix -> Matrix
    """

    # 2. System Initialization
    ctx = PhiContext()     # Empty Core
    parser = PhiParser(ctx) # Parser connected to the Kernel

    # 3. The parser reads the text and feeds it to the kernel.
    parser.parse(source_code_phi)

    # ... (the rest of the code remains unchanged) ...

    # 4. We run Kernel Validation on the data (Runtime)
    val = Validator()
    
    print("--- STARTING THE USER PROGRAM ---")
    
    # CHANGE: We use 2x2 matrices, which are NOT commutative.
    # A = [[1, 0], [0, 0]]
    # B = [[0, 1], [0, 0]]
    # A*B = [[0, 1], [0, 0]], but B*A = [[0, 0], [0, 0]]

    # We just need to slightly tweak the Matrix class in the code (Part 3),
    # because that one was simplified to 1x1.
    # Below is the full, replaced Matrix class and test:

    # (Paste this in place of the old Matrix class in Part 3)
    class Matrix:
        def __init__(self, v): self.v = v
        def __repr__(self): return f"Mat{self.v}"
        def __mul__(self, other):
            # Full 2x2 matrix multiplication
            val = [[0,0],[0,0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        val[i][j] += self.v[i][k] * other.v[k][j]
            return Matrix(val)
        def __eq__(self, other): return self.v == other.v

    m1 = Matrix([[1, 0], [0, 0]])
    m2 = Matrix([[0, 1], [0, 0]])
    
    def run_matrix_mult(a, b): return a * b

    val.validate("matrix_multiply", run_matrix_mult, [m1, m2], ctx)

    # working prototype of the $\Phi$ Language Compiler