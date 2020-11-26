Para ejecutar el programa con interfaz visual ejecutar: python app.py

Para ejecutar el programa sin interfaz visual:
Crear un archivo dentro de esta misma carpeta, que contendrá la entrada. El formato del archivo debe ser el siguiente:
-La primera línea debe contener dos enteros W, H: el ancho y el alto de la hoja principal.
-Las siguientes n líneas deben contener cada una tres enteros wi, hi, di: ancho, altura y demanda del pedido #i.

Ejecutar el comando: python main.py <nombre del archivo de entrada> <nombre del archivo de salida>

Luego de finalizada la ejecución del programa la salida del mismo se encontrará dentro del archivo cuyo nombre se especificó en el segundo argumento del anterior comando. La estructura del archivo es la siguiente:
- Primero se lista la entrada del programa.
- Luego se muestran los parametros que utilizó el algoritmo genético en su ejecución.
- A continuación se muestra la salida del programa:
    - Una lista de patrones de corte. Cada patron de corte se representa con tres elementos: una lista de cortes, el desperdicio que genera aplicar ese patrón, y la cantidad de veces que debe utilizarse. Cada corte tiene el formato <(x, y): w X h>. x, y son las coordenadas de la esquina inferiror izquierda del corte. w,h son el ancho y el alto correspondiente a las dimensiones del corte.
    - El desperdicio total que se genera.
    - El tiempo que demoró la ejecución del programa.

Ejemplo:
input.txt:

100 91
51 79 820672
63 20 659430
79 31 253405
23 74 478282
52 69 785027
44 21 610940

python main.py input.txt output.txt

output.txt:

Input data:
Main sheet: 100 X 91
Orders:
51 X 79: 820672
63 X 20: 659430
79 X 31: 253405
23 X 74: 478282
52 X 69: 785027
44 X 21: 610940

Parameters:
Population size: 60
No. generations: 30
Random walk steps: 100
Hill climbing neighbors: 25
No. best solutions: 10
Roulette population size: 45
Crossover probability: 0.75

Output:
(0, 91): 52 X 69  (52, 91): 31 X 79  (0, 22): 44 X 21
free space: 2139   No. of prints: 820672

(0, 91): 51 X 79  (51, 91): 23 X 74  (74, 91): 20 X 63
free space: 2109   No. of prints: 659430

fitness: 5016405077.0
Time:5.86074423789978 seconds