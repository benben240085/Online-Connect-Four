import pygame
from network import Network

pygame.font.init()

width, height = 750, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect Four Online Client")


def redraw_window(window, game, player):
    window.fill((255, 255, 255))

    if not game.connected():
        fnt = pygame.font.SysFont("Comic Sans MS", 80)
        text = fnt.render("Waiting for player...", True, (255, 0, 0), True)
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        fnt = pygame.font.SysFont("Comic Sans MS", 40)
        wins = str(game.wins[player])
        text = fnt.render("Wins: " + wins, True, (255, 0, 0))
        window.blit(text, (width - text.get_width() - 10, 0))

        if player == 0 and game.p1Went:
            text = fnt.render("Opp. Move", True, (255, 0, 0))
            window.blit(text, (width / 2 - text.get_width() / 2, 0))
        elif player == 0 and (not game.p1Went):
            text = fnt.render("Your Move", True, (255, 0, 0))
            window.blit(text, (width / 2 - text.get_width() / 2, 0))
        elif player == 1 and (not game.p1Went):
            text = fnt.render("Opp. Move", True, (255, 0, 0))
            window.blit(text, (width / 2 - text.get_width() / 2, 0))
        elif player == 1 and game.p1Went and (not game.p2Went):
            text = fnt.render("Your Move", True, (255, 0, 0))
            window.blit(text, (width / 2 - text.get_width() / 2, 0))

        game.draw(window)

    pygame.display.update()


game = None


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    key = None

    while run:
        global game
        clock.tick(60)

        try:
            game = n.send("get")
        except:
            print("Couldn't find game")
            break

        font = pygame.font.SysFont("Comic Sans MS", 40)
        is_reset = False
        txt = None
        if (player == 0 and game.winner() == 0) or (player == 1 and game.winner() == 1):
            txt = font.render("You Won!", True, (255, 0, 0))
            if player == 0:
                game = n.send("zero")
            else:
                game = n.send("one")
            is_reset = True
        elif (player == 0 and game.winner() == 1) or (player == 1 and game.winner() == 0):
            txt = font.render("You Lost :(", True, (255, 0, 0))
            is_reset = True
        elif player == 0 and game.winner() == -1:
            txt = font.render("You tied", True, (255, 0, 0))
            game = n.send("tie")
            is_reset = True
        elif player == 1 and game.winner() == -1:
            txt = font.render("You tied", True, (255, 0, 0))
            is_reset = True

        if is_reset:
            redraw_window(win, game, player)
            win.blit(txt, (width / 2 - txt.get_width() / 2, height / 2 - txt.get_height() / 2 + 30))
            pygame.display.update()
            pygame.time.delay(2000)
            game = n.send("n")

        if game.bothWent():
            try:
                game = n.send("t")
            except:
                print("Couldn't find game")
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = "0"
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = "1"
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = "2"
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = "3"
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = "4"
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = "5"
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = "6"

                if key and game.board[0][int(key)] != 0:
                    key = None

                if game.connected():
                    if player == 0 and (not game.p1Went) and key:
                        n.send(key)
                        key = None
                    elif player == 1 and game.p1Went and (not game.p2Went) and key:
                        n.send(key)
                        key = None

        redraw_window(win, game, player)


main()
