# Heat Transfer FEM Solver

Aplikacja do rozwiązywania jednowymiarowego problemu przewodzenia ciepła metodą elementów skończonych (FEM).


##  Opis projektu

Program oblicza rozkład temperatury w pręcie o długości `L = 2`, wykorzystując metodę elementów skończonych (FEM).

Uwzględnia:

* zmienną przewodność cieplną
* warunki brzegowe
* funkcję źródła

Użytkownik podaje liczbę elementów siatki, a aplikacja:

1. Buduje układ równań
2. Rozwiązuje go numerycznie
3. Wyświetla wykres temperatury---

## Model matematyczny

Rozwiązywane równanie:

- d/dx ( k(x) * dT/dx ) = f(x)

### Parametry:

* przewodność cieplna:

  * k(x) = 1  dla x [0,1] 
  * k(x) = 2x dla x (1,2]
* źródło:

  * ( f(x) = 100x )

### Warunki brzegowe:

* warunek mieszany w x = 0 
* temperatura zadana: T(2) = 0 


### Funkcjonalności:

* pole do wprowadzenia liczby elementów `n`
* przycisk **Solve**
* automatyczne generowanie wykresu


## Uwagi

* Minimalna liczba elementów: `n > 2`
* Dokładność rośnie wraz z zagęszczeniem siatki
* Implementacja wykorzystuje lokalność funkcji bazowych




