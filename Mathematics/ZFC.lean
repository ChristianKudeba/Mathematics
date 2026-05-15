/-
ZFC_Axioms.lean

This file axiomatizes ZFC inside Lean 4.

Important: this does not make Lean's own foundation become ZFC. Rather, it
introduces an abstract type `ZFSet`, a membership relation `∈`, and then states
axioms saying that these objects satisfy the ZFC axioms.

Separation and Replacement are represented as Lean-level schema axioms by
quantifying over predicates/relations. This is stronger-looking than a purely
first-order list of formulas, but it is the usual clean way to encode axiom
schemas inside a higher-order metalanguage such as Lean.
-/

namespace ZFC

/-- The type of abstract ZFC sets. -/
axiom ZFSet : Type

/-- The primitive membership relation. -/
axiom Mem : ZFSet → ZFSet → Prop

/-- Tell Lean how to interpret `x ∈ y` for abstract ZFC sets. -/
instance : Membership ZFSet ZFSet where
  mem := Mem

/-- Subset relation, defined from membership. -/
def Subset (a b : ZFSet) : Prop :=
  ∀ x : ZFSet, x ∈ a → x ∈ b

infix:50 " ⊆ " => Subset

/-- Two sets are disjoint if they have no common element. -/
def Disjoint (a b : ZFSet) : Prop :=
  ∀ x : ZFSet, x ∈ a → x ∉ b

/-- A set is empty iff it has no elements. -/
def IsEmptySet (a : ZFSet) : Prop :=
  ∀ x : ZFSet, x ∉ a

/-- A set `s` is the unordered pair `{a,b}`. -/
def IsPair (s a b : ZFSet) : Prop :=
  ∀ x : ZFSet, x ∈ s ↔ x = a ∨ x = b

/-- A set `s` is the singleton `{a}`. -/
def IsSingleton (s a : ZFSet) : Prop :=
  ∀ x : ZFSet, x ∈ s ↔ x = a

/-- A set `u` is the union `⋃ a`. -/
def IsUnion (u a : ZFSet) : Prop :=
  ∀ x : ZFSet, x ∈ u ↔ ∃ y : ZFSet, y ∈ a ∧ x ∈ y

/-- A set `p` is the powerset `𝒫(a)`. -/
def IsPowerSet (p a : ZFSet) : Prop :=
  ∀ x : ZFSet, x ∈ p ↔ x ⊆ a

/-- A set `s` is the separation subset `{x ∈ a | φ x}`. -/
def IsSeparation (s a : ZFSet) (φ : ZFSet → Prop) : Prop :=
  ∀ x : ZFSet, x ∈ s ↔ x ∈ a ∧ φ x

/--
`b` is the image of `a` under the functional relation `F`.

The relation `F x y` plays the role of a formula saying that `y` is the unique
output associated with `x`.
-/
def IsReplacementImage (b a : ZFSet) (F : ZFSet → ZFSet → Prop) : Prop :=
  ∀ y : ZFSet, y ∈ b ↔ ∃ x : ZFSet, x ∈ a ∧ F x y

/-- The successor operation in set-theoretic form: `s = x ∪ {x}`. -/
def IsSucc (s x : ZFSet) : Prop :=
  ∃ singletonX unionInput : ZFSet,
    IsSingleton singletonX x ∧
    IsPair unionInput x singletonX ∧
    IsUnion s unionInput

/-- A set is inductive iff it contains `∅` and is closed under successor. -/
def IsInductive (a : ZFSet) : Prop :=
  (∃ e : ZFSet, IsEmptySet e ∧ e ∈ a) ∧
  ∀ x : ZFSet, x ∈ a → ∃ sx : ZFSet, IsSucc sx x ∧ sx ∈ a

/-- A set is nonempty iff it has at least one element. -/
def NonemptySet (a : ZFSet) : Prop :=
  ∃ x : ZFSet, x ∈ a

/--
A choice set for a family `a` of pairwise disjoint nonempty sets.
It contains exactly one element from each member of the family.
-/
def IsChoiceSetFor (c a : ZFSet) : Prop :=
  ∀ y : ZFSet, y ∈ a →
    ∃ x : ZFSet,
      x ∈ y ∧ x ∈ c ∧
      ∀ z : ZFSet, z ∈ y ∧ z ∈ c → z = x

/-!
## The ZFC axioms
-/

