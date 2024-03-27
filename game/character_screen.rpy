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

# Purple default background
image menu_background = Movie(play="assets/backgrounds/menu-background.webm", loop=True)

screen character_screen(character):
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
        $ character_info = char_and_ach["characters_and_achievements"][characters.index(character)]
        
        # Character description
        text character_info['description'] style "character_desc_style"

        # Relationship with character section (heart section)
        text "YOUR RELATIONSHIP WITH [character!u]" style "relationship_label_style"
        # There's already one variable for each character's points, so we can use it to display the hearts
        # Ex: points_character1, points_character2, points_character3, etc.
        $ exec("hearts = '♥' * points_%s" % character)
        # Max points is 10, but max hearts are 5, so we need to divide by 2
        if len(hearts) < character_info["max_points"]//2:
            $ hearts = hearts + ("♡"* (character_info["max_points"]//2 - len(hearts)))
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
        hbox style "character_gallery_style":
            for char in characters:
                if char != character:
                    # define a variable with an action if the player has unlocked the character
                    $ action_enable = ShowMenu("character_screen", char) if (current_episode >= get_episode(char) and current_scene >= get_scene(char)) else None
                    button action action_enable style "character_detail_character_gallery":
                        if action_enable:
                            # Add a background to the character button
                            add Frame(Solid("#54106b7c"))
                            # If the player has unlocked the character, we display the character image
                            add Frame("assets/characters/%s.png" % char)
                            $ exec("hearts = '♥' * points_%s" % char)
                            if len(hearts) < character_info["max_points"]//2:
                                $ hearts = hearts + ("♡"* (character_info["max_points"]//2 - len(hearts)))
                            text hearts style "hearts_style"
                            text "[char!u]" style "char_button_text"
                        else:
                            add Frame(im.MatrixColor("assets/characters/%s.png"% char , im.matrix.brightness(-0.3)))
                            add Image("/assets/lock.png", style="locked_char_icon")
                            $ text_label = "???"
                            text text_label style "locked_char_button_text"


style back_button:
    xpos 190
    ypos 15
    size 30
    bold True
    color "#a7a4a4"
    hover_color "#ffffff"
    font "assets/fonts/Source Sans Pro.ttf"

style character_image_style:
    xpos 1100
    ypos 20

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
    spacing 2
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


