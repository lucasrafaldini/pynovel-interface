init python:
    import re

    # receive a folder and return a list of paths to the files in that folder
    def file_list(dir=""):
        list = renpy.list_files()
        rv = []
        for f in list:
            if re.match(dir, f):
                rv.append(f[(len(dir)):])
        return rv

    def calculate_hearts(char_points, max_points):
        max_hearts = max_points // 2
        hearts = '♥' * char_points if char_points <= max_hearts else '♥' * max_hearts
        if len(hearts) < max_hearts:
            hearts = hearts + ("♡" * (max_hearts - len(hearts)))
        return hearts
    
    def check_character_unlocked(current_episode, current_scene, character):
        return current_episode > get_episode(character) or (current_episode == get_episode(character) and current_scene >= get_scene(character))
    
    def move_left(char_list):
        return char_list[-1:] + char_list[:-1]

    def move_right(char_list):
        return char_list[1:] + char_list[:1]

# Purple default background
image menu_background = Movie(play="assets/backgrounds/menu-background.webm", loop=True)

screen character_screen(character, char_list):
    add "menu_background"
    # Back button
    textbutton "←" style "back_button" action Hide("character_screen")
    # Character image
    image Image("assets/characters/%s.png" % character, style="character_image_style")
    vbox:
        # Character section

        # Character name
        text character style "character_name_style"
        
        # Saving this info in a variable to use it later and simplify future indexing
        $ character_info = char_and_ach["characters_and_achievements"][char_list.index(character)]

        # Character description
        text character_info['description'] style "character_desc_style"

        # Relationship with character section (heart section)
        text "YOUR RELATIONSHIP WITH [character!u]" style "relationship_label_style"
        $ hearts = calculate_hearts(eval("points_%s" % character), character_info["max_points"])
        text hearts style "hearts_style_character_desc"
        
        # Scenes gallery section
        text "[character!u]'S SCENES" style "scenes_gallery_title_style"
        hbox style "scenes_gallery_style":
            # There's a key in the variable (dict) 'achievements' for each possible achievement
            # in character_info["achievements"]

            # The value for those keys are boolean, so we can use them to check if the player
            # has unlocked that achievement

            # If the player has unlocked the achievement, we display the image related to it into 'character_info["achievements"]'
            # If not, we display a locked image
            for achievement in character_info["achievements"].keys():
                button style "scenes_button":
                    if not achievements[achievement]:
                        # We can use the 'im' object to apply a filter to the image
                        add Frame(im.Scale(im.MatrixColor(Image("assets/images/%s.webp" % character_info['achievements'][achievement]),  im.matrix.brightness(-0.2)), 178, 94))
                        # and add a lock image
                        add Image("/assets/lock.png", style="locked_scene_icon") 
                    else:
                        # I added this frame just to make the image as same size
                        # as the unlocked ones
                        add Frame(im.Scale(Image("assets/images/%s.webp" % character_info['achievements'][achievement]), 178, 94))

        # Characters gallery
        text "MORE CHARACTERS"   style "character_gallery_title_style"
        hbox style "arrow_box":
            textbutton "←" action ShowMenu("character_screen", character, move_left(char_list))   style "left_arrow"
            textbutton "→" action ShowMenu("character_screen", character, move_right(char_list))   style "right_arrow"
        hbox style "character_gallery_style":
            $ cleaned_char_list = [char for char in char_list if char != character]
            for i, char in enumerate(cleaned_char_list[:-4]): 
                $ character_info = char_and_ach["characters_and_achievements"][i]
                # define a variable with an action if the player has unlocked the character
                $ action_enable = ShowMenu("character_screen", char, characters) if check_character_unlocked(current_episode, current_scene, char) else None
                button action action_enable style "character_detail_character_gallery":
                    if action_enable:
                        # Add a background to the character button
                        add Frame(Solid("#54106b7c"))
                        # If the player has unlocked the character, we display the character image
                        add Frame("assets/characters/%s.png" % char)
                        $ hearts = calculate_hearts(eval("points_%s" % char), character_info["max_points"])
                        text hearts style "hearts_style"
                        text "[char!u]" style "char_button_text"
                    else:
                        add Frame(im.MatrixColor("assets/characters/%s.png"% char , im.matrix.brightness(-0.3)))
                        add Image("/assets/lock.png", style="locked_char_icon")
                        $ text_label = "???"
                        text text_label style "locked_char_button_text"

style arrow_box:
    xpos 1280
    ypos 260
    spacing 20

style left_arrow:
    size 20
    selected_color "#a7a4a4"
    hover_color "#ffffff"
    font "assets/fonts/Source Sans Pro.ttf"

style right_arrow:
    size 20
    idle_color "#a7a4a4"
    hover_color "#ffffff"
    font "assets/fonts/Source Sans Pro.ttf"

style back_button:
    xpos 190
    ypos 15
    size 30
    bold True
    color "#a7a4a4"
    hover_color "#ffffff"
    font "assets/fonts/Source Sans Pro.ttf"

style character_image_style:
    size (400, 400)
    xpos 1100
    # ypos 20

style scenes_button:
    xsize 178
    ysize 94
    idle_background Solid("#54106b7c")
    hover_background Solid("#ffffffff", alpha=0.1)

style character_name_style:
    font "assets/fonts/Hoollidday.ttf"
    xpos 200
    ypos 40
    size 108
    outlines [(8, "#6419a5", 0, 0)]
    color "#ffffff"

style character_desc_style:
    font "assets/fonts/Source Sans Pro.ttf"
    xpos 200
    ypos 50
    xsize 623
    ysize 108
    size 18
    line_spacing 2.0
    color "#ffffff"
    

style relationship_label_style:
    xpos 200
    ypos 130
    bold True
    size 18

style hearts_style_character_desc:
    bold True
    xpos 200
    ypos 140
    size 32
    color "#ffffff"

style scenes_gallery_title_style:
    font "assets/fonts/Source Sans Pro.ttf"
    bold True
    xpos 200
    ypos 200
    size 18
    color "#ffffff"

style scenes_gallery_style:
    xpos 200
    ypos 230
    spacing 20

style character_gallery_title_style:
    font "assets/fonts/Source Sans Pro.ttf"
    bold True
    xpos 200
    ypos 260
    size 12
    color "#ffffff"

style character_gallery_style:
    xpos 180
    ypos 290
    spacing 45
    background Solid("#54106b7c")

style character_detail_character_gallery:
    xsize 190 
    ysize 281
    idle_background Solid("#54106b7c")
    hover_background Solid("#ffffffff", alpha=0.1)
    outlines [(8, "#fbfbfb", 0, 0)]
    
style locked_scene_icon:
    size 3
    xalign .5
    yalign .5


