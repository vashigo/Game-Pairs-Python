import random, pygame, sys
from pygame.locals import *

#Variables del Tablero
pygame.init()
FPS = 30 # Cuadros por segundo, la velocidad general del programa
FPSCLOCK = pygame.time.Clock()
PANTALLAANCHO = 800 # Tamaño del ancho de la ventana en píxeles.
PANTALLALARGO = 600 # Tamaño del largo de la ventana en píxeles.
VELOCIDADREVELADO = 8 # velocidad de desplazamiento de cajas
CAJATAMAÑO = 40 # Tamaño de la caja alto y ancho en píxeles
DIVISIONTAMAÑO = 10 # Tamaño de la brecha entre cajas en píxeles
TABLEROANCHO = 2 # número de columnas de iconos / DEJARLO MAXIMO DE 10 POR VENTANA DE JUEGO!
TABLEROLARGO = 2 # número de filas de iconos / DEJARLO MAXIMO DE 10 POR VENTANA DE JUEGO!
PANTALLA = pygame.display.set_mode((PANTALLAANCHO, PANTALLALARGO)) #pantalla principal
XMARGEN = int((PANTALLAANCHO - (TABLEROANCHO * (CAJATAMAÑO + DIVISIONTAMAÑO))) / 2) #Margen x en la pantalla
YMARGEN = int((PANTALLALARGO - (TABLEROLARGO * (CAJATAMAÑO + DIVISIONTAMAÑO))) / 2) #Margen y en la pantalla

#Tamaños Predeterminados de los textos
pequeñaFuente = pygame.font.SysFont("comicsansns",15)
medianaFuente = pygame.font.SysFont("comicsansns",40)
grandeFuente = pygame.font.SysFont("comicsansns",80)

#colores a usar en el programa
#              R    G    B
GRIS       = (100, 100, 100)
AZULNAVAL  = ( 60,  60, 100)
BLANCO     = (255, 255, 255)
ROJO       = (255,   0,   0)
VERDE      = (  0, 255,   0)
NEGRO      = ( 00, 00,   00)
AZUL       = (  0,   0, 255)
AMARILLO   = (255, 255,   0)
NARANJA    = (255, 128,   0)
MORADO     = (255,   0, 255)
CYAN       = (  0, 255, 255)
ROSA       = (255, 153, 153)
ROSAOSCURO = (150,   7,  72)

BGCOLOR = ROSA #COLOR FONDO
LIGHTBGCOLOR = GRIS #COLOR VARIAR AL GANAR O PERDER
CAJACOLOR = ROSAOSCURO #COLOR CAJAS O CONTENEDOR
HIGHLIGHTCOLOR = AZUL #COLOR BORDE AL SELECCIONARLAS

#figuras a usar
DONA = 'dona'
CUADRADO = 'cuadrado'
DIAMANTE = 'diamante'
LINEAS = 'lineas'
OVALO = 'ovalo'
VIDAS = 0 #intentos del jugador, pero se controla al momento de pedir datos

ALLCOLORES = (ROJO, VERDE, AZUL, AMARILLO, NARANJA, MORADO, CYAN, NEGRO, BLANCO, AZULNAVAL)#lista de Colores a usar en tablero
ALLFIGURAS = (DONA, CUADRADO, DIAMANTE, LINEAS, OVALO) #lista de figuras a usar en tablero

