import re
from typing import Any, Callable, List, Dict
from enum import Enum

# ==========================================
# 1. KERNEL STRUCTURES
# ==========================================

class RuleType(Enum):
    HARD = "hard"
    SOFT = "soft"

class Rule:
    def __init__(self, name: str, kind: RuleType, logic: Callable, source_module: str):
        self.name = name
        self.kind = kind
        self.logic = logic
        self.source_module = source_module # Trace of the origin of the rule
        self.active = True

class Generator:
    def __init__(self, name: str, py_cls: Any):
        self.name = name
        self.py_cls = py_cls

class Module: 
    def __init__(self, name: str):
        self.name = name
        self.generators: Dict[str, Generator] = {}
        self.rules: List[Rule] = []
        self.imports: List['Module'] = [] # COMPOSITION (C) - Dependency List

    def add_rule(self, rule: Rule):
        self.rules.append(rule)
        
    def add_import(self, module):
        self.imports.append(module)

# ==========================================
# 2. SYSTEM KERNEL (SYSTEM CONTEXT)
# ==========================================

class PhiSystem:
    def __init__(self):
        self.modules: Dict[str, Module] = {}
        self.current_module: Module = None 

    def create_module(self, name: str):
        # If the module already exists, we return it (so we can edit/extend it)
        if name in self.modules:
            self.current_module = self.modules[name]
            return self.modules[name]
            
        print(f"[System] Creating a new module: '{name}'")
        mod = Module(name)
        self.modules[name] = mod
        self.current_module = mod 
        return mod

    def get_module(self, name: str):
        return self.modules.get(name)

class Validator:
    """RECURSIVE validator - checks its own AND imported rules"""
    
    def _collect_rules(self, module: Module, collected_rules: List[Rule], visited: set):
        """Collects rules from a module and its imports (avoids loops)"""
        if module.name in visited: return
        visited.add(module.name)
        
        # 1. Add rules for this module
        for rule in module.rules:
            collected_rules.append(rule)
            
        # 2. Recursion to imports
        for imp_mod in module.imports:
            self._collect_rules(imp_mod, collected_rules, visited)

    def validate(self, module_name: str, func_name: str, func: Callable, args: List[Any], system: PhiSystem):
        target_module = system.get_module(module_name)
        if not target_module:
            print(f"ERROR: Module not found {module_name}")
            return False

        print(f"\n--- [V*] Validation in: '{module_name}' (with imports) ---")
        print(f"    Function: {func_name}")

        # 1. Wykonanie
        try:
            result = func(*args)
            print(f"    Result: {result}")
        except Exception as e:
            print(f"    EXECUTION ERROR: {e}")
            return False

        # 2. Collecting ALL applicable rules (C - Composition)
        all_rules = []
        self._collect_rules(target_module, all_rules, set())
        
        print(f"    [Audit] I'm checking {len(all_rules)} rules (including imports)...")

        # 3. Verification
        for rule in all_rules:
            if not rule.active: continue
            
            try:
                is_ok = rule.logic(*args)
            except Exception:
                continue 

            if is_ok:
                # Optional: we don't spam OK for every rule, only for important ones
                pass 
            else:
                print(f"    [!] CONFLICT with the rule '{rule.name}' (Source: {rule.source_module})")
                
                if rule.kind == RuleType.HARD:
                    print("    [STOP] Violation of the HARD rule. Rejected.")
                    return False
                elif rule.kind == RuleType.SOFT:
                    print(f"    [AI-FIX] SOFT rule. I disable it locally.")
                    rule.active = False
                    return self.validate(module_name, func_name, func, args, system)

        print(f"--- [V*] STATUS: ACCEPT ---")
        return True

# ==========================================
# 3. PARSER (WITH IMPORT SUPPORT)
# ==========================================

class PhiParser:
    def __init__(self, system: PhiSystem):
        self.system = system

    def parse(self, code: str):
        lines = code.split('\n')
        print("\n>>> [PARSER] Code analysis...")
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"): continue

            if line.startswith("module"):
                match = re.search(r"module\s+(\w+)", line)
                if match: self.system.create_module(match.group(1))
            
            elif line.startswith("import"):
                # Składnia: import ModuleName
                match = re.search(r"import\s+(\w+)", line)
                if match and self.system.current_module:
                    imp_name = match.group(1)
                    imp_mod = self.system.get_module(imp_name)
                    if imp_mod:
                        self.system.current_module.add_import(imp_mod)
                        print(f"    + [C] Import modułu '{imp_name}' to '{self.system.current_module.name}'")
                    else:
                        print(f"    [!] Import error: Module '{imp_name}' unknown (must be defined beforehand)")

            elif self.system.current_module:
                self._parse_instruction(line)

    def _parse_instruction(self, line):
        if line.startswith("data"):
            # ... (simplified for readability, same as before)
            pass 

        elif line.startswith("axiom"):
            # axiom name : type (logic)
            parts = line.split(":")
            header = parts[0].strip()
            body = parts[1].strip()
            name = header.split()[1]
            kind = RuleType.SOFT if "soft" in body else RuleType.HARD
            logic = self._resolve_logic(name)
            # We save source_module!
            rule = Rule(name, kind, logic, self.system.current_module.name)
            self.system.current_module.add_rule(rule)
            print(f"    + [R] Rule added '{name}'")

    def _resolve_logic(self, name):
        if name == "nonzero": return lambda a, b: b != 0 # Division rule
        if name == "positive": return lambda a: a > 0
        return lambda *args: True

# ==========================================
# 4. TEST SCENARIO (Dependency Chain)
# ==========================================

if __name__ == "__main__":
    # We define a chain of dependencies
    source_code = """
    // 1. Core Module (Foundation)
    module CoreMath {
        // HARD rule of the universe: don't divide by 0
        axiom nonzero : hard ( b != 0 )
    }

    // 2. Finance Module (Builds on CoreMath)
    module Finance {
        import CoreMath
        // Finance adds its own rules, e.g., amounts must be positive (but this is soft, because debts exist)
        axiom positive : soft ( a > 0 )
    }
    """

    sys = PhiSystem()
    parser = PhiParser(sys)
    parser.parse(source_code)
    validator = Validator()

    # Division function (T)
    def safe_divide(a, b): return a / b

    # SCENARIO: We're trying to divide by zero in the FINANCE module.
    # Note: we did NOT write a "nonzero" rule in the Finance module.
    # But we did import CoreMath. The kernel should detect this.
    
    print("\n>>> TEST: Division by zero in the Finance module")
    # Division 100 / 0
    validator.validate("Finance", "calc_roi", safe_divide, [100, 0], sys)

    print("\n>>> TEST: Correct division")
    # Division 100 / 10
    validator.validate("Finance", "calc_roi", safe_divide, [100, 10], sys)