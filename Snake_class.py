import pygame
# create snake segment class

class Segment():
    # init function with arguments

    def __init__(self, class_screen, color = (255, 255, 0), position_x = 0, position_y = 0, length = 10, width = 10):
        self.class_screen = class_screen
        self.color = color
        self.position_x = position_x
        self.position_y = position_y
        self.length = length
        self.width = width

    # drawing function
    def draw_segment(self):
        pygame.draw.rect(self.class_screen, self.color, pygame.Rect(self.position_x, self.position_y, self.length, self.width))

# create frame class

class Frame():
    def __init__(self, class_screen, color = (0, 0, 200), frame_x = 0, frame_y = 0):
        self.class_screen = class_screen
        self.color = color
        self.frame_x = frame_x
        self.frame_y = frame_y

    # drawing function

    def draw_frame(self):
        pygame.draw.rect(self.class_screen, self.color, pygame.Rect(0, 0, 10, self.frame_y))
        pygame.draw.rect(self.class_screen, self.color, pygame.Rect(0, 0, self.frame_x, 10))
        pygame.draw.rect(self.class_screen, self.color, pygame.Rect(self.frame_x - 10, 0, 10, self.frame_y))
        pygame.draw.rect(self.class_screen, self.color, pygame.Rect(0, self.frame_y - 10, self.frame_x, 10))


# function which writes down results achieved by best players

def Write_player_score(class_screen, list, font, board_dimension_x, text_place):
    move_score = 30

    for record in list:

        name_player = record[1]
        score_player = str(record[0])
        name = font.render(name_player, True, (255, 255, 0))
        name_Rect = name.get_rect()
        name_Rect.midleft = (board_dimension_x // 2 - 140, text_place + move_score)

        score = font.render(score_player, True, (255, 255, 0))
        score_Rect = score.get_rect()
        score_Rect.midleft = (board_dimension_x // 2 + 80, text_place + move_score)
        move_score += 30


        class_screen.blit(name, name_Rect)
        class_screen.blit(score, score_Rect)







