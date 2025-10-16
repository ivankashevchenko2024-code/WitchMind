import pygame
from pygame import mixer
pygame.mixer.init()

music_enabled = True
effects_enabled = True
sounds_enabled = True

music_bg = "bgandsound/bgsound.mp3"
volume_music = 1

happy_animation = "yes.png"
angry_animation = "no.png"
maybe_animation = "maybe.png"

yes_sound = "bgandsound/happywitch.mp3"
no_sound = "bgandsound/angrywitch.mp3"
maybe_sound = "bgandsound/unsurewitch.mp3"

def toggle_music():
    global music_enabled
    music_enabled = not music_enabled
    if music_enabled:
        play_music()
    else:
        mixer.music.stop()

def toggle_effects():
    global effects_enabled
    effects_enabled = not effects_enabled

def toggle_sounds():
    global sounds_enabled
    sounds_enabled = not sounds_enabled

def play_music():
    try:
        mixer.music.load(music_bg)
        mixer.music.set_volume(volume_music)
        mixer.music.play(-1)
    except Exception as e:
        print("Не вдалося відтворити музику:", e)

def play_yes_sound():
    if sounds_enabled:
        sound = mixer.Sound(yes_sound)
        sound.play()

def play_no_sound():
    if sounds_enabled:
        sound = mixer.Sound(no_sound)
        sound.play()

def play_maybe_sound():
    if sounds_enabled:
        sound = mixer.Sound(maybe_sound)
        sound.play()

if music_enabled:
    play_music()