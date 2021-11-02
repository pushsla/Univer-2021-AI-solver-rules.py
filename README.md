# Импликативный решатель

Наборчик для осуществления поиска истинных предикатов на основе импликативных решающих правил

## Usage

В самом простом случае требуется инициализировать экземпляр класса *solver.Solver.Solver*

После следует добавить правила вывода методом *Solver.add_rule*

Запустить вывод можно передав в метод *Solver.solve* набор аксиом в виде *python set*

**Любые формулы являются надстройкой над системой классов, доступных для непосредственной инициализации**

Данные записи равносильны (1 по сути преобразуется в 2):
```python
slv.add_rule("!low_level -> high_level")
slv.add_rule("!low_level & !high_level -> high_level")
slv.add_rule("low_level & !runtimed & !typed -> asm")
slv.add_rule("runtimed -> !asm")
slv.add_rule("compiling -> !interpreting")
slv.add_rule("compiling -> c++")
slv.solve({"low_level", "runtimed"})
```

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

### Общий синтаксис
Правило вывода, вывод и посылка могут быть записаны при помощи любых символов.

Символы *&*, *|* и *!* зарезервированы для AND, OR и NOT соответственно

Последовательность *->* зарезервирована для импликации правила вывода

Любая последовательность символов, не содержащая зарезервированных символов и последовательностей, интерпретируется как имя истинного предиката

Пробелы игнорируются

Вложенность и скобки не поддерживаются

#### Синтаксис правил вывода
Скрипт правила вывода имеет вид **посылка -> вывод**

Правила вывода любой вложенности и сложности могут быть инициализированы напрямую, как экземпляры класса *solver.Rules.Rule*

#### Синтаксис посылки
Посылка состоит из множества предикатов, модифицированных и/или объединенных при помощи AND, OR, NOT (&, |, !)

При разборе формулы операторы имеют следующий приоритет:
1. NOT
2. OR
3. AND

Посылка любой вложенности и сложности может быть инициализирована напрямую, как композиция экземпляров одного из классов *solver.Logic*

#### Синтаксис вывода
Вывод может содержать только один предикат или его отрицание

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
   * Предикат истинен, если ни один из прдикатов внури не истинен
4. Is(*args: [Logic, str])
   * Ссылка на And

#### Вывод
Точно так же, как и в записи формулой

#### Набор аксиом
Экземпляр класса *solver.Entity.Entity*

## Insides
Аксиомы рассматриваются, как аттрибуты объекта Entity, а посылки - предикаты любой втепени вложенности, определяющие соответствие экземпляра Entity соответствующему набору аттрибутов.

Правило вывода определяет истинность посылки для экземпляра Entity, и в случае соответствия добавляет аттрибут вывода в экземпляр

Решатель использует все доступные правила на переданном объекте до тех пор, пока множество его аттрибутов не перестает изменяться, после чего задача считается решенной

При этом каждый класс-контейнер способен определять, был ли параметр передан в виде формулы или в виде экземпляра необходимого класса, и в первом
случае происходит разбор формулы средствами необходимого для работы класса

При добавлении нескольких правил с идентичным выводом они объединяются внешним объектом Or с сохранением вывода

Противоречия не проверяются

## Requires