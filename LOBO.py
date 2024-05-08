# LOBO language.            Karen Navarro Arroyo, A01641532

import turtle
import re
import sys
    
e = []     
prog = []
global i 
i = 0

""" --------------------------------------------------
Especificaciones:
utiliza descenso recursivo para repeat (repetir)

nombre       equivalencia   descripción
av, avanza          fd      avanza
rv, reves           bk      avnza al reves
gd, girod           rt      giro derecha
gi, giroi           lt      giro izquierda
ct, centro          ct      centrar
br, borrar          cs      reset canvas
nd                  pu      punUp/ no dibujar
sd                  pd      penDown/ dibujar
color               pc      color
repetir b [a]       repeat  repetir a, b veces

Lista de colores:
tinto               #770606     201
rojo                #db0e0e     202
naranja             #eb5d0b     203
amarillo            #e7ca0e     204
verde               #26820f     205
lima                #0ee91d     206
turquesa            #12ad79     207
azul                #1319c4     208
morado              #730fad     209
lila                #c876ff     210
rosa                #ed55ba     211
cafe                #53220b     212
negro               #000000     213
gris                #888888     214
blanco              #FFFFFF     215
    -------------------------------------------------- """ 

# Códigos de color. Recibe el código (201-215) y regresa el código Hex
def colorACod(c):
    comanCod= [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215]
    hexad   = ['#770606', '#db0e0e', '#eb5d0b', '#e7ca0e', '#26820f', '#0ee91d', '#12ad79', '#1319c4', '#730fad', '#c876ff', '#ed55ba', '#53220b', '#000000', '#888888', '#FFFFFF']
    return hexad[comanCod.index(c)]
    
# Se valida que todas las entradas existan y sean válidas. Regresa un código INT para cada entrada (comando, número, corchete, etc)
def validarCom(a):
          # Regex                   #Descripción    Código de aceptación
    com = [r'^[\d]*$',              # Número        100
           r'(^av$)|(^avanza$)',    # Avanzar       101
           r'(^rv$)|(^reves$)',     # Reves         102
           r'(^gd$)|(^girod$)',     # Giro der.     103
           r'(^gi$)|(^giroi$)',     # Giro izq.     104
           r'(^ct$)|(^centro$)',    # Centrar       105
           r'(^br$)|(^borrar$)',    # Reiniciar     106
           r'(^nd$)',               # No Dibujar    107
           r'(^sd$)',               # Sí dibujar    108
           r'(^color$)',            # Color         109
           r'(^repetir$)',          # Repetir       110
                                    # Casos especiales de REPETIR
           r'(^\[$)',               # [             301    
           r'(^\]$)',               # ]             302
                                    # Colores       201-215
           r'(^tinto$)',r'(^rojo$)',r'(^naranja$)',r'(^amarillo$)',r'(^verde$)', r'(^lima$)',r'(^turquesa$)',r'(^azul$)',r'(^morado$)',r'(^lila$)',r'(^rosa$)',r'(^cafe$)',r'(^negro$)',r'(^gris$)', r'(^blanco$)']          
    codigo =  [100, 101,  102,  103,  104,  105,  106,  107, 108, 109, 110,                    # Comandos
                    301, 302,                                                                  # En relación a repetir [ ]
                    201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215] # Colores
    l = 0
    for i in com:
        if (re.match(i, a) != None):
            return codigo[l]            
        else:
            l-=-1
    sys.exit(f"\n\nERROR: No se pudo interpretar \'{a}\'\nCódigo terminado")  
    
# Evalúa la sintaxis en base a los códigos recibidos en la función anterior (validarCom)
# A partir de aquí entra la implementación de la gramática BNF y descenso recursivo.
def S():        # <S> ::= ( <Mo> | <N> | <Co> | <Re> ) (<S> | ε )
    global i
    if (prog[i]>=101 and prog[i]<=104):     # Para 101-104, <Mo>
        Mo()
    elif (prog[i]>=105 and prog[i]<=108):   # 105-108,      <N>
        N()
    elif (prog[i]==109):                    # 109, 201-215, <Co>
        Co()
    elif (prog[i]==110):                    # 110, 301-302, <Re>
        Re()
        i = i+1
    else:
        sys.exit(f"\n\nERROR: El código no pudo ejecutarse. Error en \'{e[i]}\'\nCódigo terminado")  
                
    if (prog[i]  != 400 and prog[i]  != 302):   # 400=Fin de código, 302=], fin de repetir
        S()                                     # Continuar S() Si no es ningún código de fin
    
