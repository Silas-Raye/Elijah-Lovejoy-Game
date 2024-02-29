import pygame
import os
import time
import random
import asyncio



async def main():

    # Initialize Pygame and set up the screen
    pygame.init()
    screen_width = 1248
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("The Observer")
    clock = pygame.time.Clock()

    # Lovejoy sprite
    class MainCharacter(pygame.sprite.Sprite):
        def __init__(self, start_pos=(0, 0), scale=1):
            super().__init__()
            self.scale = scale
            self.images = {
                "idle": [pygame.image.load(os.path.join("assets", "lovejoy", f"idle-{i}.png")).convert_alpha() for i in range(1, 10)],
                "walk": [pygame.image.load(os.path.join("assets", "lovejoy", f"walk-{i}.png")).convert_alpha() for i in range(1, 10)]
            }
            self.current_frame = 0
            self.image = self.images["idle"][0]
            self.rect = self.image.get_rect()
            self.rect.topleft = start_pos
            self.direction = "right"  # Initial direction
            self.action = "idle"      # Initial action

        def update(self):
            if self.action == "walk":
                self.current_frame = (self.current_frame + 1) % len(self.images["walk"])
                self.image = pygame.transform.scale(self.images["walk"][self.current_frame], 
                                                    (int(self.rect.width * self.scale), int(self.rect.height * self.scale)))
            elif self.action == "idle":
                self.current_frame = (self.current_frame + 1) % len(self.images["idle"])
                self.image = pygame.transform.scale(self.images["idle"][self.current_frame], 
                                                    (int(self.rect.width * self.scale), int(self.rect.height * self.scale)))
            
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    main_character = MainCharacter(start_pos=(-325, 325), scale=12)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(main_character)
    character_speed = 27

    # Paperboy sprite
    class PaperBoy(pygame.sprite.Sprite):
        def __init__(self, start_pos=(0, 0), scale=1):
            super().__init__()
            self.scale = scale
            self.images = {
                "idle": [pygame.image.load(os.path.join("assets", "paperboy", f"idle-{i}.png")).convert_alpha() for i in range(1, 10)],
                "walk": [pygame.image.load(os.path.join("assets", "paperboy", f"walk-{i}.png")).convert_alpha() for i in range(1, 10)]
            }
            self.current_frame = 0
            self.image = self.images["idle"][0]
            self.rect = self.image.get_rect()
            self.rect.topleft = start_pos
            self.direction = "right"  # Initial direction
            self.action = "idle"      # Initial action

        def update(self):
            if self.action == "walk":
                self.current_frame = (self.current_frame + 1) % len(self.images["walk"])
                self.image = pygame.transform.scale(self.images["walk"][self.current_frame], 
                                                    (int(self.rect.width * self.scale), int(self.rect.height * self.scale)))
            elif self.action == "idle":
                self.current_frame = (self.current_frame + 1) % len(self.images["idle"])
                self.image = pygame.transform.scale(self.images["idle"][self.current_frame], 
                                                    (int(self.rect.width * self.scale), int(self.rect.height * self.scale)))
            
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    paper_boy = PaperBoy(start_pos=(174, 348), scale=12)

    # Printer sprite
    class PrinterGuy(pygame.sprite.Sprite):
        def __init__(self, start_pos=(0, 0), scale=1):
            super().__init__()
            self.scale = scale
            self.images = {
                "idle": [pygame.image.load(os.path.join("assets", "printer", f"idle-{i}.png")).convert_alpha() for i in range(1, 10)],
                "work": [pygame.image.load(os.path.join("assets", "printer", f"work-{i}.png")).convert_alpha() for i in range(1, 10)]
            }
            self.current_frame = 0
            self.image = self.images["idle"][0]
            self.rect = self.image.get_rect()
            self.rect.topleft = start_pos
            self.direction = "right"  # Initial direction
            self.action = "idle"      # Initial action

        def update(self):
            if self.action == "work":
                self.current_frame = (self.current_frame + 1) % len(self.images["work"])
                self.image = pygame.transform.scale(self.images["work"][self.current_frame], 
                                                    (int(self.rect.width * self.scale), int(self.rect.height * self.scale)))
            elif self.action == "idle":
                self.current_frame = (self.current_frame + 1) % len(self.images["idle"])
                self.image = pygame.transform.scale(self.images["idle"][self.current_frame], 
                                                    (int(self.rect.width * self.scale), int(self.rect.height * self.scale)))
            
            if self.direction == "left":
                self.image = pygame.transform.flip(self.image, True, False)

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    printer_guy = PrinterGuy(start_pos=(474, 348), scale=12)

    # Define color variables
    gold = (204, 170, 0)
    maroon = (128, 0, 0)
    forest_green = (34, 139, 34)
    tan = (210, 180, 140)
    dark_tan = (170, 136, 85)
    darker_tan = (120, 86, 35)
    white = (255, 255, 255)
    transparent_grey = (128, 128, 128, 128)
    black = (0, 0, 0)

    # Load fonts and images
    bar_font = pygame.font.Font("assets/pixelated-times-new-roman.ttf", 50)
    medium_font = pygame.font.Font("assets/pixelated-times-new-roman.ttf", 75)
    large_font = pygame.font.Font("assets/pixelated-times-new-roman.ttf", 100)
    extra_large_font = pygame.font.Font("assets/pixelated-times-new-roman.ttf", 200)

    background = pygame.image.load(os.path.join("assets", "background.png")).convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    printing_press = pygame.image.load(os.path.join("assets", "printing-press.png")).convert_alpha()
    printing_press.set_colorkey(white)  # Set white color as transparent
    press_scale = .7
    shop_press = pygame.transform.scale(printing_press, (printing_press.get_width()*press_scale, printing_press.get_height()*press_scale))
    shop_press.set_colorkey(white)

    ink = pygame.image.load(os.path.join("assets", "ink.png")).convert_alpha()
    ink.set_colorkey(white)  # Set white color as transparent
    ink_scale = 1.8
    shop_ink = pygame.transform.scale(ink, (ink.get_width()*ink_scale, ink.get_height()*ink_scale))
    shop_ink.set_colorkey(white)

    paper = pygame.image.load(os.path.join("assets", "paper.png")).convert_alpha()
    paper.set_colorkey(white)  # Set white color as transparent
    paper_scale = 2
    shop_paper = pygame.transform.scale(paper, (paper.get_width()*paper_scale, paper.get_height()*paper_scale))
    shop_paper.set_colorkey(white)

    news = pygame.image.load(os.path.join("assets", "news.png")).convert_alpha()
    news.set_colorkey(white)  # Set white color as transparent

    shop_og = pygame.image.load(os.path.join("assets", "shop.png")).convert_alpha()
    shop_scale = 1
    shop = pygame.transform.scale(shop_og, (shop_og.get_width()*shop_scale, shop_og.get_height()*shop_scale))
    shop.set_colorkey(white)  # Set white color as transparent

    home_og = pygame.image.load(os.path.join("assets", "home.png")).convert_alpha()
    home_scale = 1
    home = pygame.transform.scale(home_og, (home_og.get_width()*home_scale, home_og.get_height()*home_scale))
    home.set_colorkey(white)  # Set white color as transparent

    mob_og = pygame.image.load(os.path.join("assets", "mob.png")).convert_alpha()
    mob_scale = 2
    mob = pygame.transform.scale(mob_og, (mob_og.get_width()*mob_scale, mob_og.get_height()*mob_scale))
    mob.set_colorkey(white)  # Set white color as transparent

    pb_shop = pygame.image.load(os.path.join("assets", "paperboy", "walk-3.png")).convert_alpha()
    pb_scale = 7
    paper_boy_shop = pygame.transform.scale(pb_shop, (pb_shop.get_width()*pb_scale, pb_shop.get_height()*pb_scale))
    paper_boy_shop.set_colorkey(white)  # Set white color as transparent

    pg_shop = pygame.image.load(os.path.join("assets", "printer", "idle-1.png")).convert_alpha()
    pg_scale = 6
    printing_guy_shop = pygame.transform.scale(pg_shop, (pg_shop.get_width()*pg_scale, pg_shop.get_height()*pg_scale))
    printing_guy_shop.set_colorkey(white)  # Set white color as transparent

    title_text_og = pygame.image.load(os.path.join("assets", "title-text.png")).convert_alpha()
    title_text_scale = .5
    title_text = pygame.transform.scale(title_text_og, (title_text_og.get_width()*title_text_scale, title_text_og.get_height()*title_text_scale))
    title_text.set_colorkey(white)   # Set white color as transparent

    history_text_og = pygame.image.load(os.path.join("assets", "history-text.png")).convert_alpha()
    history_text_scale = .5
    history_text = pygame.transform.scale(history_text_og, (history_text_og.get_width()*history_text_scale, history_text_og.get_height()*history_text_scale))
    history_text.set_colorkey(white)   # Set white color as transparent

    credit_text_og = pygame.image.load(os.path.join("assets", "credit-text.png")).convert_alpha()
    credit_text_scale = .5
    credit_text = pygame.transform.scale(credit_text_og, (credit_text_og.get_width()*credit_text_scale, credit_text_og.get_height()*credit_text_scale))
    credit_text.set_colorkey(white)   # Set white color as transparent

    win_text_og = pygame.image.load(os.path.join("assets", "win-text.png")).convert_alpha()
    win_text_scale = .5
    win_text = pygame.transform.scale(win_text_og, (win_text_og.get_width()*win_text_scale, win_text_og.get_height()*win_text_scale))
    win_text.set_colorkey(white)   # Set white color as transparent

    lose_text_og = pygame.image.load(os.path.join("assets", "lose-text.png")).convert_alpha()
    lose_text_scale = .5
    lose_text = pygame.transform.scale(lose_text_og, (lose_text_og.get_width()*lose_text_scale, lose_text_og.get_height()*lose_text_scale))
    lose_text.set_colorkey(white)   # Set white color as transparent

    # Load sound
    pygame.mixer.init()
    buying_ink_sound = pygame.mixer.Sound("assets/sound/buying-ink.mp3")
    buying_paper_sound = pygame.mixer.Sound("assets/sound/buying-paper-louder.mp3")
    newspaper_sale_sound = pygame.mixer.Sound("assets/sound/newspaper-sale-louder.mp3")
    buying_printing_press_sound = pygame.mixer.Sound("assets/sound/buying-printing-press.mp3")
    step_sounds = []
    for i in range(1, 7):
        sound_path = os.path.join("assets", "sound", "steps", f"step-{i}.mp3")
        step_sound = pygame.mixer.Sound(sound_path)
        step_sounds.append(step_sound)
    step_channel = pygame.mixer.Channel(1)
    normal_music = pygame.mixer.Sound("assets/sound/normal-music-quieter.mp3")
    mob_music = pygame.mixer.Sound("assets/sound/mob-music.mp3")

    # Set up the initial music
    current_music = normal_music
    current_music.play(loops=-1)  # Start playing the normal music on loop initially

    # Functions
    def draw_ink_bottles(num_bottles):
        x = 115
        y = 146

        for _ in range(num_bottles):
            screen.blit(ink, (x, y))
            x += ink.get_width()

    def draw_paper(num_stacks):
        x = 875
        y = 360

        for _ in range(num_stacks):
            screen.blit(paper, (x, y))
            y -= paper.get_height() / 2
            
    def draw_news_paper(num_stacks):
        remaining_stacks = num_stacks
        x1 = 130
        x2 = 130 + news.get_width() + 12
        y1 = 400
        y2 = 400

        for _ in range(num_stacks):
            if remaining_stacks % 2 != 0:
                screen.blit(news, (x1, y1))
                y1 -= news.get_height() / 2
            else:
                screen.blit(news, (x2, y2))
                y2 -= news.get_height() / 2
            remaining_stacks -= 1

    def draw_progress_bar(x, y, width, height, percent, color, label):
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height))  # Background of progress bar
        fill_width = percent * width / 100
        pygame.draw.rect(screen, color, (x, y, fill_width, height))  # Filling progress bar
        text = bar_font.render(label, True, white)
        screen.blit(text, (x, y - 40))

    def draw_thought_bubble(screen, x, y, texts):    
        # Calculate the size of the bubble
        max_width = max(bar_font.size(text)[0] for text in texts)
        bubble_width = max_width + 30
        bubble_height = len(texts) * bar_font.get_linesize() + 20
        
        # Draw the bubble
        pygame.draw.rect(screen, black, (x-5, y-5, bubble_width+10, bubble_height+10))
        pygame.draw.rect(screen, white, (x, y, bubble_width, bubble_height))
        
        # Draw the text
        for index, text in enumerate(texts):
            text_rendered = bar_font.render(text, True, black)
            text_rect = text_rendered.get_rect(center=(x + bubble_width // 2, y + 25 + index * bar_font.get_linesize()))
            screen.blit(text_rendered, text_rect)

    def draw_paragraph(start_x, start_y, lines):
        x, y = start_x, start_y
        
        for line in lines:
            text_surface = bar_font.render(line, True, darker_tan)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y)
            screen.blit(text_surface, text_rect)
            y += text_rect.height # Adjusting vertical spacing

    def play_random_step_sound():
        # Check if the step channel is not busy
        if not step_channel.get_busy():
            # Select a random step sound
            random_step_sound = random.choice(step_sounds)
            # Play the selected step sound
            step_channel.play(random_step_sound)

    # Main game loop
    running = True
    shopping = False
    movement_enabled = False
    character_frozen = False
    shopping_enabled = True
    printer_guy_progress = 0
    alpha = 0
    money = 137
    outrage = 0
    inspo = 0
    num_ink = 0
    num_paper = 0
    num_news = 0
    lvl_time = 120
    paper_price = 20
    tutorial_stage = 1
    screen_num = 0
    has_paperboy = False
    has_printer = False
    has_printing_press = False
    timer_started = False
    start_time = None
    holding_news = False
    paperboy_holding_news = False
    play_black = False
    history_black = False
    credits_black = False
    sequence = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
    sequence_index = 0
    mob_scroll = -mob.get_width()
    printing_press_scroll = 156
    last_key_time = {pygame.K_a: 0, pygame.K_b: 0, pygame.K_c: 0, pygame.K_d: 0, pygame.K_e: 0,
                    pygame.K_f: 0, pygame.K_g: 0, pygame.K_h: 0, pygame.K_i: 0, pygame.K_j: 0,
                    pygame.K_k: 0, pygame.K_l: 0, pygame.K_m: 0, pygame.K_n: 0, pygame.K_o: 0,
                    pygame.K_p: 0, pygame.K_q: 0, pygame.K_r: 0, pygame.K_s: 0, pygame.K_t: 0,
                    pygame.K_u: 0, pygame.K_v: 0, pygame.K_w: 0, pygame.K_x: 0, pygame.K_y: 0,
                    pygame.K_z: 0}


    while running:
        for event in pygame.event.get():
            if screen_num == 0:
                if event.type == pygame.MOUSEMOTION:
                    # Check if the mouse is over each text element and update boolean variables accordingly
                    play_black = (130 <= event.pos[0] <= 130 + large_font.size("PLAY")[0]) and (365 <= event.pos[1] <= 365 + large_font.size("PLAY")[1])
                    history_black = (500 <= event.pos[0] <= 500 + large_font.size("HISTORY")[0]) and (365 <= event.pos[1] <= 365 + large_font.size("HISTORY")[1])
                    credits_black = (920 <= event.pos[0] <= 920 + large_font.size("CREDITS")[0]) and (365 <= event.pos[1] <= 365 + large_font.size("CREDITS")[1])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_black:
                        screen_num = 1
                    elif history_black:
                        screen_num = 2
                    elif credits_black:
                        screen_num = 3
            elif screen_num == 1:
                if event.type == pygame.KEYDOWN and 755 <= main_character.rect.x <= 999 and not holding_news:
                    current_time = time.time()
                    if event.key in last_key_time:
                        if current_time - last_key_time[event.key] >= 1:
                            inspo += 1
                            if inspo > 100: inspo = 100
                            last_key_time[event.key] = current_time
                elif event.type == pygame.KEYDOWN and 295 <= main_character.rect.x <= 650 and has_printing_press and inspo >= 20 and num_ink >= 1 and num_paper >= 1:
                    if event.key == pygame.K_RETURN:
                        if sequence_index == len(sequence):
                                sequence_index = 0
                                inspo -= 20
                                num_ink -= 1
                                num_paper -= 1
                                num_news += 1
                    elif sequence_index < len(sequence) and event.unicode.lower() in sequence and event.unicode.lower() == sequence[sequence_index]:
                        sequence_index += 1
                    else:
                        sequence_index = 0
                elif -1 <= main_character.rect.x <= 250 and num_news >= 1 and not holding_news:
                    num_news -= 1
                    holding_news = True
                elif main_character.rect.x <= -100 and holding_news:
                    money += paper_price
                    holding_news = False
                    newspaper_sale_sound.play()
                    if not timer_started:
                        timer_started = True
                        start_time = time.time()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if home.get_rect(topleft=(20, 25)).collidepoint(event.pos):
                        play_black = False
                        screen_num = 0
                    elif shop.get_rect(topleft=(1140, 25)).collidepoint(event.pos) and not shopping and shopping_enabled:
                        shopping = True
                        if tutorial_stage == 1: tutorial_stage += 1
                    elif shopping and 100 <= event.pos[0] <= 160 and 150 <= event.pos[1] <= 210:
                        shopping = False
                    elif shopping and 195 <= event.pos[0] <= 195+190 and 205 <= event.pos[1] <= 205+190 and money >= 2 and num_ink < 5:
                        if tutorial_stage <= 5 and num_ink != 1:
                            buying_ink_sound.play()
                            money -= 2
                            num_ink += 1
                        elif tutorial_stage > 5:
                            buying_ink_sound.play()
                            money -= 2
                            num_ink += 1
                    elif shopping and 195 <= event.pos[0] <= 195+190 and 465 <= event.pos[1] <= 465+190 and money >= 5 and num_paper < 5:
                        if tutorial_stage <= 5 and num_paper != 1:
                            buying_paper_sound.play()
                            money -= 5
                            num_paper += 1
                        elif tutorial_stage > 5:
                            buying_paper_sound.play()
                            money -= 5
                            num_paper += 1
                    elif shopping and 430 <= event.pos[0] <= 430+390 and 235 <= event.pos[1] <= 235+390 and money >= 130 and not has_printing_press:
                        if 11 <= tutorial_stage <= 12:
                            money -= 130
                            tutorial_stage = 13
                        else:
                            money -= 130
                            has_printing_press = True
                            buying_printing_press_sound.play()
                    elif shopping and 865 <= event.pos[0] <= 865+190 and 465 <= event.pos[1] <= 465+190 and money >= 140 and not has_paperboy:
                        money -= 140
                        has_paperboy = True
                    elif shopping and 865 <= event.pos[0] <= 865+190 and 205 <= event.pos[1] <= 205+190 and money >= 150 and not has_printer:
                        money -= 140
                        has_printer = True
            elif screen_num >= 2:
                if event.type == pygame.MOUSEBUTTONDOWN and 1155 <= event.pos[0] <= 1155+65 and 685 <= event.pos[1] <= 685+65:
                    history_black = False
                    credits_black = False
                    play_black = False
                    screen_num = 0

        if screen_num == 1:
            # Start the timer if the player gets to 6 newspapers
            if not timer_started and num_news > 5:
                timer_started = True
                start_time = time.time()

            # Draw background
            screen.blit(background, (0, 0))
            if has_printing_press:
                screen.blit(printing_press, (393, printing_press_scroll))

            # Draw sprites
            draw_ink_bottles(num_ink)
            draw_paper(num_paper)
            draw_news_paper(num_news)

            # Draw progress bars
            draw_progress_bar(135, 60, 300, 50, (money / 1000) * 100, forest_green, f"Money ${money}")
            draw_progress_bar(470, 60, 300, 50, outrage, maroon, "Outrage")
            draw_progress_bar(805, 60, 300, 50, inspo, gold, "Inspiration")

            # Timer
            if timer_started:
                # Calculate outrage increment based on elapsed time
                elapsed_time = time.time() - start_time
                if elapsed_time < lvl_time:  # Ensure outrage fills in 2 minutes
                    outrage = (elapsed_time / lvl_time) * 100
                else:
                    outrage = 100

            # Draw shop button
            screen.blit(shop, (1140, 25))
            screen.blit(home, (20, 25))

            # Tutorial
            if not shopping:
                if movement_enabled and tutorial_stage == 1:
                    draw_thought_bubble(screen, 870, 132, ["Buy a printing press, paper,", "and ink from the shop."])

                if tutorial_stage == 3:
                    if inspo < 20: draw_thought_bubble(screen, 860, 157, ["Type letters at the desk", "to gain inspiration."])
                    if inspo >= 20: tutorial_stage += 1

                if tutorial_stage == 5:
                    draw_thought_bubble(screen, 40, 295, ["Pick up the newspaper", "and take it out the door to sell it."])
                    if timer_started: tutorial_stage += 1

                if tutorial_stage == 6:
                    draw_thought_bubble(screen, 750, 145, ["Now that you've sold your first paper", "preaching the abolition of slavery,", "it's only a matter of time before", "a pro-slavery mob comes for you.", "Quick! Buy more supplies", "and get to printing!!"])
                    if outrage >= 10: tutorial_stage += 1

                if tutorial_stage == 8 and alpha == 0:
                    draw_thought_bubble(screen, 710, 145, ["After having your printing press destroyed", "and receiving several death threats,", "you decide to move across the Mississippi", "to the free state of Illinois.", "There you buy a new printing press", "and continue to preach abolition."])
                    if timer_started: tutorial_stage += 1

                if tutorial_stage == 9:
                    draw_thought_bubble(screen, 390, 145, ["You have become famous for your radical views,", "and you sell more newspapers than ever before.", "Your papers now sell for more,", "but public outrage increases quicker."])
                    if outrage >= 10: tutorial_stage += 1

                if tutorial_stage == 11 and alpha == 0:
                    draw_thought_bubble(screen, 422, 175, ["\"I can die at my post, but I cannot desert it.\""])
                    if timer_started: tutorial_stage += 1

            # Have Lovejoy walk on screen
            if main_character.rect.x < (screen_width // 2) - 150 and not movement_enabled:
                main_character.direction = "right"
                main_character.action = "walk"
                main_character.rect.x += character_speed  # Move the character towards the center of the screen
                play_random_step_sound()
            elif outrage < 100:
                movement_enabled = True  # Enable movement once the character reaches the center

            # Draw Lovejoy
            keys = pygame.key.get_pressed()
            if movement_enabled and not character_frozen:  # Allow movement only when enabled
                if keys[pygame.K_LEFT] and main_character.rect.x > -250:  # Check if not at left edge
                    main_character.direction = "left"
                    main_character.action = "walk"
                    main_character.rect.x -= character_speed
                    play_random_step_sound()
                elif keys[pygame.K_RIGHT] and main_character.rect.x < (screen_width - 250):  # Check if not at right edge
                    main_character.direction = "right"
                    main_character.action = "walk"
                    main_character.rect.x += character_speed
                    play_random_step_sound()
                else:
                    main_character.action = "idle"
            elif character_frozen:
                main_character.action = "idle"

            # Draw paperboy
            if has_paperboy:
                all_sprites.add(paper_boy)

                if num_news == 0 and paper_boy.rect.x == 174:
                    paper_boy.direction = "left"
                    paper_boy.action = "idle"
                elif num_news >= 1 and 150 <= paper_boy.rect.x <= 250 and not paperboy_holding_news:
                    num_news -= 1
                    paperboy_holding_news = True
                elif paper_boy.rect.x <= -250 and paperboy_holding_news:
                    money += paper_price
                    paperboy_holding_news = False
                    newspaper_sale_sound.play()
                    if not timer_started:
                        timer_started = True
                        start_time = time.time()

                if paperboy_holding_news:
                    paper_boy.direction = "left"
                    paper_boy.action = "walk"
                    paper_boy.rect.x -= character_speed
                    play_random_step_sound()
                elif paper_boy.rect.x <= 150 and not paperboy_holding_news:
                    paper_boy.direction = "right"
                    paper_boy.action = "walk"
                    paper_boy.rect.x += character_speed
                    play_random_step_sound()

            # Draw printer
            if has_printer:
                all_sprites.add(printer_guy)

                if has_printing_press and num_paper >= 1 and num_ink >= 1 and inspo >= 20:
                    printer_guy.direction = "right"
                    printer_guy.action = "work"
                    printer_guy_progress += 1
                    if printer_guy_progress >= 20:
                        printer_guy_progress = 0
                        num_news += 1
                        num_ink -= 1
                        num_paper -= 1
                        inspo -= 20
                else:
                    printer_guy.direction = "right"
                    printer_guy.action = "idle"

            # Update Lovejoy
            all_sprites.update()
            all_sprites.draw(screen)

            # Holding newspaper animation
            if holding_news:
                if main_character.direction == "left":
                    screen.blit(news, (main_character.rect.x, main_character.rect.y + 90))
                elif main_character.direction == "right":
                    screen.blit(news, (main_character.rect.x + 130, main_character.rect.y + 90))
            if paperboy_holding_news:
                if paper_boy.direction == "left":
                    screen.blit(news, (paper_boy.rect.x, paper_boy.rect.y + 90))
                elif paper_boy.direction == "right":
                    screen.blit(news, (paper_boy.rect.x + 130, paper_boy.rect.y + 90))

            # Draw shop
            if shopping:
                pygame.draw.rect(screen, tan, (100, 150, screen_width - 200, screen_height - 200)) # Draw the background

                text = large_font.render("X", True, dark_tan) # Draw the X that closes the shop
                screen.blit(text, (115, 145))

                small_transparent_surface = pygame.Surface((190, 190), pygame.SRCALPHA)
                small_transparent_surface.fill(transparent_grey)
                large_transparent_surface = pygame.Surface((390, 390), pygame.SRCALPHA)
                large_transparent_surface.fill(transparent_grey)

                pygame.draw.rect(screen, dark_tan, (190, 200, 200, 200))
                pygame.draw.rect(screen, tan, (195, 205, 190, 190))
                screen.blit(shop_ink, (242, 216))
                text = bar_font.render("Ink" + " " * 16 + "$2", True, white)
                screen.blit(text, (195, 400))
                if money < 2 or num_ink >= 5 or (tutorial_stage <= 5 and num_ink == 1):
                    screen.blit(small_transparent_surface, (195, 205))

                pygame.draw.rect(screen, dark_tan, (190, 460, 200, 200))
                pygame.draw.rect(screen, tan, (195, 465, 190, 190))
                screen.blit(shop_paper, (208, 495))
                text = bar_font.render("Paper" + " " * 12 + "$5", True, white)
                screen.blit(text, (195, 660))
                if money < 5 or num_paper >= 5 or (tutorial_stage <= 5 and num_paper == 1):
                    screen.blit(small_transparent_surface, (195, 465))
                
                pygame.draw.rect(screen, dark_tan, (860, 200, 200, 200))
                pygame.draw.rect(screen, tan, (865, 205, 190, 190))
                screen.blit(printing_guy_shop, (905, 210))
                text = bar_font.render("Printer" + " " * 7 + "$150", True, white)
                screen.blit(text, (865, 400))
                if money < 150 or has_printer:
                    screen.blit(small_transparent_surface, (865, 205))

                pygame.draw.rect(screen, dark_tan, (860, 460, 200, 200))
                pygame.draw.rect(screen, tan, (865, 465, 190, 190))
                screen.blit(paper_boy_shop, (895, 452))
                text = bar_font.render("Paper Boy" + " " * 2 + "$140", True, white)
                screen.blit(text, (865, 660))
                if money < 140 or has_paperboy:
                    screen.blit(small_transparent_surface, (865, 465))

                pygame.draw.rect(screen, dark_tan, (425, 230, 400, 400))
                pygame.draw.rect(screen, tan, (430, 235, 390, 390))
                screen.blit(shop_press, (485, 260))
                text = bar_font.render("Printing Press" + " " * 22 + "$130", True, white)
                screen.blit(text, (430, 630))
                if money < 130 or has_printing_press:
                    screen.blit(large_transparent_surface, (430, 235))

                if tutorial_stage == 2:
                    draw_thought_bubble(screen, 750, 170, ["Click on items", "to buy them."])
                    if has_printing_press and num_ink == 1 and num_paper == 1: tutorial_stage += 1

                if tutorial_stage == 13:
                    draw_thought_bubble(screen, 345, 370, ["The mob intercepts your third printing press", "and throws it into the river.", "You must buy another one to continue printing."])
                    if has_printing_press: tutorial_stage += 1

            if not shopping and tutorial_stage == 4:
                    draw_thought_bubble(screen, 345, 600, ["Stand in front of the printing press", "and roll it with ink by sliding", "your finger across the home row (A-L)", "then hit enter to press a newspaper."])
                    if num_news >= 1: tutorial_stage += 1

            if outrage == 100:
                if current_music != mob_music:
                    current_music.stop()  # Stop current music
                    current_music = mob_music  # Change to mob music
                    current_music.play(loops=-1)  # Start playing mob music on loop
                shopping = False
                character_frozen = True
                shopping_enabled = False
                if mob_scroll > -400 and alpha < 255:
                    alpha += 5
                    rectangle_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                    rectangle_surface.fill((0, 0, 0, alpha))
                    screen.blit(rectangle_surface, (0, 0))
                if alpha == 255:
                    if current_music != normal_music:
                        current_music.fadeout(1000)  # Fade out the current music
                        current_music = normal_music  # Change to normal music
                        current_music.play(loops=-1, fade_ms=1000)  # Start playing normal music with fade-in
                    tutorial_stage += 1
                    outrage = 0
                    inspo = 0
                    num_ink = 0
                    num_news = 0
                    num_paper = 0
                    printing_press_scroll = 156
                    mob_scroll = -mob.get_width()
                    has_printing_press = False
                    character_frozen = False
                    shopping_enabled = True
                    timer_started = False
                    start_time = None
                    holding_news = False
                    if tutorial_stage == 8:
                        lvl_time = 80
                        paper_price = 25
                        if money < 137:
                            money = 137
                            has_paperboy = False
                            all_sprites.remove(paper_boy)
                            has_printer = False
                            all_sprites.remove(printer_guy)
                            lvl_time = 120
                            paper_price = 20
                            tutorial_stage = 1
                            screen_num = 5
                    if tutorial_stage == 11:
                        lvl_time = 40
                        paper_price = 30
                        if money < 267:
                            money = 137
                            has_paperboy = False
                            all_sprites.remove(paper_boy)
                            has_printer = False
                            all_sprites.remove(printer_guy)
                            lvl_time = 120
                            paper_price = 20
                            tutorial_stage = 1
                            screen_num = 5
                    if tutorial_stage >= 13:
                        money = 137
                        has_paperboy = False
                        all_sprites.remove(paper_boy)
                        has_printer = False
                        all_sprites.remove(printer_guy)
                        lvl_time = 120
                        paper_price = 20
                        tutorial_stage = 1
                        screen_num = 4
                    pygame.time.delay(1000)
                else:
                    if mob_scroll <= -20: mob_scroll += 20
                    if printing_press_scroll < 550 and mob_scroll > -1500: printing_press_scroll += random.randint(-3, 10)
                    screen.blit(mob, (mob_scroll, 150))
            elif alpha > 0:
                alpha -= 5
                rectangle_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                rectangle_surface.fill((0, 0, 0, alpha))
                screen.blit(rectangle_surface, (0, 0))

        elif screen_num == 0:
            pygame.draw.rect(screen, tan, (0, 0, screen_width, screen_height))
            pygame.draw.rect(screen, darker_tan, (0, 15, screen_width, 15))
            pygame.draw.rect(screen, darker_tan, (0, 35, screen_width, 5))
            pygame.draw.rect(screen, darker_tan, (0, 15+60, screen_width, 15))
            pygame.draw.rect(screen, darker_tan, (0, 35+60, screen_width, 5))
            text = extra_large_font.render("THE OBSERVER", True, darker_tan)
            screen.blit(text, (200, 100))
            pygame.draw.rect(screen, darker_tan, (0, 35+200, screen_width, 5))
            pygame.draw.rect(screen, darker_tan, (0, 35+210, screen_width, 5))
            text = medium_font.render("Alton, Illinois; November 7, 1837.", True, darker_tan)
            screen.blit(text, (342, 265))
            pygame.draw.rect(screen, darker_tan, (0, 335, screen_width, 5))
            pygame.draw.rect(screen, darker_tan, (0, 345, screen_width, 15))
            if play_black: text = large_font.render("PLAY", True, black)
            else: text = large_font.render("PLAY", True, darker_tan)
            screen.blit(text, (130, 365))
            if history_black: text = large_font.render("HISTORY", True, black)
            else: text = large_font.render("HISTORY", True, darker_tan)
            screen.blit(text, (500, 365))
            if credits_black: text = large_font.render("CREDITS", True, black)
            else: text = large_font.render("CREDITS", True, darker_tan)
            screen.blit(text, (920, 365))
            screen.blit(title_text, (0, 432))

        if screen_num == 2:
            pygame.draw.rect(screen, tan, (0, 0, screen_width, screen_height))
            screen.blit(history_text, (0, 10))
            pygame.draw.rect(screen, darker_tan, (0, 15, screen_width, 15))
            pygame.draw.rect(screen, darker_tan, (0, 35, screen_width, 5))
            text = large_font.render("A short history of Elijah Parish Lovejoy", True, darker_tan)
            screen.blit(text, (150, 50))
            pygame.draw.rect(screen, darker_tan, (0, 135, screen_width, 5))
            pygame.draw.rect(screen, darker_tan, (0, 145, screen_width, 15))

        if screen_num == 3:
            screen.blit(credit_text, (0, 0))

        if screen_num == 4:
            screen.blit(win_text, (0, 0))

        if screen_num == 5:
            screen.blit(lose_text, (0, 0))

        # Update display
        pygame.display.flip()
        clock.tick(18)
        await asyncio.sleep(0)

asyncio.run(main())
