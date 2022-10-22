# HW Logika 1 - Úradník

Úkol jsem se rozhodl pojmout trochu obecněji, protože jsem si říkal že by se
mohlo v budoucnu hodit mít Pythonní rozhraní pro ten SAT solver. Tak jsem ho
napsal, zatím jsem ho dal do soukromého repa, ať není podezření o podvádění :D

Modul glupy dělá komunikaci se SAT solverem a parsování vstupu. Řešení těch
příkladů je ve složce examples. Výhoda toho mít Pythonní rozhraní je, že můžu
zautomatizovat zadávání těch příkazů do SAT solveru. Takže třeba ten úkol 2b
znamenal pro mě zadat jméno souboru, nechat to postupně iterovat přes ta čísla
a zvyšovat timeout pro SAT solver.

### Upozornění: vyžaduje Python 3.10 a vyšší

# Otázky

a) není 3, 5, je 10.
b) 3 je 8 < C <= 45, 4 je 9 < C <= 12

# Soubory

## glupy/solver

Komunikuje se sat solverem.

## glupy/cnf

Reprezentace CNF výroku. Umí dělat věci jako ukládat se do souboru atd.

## glupy/file_parsers

Parsování pro CNF a grafy.

## examples/approx_graph_chromatic_number

Postupně checkuje všechny záznamy s nízkým timeoutem. Pokaždé když narazí na
False, tak ví, že všechny pod ním jsou taky False, a když na True, tak všechny
nad ním jsou True. Hledá pomezí mezi True a False, což je právě to chromatické
číslo.

### Usage
```
python -m examples.approx_graph_chromatic_number /absolutni/cesta/ke/grafu
```

## examples/check_graph_coloring

Vygeneruje z grafu CNF objekt splnitelný právě když je graf k-obarvitelný.
Detaily jsou popsané v komentáři v kódu.

### Usage
```
python -m examples.check_graph_coloring /absolutni/cesta/ke/grafu pocet_barev
```
