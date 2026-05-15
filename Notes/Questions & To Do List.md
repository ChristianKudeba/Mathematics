- Is Claude's Lean translation correct?
	- Have Claude comment about its translation decisions
- See a theorem's definition in right side panel when you click it in graph view along with useful info about the theorem
- Make graphs mergeable
	- check for equivalent theorems
- Every time you convert a paper, have an agent keep a log of how good of a job the translation agent did and eventually use that to update the translation skill
- What happens if a PDF under a Lean file generates another Lean file?
- Lean to Latex converter
- make the x's to close a file larger
- make the graph editable
- decide which axioms, definitions, lemmas, theorems to show
- make the graph prettier
- Have agents do research

To learn:
- Lean
	1. Kernel checking rules  
		- what counts as a valid term  
		- what counts as a valid type  
		- definitional equality  
		- reduction/computation  
	2. Universes  
		- Prop  
		- Type  
		- Type u  
	3. Terms and types  
		- t : α  
	4. Function types  
		- α → β  
		- (x : α) → β x  
		- ∀ x, P x  
	5. Lambda terms and application  
		- fun x => ...  
		- f x  
	6. Inductive types  
		- Nat  
		- Bool  
		- Eq  
		- And  
		- Or  
		- Exists  
		- custom inductive types  
	7. Constructors and eliminators  
		- Nat.zero  
		- Nat.succ  
		- Eq.refl  
		- And.intro  
		- induction principles  
	8. Definitions  
		- def  
	9. Theorems  
		- theorem  
		- example  
	10. Axioms  
		- propext  
		- Classical.choice  
		- Quot.sound  
		- user-declared axioms  
	11. Tactics and automation  
		- rfl  
		- exact  
		- rw  
		- simp  
		- ring  
		- linarith
- Claude