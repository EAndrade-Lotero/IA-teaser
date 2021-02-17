import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import numpy as np
from random import choice, sample
import copy

def truncar(x):
    if x < 0:
        return 0
    elif x > 3:
        return 3
    else:
        return x

def adyacentes(casilla):
    x, y = casilla
    adyacentes = [
        (truncar(x - 1), y), (truncar(x + 1), y),
        (x, truncar(y - 1)), (x, truncar(y + 1))
    ]
#    adyacentes = list(set(adyacentes)) # Eliminamos repeticiones
    adyacentes = [c for c in adyacentes if c != casilla]
    return adyacentes

class wumpus:

    fig, axes = None, None

    def __init__(self, agente_inicia_en=(0,0), vacio=False):
        casillas = [(x, y) for x in range(4) for y in range(4)]
        casillas_sin_inicial = [casilla for casilla in casillas if casilla != (0,0)]
        self.oro_tomado = False
        self.wumpus_vivo = True
        self.flecha = True
        self.direccion = 'este'
        self.puntaje = 0
        self.juego_activo = True
        self.grito = False # para determinar cuándo el wumpus grita de agonía
        self.bump = False # para determinar cuándo el agente golpea un muro
        self.heroe = agente_inicia_en
        if not vacio:
            self.wumpus = choice(casillas_sin_inicial)
            self.hedor = adyacentes(self.wumpus)
            self.oro = choice(casillas)
            self.pozos = sample(casillas_sin_inicial, int(len(casillas_sin_inicial)*0.2))
            aux = []
            for c in self.pozos:
                aux += adyacentes(c)
            self.brisa = aux
        else:
            self.wumpus = np.nan
            self.hedor = []
            self.oro = np.nan
            self.pozos = []
            self.brisa = []


    def pintar_todo(self):
        # Dibuja el tablero correspondiente al estado
        fig, axes = plt.subplots(figsize=(8, 8))

        # Dibujo el tablero
        step = 1./4
        offset = 0.001
        tangulos = []

        # Borde del tablero
        tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
                                          facecolor='cornsilk',\
                                         edgecolor='black',\
                                         linewidth=2))

        # Creo las líneas del tablero
        for j in range(4):
            locacion = j * step
            # Crea linea horizontal en el rectangulo
            tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
                    facecolor='black'))
            # Crea linea vertical en el rectangulo
            tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
                    facecolor='black'))

        for t in tangulos:
            axes.add_patch(t)

        # Cargando imagen del heroe
        arr_img_hero = plt.imread("./imagenes/hero_" + self.direccion + ".png", format='png')
        image_hero = OffsetImage(arr_img_hero, zoom=0.3)
        image_hero.image.axes = axes

        # Cargando imagen del Wumpus
        arr_img_wumpus = plt.imread("./imagenes/wumpus.png", format='png')
        image_wumpus = OffsetImage(arr_img_wumpus, zoom=0.45)
        image_wumpus.image.axes = axes

        # Cargando imagen del hedor
        arr_img_stench = plt.imread("./imagenes/stench.png", format='png')
        image_stench = OffsetImage(arr_img_stench, zoom=0.35)
        image_stench.image.axes = axes

        # Cargando imagen del oro
        arr_img_gold = plt.imread("./imagenes/gold.png", format='png')
        image_gold = OffsetImage(arr_img_gold, zoom=0.25)
        image_gold.image.axes = axes

        # Cargando imagen del pozo
        arr_img_pit = plt.imread("./imagenes/pit.png", format='png')
        image_pit = OffsetImage(arr_img_pit, zoom=0.35)
        image_pit.image.axes = axes

        # Cargando imagen de la brisa
        arr_img_breeze = plt.imread("./imagenes/breeze.png", format='png')
        image_breeze = OffsetImage(arr_img_breeze, zoom=0.35)
        image_breeze.image.axes = axes

        offsetX = 0.125
        offsetY = 0.125

        for casilla in self.pozos:
            # Pintando un pozo
            X, Y = casilla
            ab = AnnotationBbox(
                image_pit,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

        for casilla in self.hedor:
            # Pintando el hedor
            X, Y = casilla
            ab = AnnotationBbox(
                image_stench,
                [(X*step) + offsetX, (Y*step) + offsetY - 0.075],
                frameon=False)
            axes.add_artist(ab)

        for casilla in self.brisa:
            # Pintando la brisa
            X, Y = casilla
            ab = AnnotationBbox(
                image_breeze,
                [(X*step) + offsetX, (Y*step) + offsetY + 0.075],
                frameon=False)
            axes.add_artist(ab)

        # Pintando el wumpus
        X, Y = self.wumpus
        ab = AnnotationBbox(
            image_wumpus,
            [(X*step) + offsetX, (Y*step) + offsetY],
            frameon=False)
        axes.add_artist(ab)

        # Pintando el heroe
        X, Y = self.heroe
        ab = AnnotationBbox(
            image_hero,
            [(X*step) + offsetX, (Y*step) + offsetY],
            frameon=False)
        axes.add_artist(ab)

        # Pintando el oro
        if not self.oro_tomado:
            X, Y = self.oro
            ab = AnnotationBbox(
                image_gold,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

        axes.axis('off')
        return axes

    def pintar_casilla(self):
        if self.juego_activo:
            # Dibuja el tablero correspondiente al estado
            fig, axes = plt.subplots(figsize=(8, 8))

            # Dibujo el tablero
            step = 1./4
            offset = 0.001
            tangulos = []

            # Borde del tablero
            tangulos.append(patches.Rectangle((0,0),0.998,0.998,\
                                              facecolor='cornsilk',\
                                             edgecolor='black',\
                                             linewidth=2))

            # Creo las líneas del tablero
            for j in range(4):
                locacion = j * step
                # Crea linea horizontal en el rectangulo
                tangulos.append(patches.Rectangle(*[(0, locacion), 1, 0.008],\
                        facecolor='black'))
                # Crea linea vertical en el rectangulo
                tangulos.append(patches.Rectangle(*[(locacion, 0), 0.008, 1],\
                        facecolor='black'))

            for t in tangulos:
                axes.add_patch(t)

            # Cargando imagen del heroe
            arr_img_hero = plt.imread("./imagenes/hero_" + self.direccion + ".png", format='png')
            image_hero = OffsetImage(arr_img_hero, zoom=0.3)
            image_hero.image.axes = axes

            # Cargando imagen del Wumpus
            arr_img_wumpus = plt.imread("./imagenes/wumpus.png", format='png')
            image_wumpus = OffsetImage(arr_img_wumpus, zoom=0.45)
            image_wumpus.image.axes = axes

            # Cargando imagen del hedor
            arr_img_stench = plt.imread("./imagenes/stench.png", format='png')
            image_stench = OffsetImage(arr_img_stench, zoom=0.35)
            image_stench.image.axes = axes

            # Cargando imagen del oro
            arr_img_gold = plt.imread("./imagenes/gold.png", format='png')
            image_gold = OffsetImage(arr_img_gold, zoom=0.25)
            image_gold.image.axes = axes

            # Cargando imagen del pozo
            arr_img_pit = plt.imread("./imagenes/pit.png", format='png')
            image_pit = OffsetImage(arr_img_pit, zoom=0.35)
            image_pit.image.axes = axes

            # Cargando imagen de la brisa
            arr_img_breeze = plt.imread("./imagenes/breeze.png", format='png')
            image_breeze = OffsetImage(arr_img_breeze, zoom=0.35)
            image_breeze.image.axes = axes

            offsetX = 0.125
            offsetY = 0.125

            casilla = self.heroe

            if casilla in self.pozos:
                # Pintando un pozo
                X, Y = casilla
                ab = AnnotationBbox(
                    image_pit,
                    [(X*step) + offsetX, (Y*step) + offsetY],
                    frameon=False)
                axes.add_artist(ab)

            if casilla in self.hedor:
                # Pintando el hedor
                X, Y = casilla
                ab = AnnotationBbox(
                    image_stench,
                    [(X*step) + offsetX, (Y*step) + offsetY - 0.075],
                    frameon=False)
                axes.add_artist(ab)

            if casilla in self.brisa:
                # Pintando la brisa
                X, Y = casilla
                ab = AnnotationBbox(
                    image_breeze,
                    [(X*step) + offsetX, (Y*step) + offsetY + 0.075],
                    frameon=False)
                axes.add_artist(ab)

            if casilla == self.wumpus:
                # Pintando el wumpus
                X, Y = self.wumpus
                ab = AnnotationBbox(
                    image_wumpus,
                    [(X*step) + offsetX, (Y*step) + offsetY],
                    frameon=False)
                axes.add_artist(ab)

            # Pintando el heroe
            X, Y = casilla
            ab = AnnotationBbox(
                image_hero,
                [(X*step) + offsetX, (Y*step) + offsetY],
                frameon=False)
            axes.add_artist(ab)

            if casilla == self.oro:
                # Pintando el oro
                if not self.oro_tomado:
                    X, Y = self.oro
                    ab = AnnotationBbox(
                        image_gold,
                        [(X*step) + offsetX, (Y*step) + offsetY],
                        frameon=False)
                    axes.add_artist(ab)

            axes.axis('off')
            return axes
        else:
            return None

    def transicion(self, accion):
        if self.juego_activo:
            self.grito = False
            self.bump = False
            self.puntaje -= 1
            if accion == 'agarrar':
                if (self.oro == self.heroe) and (self.oro_tomado == False):
                    self.puntaje += 1000
                    self.oro_tomado = True
            elif accion == 'adelante':
                x, y = self.heroe
                if self.direccion == 'este':
                    self.heroe = (truncar(x + 1), y)
                    self.bump = True if truncar(x + 1) == x else False
                if self.direccion == 'oeste':
                    self.heroe = (truncar(x - 1), y)
                    self.bump = True if truncar(x - 1) == x else False
                if self.direccion == 'norte':
                    self.heroe = (x, truncar(y + 1))
                    self.bump = True if truncar(y + 1) == y else False
                if self.direccion == 'sur':
                    self.heroe = (x, truncar(y - 1))
                    self.bump = True if truncar(y - 1) == y else False
            elif accion == 'salir':
                if self.heroe == (0, 0):
                    self.juego_activo = False
                    print("¡Juego terminado!")
                    print("Puntaje:", self.puntaje)
                    self.pintar_todo()
            elif accion == 'voltearIzquierda':
                if self.direccion == 'este':
                    self.direccion = 'norte'
                elif self.direccion == 'oeste':
                    self.direccion = 'sur'
                elif self.direccion == 'norte':
                    self.direccion = 'oeste'
                elif self.direccion == 'sur':
                    self.direccion = 'este'
            elif accion == 'voltearDerecha':
                if self.direccion == 'este':
                    self.direccion = 'sur'
                elif self.direccion == 'oeste':
                    self.direccion = 'norte'
                elif self.direccion == 'norte':
                    self.direccion = 'este'
                elif self.direccion == 'sur':
                    self.direccion = 'oeste'
            elif accion == 'disparar':
                if self.flecha:
                    self.flecha = False
                    if self.wumpus_vivo:
                        x_wumpus, y_wumpus = self.wumpus
                        x_heroe, y_heroe = self.heroe
                        if (self.direccion == 'este') and ((x_heroe < x_wumpus) and (y_heroe == y_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                        if (self.direccion == 'oeste') and ((x_heroe > x_wumpus) and (y_heroe == y_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                        if (self.direccion == 'norte') and ((y_heroe < y_wumpus) and (x_heroe == x_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
                        if (self.direccion == 'sur') and ((y_heroe > y_wumpus) and (x_heroe == x_wumpus)):
                            self.wumpus_vivo = False
                            self.grito = True
            else:
                print('¡Acción incorrecta!')
            if self.heroe in self.pozos:
                self.puntaje -= 1000
                self.juego_activo = False
                print("¡Juego terminado!")
                print("El héroe a caido en un pozo")
                print("Puntaje:", self.puntaje)
                self.pintar_todo()
            elif (self.heroe == self.wumpus) and self.wumpus_vivo:
                self.puntaje -= 1000
                self.juego_activo = False
                print("¡Juego terminado!")
                print("El héroe ha sido devorado por el Wumpus")
                print("Puntaje:", self.puntaje)
                self.pintar_todo()
        else:
            print("El juego ha terminado.")

def percibir(mundo):

    # Lista de sensores [hedor, brisa, brillo, batacazo, grito]
    hedor = 'hedor' if mundo.heroe in mundo.hedor else None
    brisa = 'brisa' if mundo.heroe in mundo.brisa else None
    brillo = 'brillo' if ((mundo.heroe == mundo.oro) and not mundo.oro_tomado) else None
    batacazo = 'batacazo' if mundo.bump else None
    grito = 'grito' if mundo.grito else None
    return [hedor, brisa, brillo, batacazo, grito]

def f(n, indice):
    # Distancia Manhattan
    # Input: n, nodo de la rejilla
    #        indice, casilla como pareja de enteros (x,y)
    x1, y1 = n.estado
    x2, y2 = indice
    return abs(x1 - x2) + abs(y1 - y2) + n.costo

def nodo_en_frontera(n, objetivo, frontera):
    if f(n, objetivo) not in frontera.keys():
        return False
    elif n not in frontera[f(n, objetivo)]:
        return False
    else:
        return True

class planeadorRuta:

    # Problema del tránsito por la rejilla
    # desde donde está el héroe hasta una
    # casilla objetivo

    def __init__(self, actual, objetivo, seguras):
        self.estado_inicial = actual
        self.estado_objetivo = objetivo
        self.casillas_seguras = seguras

    def acciones_aplicables(self, estado):
        return [casilla for casilla in adyacentes(estado) if casilla in self.casillas_seguras]

    def transicion(self, estado, accion):
        return accion

    def test_objetivo(self, estado):
        return estado == self.estado_objetivo

    def costo(self, estado, accion):
        return 1

def A_star_search(problema):

    raiz = nodo(problema.estado_inicial, None, None, 0)
    if problema.test_objetivo(raiz.estado):
        return raiz
    objetivo = problema.estado_objetivo
    frontera = {f(raiz, objetivo): [raiz]}
    explored = []

    while (len(frontera) > 0):
        n = choice(frontera[min(frontera.keys())])
        frontera[f(n, objetivo)].remove(n)
        if len(frontera[f(n, objetivo)]) == 0:
            del frontera[f(n, objetivo)]
        explored.append(n.estado)
        acciones = problema.acciones_aplicables(n.estado)
        for a in acciones:
            N = nodo_hijo(problema, n, a)
            if problema.test_objetivo(N.estado):
                return N
            elif (N.estado not in explored) and not nodo_en_frontera(N, objetivo, frontera):
                try:
                    frontera[f(N, objetivo)].append(N)
                except:
                    frontera[f(N, objetivo)] = [N]

    return None

def voltear(direccion_inicial, direccion_final):
    acciones = []
    if direccion_inicial == direccion_final:
        return acciones
    else:
        if direccion_final == 'este':
            if direccion_inicial == 'norte':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'sur':
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearDerecha')
                acciones.append('voltearDerecha')
        elif direccion_final == 'norte':
            if direccion_inicial == 'este':
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'sur':
                acciones.append('voltearIzquierda')
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearDerecha')
        elif direccion_final == 'oeste':
            if direccion_inicial == 'este':
                acciones.append('voltearIzquierda')
                acciones.append('voltearIzquierda')
            elif direccion_inicial == 'sur':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'norte':
                acciones.append('voltearIzquierda')
        elif direccion_final == 'sur':
            if direccion_inicial == 'este':
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'norte':
                acciones.append('voltearDerecha')
                acciones.append('voltearDerecha')
            elif direccion_inicial == 'oeste':
                acciones.append('voltearIzquierda')
    return acciones

def acciones_camino(camino, direccion):
    acciones = []
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        diferencia_x = x2 - x1
        diferencia_y = y2 - y1
        if (diferencia_x != 0) and (diferencia_y != 0):
            print("Camino incorrecto!: No debe incluir diagonales.")
            return None
        elif diferencia_x > 0:
            acciones += voltear(direccion, 'este')
            direccion = 'este'
        elif diferencia_x < 0:
            acciones += voltear(direccion, 'oeste')
            direccion = 'oeste'
        elif diferencia_y > 0:
            acciones += voltear(direccion, 'norte')
            direccion = 'norte'
        elif diferencia_y < 0:
            acciones += voltear(direccion, 'sur')
            direccion = 'sur'
        acciones.append('adelante')
    return acciones

class codigos:

    # Clase para agrupar las funciones de codificación
    # de letras proposicionales

    def __init__(self, Nf, Nc, No):
        self.Nf = Nf # Número de filas
        self.Nc = Nc # Número de columnas
        self.No = No # Número de opciones de información

    def codifica(self, f, c, Nf, Nc):
        # Funcion que codifica la fila f y columna c
        assert((f >= 0) and (f <= Nf - 1)), 'Primer argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nf - 1)  + "\nSe recibio " + str(f)
        assert((c >= 0) and (c <= Nc - 1)), 'Segundo argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nc - 1)  + "\nSe recibio " + str(c)
        n = Nc * f + c
        # print(u'Número a codificar:', n)
        return n

    def decodifica(self, n, Nf, Nc):
        # Funcion que codifica un caracter en su respectiva fila f y columna c de la tabla
        assert((n >= 0) and (n <= Nf * Nc - 1)), 'Codigo incorrecto! Debe estar entre 0 y ' + str(Nf * Nc - 1) + "\nSe recibio " + str(n)
        f = int(n / Nc)
        c = n % Nc
        return f, c

    def P(self, f, c, o):
        # Funcion que codifica tres argumentos
        assert((f >= 0) and (f <= self.Nf - 1)), 'Primer argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nf - 1) + "\nSe recibio " + str(f)
        assert((c >= 0) and (c <= self.Nc - 1)), 'Segundo argumento incorrecto! Debe ser un numero entre 0 y ' + str(Nc - 1) + "\nSe recibio " + str(c)
        assert((o >= 0) and (o <= self.No - 1)), 'Tercer argumento incorrecto! Debe ser un numero entre 0 y ' + str(No - 1)  + "\nSe recibio " + str(o)
        v1 = self.codifica(f, c, self.Nf, self.Nc)
        v2 = self.codifica(v1, o, self.Nf * self.Nc, self.No)
        codigo = chr(256 + v2)
        return codigo

    def Pinv(self, codigo):
        # Funcion que codifica un caracter en su respectiva fila f, columna c y objeto o
        x = ord(codigo) - 256
        v1, o = self.decodifica(x, self.Nf * self.Nc, self.No)
        f, c = self.decodifica(v1, self.Nf, self.Nc)
        return f, c, o

    def imprime_formula(self, fml):
        for c in fml:
            if c in ['Y', '>', '-']:
                print(c, end="")
            else:
                x, y, o = self.Pinv(c)
                if o == 0:
                    print("Segura" + str((x, y)), end="")
                elif o == 1:
                    print("Brisa" + str((x, y)), end="")
                elif o == 2:
                    print("Pozo" + str((x, y)), end="")
                elif o == 3:
                    print("Hedor" + str((x, y)), end="")
                elif o == 4:
                    print("Wumpus" + str((x, y)), end="")
                elif o == 5:
                    print("Visitada" + str((x, y)), end="")
                else:
                    print("ESTATICO" + str((x, y)), end="")

def formulas_brisa(cods, n=4):
    formulas_brisa = []
    for x in range(n):
        for y in range(n):
            # Para las implicaciones positivas
            inicial = True
            for p in adyacentes((x,y)):
                i, j = p
                # Para las implicaciones negativas
                formulas_brisa.append("-" + cods.P(i, j, 1) + ">-" + cods.P(x, y, 2))
                # Para las implicaciones positivas
                if inicial:
                    clausula = cods.P(i, j, 1)
                    inicial = False
                else:
                    clausula += "Y" + cods.P(i, j, 1)
            formulas_brisa.append(clausula + ">" + cods.P(x, y, 2))
    return formulas_brisa

def formulas_hedor(cods, n=4):
    formulas_hedor = []
    for x in range(n):
        for y in range(n):
            # Para las implicaciones positivas
            for p in adyacentes((x,y)):
                i, j = p
                # Para las implicaciones negativas
                formulas_hedor.append("-" + cods.P(i, j, 3) + ">-" + cods.P(x, y, 4))
            # Como solo hay un Wumpus, dos hedores localizan al Wumpus
            aux1 = [p for p in adyacentes((x,y))]
            if len(aux1) == 2:
                p = aux1[0]
                q = aux1[1]
                formulas_hedor.append(cods.P(*p, 3) + "Y" + cods.P(*q, 3) + ">" + cods.P(x, y, 4))
            else:
                for i in range(len(aux1)):
                    for j in range(i + 1, len(aux1)):
                        a1, b1 = aux1[i]
                        a2, b2 = aux1[j]
                        formulas_hedor.append(cods.P(a1, b1, 3) + "Y" + cods.P(a2, b2, 3) + ">" + cods.P(x, y, 4))
            # FALTA INCLUIR LAS FORMULAS PARA EL RAZONAMIENTO
            # QUE SE REALIZA EN EL EJERCICIO 7 DEL PRIMER NOTEBOOK
            # Wumpus localizado implica que no está en las demás
            casillas = [(x1, y1) for x1 in range(4) for y1 in range(4) if x1!=x and y1!=y]
            for casilla in casillas:
                x1, y1 = casilla
                formulas_hedor.append(cods.P(x, y, 4) + ">-" + cods.P(x1, y1, 4))
    return formulas_hedor

def formulas_segura(cods, n=4):
    formulas_segura = []
    for x in range(n):
        for y in range(n):
            formulas_segura.append("-" + cods.P(x, y, 2) + "Y-" + cods.P(x, y, 4) + ">" + cods.P(x, y, 0))
    return formulas_segura

class lp_query:

    def __init__(self, base_conocimiento_lista, cods):

        # Con base en la lista de cláusulas en la base de
        # conocimiento, crea un diccionario optimizado para
        # la búsqueda
        # Input: base_conocimiento_lista, que es una lista de fórmulas 'pseudo' cláusulas de Horn
        #        cods, un objeto de clase codigos
        self.base_conocimiento = {'datos':[], 'reglas':{}}
        for formula in base_conocimiento_lista:
            indice_conectivo = formula.find('>')
            if indice_conectivo > 0:
                cuerpo = formula[:indice_conectivo]
                cabeza = formula[indice_conectivo + 1:]
                try:
                    self.base_conocimiento['reglas'][cabeza].append(cuerpo)
                except:
                    self.base_conocimiento['reglas'][cabeza] = [cuerpo]
            else:
                try:
                    self.base_conocimiento['datos'].append(formula)
                except:
                    self.base_conocimiento['datos'] = [formula]
        self.cods = cods

    def visualizar(self, parte='todo'):
        if (parte=='todo') or (parte=='datos'):
            print("Datos:")
            for l in self.base_conocimiento['datos']:
                self.cods.imprime_formula(l)
                print('')
        if (parte=='todo') or (parte=='reglas'):
            print("\nReglas:")
            for k in self.base_conocimiento['reglas'].keys():
                for c in self.base_conocimiento['reglas'][k]:
                    self.cods.imprime_formula(c)
                    print(">", end="")
                    self.cods.imprime_formula(k)
                    print(" ")

    def reglas_aplicables(self, head):
        # Devuelve una lista de cláusulas de Horn cuya cabeza
        # es el estado/literal
        # Input: head, que es un literal
        # Output: lista de cláusulas de Horn
        try:
            cuerpo = self.base_conocimiento['reglas'][head]
        except:
            cuerpo = []

        return cuerpo

    def transicion(self, head, body):
        # Devuelve una lista con los literales en la clausula
        # Input: head, que es un literal se asume que head:- body es una regla
        #        body, que es una lista de cláusulas de Horn
        return body.split('Y')

    def test_objetivo(self, literal):
        # Devuelve True/False dependiendo si el literal
        # está en la base de datos
        # Input: literal
        # Output: True/False
        literales = self.base_conocimiento['datos']
        return True if literal in literales else False

def TELL(base, formula):
    indice_conectivo = formula.find('>')
    if indice_conectivo > 0:
        cuerpo = formula[:indice_conectivo]
        cabeza = formula[indice_conectivo + 1:]
        try:
            if cuerpo not in base.base_conocimiento['reglas'][cabeza]:
                base.base_conocimiento['reglas'][cabeza].append(cuerpo)
        except:
            base.base_conocimiento['reglas'][cabeza] = [cuerpo]
    else:
        lista_hechos = formula.split('Y')
        for literal in lista_hechos:
            try:
                if literal not in base.base_conocimiento['datos']:
                    base.base_conocimiento['datos'].append(literal)
            except:
                base.base_conocimiento['datos'] = [literal]

def ASK(objetivo, valor:bool, base):
    ask = True if (and_or_graph_search(objetivo, base) != 'failure') else False
    return (ask == valor)

def and_or_graph_search(objetivo, base):
    return or_search(objetivo, base, [])

def or_search(head, base, camino):
    if base.test_objetivo(head):
        return 'success'
    elif head in camino:
        return 'failure'
    reglas = base.reglas_aplicables(head)
    if not reglas:
        return 'failure'
    for regla in reglas:
        plan = and_search(base.transicion(head, regla), base, [head] + camino)
        if plan != 'failure':
            return 'success'
    return 'failure'

def and_search(literales, base, camino):
    for literal in literales:
        plan = or_search(literal, base, camino)
        if plan == 'failure':
            return 'failure'
    return 'success'

class nodo:

    # Clase para crear los nodos

    def __init__(self, estado, madre, accion, costo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo = costo

def nodo_hijo(problema, madre, accion):

    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo

    return nodo(
        problema.transicion(madre.estado, accion),
        madre,
        accion,
        costo = madre.costo + problema.costo(madre.estado, accion)
        )

def solucion(n):

    # Devuelve la secuencia de estados que va desde la raíz
    # hasta el nodo n
    # Input: n, nodo
    # Output: l, lista de acciones

    acciones_invertidas = []
    m = copy.deepcopy(n)
    while m.madre != None:
        acciones_invertidas.append(m.accion)
        m = m.madre

    num_acciones = len(acciones_invertidas)
    acciones = []
    for i in range(1, num_acciones + 1):
        acciones.append(acciones_invertidas[num_acciones - i])

    return acciones

def casillas_seguras(base, cods):
    # Extrae los literales Seguras de la base de datos
    seguras = []
    for literal in base.base_conocimiento['datos']:
        if len(literal) == 1:
            if ord(literal) < 9999:
                x, y, z = cods.Pinv(literal)
                if z == 0:
                    seguras.append((x,y))
    return seguras

def casillas_visitadas(base, cods):
    # Extrae los literales Visitadas de la base de datos
    visitadas = []
    for literal in base.base_conocimiento['datos']:
        if len(literal) == 1:
            if ord(literal) < 9999:
                x, y, z = cods.Pinv(literal)
                if z == 5:
                    visitadas.append((x,y))
    return visitadas

def hybrid_wumpus_agent(percept, turno, locacion, direccion, Base_wumpus, cods, plan):

    # Incluye los axiomas de los fluentes para el turno respectivo
    # Brillo
    fml_lista = [cods.F(turno, 0) + "Y-" + cods.F(turno, 1) + ">" + cods.F(turno + 1, 0)]
    fml_lista.append("-" + cods.F(turno, 0) + ">-" + cods.F(turno + 1, 0))
    fml_lista.append(cods.F(turno, 1) + ">-" + cods.F(turno + 1, 0))
    # TenerFlecha
    fml_lista.append(cods.F(turno, 2) + "Y-" + cods.F(turno, 3) + ">" + cods.F(turno + 1, 2))
    fml_lista.append("-" + cods.F(turno, 2) + ">-" + cods.F(turno + 1, 2))
    fml_lista.append(cods.F(turno, 3) + ">-" + cods.F(turno + 1, 2))
    for fml in fml_lista:
        TELL(Base_wumpus, fml)

    # Incluye la información de los sensores en la base de datos
    datos = make_percept_sentence(percept, locacion, turno, cods)
    TELL(Base_wumpus, datos)
    # Razona para determinar cuáles casillas son seguras
    for casilla in [locacion] + adyacentes(locacion):
        x, y = casilla
        objetivo = cods.P(x, y, 0)
        if ASK(objetivo, True, Base_wumpus):
            TELL(Base_wumpus, cods.P(x, y, 0))

    # Incluye la información de que la casilla actual es visitada
    x, y = locacion
    TELL(Base_wumpus, cods.P(x, y, 5))

    # Obtiene las casillas seguras de la base de datos
    seguras = casillas_seguras(Base_wumpus, cods)
    #print('seguras', seguras)
    # Obtiene las casillas visitadas de la base de datos
    visitadas = casillas_visitadas(Base_wumpus, cods)
    #print('visitadas', visitadas)
    # Calcula las casillas seguras no visitadas
    seguras_no_visitadas = [casilla for casilla in seguras if casilla not in visitadas]
    #print('seguras no visitadas', seguras_no_visitadas)

    # Si percibe un brillo, toma el oro y planea su regreso a la salida
    if ASK(cods.F(turno, 0), True, Base_wumpus):
        #print("Aquí está el oro!")
        plan = ['agarrar']
        R = planeadorRuta(locacion, (0,0) , seguras)
        camino = A_star_search(R)
        if camino != None:
            camino = solucion(camino)
        else:
            camino = []
        plan += acciones_camino([locacion] + camino, direccion)
        plan += ['salir']

    # Planea moverse a una casilla segura no visitada
    if (len(plan) == 0) and (len(seguras_no_visitadas) > 0):
        #print("Voy a una casilla segura no visitada")
        objetivo = choice(seguras_no_visitadas)
        R = planeadorRuta(locacion, objetivo, seguras)
        camino = A_star_search(R)
        if camino != None:
            camino = solucion(camino)
        else:
            camino = []
        plan = acciones_camino([locacion] + camino, direccion)

    # Si no hay casillas seguras por visitar, sale de la cueva
    elif len(plan) == 0:
        #print("No hay casillas seguras por visitar. Me voy!")
        objetivo = (0,0)
        R = planeadorRuta(locacion, objetivo, seguras)
        camino = A_star_search(R)
        if camino != None:
            camino = solucion(camino)
        else:
            camino = []
        plan = acciones_camino([locacion] + camino, direccion)
        plan += ['salir']

    # Decide la acción y actualiza la base de conocimiento
    accion = plan.pop(0)
    fml = make_action_sentence(accion, turno, cods)
    TELL(Base_wumpus, fml)
    return accion

def inicializar(self, Nf, Nc, No, Nt, Nfo):
    self.Nf = Nf # Número de filas
    self.Nc = Nc # Número de columnas
    self.No = No # Número de opciones de información estática
    self.Nt = Nt # Número de turnos de los fluentes
    self.Nfo = Nfo # Número de opciones de información fluentes

def F(self, t, o):
    # método para la codificación de fluentes
    v = self.codifica(t, o, self.Nt, self.Nfo)
    codigo = chr(10000 + v) # NOS ASEGURAMOS DE NO INTERSECTAR LOS ATOMOS ESTATICOS
    return codigo

def Finv(self, codigo):
    # Funcion que codifica un caracter en su respectiva fila f, columna c y objeto o
    x = ord(codigo) - 10000
    t, o = self.decodifica(x, self.Nt, self.Nfo)
    return t, o

def imprime_formula(self, fml):
    for c in fml:
        if c in ['Y', '>', '-']:
            print(c, end="")
        else:
            if ord(c) > 9999:
                t, o = self.Finv(c)
                if o == 0:
                    print("Brillo(" + str(t) + ")", end="")
                elif o == 1:
                    print("Agarrar(" + str(t) + ")", end="")
                elif o == 2:
                    print("TenerFlecha(" + str(t) + ")", end="")
                elif o == 3:
                    print("Disparar(" + str(t) + ")", end="")
                else:
                    print("FLUENTE("  + str(t) + ")", end="")
            else:
                x, y, o = self.Pinv(c)
                if o == 0:
                    print("Segura" + str((x, y)), end="")
                elif o == 1:
                    print("Brisa" + str((x, y)), end="")
                elif o == 2:
                    print("Pozo" + str((x, y)), end="")
                elif o == 3:
                    print("Hedor" + str((x, y)), end="")
                elif o == 4:
                    print("Wumpus" + str((x, y)), end="")
                elif o == 5:
                    print("Visitada" + str((x, y)), end="")
                else:
                    print("ESTATICO" + str((x, y)), end="")

def actualizar_codigos():
    # Incluye las funciones como métodos de la clase codigos
    setattr(codigos,"__init__", inicializar)
    setattr(codigos,"F", F)
    setattr(codigos,"Finv", Finv)
    setattr(codigos,"imprime_formula", imprime_formula)

def make_action_sentence(action, turno, cods):
    # Crea una conjuncion de literales para añadir a la base de datos
    literales = ''
    if action == 'agarrar':
        literales += cods.F(turno, 1)
    else:
        literales += '-' + cods.F(turno, 1)
    if action == 'disparar':
        literales += 'Y' + cods.F(turno, 3)
    else:
        literales += 'Y-' + cods.F(turno, 3)
    return literales

def make_percept_sentence(percept, indice, turno, cods):
    # Crea una conjuncion de literales para añadir a la base de datos
    literales = ''
    x, y = indice
    if percept[0] != None:
        literales += cods.P(x, y, 3)
    else:
        literales += '-' + cods.P(x, y, 3)
    if percept[1] != None:
        literales += 'Y' + cods.P(x, y, 1)
    else:
        literales += 'Y-' + cods.P(x, y, 1)
    if percept[2] != None:
        literales += 'Y' + cods.F(turno, 0)
    else:
        literales += 'Y-' + cods.F(turno, 0)
    literales += 'Y-' + cods.P(x, y, 2)
    literales += 'Y-' + cods.P(x, y, 4)
    return literales
