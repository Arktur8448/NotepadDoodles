import random

import arcade

MUSIC_VOLUME = 50
SOUND_VOLUME = 50
CURRENT_MUSIC = None
CURRENT_PLAYER = None
MUSIC_NUMBER_MAX = 3
MUSIC_NUMBER_COUNTER = random.randint(1,MUSIC_NUMBER_MAX)


def set_music_volume(volume):
    global MUSIC_VOLUME
    MUSIC_VOLUME = volume
    if CURRENT_MUSIC is not None:
        CURRENT_MUSIC.set_volume(MUSIC_VOLUME / 100, CURRENT_PLAYER)


def set_sound_volume(volume):
    global SOUND_VOLUME
    SOUND_VOLUME = volume


def get_music_volume():
    global MUSIC_VOLUME
    return MUSIC_VOLUME


def get_sound_volume():
    global SOUND_VOLUME
    return SOUND_VOLUME


def start_playing_music():
    global CURRENT_MUSIC, CURRENT_PLAYER, MUSIC_NUMBER_COUNTER
    music = arcade.Sound(f"sounds/music/music{MUSIC_NUMBER_COUNTER}.mp3")
    CURRENT_PLAYER = music.play(MUSIC_VOLUME / 100)
    CURRENT_MUSIC = music


def update_music_player():
    global CURRENT_MUSIC, CURRENT_PLAYER, MUSIC_NUMBER_COUNTER, MUSIC_NUMBER_MAX
    if CURRENT_MUSIC.get_stream_position(CURRENT_PLAYER) == 0:
        MUSIC_NUMBER_COUNTER += 1
        if MUSIC_NUMBER_COUNTER > MUSIC_NUMBER_MAX:
            MUSIC_NUMBER_COUNTER = 1
        music = arcade.Sound(f"sounds/music/music{MUSIC_NUMBER_COUNTER}.mp3")
        CURRENT_PLAYER = music.play(MUSIC_VOLUME / 100)
        CURRENT_MUSIC = music


def play_random_paper():
    global SOUND_VOLUME
    arcade.Sound(f"sounds/paper/paper{random.randint(1,4)}.mp3").play(SOUND_VOLUME / 100)


def play_random_write():
    global SOUND_VOLUME
    arcade.Sound(f"sounds/write/writing{random.randint(1, 3)}.mp3").play(SOUND_VOLUME / 100)


def play_sound(path):
    global SOUND_VOLUME
    arcade.Sound(path).play(SOUND_VOLUME / 100)