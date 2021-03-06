# Импликативный решатель

## Have fun!
If you find this code useful, I will be glad if you use it in your GPL3-compatible licensed project.

**"Why GPL-3. Author, are you too proud?"**
> Nope. It's just that I'm fighting for free software, and any possibility that someone else is using my code on a project that people, myself included, will have to pay for is unacceptable.
> My code is neither perfect nor revolutionary. But the world is crazy, you know

Any help and criticism is greatly appreciated.

Наборчик для осуществления поиска истинных предикатов на основе импликативных решающих правил

## Usage

В самом простом случае требуется инициализировать экземпляр класса *solver.Solver.Solver*

После следует добавить правила вывода методом *Solver.add_rule*

Запустить вывод можно передав в метод *Solver.solve* набор аксиом в виде *python set*

**Любые формулы являются надстройкой над системой классов, доступных для непосредственной инициализации**

Данные записи равносильны (1 по сути преобразуется в 2):

**запись формулой**
```python
slv.add_rule("!low_level -> high_level")
slv.add_rule("!low_level & !high_level -> high_level")
slv.add_rule("low_level & !runtimed & !typed -> asm")
slv.add_rule("runtimed -> !asm")
slv.add_rule("compiling -> !interpreting")
slv.add_rule("compiling -> c++")
slv.solve({"low_level", "runtimed"})
```

**использование экземпляров**
```python
slv.add_rule(Rule(Not("low_level"), "high_level"))
slv.add_rule(Rule(And(Not("low_level"), Not("high_level")), "high_level"))
slv.add_rule(Rule(And("low_level", Not("runtimed", "typed")), "asm"))
slv.add_rule(Rule("runtimed"), "!asm")
slv.add_rule(Rule(Is("compiling"), "!interpreting"))
slv.add_rule(Rule(And("compiling"), "c++"))

e = Entity({"low_level", "runtimed"})
slv.solve(e)
```

### Общий синтаксис формул
Правило вывода, вывод и посылка могут быть записаны при помощи любых символов.

Символы *&*, *|*, *!* и *?* зарезервированы для AND, OR, NOT и UNKNOWN/NOT соответственно

Символ *.* зарезервирован для создания **паттернов**

Последовательность *->* зарезервирована для импликации правила вывода

Любая последовательность символов, не содержащая зарезервированных символов и последовательностей, интерпретируется как имя истинного предиката

Пробелы игнорируются

Вложенность поддерживается толко при использивании экземпляров классов. Вложенность в формулах не поддерживается.

#### Синтаксис правил вывода
Скрипт правила вывода имеет вид **посылка -> вывод**

Правила вывода любой вложенности и сложности могут быть инициализированы напрямую, как экземпляры класса *solver.Rules.Rule*

#### Синтаксис посылки
Посылка состоит из множества предикатов, модифицированных и/или объединенных при помощи AND, OR, NOT, UNKNOWN/NOT (&, |, !, ?)

При разборе формулы операторы имеют следующий приоритет:

1. UNKNOWN/NOT
2. NOT
3. OR
4. AND

Посылка любой вложенности и сложности может быть инициализирована напрямую, как композиция экземпляров одного из классов *solver.Logic*

Обратите внимание, что NOT требует, чтобы отрицание отверждения было указано или выведено в явном виде, в то время, как
UNKNOWN/NOT требует, чтобы утверждение не было истинным (ложное или не указано)

#### Синтаксис вывода
Вывод может содержать композицию из 1 или более утверждений и их отрицаний, объединенных *&* (AND)

Если в выводе содержится отрицание, считается, что отрицание утверждения станет аксиомой для объекта.

### Использование классов

#### Правило
Экземпляр класса *solver.Rules.Rule*

#### Посылка
Композиция из экземпляров классов *solver.Logic*

Если требуется указать единственный предикат, достаточно указать только его имя. Автоматически преобразуется в экземпляр класса *Is*

Доступные классы:
1. And(*args: [Logic, str])
   * Список solver.Logic
   * Предиат истинен, если все предикаты внутри истинны
2. Or(*args: [Logic, str])
   * Список solver.Logic
   * Предикат истинен, если хотябы один из предикатов внутри истинен