def Mo(): # <Mo> ::= <mov> 100 
    global i
    mov()
    if (prog[i] == 100):
        ejecutar(prog[i-1], e[i])
        i = i+1
    else:
        sys.exit(f"\n\nERROR: Se esperaba número después de \'{e[i-1]}\'\nCódigo terminado")  
    
def mov(): # <mov> ::= 101 | 102 | 103 | 104
    global i
    if (prog[i] >= 101 and prog[i]<=104):
        i = i+1
    else:
        sys.exit(f"\n\nERROR[1]: Este ERROR No devería ser visible")  
        
def N(): # <N> ::= 105 | 106 | 107 | 108
    global i
    ejecutar(prog[i], 0)
    i = i+1
        
def Co(): # <Co> ::= 109 <color>
    global i
    i = i+1
    if (prog[i]>= 201 and prog[i]<= 215):
        color()
    else:
        sys.exit(f"\n\nERROR: Se esperaba el nombre de un color después de \'{e[i-1]}\'\n(Ej.: 'tinto', 'rojo', 'naranja', 'amarillo', 'verde',\n'lima', 'turquesa', 'azul', 'morado', 'lila', 'rosa', \n'cafe', 'negro', 'gris', 'blanco')\nCódigo terminado")  
    
def color(): # <color> ::= 201 | 202 | 203 | 204 | 205 [...] | 215
    global i
    ejecutar(109, prog[i])
    i = i+1
    
def Re(): # <Re> ::= 110 100 '[' <S> ']'
    global i
    i = i+1
    if (prog[i] == 100):
        if (int(e[i]) >= 1):
            i = i+1
            if (prog[i] == 301 and prog[i-1] != 301):
                i = i+1     # Primer token de ciclo repetir
                j = i       # Guardar el índice del primer token después de [
                S()
                Re2(j, int(e[j-2])-1)   # n es el valor de repeticiones de ciclo (n=e[j-2])-1)
            else:
                sys.exit(f"\n\nERROR: Se esperaba \'[\'\nCódigo terminado")  
        else:
            sys.exit(f"\n\nERROR: El ciclo repetir debe tener un valor igual o mayor a 1\nCódigo terminado")  
    else:
        sys.exit(f"\n\nERROR: Se esperaba número después de \'{e[i-1]}\'\nCódigo terminado")  
    
def Re2(j, n): # Función auxiliar de Re para completar el ciclo
    global i
    if (prog[i] == 302):
        if (n > 0):
            i = j         # Regresar al índice del primer token de ciclo, que se guardó en <Re> como j
            S()
            Re2(j, n-1)
    else:
        sys.exit(f"\n\nERROR: Se esperaba \']\'\nCódigo terminado") 

def ejecutar(token, arg): # Función para ejecución del código.
    if (token == 101):
        t.forward(int(arg))
    elif (token == 102):
        t.backward(int(arg))
    elif (token == 103):
        t.right(int(arg))
    elif (token == 104):
        t.left(int(arg))
    elif (token == 105):
        t.home()    
    elif (token == 106):
        t.reset()
    elif (token == 107):
        t.penup()    
    elif (token == 108):    
        t.pendown()
    elif (token == 109):
        t.pencolor(colorACod(arg))   
    else: 
        sys.exit("Este mensaje no debería ser visible.\nFavor de demandar al Administrador")   

# _____________________________________________________________________
# MAIN ---------------------------------------------------------------|

txt = open("Interface.txt", "r")
entrada = txt.read()
txt.close()
entrada = entrada.strip().lower()
entrada = re.sub(r"\]", " ] ", entrada)
entrada = re.sub(r"\[", " [ ", entrada)
e = entrada.split()

s = turtle.getscreen()      
t = turtle.Turtle()
t.shape('classic')    
t.speed(0)

j = 0
while j<len(e):
    prog.append(validarCom(e[j]))
    j = j+1
prog.append(400) # 400 es el código de fin de programa

S()
print(f"El código se ha ejecutado con éxito")
a = input("Enter para cerrar")