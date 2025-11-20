# 🚀 $\Phi$-lang Kernel Prototype

## Universal Mathematics with Neuro-Symbolic Validation

This project presents a **Proof-of-Concept (PoC)** for the $\Phi$-language, a meta-theory designed to serve as a **universal, self-validating framework for mathematics and computation**. Unlike traditional programming languages that strictly halt on type or assertion errors, $\Phi$-lang incorporates a **Neuro-Symbolic Validation Loop ($V^*$)** that allows the system to adapt its internal rules to new, conflicting contexts.

This paradigm is built on the core principle of **"Conditional Inheritance of Truth,"** where axioms and rules are not globally immutable but are dynamically checked and potentially relaxed based on the specific context (Module) in which they are applied.

Errors arise where there is a lack of framework...
framework ↔ space
restriction ↔ freedom
control ↔ expansion

And the best systems are neither completely restrictive nor completely open.
They create a "framework space"—a structure that is also stable in development.

"Order without freedom is dead, freedom without order is formless." chatGPT

"Idea for $\Phi$-lang with the $V^*$ validator has the potential to create a Universal Knowledge Engineering Language." Gemini 3


-----

## 💡 Theoretical Core: The G-T-R-C Architecture

The $\Phi$-lang Kernel implements the G-T-R-C architecture, conceptualizing the system as a structured **Semantic Embedding** for an underlying AI decision-maker.

  * **G (Generators):** The fundamental **data structures** or types (e.g., `Number`, `Matrix`). Defines the *reality* of a context.
  * **T (Transformations):** The **functions** or operations that act upon the Generators (e.g., `multiply`).
  * **R (Rules/Axioms):** The **logical constraints** or mathematical laws. They are characterized by a $\mathbf{Kind}$:
      * **HARD:** Non-negotiable (e.g., Identity, Non-Zero Division). Violation halts the system.
      * **SOFT:** Negotiable (e.g., Commutativity, Associativity). Violation triggers the $V^*$ loop.
  * **C (Composition):** The **Modularity** layer, enabling the creation of isolated environments (Modules) and managing dependencies between them via `import` statements.
  * **$V^*$ (Validator/Resolver):** The **Neuro-Symbolic Core**. It executes the G-T-R Validation Loop. When an **R**ule violation is detected:
    1.  It checks the rule's $\mathbf{Kind}$.
    2.  If the rule is **SOFT**, the $V^*$ system decides to **adapt** the environment by deactivating the rule *locally* to allow the Transformation to proceed, effectively creating a new, valid context. This mechanism dramatically reduces common programming errors stemming from rigid rule adherence.

-----

## 📂 Project Files and Architecture

The project is realized through two core files: the initial conceptual test, and the final modular system.

### `phi_full_system.py`

  * **Purpose:** Initial Proof-of-Concept (PoC). Demonstrates the basic **Parser** functionality and the **HARD/SOFT** rule mechanism in a single, flat namespace.
  * **Key Insight:** This code successfully simulated the **Soft Rule relaxation** when testing non-commutative $2 \times 2$ matrices against the general commutativity axiom.

### `phi_modular_system.py` (The Final Kernel)

This file contains the final, modular architecture demonstrating the power of **Composition (C)** and **"Conditional Inheritance of Truth"**.

| Component | Class/Code Snippet | Description |
| :--- | :--- | :--- |
| **Parser** | `PhiParser` | Translates the $\Phi$-lang source code (text) into structured Python objects for the Kernel. Handles `module`, `axiom`, and crucially, the **`import`** statement. |
| **Kernel Context** | `PhiSystem`, `Module` | The central structure. A `PhiSystem` is a collection of isolated `Module`s. Each `Module` holds its own local $G$ and $R$ and maintains a list of **imported dependencies ($C$)**. |
| **Validator** | `Validator` | Implements the $V^*$ loop. It performs a **recursive audit**: when validating a Module, it automatically checks rules from that Module *and* all rules inherited from its imported dependencies, ensuring cross-module consistency. |
| **Test Case** | `CoreMath` $\rightarrow$ `Finance` | Demonstrates the mechanism: `CoreMath` defines the `HARD` rule **`nonzero`** (no division by zero). `Finance` imports `CoreMath` and automatically inherits the $R$ constraint, successfully blocking a division-by-zero attempt without explicitly defining the rule locally. |

-----

## 🛠️ Execution and Verification

The successful execution of the final system confirms the architectural goals:

### Final Execution Log (Linear Algebra)

```text
>>> TEST 2: Środowisko LinearAlgebra
--- [V*] Walidacja w kontekście modułu: 'LinearAlgebra' ---
    Funkcja: mat_multiply
    Wynik: Mat[[0, 1], [0, 0]]
    [!] KONFLIKT z regułą 'commutativity' (soft)
    [AI-FIX] Reguła jest SOFT. W tym module ('LinearAlgebra') ją wyłączam.
    ...
--- [V*] STATUS: ACCEPT (LinearAlgebra) --- 
```

**Conclusion:** The system successfully demonstrated **Adaptation**. It recognized the conflict (non-commutative matrices), identified the rule as SOFT (negotiable), and performed an **Automatic Fix** by locally disabling the rule, thus preventing a runtime error and allowing the program to proceed in a mathematically validated state.

### Final Execution Log (Import Dependency)

When attempting to divide by zero in the `Finance` module:

```text
>>> TEST: Dzielenie przez zero w module Finance
--- [V*] Walidacja w: 'Finance' (z importami) ---
    Funkcja: calc_roi
    [!] KONFLIKT z regułą 'nonzero' (Źródło: CoreMath)
    [STOP] Naruszenie reguły HARD. Odrzucam.
```

**Conclusion:** The system successfully demonstrated **Compositional Safety**. The `HARD` rule from the imported `CoreMath` module was enforced in `Finance`, validating the core concept of **Conditional Inheritance of Truth**.