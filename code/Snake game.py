# Python Snake
# Importiamo i moduli tkinter per creare l'interfaccia grafica e random per generare numeri casuali
from tkinter import *
import random

# Definiamo alcune costanti per le dimensioni del gioco, la velocità, la dimensione degli spazi, il numero di parti del corpo del serpente, i colori del serpente, del cibo e dello sfondo
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Creiamo una classe Snake per rappresentare il serpente
class Snake:

    # Il metodo __init__ viene chiamato quando creiamo un'istanza della classe Snake
    def __init__(self):
        # Inizializziamo il numero di parti del corpo del serpente, una lista di coordinate per ogni parte e una lista di quadrati per disegnare il serpente
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Aggiungiamo alla lista delle coordinate le posizioni iniziali del serpente, partendo da (0, 0)
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Per ogni coppia di coordinate, creiamo un quadrato sul canvas con il colore e il tag del serpente e lo aggiungiamo alla lista dei quadrati
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Creiamo una classe Food per rappresentare il cibo
class Food:

    # Il metodo __init__ viene chiamato quando creiamo un'istanza della classe Food
    def __init__(self):

        # Generiamo una posizione casuale per il cibo, in modo che sia allineata con gli spazi del gioco
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        # Memorizziamo le coordinate del cibo in un attributo della classe
        self.coordinates = [x, y]

        # Creiamo un cerchio sul canvas con il colore e il tag del cibo
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Definiamo una funzione next_turn che esegue il prossimo turno del gioco
def next_turn(snake, food):

    # Prendiamo le coordinate della testa del serpente
    x, y = snake.coordinates[0]

    # Aggiorniamo le coordinate in base alla direzione del serpente
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Inseriamo le nuove coordinate in testa alla lista delle coordinate del serpente
    snake.coordinates.insert(0, (x, y))

    # Creiamo un nuovo quadrato sul canvas con le nuove coordinate e il colore del serpente
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    # Inseriamo il nuovo quadrato in testa alla lista dei quadrati del serpente
    snake.squares.insert(0, square)

    # Controlliamo se il serpente ha mangiato il cibo, confrontando le coordinate della testa con quelle del cibo
    if x == food.coordinates[0] and y == food.coordinates[1]:

        # Se il serpente ha mangiato il cibo, incrementiamo il punteggio
        global score

        score += 1

        # Aggiorniamo il testo dell'etichetta con il nuovo punteggio
        label.config(text="Score:{}".format(score))

        # Eliminiamo il cibo dal canvas
        canvas.delete("food")

        # Creiamo un nuovo cibo
        food = Food()

    else:

        # Se il serpente non ha mangiato il cibo, eliminiamo l'ultima parte del corpo del serpente
        del snake.coordinates[-1]

        # Eliminiamo l'ultimo quadrato dal canvas
        canvas.delete(snake.squares[-1])

        # Eliminiamo l'ultimo quadrato dalla lista dei quadrati
        del snake.squares[-1]

    # Controlliamo se il serpente ha colliso con i bordi del gioco o con se stesso
    if check_collisions(snake):
        # Se il serpente ha colliso, terminiamo il gioco
        game_over()

    else:
        # Se il serpente non ha colliso, ripetiamo la funzione next_turn dopo un intervallo di tempo determinato dalla velocità
        window.after(SPEED, next_turn, snake, food)

# Definiamo una funzione change_direction che cambia la direzione del serpente in base al tasto premuto dall'utente
def change_direction(new_direction):

    # Usiamo una variabile globale per memorizzare la direzione del serpente
    global direction

    # Cambiamo la direzione solo se non è opposta a quella attuale, per evitare che il serpente si mangi da solo
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

# Definiamo una funzione check_collisions che controlla se il serpente ha colliso con i bordi del gioco o con se stesso
def check_collisions(snake):

    # Prendiamo le coordinate della testa del serpente
    x, y = snake.coordinates[0]

    # Controlliamo se le coordinate sono fuori dai limiti del gioco
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # Controlliamo se le coordinate coincidono con quelle di una parte del corpo del serpente
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    # Se non ci sono collisioni, restituiamo False
    return False

# Definiamo una funzione game_over che termina il gioco
def game_over():

    # Eliminiamo tutto dal canvas
    canvas.delete(ALL)
    # Creiamo un testo sul canvas con il messaggio "GAME OVER" in rosso
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
    # Abilitiamo il pulsante di restart
    button.config(state=NORMAL)
    # Ridimensioniamo il canvas in modo che il pulsante sia visibile
    canvas.config(height=GAME_HEIGHT - SPACE_SIZE) 
    


# Definiamo una funzione restart che resetta il gioco
def restart():
    # Disabilitiamo il pulsante di restart
    button.config(state=DISABLED)
    # Resetiamo il punteggio a zero e la direzione a 'down'
    global score, direction
    score = 0
    direction = 'down'
    # Aggiorniamo il testo dell'etichetta con il punteggio
    label.config(text="Score:{}".format(score))
     # Eliminiamo il testo "GAME OVER" dal canvas quando fai restart
    canvas.delete("gameover") 
    # Creiamo un'istanza della classe Snake e una della classe Food
    snake = Snake()
    food = Food()
    # Chiamiamo la funzione next_turn per iniziare il gioco, passando come argomenti il serpente e il cibo
    next_turn(snake, food)




# Creiamo una finestra con il titolo "Snake game" e la rendiamo non ridimensionabile
window = Tk()
window.title("Snake game")
window.resizable(False, False)

# Inizializziamo il punteggio a zero e la direzione a 'down'
score = 0
direction = 'down'

# Creiamo un'etichetta sulla finestra con il testo "Score:0" e il font 'consolas' di dimensione 40
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Creiamo un canvas sulla finestra con il colore di sfondo nero e le dimensioni del gioco
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Aggiorniamo la finestra
window.update()

# Calcoliamo la larghezza e l'altezza della finestra e dello schermo
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calcoliamo la posizione della finestra in modo che sia centrata sullo schermo
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# Impostiamo la geometria della finestra con la larghezza, l'altezza e la posizione calcolate
window.geometry(f"{window_width}x{window_height}+{x}+{y}")



# Associamo i tasti freccia alla funzione change_direction, passando come parametro la nuova direzione
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


# Creiamo un pulsante sulla finestra con il testo "Restart" e la funzione restart come comando
button = Button(window, text="Restart", command=restart)
# Disabilitiamo il pulsante all'inizio del gioco
button.config(state=DISABLED)
# Posizioniamo il pulsante sotto l'etichetta del punteggio
button.pack()


# Creiamo un'istanza della classe Snake e una della classe Food
snake = Snake()
food = Food()

# Chiamiamo la funzione next_turn per iniziare il gioco, passando come argomenti il serpente e il cibo
next_turn(snake, food)

# Avviamo il ciclo principale della finestra per gestire gli eventi
window.mainloop()
