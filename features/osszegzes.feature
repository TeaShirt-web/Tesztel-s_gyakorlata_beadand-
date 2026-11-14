# language: en
Feature: Beküldött számok összegzése
  Felhasználóként egész számokat szeretnék beküldeni az API-nak,
  hogy bármikor lekérdezhessem az eddig beküldött számok összegét.

  Background:
    Given az alkalmazás fut és még nincs beküldött szám

  Scenario: Kezdetben az összeg nulla
    When lekérdezem az összeget
    Then a válasz státuszkódja 200
    And az összeg 0

  Scenario: Több szám beküldése után az összeg helyes
    When beküldöm a 5 számot
    And beküldöm a 10 számot
    And beküldöm a -3 számot
    And lekérdezem az összeget
    Then a válasz státuszkódja 200
    And az összeg 12

  Scenario Outline: Számsorozat összege
    When beküldöm a következő számokat: "<szamok>"
    And lekérdezem az összeget
    Then az összeg <osszeg>

    Examples:
      | szamok         | osszeg |
      | 1,2,3          | 6      |
      | 100,-100       | 0      |
      | 0              | 0      |
      | 999,1          | 1000   |

  Scenario: Érvénytelen érték beküldése elutasításra kerül
    When beküldöm a "abc" szöveget számként
    Then a válasz státuszkódja 400
    When lekérdezem az összeget
    Then az összeg 0