3. Not(*args: [Logic, str])
   * Список solver.Logic
   * Предикат истинен, если все предикаты внутри ложны
4. SoftNot(*args: [Logic: str])
   * Список solver.Logic
   * Предикат истинен, если среди внутренних нет ни одного истинного
5. Is(*args: [Logic, str])
   * То же самое, что And

#### Вывод
Точно так же, как и в записи формулой

#### Набор аксиом
Экземпляр класса *solver.Entity.Entity*

## Паттерны

Паттерн представляет собой уточнение истинного свойства. По сути это обертка над обычными свойствами.

Синтаксис паттерна: axiom.subaxiom.subaxiom...

Паттерны могут быть любой степени вложенности.

При добавлении паттерна требуется выполнение следующих условий:
1. Префикс паттерна (все до последней точки) является истинной аксиомой

Чтобы добавить ложный паттерн нужно указать "!pattern_full_name"

Префикс ложного паттерна должен быть истинным.


```python
slv.add_rule("tail -> animal")
slv.add_rule("animal & milk -> animal.mammal")
slv.add_rule("animal.mammal & horns -> animal.mammal.hoofed")
slv.add_rule("animal.mammal -> !animal.cold_blood")

slv.solve({"tail", "milk", "horns"})
```
приведет к следующей системе аксиом:
```
{'!animal.cold_blood', animal.mammal.hoofed', 'animal.mammal', 'tail', 'horns', 'milk', 'animal'}
```

Добавление правила, ведущего к "!animal.cold_blood.smth" или "animal.cold_blood.smth" вызовет исключение, так как уточнение ложной аксиомы не разрешено.

Использование ложного паттерна в посылке возможно, так как это всего лишь ложная аксиома.

Гарантируется, что, при построении очереди правил, правила с выводами паттернами выполняются после правил с выводами префиксами этих паттернов.

## Insides
Аксиомы рассматриваются, как аттрибуты объекта Entity, а посылки - предикаты любой втепени вложенности, определяющие соответствие экземпляра Entity соответствующему набору аттрибутов.

Правило вывода определяет истинность посылки для экземпляра Entity, и в случае соответствия добавляет аттрибут вывода в экземпляр

Решатель использует все доступные правила на переданном объекте до тех пор, пока множество его аттрибутов не перестает изменяться, после чего задача считается решенной

При этом каждый класс-контейнер способен определять, был ли параметр передан в виде формулы или в виде экземпляра необходимого класса, и в первом
случае происходит разбор формулы средствами необходимого для работы класса

### Оптимизация правил

Все правила с выводом более чем одного утверждения разбиваются. Таким образом внутри все решающие правила имеют одно утверждение или его отрицание в выводе.

При добавлении нескольких правил с идентичным выводом они объединяются внешним объектом Or с сохранением вывода

Таким образом проивходит следующее преобразование:
```
memory_safe -> !asm & runtimed
high_level -> memory_safe
!memory_safe -> low_level
low_level & !typed -> asm
runtimed -> !asm
low_level & !asm -> rust
script -> python
!typed & !compiling -> python
high_level & interpreting & !python -> java
compiling -> !interpreting
interpreting -> !compiling
script -> interpreting & !compiling
compiling -> c++
```

```
Is('memory_safe',) -> runtimed
And(Is('low_level',), Not('typed',)) -> asm
Is('interpreting',) -> !compiling
Is('script',) -> interpreting
Is('compiling',) -> !interpreting
Is('high_level',) -> memory_safe
Is('script',) -> !compiling
And(Is('low_level',), Not('asm',)) -> rust
Not('memory_safe',) -> low_level
And(Is('high_level',), Is('interpreting',), Not('python',)) -> java
Or(Is('memory_safe',), Is('runtimed',)) -> !asm
Is('compiling',) -> c++
Or(And(Not('typed',), Not('compiling',)), Is('script',)) -> python
```


При возникновении противоречия в ходе решения возникает исключение *SolverConflictException*
```python
slv.add_rule("a -> !b")
slv.add_rule(Rule("a", "b"))

slv.solve({'a'})
```
```
solver.Exceptions.RuleConflictException: Is('a',) -> b result conflicts with {'a', '!b'} entity; start: {'a'}; rule trace: ["Is('a') -> !b", "Is('a') -> b"]
```
