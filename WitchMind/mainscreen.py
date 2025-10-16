import pygame
from pygame import *
import random
import soundandanimation
from studentsinfo import students

pygame.init()
window = display.set_mode((520,670))
display.set_caption("WitchMind")

startbg_img = transform.scale(image.load("images/startbg.png").convert(), (520, 670))
entirebtn_img = transform.scale(image.load("images/entirebtn.png").convert_alpha(), (380, 380))
entire_mask = pygame.mask.from_surface(entirebtn_img)
entire_btn = entirebtn_img.get_rect(topleft=(70, 440))

settings_img = transform.scale(image.load("images/settings.png").convert_alpha(), (75, 75))
settings_mask = pygame.mask.from_surface(settings_img)
settings_btn = settings_img.get_rect(topleft=(2, 3))

settings_bg = transform.scale(image.load("images/settingsbg.png").convert(), (520, 670))

setback_img = transform.scale(image.load("images/settingsback.png").convert_alpha(), (75, 105))
setback_mask = pygame.mask.from_surface(setback_img)
setback_btn_settings = setback_img.get_rect(topleft=(0, 0))
setback_btn_game = setback_img.get_rect(bottomleft=(0, 670))

music_img = transform.scale(image.load("images/music.png").convert_alpha(), (230, 200))
effects_img = transform.scale(image.load("images/effects.png").convert_alpha(), (230, 200))
sounds_img = transform.scale(image.load("images/sounds.png").convert_alpha(), (230, 200))

toggle_off = transform.scale(image.load("images/off.png").convert_alpha(), (160, 150))
toggle_on = transform.scale(image.load("images/on.png").convert_alpha(), (160, 150))
toggleoff_mask = pygame.mask.from_surface(toggle_off)
toggleon_mask = pygame.mask.from_surface(toggle_on)
music_toggle_rect = toggle_off.get_rect(topleft=(320, 130))
effects_toggle_rect = toggle_off.get_rect(topleft=(320, 230))
sounds_toggle_rect = toggle_off.get_rect(topleft=(320, 330))

justwitch_img = transform.scale(image.load("images/justwitch.png").convert_alpha(), (330,380))
happy_animation = transform.scale(image.load("images/yes.png").convert_alpha(), (330,430))
angry_animation = transform.scale(image.load("images/no.png").convert_alpha(), (330,430))
maybe_animation = transform.scale(image.load("images/maybe.png").convert_alpha(), (330,430))
witch_rect = justwitch_img.get_rect(center=(260, 530))

tak_img = transform.scale(image.load("images/так.png").convert_alpha(), (250, 170))
ni_img = transform.scale(image.load("images/ні.png").convert_alpha(), (250, 170))
mozlivo_img = transform.scale(image.load("images/можливо.png").convert_alpha(), (250, 170))
tak_mask = pygame.mask.from_surface(tak_img)
ni_mask = pygame.mask.from_surface(ni_img)
mozlivo_mask = pygame.mask.from_surface(mozlivo_img)
tak_rect = tak_img.get_rect(center=(260, 120))
ni_rect = ni_img.get_rect(center=(260, 220))
mozlivo_rect = mozlivo_img.get_rect(center=(260, 320))

fail_ops = transform.scale(image.load("images/fail.png").convert_alpha(), (500,300))
victory_yes = transform.scale(image.load("images/victory.png").convert_alpha(), (500,300))

font_path = "fonts/Amatic_SC/AmaticSC-Bold.ttf"
font = pygame.font.Font(font_path, 28)

game_state = "menu"
running = True
current_candidates = list(students.keys())
question_counter = 0
current_question = ""
guess_name = ""
witch_img = justwitch_img
animating = False
anim_start_time = 0
confirm_exit = False
exit_wait_start = 0
waiting_time = 0

soundandanimation.music_enabled = True
soundandanimation.play_music()

def fade_in(surface, color=(0, 0, 0), duration=270):
    fade = pygame.Surface(surface.get_size())
    fade.fill(color)
    clock = pygame.time.Clock()
    for alpha in range(0, 255, int(255 / (duration / 6))):
        fade.set_alpha(alpha)
        surface.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(60)

def fade_out(surface, color=(0, 0, 0), duration=270):
    fade = pygame.Surface(surface.get_size())
    fade.fill(color)
    clock = pygame.time.Clock()
    for alpha in range(255, -1, -int(255 / (duration / 6))):
        fade.set_alpha(alpha)
        surface.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(60)

def get_random_question():
    if not current_candidates:
        return None
    student = random.choice(current_candidates)
    fact, value = random.choice(list(students[student].items()))
    templates = {
        "age": f"Чи твоєму персонажу {value} років?",
        "hair": f"Чи у твого персонажа {value} колір волосся?",
        "eyes": f"Чи у твого персонажа {value} колір очей?",
        "work": f"Чи твій персонаж {value}?",
        "town": f"Чи твій персонаж живе у місті {value}?",
        "hobby": f"Чи у твого персонажа хобі — {value}?",
        "economy": f"Чи твій персонаж любить {value} гроші?",
        "charachter": f"Чи твій персонаж — {value}?",
        "taste": f"Чи твій персонаж любить {value}?",
        "film": f"Чи улюблений фільм твого персонажа — {value}?",
        "phrase": f"Чи твій персонаж часто каже «{value}»?",
    }
    return fact, value, templates.get(fact, f"Чи у твого персонажа {fact} — {value}?")

