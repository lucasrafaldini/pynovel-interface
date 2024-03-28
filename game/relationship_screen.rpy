init python:
    import json
    import re

    # Hard coded values just to test
    achievements = dict(
    went_games = True,
    ep2_julia_kiss = False,
    ep4_julialunch_kiss_julia = False,
    ep4_livingsituation_julia = True,
    ep5_juliaroof_we_will = False,
    ep7_gettingcaught_kiss_julia = False)

    # Hard coded values just to test
    current_episode = 1
    current_scene = 8

    char_and_ach = json.load(renpy.file("assets/characters_and_achievements.json"))
    characters = [i["model"] for i in char_and_ach["characters_and_achievements"]]

    # Create a variable for each character with the points
    # (points_julia starts with 2 because she is the main character and is used for test)
    for char in characters:
        if char == "julia":
            exec("points_%s = 2" % char)
        else:
            exec("points_%s = 0" % char)

    # Get the episode and scene of the first appearance of the character
    def get_episode(character):
        episode = char_and_ach["characters_and_achievements"][characters.index(character)]["first_appearance"]
        return int(re.match(r"ep(\d+)_(\d+)", episode).group(1))

    def get_scene(character):
        episode = char_and_ach["characters_and_achievements"][characters.index(character)]["first_appearance"]
        return int(re.match(r"ep(\d+)_(\d+)", episode).group(2))



screen relationship_screen():
    add "black"
    add "menu_background"
    textbutton "←" style "back_button" action Hide("relationship_screen")
    text "CHARACTERS" style "character_title_style"
    grid 5 2:
        style "char_grid_style"
        for i, character in enumerate(characters):
            $ character_info = char_and_ach["characters_and_achievements"][i]
            # Check if the character is unlocked
            $ action_enable = ShowMenu("character_screen", character) if check_character_unlocked(current_episode, current_scene, character) else None 
            button action action_enable style "char_button":
                if action_enable:
                    # If the character is unlocked, show the button with the character image
                    add Frame(Solid("#54106b7c"))
                    add Frame("assets/characters/%s.png" % character)
                    $ hearts = calculate_hearts(eval("points_%s" % character), character_info["max_points"])
                    text hearts style "hearts_style"
                    text "[character!u]" style "char_button_text"
                else:
                    # If the character is locked, show a locked button
                    style "locked_char_button"
                    add Frame(im.MatrixColor("assets/characters/%s.png"% character , im.matrix.brightness(-0.3)))
                    add Image("/assets/lock.png", style="locked_char_icon")
                    $ text_label = "???"
                    text text_label style "locked_char_button_text"


style character_title_style:
    xpos 210
    ypos 120
    size 18
    bold True
    color "#ffffff"

style char_grid_style:
    xalign 0.5
    yalign 0.8
    spacing 70

style char_button:
    xsize 249
    ysize 369
    idle_background Solid("#54106b7c")
    hover_background Solid("#ffffffff", alpha=0.1)

style char_button_text:
    align(0.5, 0.95)
    hover_align(0.5, 0.80)
    size 18
    idle_color "#a09e9e"
    hover_color "#ffffff"
    bold True
    font "assets/fonts/Source Sans Pro.ttf"

style hearts_style:
    bold True
    align(0.5, 0.9)
    size 20
    hover_color "#ffffff"
    idle_color "#ffffff00"

    
style locked_char_icon:
    size 60
    xalign .5
    yalign .5

style locked_char_button_text:
    align(0.5, 0.95)
    size 18
    color "#898787"
    font "assets/fonts/Source Sans Pro.ttf"
