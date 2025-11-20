import re
from typing import Any, Callable, List, Dict
from enum import Enum

# ==========================================
# 1. KERNEL EMBEDDINGS
# ==========================================

class RuleType(Enum):
    HARD = "hard"
    SOFT = "soft"

class Rule:
    def __init__(self, name: str, kind: RuleType, logic: Callable):
        self.name = name
        self.kind = kind
        self.logic = logic
        self.active = True

class Generator: # Data Type Representation (G)
    def __init__(self, name: str, py_cls: Any):
        self.name = name
        self.py_cls = py_cls

class Module: # COMPOSITION (C) - Isolated world
    def __init__(self, name: str):
        self.name = name
        self.generators: Dict[str, Generator] = {}
        self.rules: List[Rule] = []
        self.transformations: Dict[str, Callable] = []

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

# ==========================================
# 2. SYSTEM KERNEL (SYSTEM CONTEXT)
# ==========================================

class PhiSystem:
    def __init__(self):
        self.modules: Dict[str, Module] = {}
        self.current_module: Module = None # Indicator: Where are we now?

    def create_module(self, name: str):
        print(f"[System] Creating a new module: '{name}'")
        mod = Module(name)
        self.modules[name] = mod
        self.current_module = mod # We switch the context to the new module
        return mod

    def get_module(self, name: str):
        return self.modules.get(name)

class Validator:
    """The validator knows which module the code is running in and only uses local rules"""
    def validate(self, module_name: str, func_name: str, func: Callable, args: List[Any], system: PhiSystem):
        
        target_module = system.get_module(module_name)
        if not target_module:
            print(f"ERROR: Module not found {module_name}")
            return False

        print(f"\n--- [V*] Validation in the context of the module: '{module_name}' ---")
        print(f"    Function: {func_name}")

        # 1. Execution
        try:
            result = func(*args)
            print(f"    Result: {result}")
        except Exception as e:
            print(f"    EXECUTION ERROR: {e}")
            return False

        # 2. Checking LOCAL Rules for this module
        # This is the Composition key (C) - we only check what applies HERE.
        for rule in target_module.rules:
            if not rule.active: continue
            
            try:
                is_ok = rule.logic(*args)
            except Exception:
                continue # The rule does not match the data type.

            if is_ok:
                print(f"    [OK] Rule '{rule.name}' fulfilled.")
            else:
                print(f"    [!] CONFLICT with the rule '{rule.name}' ({rule.kind.value})")
                
                if rule.kind == RuleType.HARD:
                    print("    [STOP] Violation of the HARD rule. I reject.")
                    return False
                elif rule.kind == RuleType.SOFT:
                    print(f"    [AI-FIX] The rule is SOFT. In this module ('{module_name}') I turn it off.")
                    rule.active = False
                    # Rekursja - sprawdź ponownie
                    return self.validate(module_name, func_name, func, args, system)

        print(f"--- [V*] STATUS: ACCEPT ({module_name}) ---")
        return True

# ==========================================
# 3. PARSER (WITH MODULE SUPPORT)
# ==========================================

class PhiParser:
    def __init__(self, system: PhiSystem):
        self.system = system

    def parse(self, code: str):
        lines = code.split('\n')
        print("\n>>> [PARSER] Modular structure analysis...")
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"): continue

            # A. Detecting the beginning of a module: "module Name {"
            if line.startswith("module"):
                match = re.search(r"module\s+(\w+)", line)
                if match:
                    mod_name = match.group(1)
                    self.system.create_module(mod_name)
            
            # B. End of module detection: "}"
            elif line == "}":
                # We exit the module (in a simple parser we do nothing, 
                # because create_module sets current, and the next module will overwrite it)
                pass

            # C. Parsing the interior (adding to current_module)
            elif self.system.current_module:
                self._parse_instruction(line)

    def _parse_instruction(self, line):
        # 1. Generators (date)
        if line.startswith("data"):
            name = line.split()[1]
            # Mapping to Python classes (mockup)
            py_cls = globals().get(name)
            self.system.current_module.generators[name] = Generator(name, py_cls)
            print(f"    + [G] Type added '{name}' to the module '{self.system.current_module.name}'")

        # 2. Rules (axiom)
        elif line.startswith("axiom"):
            # axiom name : type (logic)
            parts = line.split(":")
            header = parts[0].strip()
            body = parts[1].strip()
            name = header.split()[1]
            
            kind = RuleType.SOFT if "soft" in body else RuleType.HARD
            logic = self._resolve_logic(name)
            
            rule = Rule(name, kind, logic)
            self.system.current_module.add_rule(rule)
            print(f"    + [R] Rule added '{name}' to the module '{self.system.current_module.name}'")

    def _resolve_logic(self, name):
        if name == "commutativity": return lambda a, b: a * b == b * a
        if name == "identity": return lambda a: a == a
        return lambda *args: True

# ==========================================
# 4. DATA IMPLEMENTATIONS (G)
# ==========================================

class Number: # Commutative
    def __init__(self, v): self.v = v
    def __repr__(self): return f"Num({self.v})"
    def __mul__(self, other): return Number(self.v * other.v)
    def __eq__(self, other): return self.v == other.v

class Matrix: # Now it's real, immutable!
    def __init__(self, v): self.v = v
    def __repr__(self): return f"Mat{self.v}"
    
    def __mul__(self, other): 
        # True 2x2 matrix multiplication
        # c[i][j] = sum(a[i][k] * b[k][j])
        result = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    result[i][j] += self.v[i][k] * other.v[k][j]
        return Matrix(result)
        
    def __eq__(self, other): return self.v == other.v

# ==========================================
# 5. COMMISSIONING (ARCHITECT)
# ==========================================

if __name__ == "__main__":
    # We define the source code with two different worlds
    source_code = """
    // Arithmetic Module (Standard)
    module Arithmetic {
        data Number
        // Here, the commutativity is HARD, because it is the definition of numbers
        axiom commutativity : hard ( a * b == b * a )
    }

    // Matrix Algebra Module (Experimental)
    module LinearAlgebra {
        data Matrix
        // Here the commutativity is SOFT, because we know that matrices are hard
        axiom commutativity : soft ( a * b == b * a )
    }
    """

    # 1. Initialization
    sys = PhiSystem()
    parser = PhiParser(sys)
    
    # 2. Parsing (Building a C Structure)
    parser.parse(source_code)
    validator = Validator()

    # --- TEST 1: ARITHMETIC (Should pass, HARD rule met) ---
    print("\n>>> TEST 1: Arithmetic Environment")
    n1 = Number(2)
    n2 = Number(3)
    # Number multiplication function
    def mult_nums(a, b): return a * b
    
    # We validate in the context of Arithmetic
    validator.validate("Arithmetic", "multiply", mult_nums, [n1, n2], sys)


    # --- TEST 2: MATRICES (This should trigger a repair because the SOFT rule is not met) ---
    print("\n>>> TEST 2: LinearAlgebra environment")
    # Non-commutative matrices (A*B != B*A)
    m1 = Matrix([[1, 0], [0, 0]])
    m2 = Matrix([[0, 1], [0, 0]])
    def mult_mats(a, b): return a * b

    # We validate in the context of LinearAlgebra
    # We expect: Conflict -> SOFT detection -> Rule disable -> ACCEPT
    validator.validate("LinearAlgebra", "mat_multiply", mult_mats, [m1, m2], sys)