def apply_answer(fact, value, answer):
    global current_candidates
    if answer == "yes":
        current_candidates = [s for s in current_candidates if students[s][fact] == value]
    elif answer == "no":
        current_candidates = [s for s in current_candidates if students[s][fact] != value]

def draw_text(text, y, center=False):
    color = ("#EFBF04")
    shadow_color = ("#856A00")
    surf_shadow = font.render(text, True, shadow_color)
    surf = font.render(text, True, color)
    if center:
        rect = surf.get_rect(center=(window.get_width() // 2, y))
        rect_shadow = surf_shadow.get_rect(center=(window.get_width() // 2 + 2, y + 2))
    else:
        rect = surf.get_rect(topleft=(20, y))
        rect_shadow = surf_shadow.get_rect(topleft=(22, y + 2))
    window.blit(surf_shadow, rect_shadow)
    window.blit(surf, rect)

def set_witch_animation(answer):
    global witch_img, animating, anim_start_time
    if soundandanimation.sounds_enabled:
        if answer == "yes": soundandanimation.play_yes_sound()
        elif answer == "no": soundandanimation.play_no_sound()
        else: soundandanimation.play_maybe_sound()
    if soundandanimation.effects_enabled:
        animating = True
        anim_start_time = pygame.time.get_ticks()
        witch_img = {"yes": happy_animation, "no": angry_animation, "maybe": maybe_animation}.get(answer, justwitch_img)
    else:
        witch_img = justwitch_img

def draw_button_hover(surface, img, rect, mask, enlarge_by=5):
    mouse_pos = pygame.mouse.get_pos()
    offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
    if 0 <= offset[0] < mask.get_size()[0] and 0 <= offset[1] < mask.get_size()[1] and mask.get_at(offset):
        enlarged = pygame.transform.scale(img, (rect.width + enlarge_by, rect.height + enlarge_by))
        surface.blit(enlarged, (rect.x - enlarge_by // 2, rect.y - enlarge_by // 2))
    else:
        surface.blit(img, rect.topleft)

def is_mask_clicked(mouse_pos, rect, mask):
    offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
    if 0 <= offset[0] < mask.get_size()[0] and 0 <= offset[1] < mask.get_size()[1]:
        return mask.get_at(offset)
    return False

while running:
    mouse_pos = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if game_state == "menu":
                if is_mask_clicked(mouse_pos, entire_btn, entire_mask):
                    fade_in(window)
                    current_candidates = list(students.keys())
                    question_counter = 0
                    current_question = get_random_question()
                    witch_img = justwitch_img
                    game_state = "question"

                elif is_mask_clicked(mouse_pos, settings_btn, settings_mask):
                    fade_in(window)
                    game_state = "settings"

            elif game_state == "settings":
                if is_mask_clicked(mouse_pos, setback_btn_settings, setback_mask):
                    fade_in(window)
                    game_state = "menu"
                elif is_mask_clicked(mouse_pos, music_toggle_rect, toggleon_mask if soundandanimation.music_enabled else toggleoff_mask):
                    soundandanimation.toggle_music()
                elif is_mask_clicked(mouse_pos, effects_toggle_rect, toggleon_mask if soundandanimation.effects_enabled else toggleoff_mask):
                    soundandanimation.toggle_effects()
                elif is_mask_clicked(mouse_pos, sounds_toggle_rect, toggleon_mask if soundandanimation.sounds_enabled else toggleoff_mask):
                    soundandanimation.toggle_sounds()

            elif game_state == "question" and not animating:
                if confirm_exit:
                    if is_mask_clicked(mouse_pos, tak_rect, tak_mask):
                        fade_in(window)
                        confirm_exit = False
                        game_state = "menu"
                    elif is_mask_clicked(mouse_pos, ni_rect, ni_mask):
                        exit_wait_start = pygame.time.get_ticks()
                        confirm_exit = "wait_no"
                else:
                    if is_mask_clicked(mouse_pos, setback_btn_game, setback_mask):
                        confirm_exit = True
                    elif current_question:
                        fact, value, question_text = current_question
                        if is_mask_clicked(mouse_pos, tak_rect, tak_mask):
                            apply_answer(fact, value, "yes")
                            set_witch_animation("yes")
                            current_question = None
                            question_counter += 1
                            if not soundandanimation.effects_enabled:
                                if question_counter >= 10 or len(current_candidates) <= 2:
                                    guess_name = random.choice(current_candidates) if current_candidates else "Ніхто"
                                    game_state = "guess"
                                else:
                                    current_question = get_random_question()

                        elif is_mask_clicked(mouse_pos, ni_rect, ni_mask):
                            apply_answer(fact, value, "no")
                            set_witch_animation("no")
                            current_question = None
                            question_counter += 1
                            if not soundandanimation.effects_enabled:
                                if question_counter >= 10 or len(current_candidates) <= 2:
                                    guess_name = random.choice(current_candidates) if current_candidates else "Ніхто"
                                    game_state = "guess"
                                else:
                                    current_question = get_random_question()

                        elif is_mask_clicked(mouse_pos, mozlivo_rect, mozlivo_mask):
                            apply_answer(fact, value, "maybe")
                            set_witch_animation("maybe")
                            current_question = None
                            question_counter += 1
                            if not soundandanimation.effects_enabled:
                                if question_counter >= 10 or len(current_candidates) <= 2:
                                    guess_name = random.choice(current_candidates) if current_candidates else "Ніхто"
                                    game_state = "guess"
                                else:
                                    current_question = get_random_question()

            elif game_state == "guess" and not animating:
                if is_mask_clicked(mouse_pos, tak_rect, tak_mask):
                    set_witch_animation("yes")
                    game_state = "win"
                    waiting_time = pygame.time.get_ticks()
                elif is_mask_clicked(mouse_pos, ni_rect, ni_mask):
                    set_witch_animation("no")
                    game_state = "fail"
                    waiting_time = pygame.time.get_ticks()

    if animating and pygame.time.get_ticks() - anim_start_time > 3000:
        animating = False
        witch_img = justwitch_img
        fade_in(window)
        if game_state == "question" and not confirm_exit:
            if question_counter >= 10 or len(current_candidates) <= 2:
                guess_name = random.choice(current_candidates) if current_candidates else "Ніхто"
                game_state = "guess"
            else:
                current_question = get_random_question()

    if confirm_exit == "wait_no" and pygame.time.get_ticks() - exit_wait_start > 1000:
        confirm_exit = False
        witch_img = justwitch_img
        animating = False

    if game_state == "menu":
        window.blit(startbg_img, (0, 0))
        draw_button_hover(window, entirebtn_img, entire_btn, entire_mask)
        draw_button_hover(window, settings_img, settings_btn, settings_mask)

    elif game_state == "settings":
        window.blit(settings_bg, (0, 0))
        window.blit(music_img, (20, 100))
        window.blit(effects_img, (20, 200))
        window.blit(sounds_img, (20, 300))
        for rect, state in [(music_toggle_rect, soundandanimation.music_enabled),
                            (effects_toggle_rect, soundandanimation.effects_enabled),
                            (sounds_toggle_rect, soundandanimation.sounds_enabled)]:
            mask = toggleon_mask if state else toggleoff_mask
            draw_button_hover(window, toggle_on if state else toggle_off, rect, mask)
        draw_button_hover(window, setback_img, setback_btn_settings, setback_mask)

    elif game_state == "question":
        window.blit(settings_bg, (0, 0))
        window.blit(witch_img, witch_rect.topleft)
        draw_button_hover(window, setback_img, setback_btn_game, setback_mask)
        if confirm_exit:
            draw_text("Точно повернутися в меню?", 50, center=True)
            draw_button_hover(window, tak_img, tak_rect, tak_mask)
            draw_button_hover(window, ni_img, ni_rect, ni_mask)
        elif current_question:
            fact, value, question_text = current_question
            draw_text(question_text, 30, center=True)
            draw_button_hover(window, tak_img, tak_rect, tak_mask)
            draw_button_hover(window, ni_img, ni_rect, ni_mask)
            draw_button_hover(window, mozlivo_img, mozlivo_rect, mozlivo_mask)
        else:
            if soundandanimation.effects_enabled:
                draw_text("Зачекай... відьма думає...", 50, center=True)

    elif game_state == "guess":
        window.blit(settings_bg, (0, 0))
        window.blit(witch_img, witch_rect.topleft)
        draw_text(f"Це {guess_name} ?", 50, center=True)
        draw_button_hover(window, tak_img, tak_rect, tak_mask)
        draw_button_hover(window, ni_img, ni_rect, ni_mask)

    elif game_state == "win":
        window.blit(settings_bg, (0, 0))
        window.blit(happy_animation, (100, 340))
        window.blit(victory_yes, (30, 50))
        if pygame.time.get_ticks() - waiting_time > 3000:
            fade_in(window)
            game_state = "menu"

    elif game_state == "fail":
        window.blit(settings_bg, (0, 0))
        window.blit(angry_animation, (100, 340))
        window.blit(fail_ops, (30, 50))
        if pygame.time.get_ticks() - waiting_time > 3000:
            fade_in(window)
            game_state = "question"
            current_candidates = list(students.keys())
            question_counter = 0
            current_question = get_random_question()
            witch_img = justwitch_img

    pygame.display.update()


