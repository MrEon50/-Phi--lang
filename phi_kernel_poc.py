import inspect
from enum import Enum
from typing import Callable, Any, List, Dict

# --- 1. FUNDAMENTAL DEFINITIONS (CORE THEORY) ---

class RuleType(Enum):
    HARD = "hard"   # Stone: Unmovable (Logical Foundation)
    SOFT = "soft"   # Paper/Scissors: Negotiable (Convention/Strategy)

class PhiContext:
    """Represents the state of knowledge (Ontology G and Rules R)"""
    def __init__(self):
        self.generators: Dict[str, Any] = {}  # G
        self.rules: List['Rule'] = []         # R
        self.transformations: Dict[str, Callable] = [] # T

    def register_generator(self, name, cls):
        print(f"[G] Type registration: {name}")
        self.generators[name] = cls

    def register_rule(self, rule):
        print(f"[R] Rule registration: {rule.name} ({rule.kind.value})")
        self.rules.append(rule)

class Rule:
    """Single logical rule"""
    def __init__(self, name: str, predicate: Callable, kind: RuleType = RuleType.HARD):
        self.name = name
        self.predicate = predicate
        self.kind = kind
        self.active = True

    def check(self, *args):
        if not self.active: return True
        return self.predicate(*args)

# --- 2. BRAIN SYSTEM (NEURO-SYMBOLIC VALIDATOR) ---

class NeuralProposer:
    """Neural network simulation. In the full version, this would be the PyTorch model."""
    def propose_fix(self, rule: Rule, context: str):
        # Heuristic: If the rule is SOFT and the context is complex (e.g. matrix),
        # the network proposes to suspend it.
        if rule.kind == RuleType.SOFT:
            return "RELAX_RULE"
        return "REJECT_TRANSFORMATION"

class Validator:
    """V Engine* - Manages the validation loop"""
    def __init__(self):
        self.nn = NeuralProposer()

    def validate_transformation(self, func_name: str, func: Callable, test_data: List[Any], context: PhiContext):
        print(f"\n--- [V*] Transformation Validation: {func_name} ---")
        
        # Faza 1: Test run (Execution)
        try:
            result = func(*test_data)
            print(f"    Execution: Success. Result = {result}")
        except Exception as e:
            print(f"    Execution error: {e}")
            return False

        # Faza 2: Rule Check (R-Check)
        all_passed = True
        for rule in context.rules:
            if not rule.active: continue
            
            is_valid = rule.check(*test_data)
            print(f"    Checking the rule '{rule.name}': {'OK' if is_valid else 'FAIL'}")
            
            if not is_valid:
                # CONFLICT DETECTED!
                print(f"    [!] CONFLICT: Transformation '{func_name}' breaks the rule '{rule.name}'")
                
                # Faza 3: Repair Loop (R-G-T Loop)
                decision = self.nn.propose_fix(rule, context="ComplexStructure")
                
                if decision == "RELAX_RULE":
                    print(f"    [AI Decision] Rule is 'SOFT'. System adapts R to G.")
                    print(f"    [R] STATUS CHANGE: Disabling the rule '{rule.name}' for this context.")
                    rule.active = False
                    # Revalidation (recursion or continue)
                    print(f"    [V*] Revalidation after repair...")
                    return self.validate_transformation(func_name, func, test_data, context)
                
                elif decision == "REJECT_TRANSFORMATION":
                    print(f"    [AI Decision] Rule is 'HARD'. Transformation rejected.")
                    return False

        print(f"--- [V*] Status: ACCEPT ---\n")
        return True

# --- 3. TEST SCENARIO (MATHEMATICS) ---

# We define simple mathematical structures (G)
class Number:
    def __init__(self, v): self.v = v
    def __repr__(self): return f"Num({self.v})"
    def __mul__(self, other): return Number(self.v * other.v)
    def __eq__(self, other): return self.v == other.v

class Matrix:
    def __init__(self, v): self.v = v # Simplified: v to [[a,b], [c,d]]
    def __repr__(self): return f"Mat({self.v})"
    def __eq__(self, other): return self.v == other.v
    # Matrix multiplication (non-commutative!)
    def __mul__(self, other):
        # Simple 2x2 multiplication for demo
        a1, b1, c1, d1 = self.v[0][0], self.v[0][1], self.v[1][0], self.v[1][1]
        a2, b2, c2, d2 = other.v[0][0], other.v[0][1], other.v[1][0], other.v[1][1]
        return Matrix([
            [a1*a2 + b1*c2, a1*b2 + b1*d2],
            [c1*a2 + d1*c2, c1*b2 + d1*d2]
        ])

# Activation
if __name__ == "__main__":
    # 1. Environment Initialization
    ctx = PhiContext()
    
    # 2. We define G (Ontology)
    ctx.register_generator("Number", Number)
    ctx.register_generator("Matrix", Matrix)

    # 3. We define R (Rules)
    # HARD: Identity Coherence (a = a)
    ctx.register_rule(Rule(
        "identity_consistency", 
        lambda a, b: a == a, 
        RuleType.HARD
    ))
    
    # SOFT: Commutative property of multiplication (a * b = b * a)
    # This is a rule that applies to Numbers, but fails to apply to Matrices.
    ctx.register_rule(Rule(
        "commutativity", 
        lambda a, b: (a * b) == (b * a), 
        RuleType.SOFT
    ))

    # 4. We define T (Transformation) - Multiplication operation
    # In Python, __mul__ is our T transformation
    def multiply_op(a, b):
        return a * b

    validator = Validator()

    # SCENARIO A: Testing the Numbers (Should Go Smoothly)
    print("\n>>> SCENARIO A: Multiplying Numbers")
    n1 = Number(2)
    n2 = Number(3)
    validator.validate_transformation("multiply_numbers", multiply_op, [n1, n2], ctx)

    # Resetting the rule for test B (we assume that the rule is active again in the new module)
    ctx.rules[1].active = True 

    # SCENARIO B: Testing the Matrices (Conflict!)
    # Matrix multiplication A*B != B*A
    print(">>> SCENARIO B: Matrix Multiplication")
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[0, 1], [1, 0]])
    
    # V* should detect conflict with the 'commutativity' rule, 
    # notice that it is SOFT and turn it off.
    validator.validate_transformation("multiply_matrices", multiply_op, [m1, m2], ctx)