'''
Pantalla Principal del juego donde dara inicio al juego o saldra de este
'''
def pantallaIntroduccion():
    global FPSCLOCK, VIDAS, introJuego, TABLEROANCHO, TABLEROLARGO
    pygame.display.set_caption('Concentrese Game')
    fondo = cargar_imagen('fondo.jpg')
    PANTALLA.blit(fondo, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit() 
        mensaje("Bienvenido a Concentrese",NEGRO,-100,tamaño="grande")
        botones("Iniciar",PANTALLA,[CYAN,AMARILLO],[(PANTALLALARGO/2)+0,(PANTALLAANCHO/2)+0],[160,45],"mediano","Iniciar")#Boton Iniciar
        botones("Salir",PANTALLA,[MORADO,AMARILLO],[(PANTALLALARGO/2)+0,(PANTALLAANCHO/2)+50],[160,45],"mediano","Salir")#Boton Salir
        pygame.display.update()

'''
Pantalla secundaria antes de comenzar donde se le pedira al usuario que escoja el tamaño del tablero
'''           
def pantallaPedirDatos():
    global FPSCLOCK, VIDAS, introJuego, TABLEROANCHO, TABLEROLARGO
    pygame.display.set_caption('Concentrese Game')
    fondo = cargar_imagen('fondo.jpg')
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        PANTALLA.blit(fondo, (0, 0))
        mensaje("Por favor, elija el tamaño del tablero",NEGRO,-150,tamaño="mediano")
        mensaje("Tablero "+str(TABLEROANCHO)+" x "+str(TABLEROLARGO),NEGRO,-80,tamaño="grande")
        botones("+",PANTALLA,[CYAN,AMARILLO],[(PANTALLALARGO/2)+50,(PANTALLAANCHO/2)-100],[50,45],"mediano","Matriz+")#Boton aumentar tamaño tablero
        botones("-",PANTALLA,[CYAN,AMARILLO],[(PANTALLALARGO/2)+50,(PANTALLAANCHO/2)-50],[50,45],"mediano","Matriz-")#Boton disminuir tamaño tablero
        botones("Comenzar",PANTALLA,[ROJO,AMARILLO],[(PANTALLALARGO/2)-5,(PANTALLAANCHO/2)+50],[160,45],"mediano","Comenzar")#Boton Iniciar
        pygame.display.update()
     
'''
Pantalla secundaria despues de pedir los datos, donde se dara inicio al juego
mostrando el tablero hasta que se gane o acabe sus intentos
''' 
def pantallaTablero():
    global FPSCLOCK, VIDAS, TABLEROANCHO, TABLEROLARGO, XMARGEN, YMARGEN
    VIDAS = (TABLEROANCHO*TABLEROLARGO//2)//2 #calculo de intentos
    #Calcular la margen para despues centrar los elementos en pantalla
    XMARGEN = int((PANTALLAANCHO - (TABLEROANCHO * (CAJATAMAÑO + DIVISIONTAMAÑO))) / 2)
    YMARGEN = int((PANTALLALARGO - (TABLEROLARGO * (CAJATAMAÑO + DIVISIONTAMAÑO))) / 2)
    PANTALLA = pygame.display.set_mode((PANTALLAANCHO, PANTALLALARGO))
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Concentrese Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.
    
    PANTALLA.fill(BGCOLOR)
    startGameAnimation(mainBoard)
    
    while True: # main game loop
        mouseClicked = False
        PANTALLA.fill(BGCOLOR) # drawing the window
        puntos(VIDAS) # Dibuja mensaje en juego
        drawBoard(mainBoard, revealedBoxes)
        pygame.display.update()
        #Controlamos que saldra del juego con la tecla esc, y manejamos
        #los eventos del mouse
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                pygame.time.wait(100)
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                pygame.time.wait(100)
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if (icon1shape != icon2shape or icon1color != icon2color) and VIDAS>0:
                        # Icons don't match. Re-cover up both selections.
                        VIDAS-=1 #restamos vidas
                        #perdio
                        if VIDAS ==0:
                            gameWonLossAnimation(mainBoard,"Has Perdido!!!")
                            pygame.display.update()
                            pantallaIntroduccion()
                        else:
                            pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                            coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxx][boxy] = False
                            puntos(VIDAS)
                    elif hasWon(revealedBoxes): # check if all pairs found
                        #si Gano
                        if hasWon(revealedBoxes) and VIDAS>0:
                            gameWonLossAnimation(mainBoard,"Has Ganado!!!")
                            pygame.display.update()
                            pantallaIntroduccion()

                    firstSelection = None # reset firstSelection variable

        # ROJOraw the screen and wait a clock tick.
        FPSCLOCK.tick(FPS)

#Lee la imagen para las pantallas de introduccion y pedir datos
def cargar_imagen(nombre,transparente=False):
     imagen = pygame.image.load(nombre)
     imagen = imagen.convert()
     if transparente:
          color = imagen.get_at((0,0))
          imagen.set_colorkey(color, RLEACCEL)
     return imagen
 
#crea mensajes en botones
def TextoBoton(msg,color,BotonX,BotonY,Ancho,Alto,tamaño="pequeño"):
    textoSuperficie, textoRect = objetoTexto(msg,color,tamaño)
    textoRect.center = (BotonX+(Ancho/2),BotonY+(Alto/2))
    PANTALLA.blit(textoSuperficie,textoRect)
    
#crea Botones
#cada boton se manejara su funcionamiento por aparte
def botones(texto,superficie,estado,Pos,tam,tamañotexto, identidad=None):
    global VIDAS, TABLEROANCHO, TABLEROLARGO
    cursor = pygame.mouse.get_pos() #capturar posicion del cursor
    click = pygame.mouse.get_pressed() #capturar click del cursor
    #definir el comportamiento cuando se pasa el cursor sobre el boton y se da click
    if Pos[0]+tam[0] > cursor[0] > tam[0]  and Pos[1] + tam[1] > cursor[1] > tam[1] and Pos[1]+ tam[1] < cursor[1] + tam[1]: #si pasa
        if click[0] == 1:#si hizo click
            #si elije el boton Iniciar
            if identidad == "Iniciar":
                pantallaPedirDatos() #salte a la pantalla de pedir datos
            #si elije el boton +   
            elif identidad == "Matriz+":
                pygame.time.wait(100)
                if TABLEROANCHO>=0 and TABLEROANCHO <10: #Maximo tamaño tablero en juego = 10
                    TABLEROANCHO+=2
                    TABLEROLARGO+=2
            #si elije el boton -
            elif identidad == "Matriz-":
                pygame.time.wait(100)
                if TABLEROANCHO>2:
                    TABLEROANCHO-=2
                    TABLEROLARGO-=2
            #si elije el boton Comenzar
            elif identidad == "Comenzar":
                pantallaTablero()
            #si elije el boton Comenzar
            elif identidad == "Salir":
                pygame.quit()
                sys.exit()
        #se cambia de color amarillo con estado[1]
        boton= pygame.draw.rect(superficie,estado[1],(Pos[0],Pos[1],tam[0],tam[1]))
    else: # si no
        #se queda en su color base con estado[0] cuando no es seleccionado
        boton= pygame.draw.rect(superficie,estado[0],(Pos[0],Pos[1],tam[0],tam[1]))
    #se dibuja el texto dentro del boton con la funcion TextoBoton()
    TextoBoton(texto,NEGRO,+Pos[0],Pos[1],tam[0],tam[1],tamañotexto)
    return boton

#Objeto Texto para controlar solamente el texto, tamaño y color con el tamaño de fuentes predeterminadas al inicio
def objetoTexto(texto,color,tamaño):
    if tamaño == "pequeño":
        textoSuperficie = pequeñaFuente.render(texto,True,color)
    if tamaño == "mediano":
        textoSuperficie = medianaFuente.render(texto,True,color)
    if tamaño == "grande":
         textoSuperficie= grandeFuente.render(texto,True,color)
    return textoSuperficie, textoSuperficie.get_rect()

#dibujar texto en pantalla comodamente
def mensaje(msg,color,deplazamientoY=0,tamaño="pequeño"):
    textoSuperficie, textoRect = objetoTexto(msg,color,tamaño)
    textoRect.center = (PANTALLAANCHO/2),(PANTALLALARGO/2)+deplazamientoY
    PANTALLA.blit(textoSuperficie,textoRect)
    
#muestra los intentos del jugador en este caso son sus intentos disponibles
def puntos(marcador):
    mensaje = medianaFuente.render("INTENTOS: " + str(marcador), True, AMARILLO)
    PANTALLA.blit(mensaje,(5,5))

#generar datos de cajas reveladas en este caso una lista
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(TABLEROANCHO):
        revealedBoxes.append([val] * TABLEROLARGO)
    return revealedBoxes

#Crea la estructura de datos del tablero (representación en matriz), con iconos colocados al azar.
def getRandomizedBoard():
    #Obtener una lista de todas las formas posibles en todos los colores posibles.
    icons = []
    for color in ALLCOLORES:
        for shape in ALLFIGURAS:
            icons.append( (shape, color) )

    random.shuffle(icons) # mezcla aleatoriamente la lista de iconos
    numIconsUsed = int(TABLEROANCHO * TABLEROLARGO / 2) # calcula cuántos iconos se necesitan para jugar
    icons = icons[:numIconsUsed] * 2 # forma las parejas de cada figura
    random.shuffle(icons) #se vuelve a mezclar

    #Crea la estructura de datos del tablero, con iconos colocados al azar.
    board = []
    for x in range(TABLEROANCHO):
        column = []
        for y in range(TABLEROLARGO):
            column.append(icons[0])
            del icons[0] # Eliminar los iconos a medida que los asignamos.
        board.append(column)
    return board

#divide una lista en una lista de listas, donde las listas internas tienen
#a lo sumo la cantidad de elementos de groupSize.
def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

#Convertir las coordenadas del tablero en coordenadas de píxeles para acomodar en la pantalla
def leftTopCoordsOfBox(boxx, boxy):
    global TABLEROANCHO, TABLEROLARGO
    left = boxx * (CAJATAMAÑO + DIVISIONTAMAÑO) + XMARGEN
    top = boxy * (CAJATAMAÑO + DIVISIONTAMAÑO) + YMARGEN
    return (left, top)

#Obtiene las coordenadas de una caja en coordenadas de pixeles
def getBoxAtPixel(x, y):
    for boxx in range(TABLEROANCHO):
        for boxy in range(TABLEROLARGO):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, CAJATAMAÑO, CAJATAMAÑO)
            if boxRect.collidepoint(x, y):#prueba si un punto está dentro de la caja
                return (boxx, boxy)
    return (None, None)

