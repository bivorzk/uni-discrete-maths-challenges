# Hídprobléma – Dokumentáció

## A program célja

A program a **híd és lámpa problémát** oldja meg a **Dijkstra-algoritmus** segítségével. Meghatározza a túrázók minimális teljes átkelési idejét és az optimális lépéssorozatot.

**Szabályok:**
- Egyszerre legfeljebb két túrázó kelhet át.
- A lámpának minden átkelésnél jelen kell lennie.
- Az átkelés idejét a lassabb túrázó határozza meg.
- A program 1–10 túrázó adatait fogadja el.

## Állapotábrázolás

Az állapotot egy `(bal_part, lampa_oldala)` tuple reprezentálja.

- `bal_part`: a bal parton tartózkodók `frozenset` halmaza.
- `lampa_oldala`: `0` = bal part, `1` = jobb part.

A túrázókat 1-től kezdődő egész számok azonosítják.

## Függvények – `main.py`

| Függvény | Feladat |
|---|---|
| `crossing_groups(bank)` | Előállítja az összes lehetséges egy- és kétfős átkelő csoportot. |
| `next_states(state, everyone, times)` | Generálja a következő állapotokat, az átkelések költségeit és irányait. |
| `bridge_problem(minutes_to_cross)` | Dijkstra-algoritmussal megkeresi a minimális átkelési időt és a lépéssorozatot. |
| `read_minutes(n)` | Bekéri és ellenőrzi a pozitív egész átkelési időket. |
| `main()` | Kezeli az adatbekérést és kiírja a minimális teljes átkelési időt. |

## Az algoritmus működése

A probléma **súlyozott állapottérgráfként** modellezhető:

- **Csúcsok:** a túrázók és a lámpa aktuális helyzete.
- **Élek:** a lehetséges átkelések.
- **Élsúlyok:** az átkelési idők.

A Dijkstra-algoritmus a `heapq` prioritási sor segítségével mindig a legkisebb összköltségű állapotot dolgozza fel.

A `seen` halmaz nyilvántartja a már feldolgozott állapotokat, az `itertools.count()` pedig egyedi sorszámot biztosít a prioritási sor elemeinek.

Az útvonalat láncolt `(lépés, előző_útvonal)` párok tárolják, így nem szükséges minden új állapotnál a teljes lépéssorozatot lemásolni.

A keresés akkor ér véget, amikor a bal part kiürül.

**Visszatérési érték:**

```python
(osszes_ido, lepesek)
```

Hibás bemenet vagy sikertelen keresés esetén a program hibaüzenetet ír ki,
és üres eredményt ad vissza (`float("inf"), []`).

## Futtatás

**Főprogram:**

```bash
python main.py
```

A program bekéri a túrázók számát és átkelési idejét, majd kiírja a minimális teljes időt.

**Gráfvizualizáció – `graph.py`**

Szükséges csomagok:

```text
matplotlib>=3.7
networkx>=3.0
```

Telepítés és futtatás:

```bash
pip install matplotlib networkx
python graph.py
```

A vizualizáció az `[1, 2, 5, 10]` átkelési időkkel rendelkező példát szemlélteti.

![Hídprobléma – optimális megoldás](bridge_solution.png)

**Optimális átkelési idő: 17 perc.**