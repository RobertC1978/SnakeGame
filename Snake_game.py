import pygame, sys, random
from Snake_class import Segment
from Snake_class import Frame
from Snake_class import Write_player_score
import pickle

pygame.init()
clock = pygame.time.Clock()     # game clock
clock_inscription_snake = pygame.time.Clock()       # clock for inscription "snake"
clock_inscription_dots = pygame.time.Clock()        # clock for inscription "loading"
time_tick = 15
time = 0.0
Fail = False
Snake = []      # snake body
Extra_segment = []
move_x = 0      # snake head move
move_y = 0      # snake head move
board_x = 900       # screen dimensions
board_y = 450
Total_score = 0     # player's score
write_on_list = False
first_score = False     # first score to write on list
new_pause = False       # game pause
acceleration = 1
acceleration_score = 0      # cancel acceleration
bonus_points = False



if __name__ == "__main__":

    # create game screen

    screen = pygame.display.set_mode((board_x, board_y))

    # create frame

    frame = Frame(class_screen=screen, frame_x=board_x, frame_y=board_y)

    # create inscriptions at the beginning of the game

    font = pygame.font.SysFont('comicsans', 100)
    font_gameover = pygame.font.SysFont('comicsans', 130)
    font_player_score = pygame.font.SysFont('comicsans', 50)
    font_scores = pygame.font.SysFont('comicsans', 30)
    font_next_board = pygame.font.SysFont('comicsans', 30)

    text_snake = font.render("SNAKE", True, (255, 255, 0))
    loading = "Loading"
    font_1 = pygame.font.SysFont('comicsans', 30)
    text_loading = font_1.render(loading, True, (255, 255, 0))

    text_snake_Rect = text_snake.get_rect()
    text_snake_Rect.center = (board_x // 2, board_y // 2)

    text_loading_Rect = text_loading.get_rect()
    text_loading_Rect.center = (board_x // 2 - 80, board_y // 2 + 40)

    # time set

    time_display_snake = 0
    time_add_dot = 0

    # loop for inscriptions at the beginning of the game

    while time_display_snake < 4:

        screen.fill((0, 0, 0))
        screen.blit(text_snake, text_snake_Rect)
        screen.blit(text_loading, text_loading_Rect)
        if time_add_dot > 0.15:
            loading += "."
            text_loading = font_1.render(loading, True, (255, 255, 0))
            time_add_dot -= 0.15
        time_display_snake += clock_inscription_snake.tick() / 1000
        time_add_dot += clock_inscription_dots.tick() / 1000
        pygame.display.update()

    # create snake head

    snake_head = Segment(class_screen=screen, color=(255, 0, 0), position_x=50, position_y=50)
    Snake.append(snake_head)

    # check if snake head hit the object

    def Strike(head, object):
        if head.position_x == object.position_x and head.position_y == object.position_y:
            return True

    # check if snake head hit snake body

    def Wrapping(head, snake_body):
        num = len(snake_body)
        if num > 2:
            for i in range(2, num):
                if Strike(head, snake_body[i]):
                    return True

    # check if file "Best_Snake_results" already exists

    def check_result_file():
        try:
            file = open("Best_Snake_results", "rb")
            file.close()
            return True

        except:
            return False

    # main loop - board refresh

    while not Fail:
        time += clock.tick() / 1000
        while time > 1 / time_tick:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                # check event key down

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_x = -10
                        move_y = 0

                    if event.key == pygame.K_RIGHT:
                        move_x = 10
                        move_y = 0

                    if event.key == pygame.K_UP:
                        move_y = -10
                        move_x = 0
                    if event.key == pygame.K_DOWN:
                        move_y = 10
                        move_x = 0

                    # game pause

                    if event.key == pygame.K_p:
                        new_pause = True
                    if event.key == pygame.K_r:
                        new_pause = False

            # cancel acceleration

            if Total_score == acceleration_score + 4:
                acceleration = 1
                bonus_points = False


            time -= 1 / time_tick * acceleration        # time with acceleration

            # clear screen

            screen.fill((0, 0, 0))

            frame.draw_frame()

            # draw snake body

            for part in Snake:
                part.draw_segment()

            # change each segment position

            if new_pause == False:
                number = len(Snake)
                minus_previous_segment = 1
                for i in range(1, number):
                    Snake[number - minus_previous_segment].position_x = Snake[number - 1 - minus_previous_segment].position_x
                    Snake[number - minus_previous_segment].position_y = Snake[number - 1 - minus_previous_segment].position_y
                    minus_previous_segment += 1

                # change snake head position

                snake_head.position_x += move_x
                snake_head.position_y += move_y

            # create new element on the board in random place

            if Extra_segment == []:
                extra_segment = Segment(class_screen=screen)

                # create element with speed bonus (different color) randomly

                color_set = random.randrange(3)
                if color_set == 0:
                    extra_segment.color = (0, 50, 200)
                extra_segment.position_x = random.randrange(40, board_x - 40, 10)       # change position by 10
                extra_segment.position_y = random.randrange(40, board_y - 40, 10)
                Extra_segment.append(extra_segment)

            # draw extra element

            if Extra_segment:
                Extra_segment[0].draw_segment()

            # check strike

            if Extra_segment:
                if Strike(snake_head, Extra_segment[0]):

                    # add new element to snake body

                    new_segment = Segment(class_screen=screen)
                    Snake.append(new_segment)
                    if bonus_points == True:
                        Total_score += 2
                    else:
                        Total_score += 1

                    # check extra element color, if correct change acceleration

                    if Extra_segment[0].color == (0, 50, 200):
                        acceleration = 0.5
                        bonus_points = True
                        acceleration_score = Total_score        # new variable to cancel acceleration


                    # remove extra element

                    Extra_segment.remove(Extra_segment[0])

            pygame.display.flip()       # change board

            # # check if snake head hit snake body

            if Wrapping(snake_head, Snake) == True:
                Fail = True

            # check if snake head went beyond frame

            if snake_head.position_x < 10 or snake_head.position_x > board_x - 20:      # add frame and segment width
                Fail = True
            if snake_head.position_y < 10 or snake_head.position_y > board_y - 20:
                Fail = True

    # inscription 'GAME OVER'

    game_over = "GAME OVER"
    score = "Your score:     " + str(Total_score)
    next_board = "-- press Enter --"

    text_game_over = font_gameover.render(game_over, True, (250, 250, 0))
    text_game_over_Rect = text_game_over.get_rect()
    text_game_over_Rect.center = (board_x // 2, board_y // 2 - 100)

    text_score = font_player_score.render(score, True, (250, 250, 0))
    text_score_Rect = text_score.get_rect()
    text_score_Rect.center = (board_x // 2, board_y // 2 + 40)

    text_next_board = font_next_board.render(next_board, True, (250, 250, 0))
    text_next_board_Rect = text_next_board.get_rect()
    text_next_board_Rect.center = (board_x // 2, board_y // 2 + 150)

    display_game_over = True
    while display_game_over:
        screen.fill((0, 0, 0))
        screen.blit(text_game_over, text_game_over_Rect)
        screen.blit(text_score, text_score_Rect)
        screen.blit(text_next_board, text_next_board_Rect)
        frame.draw_frame()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    display_game_over = False

    # check if player can be added to best players list

    if check_result_file() == True:
        file = open("Best_Snake_results", "rb")
        scores_list = pickle.load(file)
        best_players_number = len(scores_list)

        # if on the best players list is less than 8 positions - add player to list,
        # else - check the last player's score

        if best_players_number < 8:
            write_on_list = True
        else:
            if scores_list[7][0] < Total_score:
                write_on_list = True
            else:
                write_on_list = False

    else:
        first_score = True

    give_name = True
    name = "_"
    enter_name = "Enter your name and press button 'Enter'"
    if write_on_list == True or first_score == True:

        while give_name:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if len(name) < 10:
                    if event.type == pygame.KEYDOWN:
                        if name == "_":
                            name = ""
                        if event.key == pygame.K_a:
                            name += "A"
                        if event.key == pygame.K_b:
                            name += "B"
                        if event.key == pygame.K_c:
                            name += "C"
                        if event.key == pygame.K_d:
                            name += "D"
                        if event.key == pygame.K_e:
                            name += "E"
                        if event.key == pygame.K_f:
                            name += "F"
                        if event.key == pygame.K_g:
                            name += "G"
                        if event.key == pygame.K_h:
                            name += "H"
                        if event.key == pygame.K_i:
                            name += "I"
                        if event.key == pygame.K_j:
                            name += "J"
                        if event.key == pygame.K_k:
                            name += "K"
                        if event.key == pygame.K_l:
                            name += "L"
                        if event.key == pygame.K_m:
                            name += "M"
                        if event.key == pygame.K_n:
                            name += "N"
                        if event.key == pygame.K_o:
                            name += "O"
                        if event.key == pygame.K_p:
                            name += "P"
                        if event.key == pygame.K_r:
                            name += "R"
                        if event.key == pygame.K_s:
                            name += "S"
                        if event.key == pygame.K_t:
                            name += "T"
                        if event.key == pygame.K_u:
                            name += "U"
                        if event.key == pygame.K_w:
                            name += "W"
                        if event.key == pygame.K_x:
                            name += "X"
                        if event.key == pygame.K_y:
                            name += "Y"
                        if event.key == pygame.K_v:
                            name += "V"
                        if event.key == pygame.K_z:
                            name += "Z"
                        if event.key == pygame.K_SPACE:
                            name += "_"
                        if event.key == pygame.K_RETURN:
                            give_name = False

                else:
                    name = name
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            give_name = False

            screen.fill((0, 0, 0))

            text_give_name = font_player_score.render(enter_name, True, (0, 0, 200))
            text_give_name_Rect = text_give_name.get_rect()
            text_give_name_Rect.center = (board_x // 2, board_y // 2 - 70)

            text_name = font.render(name, True, (0, 0, 200))
            text_name_Rect = text_name.get_rect()
            text_name_Rect.center = (board_x // 2, board_y // 2)

            screen.blit(text_give_name, text_give_name_Rect)
            screen.blit(text_name, text_name_Rect)
            frame.draw_frame()
            pygame.display.update()


    # create file and add score to list

    if first_score == True:
        scores_list = []
        record = (Total_score, name)
        scores_list.append(record)
        file = open("Best_Snake_results", "wb")
        pickle.dump(scores_list, file)
        file.close()

    # upload list from the file and add new score, leave only eight best scores

    if write_on_list == True:
        record = (Total_score, name)
        file = open("Best_Snake_results", "rb")
        scores_list = pickle.load(file)
        scores_list.append(record)
        scores_list.sort(reverse=True)
        scores_list = scores_list[:8]
        file.close()
        file = open("Best_Snake_results", "wb")
        pickle.dump(scores_list, file)
        file.close()

    # display best scores

    file = open("Best_Snake_results", "rb")
    scores_list = pickle.load(file)

    best_scores = "Best players"
    text_best_scores = font.render(best_scores, True, (255, 255, 0))
    text_best_scores_Rect = text_best_scores.get_rect()
    best_scores_position = board_y // 2 - 150
    text_best_scores_Rect.center = (board_x // 2, best_scores_position)

    # change best scores position

    best_scores_position += 50

    while True:
        screen.fill((0, 0, 0))
        screen.blit(text_best_scores, text_best_scores_Rect)

        Write_player_score(class_screen=screen, list=scores_list, font=font_scores, board_dimension_x=board_x,
                            text_place=best_scores_position)
        frame.draw_frame()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)



