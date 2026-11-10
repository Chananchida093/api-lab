# API lab results

## Part 0

- Step 0.1, the number of pizza names: 18
- Step 0.3, status code without a token: 401
- Step 0.4, the name of your pizza: The Weak Frutti di Mare
- Step 0.12, results without a session (optional): Failed
- Step 0.16, excluded tools blocks:

## Defect report

- Title:
- Request:
- Expected result:
- Actual result:
- Severity:

## Part A

- Step A4, status codes for another user:

# API Testing Lab

## Input Domain Model — POST /api/ratings

| Characteristic | Blocks | Test Values |
|---|---|---|
| C1: Value of stars | Below 1, 1-5 (base), Above 5 | 0, 3, 6 |
| C2: Type of stars | Integer (base), Decimal, Text, Missing | 3, 3.5, "3", no field |
| C3: Pizza | Exists (base), Does not exist | Valid pizza ID, 999999999 |
| C4: Token | Own token (base), None, Wrong length | auth, no header, token short |

## Part B

1.
2.
3.
4.
5.
6.
7.
8.