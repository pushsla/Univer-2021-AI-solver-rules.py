from solver.Solver import Solver

"""
Предметная область: языки программирования

Свойства:

low_level
high_level
runtimed
script
compiling
interpreting
typed
python
asm
c++
java
rust
block_parenthesis


Паттерны:

block_parenthesis.braces
block_parenthesis.round
block_parenthesis.square

Правила:
"""


slv = Solver()

slv.add_rule("memory_safe -> !asm & runtimed")
slv.add_rule("high_level -> memory_safe")
slv.add_rule("!memory_safe -> low_level")
slv.add_rule("low_level & !typed -> asm")
slv.add_rule("runtimed -> !asm")
slv.add_rule("low_level & !asm -> rust")
slv.add_rule("script -> python")
slv.add_rule("block_parenthesis -> !python & !asm")
slv.add_rule("!typed & !compiling -> python")
slv.add_rule("high_level & interpreting & !python -> java")
slv.add_rule("compiling -> !interpreting")
slv.add_rule("interpreting -> !compiling")
slv.add_rule("c++ -> block_parenthesis.braces")
slv.add_rule("script -> interpreting & !compiling")
slv.add_rule("compiling -> c++")
slv.add_rule("c++ | java | rust -> block_parenthesis")

print(slv)

print(slv.rulechain)
print()

print(slv.solve({"low_level", "runtimed"}))
print(slv.solve({"runtimed", "script"}))
print(slv.solve({"high_level", "typed"}))
print(slv.solve({"low_level", "runtimed"}))
print(slv.solve({"compiling"}))
print(slv.solve({"high_level"}))
print(slv.solve({"!memory_safe", "asm"}))