#Dibujar iconos
def drawIcon(shape, color, boxx, boxy):
    quarter = int(CAJATAMAÑO * 0.25) # Tercera parte de la caja
    half =    int(CAJATAMAÑO * 0.5)  # mitad de caja

    left, top = leftTopCoordsOfBox(boxx, boxy) # obtener coordenadas en pixeles en tablero para la caja
    # Dibujar Las Formas
    #Dona
    if shape == DONA:
        pygame.draw.circle(PANTALLA, color, (left + half, top + half), half - 5)
        pygame.draw.circle(PANTALLA, BGCOLOR, (left + half, top + half), quarter - 5)
    #cuadrado
    elif shape == CUADRADO:
        pygame.draw.rect(PANTALLA, color, (left + quarter, top + quarter, CAJATAMAÑO - half, CAJATAMAÑO - half))
    #Diamante
    elif shape == DIAMANTE:
        pygame.draw.polygon(PANTALLA, color, ((left + half, top), (left + CAJATAMAÑO - 1, top + half), (left + half, top + CAJATAMAÑO - 1), (left, top + half)))
    #lineas
    elif shape == LINEAS:
        for i in range(0, CAJATAMAÑO, 4):
            pygame.draw.line(PANTALLA, color, (left, top + i), (left + i, top))
            pygame.draw.line(PANTALLA, color, (left + i, top + CAJATAMAÑO - 1), (left + CAJATAMAÑO - 1, top + i))
    #ovalo
    elif shape == OVALO:
        pygame.draw.ellipse(PANTALLA, color, (left, top + quarter, CAJATAMAÑO, half))

