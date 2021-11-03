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

Правила:
"""


slv = Solver()

slv.add_rule("?low_level -> high_level")
slv.add_rule("low_level & !runtimed & !typed -> asm")
slv.add_rule("runtimed -> !asm")
slv.add_rule("low_level & !asm -> rust")
slv.add_rule("high_level & script -> python")
slv.add_rule("high_level & !typed & !compiling -> python")
slv.add_rule("high_level & interpreting & !python -> java")
slv.add_rule("compiling -> !interpreting")
slv.add_rule("interpreting -> !compiling")
slv.add_rule("script -> interpreting")
slv.add_rule("script -> !compiling")
slv.add_rule("compiling -> c++")

print(slv)

print(slv.solve({"low_level", "runtimed"}))
print(slv.solve({"runtimed", "script"}))
print(slv.solve({"high_level", "typed"}))
print(slv.solve({"low_level", "runtimed"}))
print(slv.solve({"compiling"}))
print(slv.solve({"high_level"}))
