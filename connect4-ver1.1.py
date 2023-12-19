class ModifiedConnectFour: #Hat mit Python 3.9 in pycharm perfekt geklappt... ich garantiere nicht es gäbe keine bugs aber ich habe keine gefunden
    def __init__(self): # auch über Terminal funktioniert es mit python3 connect4.py - Grundgerüst von Github copilot/ChatGPT-3.5
        self.board = [[' ' for _ in range(5)] for _ in range(6)]
        self.current_player = 0  # Spieler 0 beginnt
        self.bonus_used = {0: False, 1: False}  # Bonussteine für beide Spieler
        self.last_stone_in_column = [None for _ in range(10)]  # Speichert den zuletzt eingeworfenen Stein in jeder Spalte
        self.game_over = False #Nur True wenn spiel vorbei
    def switch_player(self):
        self.current_player = 1 - self.current_player  # Wechselt zwischen 0 und 1

    def get_current_stone(self):
        return 'o' if self.current_player == 0 else 'x'  # Spieler 0 spielt mit 'o', Spieler 1 mit 'x' -> hätte man auch spieler X und O nenen können

    def make_move(self, column, bonus=False): # Wenn sie das Korrigieren viel spaß beim lesen
        stone = self.get_current_stone()      # Make_move größtenteils mit Github copilot verbessert
        if bonus:
            stone = stone.upper() #Bonussteine sind Großbuchstaben
        if column < 5: # Stein wird von unten eingeworfen
            row = self.find_empty_row(column, top=False)
        else: # Stein wird von oben eingeworfen
            row = self.find_empty_row(column - 5, top=True)
        if not bonus and row is None:
            print("Spalte voll.")
        elif bonus:
            last_stone_row = self.last_stone_in_column[column] # Wenn in der Spalte kein Stein ist
            if last_stone_row is None:
                if column < 5:
                    row = self.find_empty_row(column, top=False) # Erste leere reihe wird gefunden von oben
                else:
                    row = self.find_empty_row(column - 5, top=True) # Erste leere reihe wird gefunden von unten
            elif self.board[last_stone_row][column if column < 5 else column - 5].isupper(): # Wenn der zuletzt eingeworfene Stein ein Bonusstein ist, platzieren wir den Bonusstein darüber oder darunter
                if column < 5:
                    row = last_stone_row - 1 if last_stone_row > 0 else None
                else:
                    row = last_stone_row + 1 if last_stone_row < 5 else None
            elif self.board[last_stone_row][column if column < 5 else column - 5].lower() != stone.lower(): # Wenn der zuletzt eingeworfene Stein ein Stein des Gegners ist, ersetzen wir ihn durch den Bonusstein
                row = last_stone_row
            else:
                # Wenn der zuletzt eingeworfene Stein ein eigener Stein ist, platzieren wir den Bonusstein darüber oder darunter
                if column < 5: # Bonusstein wird von unten eingeworfen
                    row = last_stone_row - 1 if last_stone_row > 0 else None
                else:
                    row = last_stone_row + 1 if last_stone_row < 5 else None
            if row is not None: # Überprüfen, ob die Reihe gültig ist, bevor der Stein platziert wird
                self.board[row][column if column < 5 else column - 5] = stone #Aktualisieren des zuletzt eingeworfenen Steins Spalte
                if self.check_winner(row, column):
                    self.game_over = True #Hier wird game beendet
                    return
                self.bonus_used[self.current_player] = True
                self.switch_player() # Spieler wechseln nach jedem Zug
            else:
                print("Bonusstein kann hier nicht platziert werden")
        elif row is not None:
            self.board[row][column if column < 5 else column - 5] = stone
            self.last_stone_in_column[column] = row
            if self.check_winner(row, column):
                print(f"Player {self.get_current_stone().upper()} wins!")
                self.game_over = True
                return
            self.switch_player() # Spieler wechseln nach jedem Zug

    def find_empty_row(self, column, top):
        if top:  # sucht von oben
            for row in range(3, 6):
                if self.board[row][column] == ' ':
                    return row
        else:  # sucht von unten
            for row in range(2, -1, -1):
                if self.board[row][column] == ' ':
                    return row
        return None

    def check_winner(self, row, column):
        if column >= 5:  # Index wird hier geändert wenn von 5-9 gespielt wird da 5-9 im endeffekt nur 0-4 sind
            column -= 5
        stone = self.board[row][column].lower()  # Kleinbuchstaben werden verwendet, um die Steine zu vergleichen
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # alle directions werden gecheckt

        for dx, dy in directions:
            count = 0
            for dir in [-1, 1]:  # Alle directions werden gecheckt
                for i in range(1, 4):  # Check three spaces //cooler code von Github copilot
                    x, y = column + i * dir * dx, row + i * dir * dy
                    if (0 <= x < 5) and (0 <= y < 6) and self.board[y][
                        x].lower() == stone:  # bonussteine zählen genau wie normale steine
                        count += 1
                    else:
                        break
            if count >= 3:  # 4 in ner reihe
                return True
        return False

    def display_board(self):
        print(' 5 6 7 8 9')
        print('┌ ─ ─ ─ ─ ─ ┐')
        for i in range(5, -1, -1):
            print('|' + ' '.join(self.board[i]) + '  | ' + str(i))
        print('└ ─ ─ ─ ─ ─ ┘')
        print(' 0 1 2 3 4')

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

    def process_moves(self, moves):
        processed_moves = []
        i = 0
        while i < len(moves):
            if moves[i].lower() == 'r':
                processed_moves.append('r')  # r wird als move gewertet, damit der ganze shit restartet
                i += 1  # nach r wird ein charakter weiter gemoved dieser charakter ist dann neuer startpunkt
            elif i + 1 < len(moves) and moves[i].isdigit() and moves[i + 1].lower() in ['x', 'o']:
                processed_moves.append(moves[i:i + 2])  # wenn nach zahl x oder o folgt wirds als ein move gewertet
                i += 2  # dieser buchstabe wird dann natürlich geskipped
            elif moves[i].isdigit():
                processed_moves.append(moves[i])  # wird eins weiter geschoben
                i += 1
            else:
                processed_moves.append(moves[i])  # wird eins weiter geschoben
                i += 1
        return processed_moves

    def play_game(self):
        self.display_board()  # Leeres Brett wird für übersichtlichkeit ausgegeben
        while not self.game_over:  # Game geht nur weiter wenn das game nicht over ist
            if self.current_player == 0:
                moves = input("akt. Spieler O\nSpalte eingeben: ")
            else:
                moves = input("akt. Spieler X\nSpalte eingeben: ")
            moves = self.process_moves(moves)
            for move in moves:
                if move.lower() == 'r': # gewünschtes feature zum resetten
                    print("Starting a new game...")
                    self.__init__()  # Game wird resettet
                    self.display_board()  # Leeres Brett wird wieder gesendet
                    self.current_player = 0  # Spieler wird zurückgesetzt
                    continue
                elif len(move) == 1 and move.isdigit():
                    self.make_move(int(move))
                    self.display_board()  # Brett wird bei jedem Zug ausgegeben
                elif len(move) == 2 and move[0].isdigit() and move[1].lower() in ['x', 'o']:
                    if move[1].lower() == self.get_current_stone():
                        if not self.bonus_used[self.current_player]:
                            column = int(move[0])
                            bonus = True
                            self.make_move(column, bonus)
                            self.display_board()  # Brett wird bei jedem Zug ausgegeben
                        else:
                            print("Bonusstein wurde schon benutzt")
                    else:
                        print("Falscher Spieler")
                else:
                    print("Ungültige Eingabe")
                if self.is_board_full():
                    print("Unentschieden")
                    break
        self.display_board()  # Brett wird hier oben einmal ausgegeben damit der gewinner unter dem Bord auftaucht
        if self.game_over:
            print(f"Spieler {self.get_current_stone().upper()} gewinnt!")  # Gewinner

if __name__ == "__main__":
    game = ModifiedConnectFour()
    game.play_game()