/-- Extensionality: sets with the same elements are equal. -/
axiom extensionality :
  ∀ a b : ZFSet, (∀ x : ZFSet, x ∈ a ↔ x ∈ b) → a = b

/-- Empty set: there exists a set with no elements. -/
axiom empty_set :
  ∃ e : ZFSet, IsEmptySet e

/-- Pairing: for any `a` and `b`, the unordered pair `{a,b}` exists. -/
axiom pairing :
  ∀ a b : ZFSet, ∃ p : ZFSet, IsPair p a b

/-- Union: for any set `a`, the union `⋃ a` exists. -/
axiom union :
  ∀ a : ZFSet, ∃ u : ZFSet, IsUnion u a

/-- Powerset: for any set `a`, its powerset exists. -/
axiom powerset :
  ∀ a : ZFSet, ∃ p : ZFSet, IsPowerSet p a

/-- Infinity: there exists an inductive set. -/
axiom infinity :
  ∃ i : ZFSet, IsInductive i

/--
Separation schema: for any set `a` and any predicate `φ`,
there is a subset of `a` containing exactly those elements satisfying `φ`.
-/
axiom separation :
  ∀ (a : ZFSet) (φ : ZFSet → Prop),
    ∃ s : ZFSet, IsSeparation s a φ

/--
Replacement schema: if `F` is functional on `a`, then the image of `a` under
`F` is a set.
-/
axiom replacement :
  ∀ (a : ZFSet) (F : ZFSet → ZFSet → Prop),
    (∀ x : ZFSet, x ∈ a →
      ∃ y : ZFSet,
        F x y ∧
        ∀ z : ZFSet, F x z → z = y) →
      ∃ b : ZFSet, IsReplacementImage b a F

/--
Foundation / Regularity: every nonempty set has an ∈-minimal element.
-/
axiom foundation :
  ∀ a : ZFSet,
    NonemptySet a →
      ∃ x : ZFSet, x ∈ a ∧ Disjoint x a

/--
Choice, in the choice-set form: every set of pairwise disjoint nonempty sets
has a choice set.

This version is equivalent to the usual axiom of choice over ZF, but avoids
having to first develop ordered pairs and functions as sets.
-/
axiom choice :
  ∀ a : ZFSet,
    (∀ y : ZFSet, y ∈ a → NonemptySet y) →
    (∀ y z : ZFSet, y ∈ a → z ∈ a → y ≠ z → Disjoint y z) →
      ∃ c : ZFSet, IsChoiceSetFor c a

/-!
## Optional theorem names matching common ZFC terminology
-/

theorem axiom_of_extensionality :
    ∀ a b : ZFSet, (∀ x : ZFSet, x ∈ a ↔ x ∈ b) → a = b :=
  extensionality

theorem axiom_of_empty_set :
    ∃ e : ZFSet, IsEmptySet e :=
  empty_set

theorem axiom_of_pairing :
    ∀ a b : ZFSet, ∃ p : ZFSet, IsPair p a b :=
  pairing

theorem axiom_of_union :
    ∀ a : ZFSet, ∃ u : ZFSet, IsUnion u a :=
  union

theorem axiom_of_powerset :
    ∀ a : ZFSet, ∃ p : ZFSet, IsPowerSet p a :=
  powerset

theorem axiom_of_infinity :
    ∃ i : ZFSet, IsInductive i :=
  infinity

theorem axiom_schema_of_separation :
    ∀ (a : ZFSet) (φ : ZFSet → Prop),
      ∃ s : ZFSet, IsSeparation s a φ :=
  separation

theorem axiom_schema_of_replacement :
    ∀ (a : ZFSet) (F : ZFSet → ZFSet → Prop),
      (∀ x : ZFSet, x ∈ a →
        ∃ y : ZFSet,
          F x y ∧
          ∀ z : ZFSet, F x z → z = y) →
        ∃ b : ZFSet, IsReplacementImage b a F :=
  replacement

theorem axiom_of_foundation :
    ∀ a : ZFSet,
      NonemptySet a →
        ∃ x : ZFSet, x ∈ a ∧ Disjoint x a :=
  foundation

theorem axiom_of_choice :
    ∀ a : ZFSet,
      (∀ y : ZFSet, y ∈ a → NonemptySet y) →
      (∀ y z : ZFSet, y ∈ a → z ∈ a → y ≠ z → Disjoint y z) →
        ∃ c : ZFSet, IsChoiceSetFor c a :=
  choice

end ZFC