#Obtener la figura y Color deseados
def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stoROJO in board[x][y][0]
    # color value for x, y spot is stoROJO in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being coveROJO/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(PANTALLA, BGCOLOR, (left, top, CAJATAMAÑO, CAJATAMAÑO))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(PANTALLA, CAJACOLOR, (left, top, coverage, CAJATAMAÑO))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(CAJATAMAÑO, (-VELOCIDADREVELADO) - 1, -VELOCIDADREVELADO):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, CAJATAMAÑO + VELOCIDADREVELADO, VELOCIDADREVELADO):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    global TABLEROANCHO, TABLEROLARGO
    # Draws all of the boxes in their coveROJO or revealed state.
    for boxx in range(TABLEROANCHO):
        for boxy in range(TABLEROLARGO):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a coveROJO box.
                pygame.draw.rect(PANTALLA, CAJACOLOR, (left, top, CAJATAMAÑO, CAJATAMAÑO))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(PANTALLA, HIGHLIGHTCOLOR, (left - 5, top - 5, CAJATAMAÑO + 10, CAJATAMAÑO + 10), 4)


def startGameAnimation(board):
    puntos(VIDAS)
    # Randomly reveal the boxes all at a time.
    coveROJOBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(TABLEROANCHO):
        for y in range(TABLEROLARGO):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(TABLEROANCHO*TABLEROLARGO, boxes)

    drawBoard(board, coveROJOBoxes)
    for boxGroup in boxGroups:
        #revelamos las figuras
        revealBoxesAnimation(board, boxGroup)
        #esperamos n*Tablero_Ancho segundos para mostrar figuras antes de comenzar
        pygame.time.wait(1000*TABLEROANCHO)
        #volvemos a tapar las figuras
        coverBoxesAnimation(board, boxGroup)


def gameWonLossAnimation(board,msg):
    # flash the background color when the player has won
    coveROJOBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        PANTALLA.fill(color1)
        drawBoard(board, coveROJOBoxes)
        mensaje(msg,ROJO,tamaño="grande")
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are coveROJO.
    return True

#Inicializar el Juego
pantallaIntroduccion()
