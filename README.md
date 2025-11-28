    -Objetivo-
Este es un proyecto hecho en Python con Flask, su objetivo crear una pagina web apta para la gestion del Inventario de una empresa mediante la implementacion de una base de datos con SQLite

    -Pagina Web- 
La aplicación se divide en una pagina de inicio de sesión que permite el acceso unicamente con las credenciales correctas.
<img width="803" height="402" alt="login" src="https://github.com/user-attachments/assets/3ac7f45c-d0ae-45c0-9546-5cbcfe003e85" />

Una vez que ingresas la pagina de inicio da una presentación y bienvenida al usuario junto con los vinculos a las paginas mediante botones y una barra de navegación a las tablas de datos, ambas dan acceso a la pagina de inicio y las 2 paginas que almacenan la informacion de los productos y de los almacenes disponibles.

<img width="1136" height="475" alt="pgInicio" src="https://github.com/user-attachments/assets/3095ede4-157e-43eb-9cd1-bc47278fcd81" />

    -Pagina Productos-
La Primera pagina es la tabla de Productos, muestra los datos y permite filtrar los productos disponibles para su busqueda a todos los usuarios pero solo autoriza que el usuario ADMIN y PRODUCTOS modifiquen los datos de la tabla.

<img width="1170" height="670" alt="pgProductos" src="https://github.com/user-attachments/assets/d9a41d59-be56-4de9-a8b1-bae39ac393fd" />

    -Pagina Almacenes-
Esta pagina permite igualmente ver y filtrar los datos de los almacenes en la tabla pero solo le da acceso a los cambios al usuario ADMIN y ALMACENES.

<img width="1127" height="630" alt="pgAlmacenes" src="https://github.com/user-attachments/assets/8240144d-7154-40d9-8a38-0e0c43ab26cf" />

    -Creacion y Modificación de Datos-
Ambas paginas le permiten a los usuarios con permisos agregar, modificar y eliminar datos en la tabla, si decides crear o modificar entras a una pagina que te pide los datos necesarios y al confirmar guarda los datos de quien realizo estos cambios junto a la fecha y hora de este proceso.

-Agregar producto:
<img width="1139" height="358" alt="agregarProd" src="https://github.com/user-attachments/assets/3f4b6276-ce36-4834-9d40-9540a9782f25" />

-Nuevo producto:
<img width="1098" height="81" alt="producto" src="https://github.com/user-attachments/assets/ea290a4e-3ff1-43d2-b408-b6646e56e1c7" />

-Agregar almacen:
<img width="588" height="283" alt="agregarAl" src="https://github.com/user-attachments/assets/f4e7d9b5-df79-43c0-8acc-a701b854f3e2" />

-Nuevo almacen:
<img width="1071" height="49" alt="almacen" src="https://github.com/user-attachments/assets/3b6dd639-f7b7-4ed9-afd0-f5ded06da12c" />

    -Filtros de los Datos-
Las 2 paginas permiten a todos el filtrar los datos para encontrar lo que desees dentro de los datos disponibles de los productos, los almacenes o los usuarios que han hecho cambios.

-Productos:
<img width="1047" height="623" alt="filtroProd" src="https://github.com/user-attachments/assets/304bcd63-3a02-4892-8c49-217dfc710cce" />

-Almacenes:
<img width="1130" height="275" alt="filtroAl" src="https://github.com/user-attachments/assets/c27a3fe6-2588-4e95-800d-c9267b04ff22" />

    -Requerimientos-
Para que el proyecto funcione se necesita instalar las dependencias de requirements.txt, para hacerlo usa la terminal de Pycharm y escribe el comando "pip install -r requirements.txt"
<img width="227" height="199" alt="requirements" src="https://github.com/user-attachments/assets/736844eb-dc35-4fbd-b4d6-930fb0814e9e" />
