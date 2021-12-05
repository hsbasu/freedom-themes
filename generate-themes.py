#!/usr/bin/python3
import os

from constants import Y_HEX_ACCENT1, Y_HEX_ACCENT2, Y_HEX_ACCENT3, Y_HEX_ACCENT4
from constants import y_hex_colors1, y_hex_colors2, y_hex_colors3, y_hex_colors4

def change_value (key, value, file):
    if value is not None:
        command = "sed -i '/%(key)s=/c\%(key)s=%(value)s' %(file)s" % {'key':key, 'value':value, 'file':file}
    else:
        command = "sed -i '/%(key)s=/d' %(file)s" % {'key':key, 'file':file}
    os.system(command)

def y_colorize_directory (path, variation):
    for accent in Y_HEX_ACCENT1:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, y_hex_colors1[variation]))
    for accent in Y_HEX_ACCENT2:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, y_hex_colors2[variation]))
    for accent in Y_HEX_ACCENT3:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, y_hex_colors3[variation]))
    for accent in Y_HEX_ACCENT4:
        os.system("find %s -name '*.*' -type f -exec sed -i 's/%s/%s/gI' {}  \\;" % (path, accent, y_hex_colors4[variation]))

if os.path.exists("usr"):
    os.system("rm -rf usr/")

os.system("mkdir -p usr/share/themes")

curdir = os.getcwd()

# Build Mint-Y Base themes (light, dark, darker)
os.chdir("src/Mint-Y")
os.system("./build-themes.py")

os.chdir(curdir)

# Mint-Y color variations
for color in y_hex_colors1.keys():
    for variant in ["", "-Dark", "-Darker"]:
        original_name = "Mint-Y%s" % variant
        path = os.path.join("src/Mint-Y/variations/%s" % color)
        if os.path.isdir(path):
            print("Derivating %s-%s" % (original_name, color))
            
            # Copy theme
            theme = "usr/share/themes/%s-%s" % (original_name, color)
            theme_index = os.path.join(theme, "index.theme")
            os.system("cp -R usr/share/themes/%s %s" % (original_name, theme))
            
            # Theme name
            for key in ["Name", "GtkTheme"]:
                change_value(key, "%s-%s" % (original_name, color), theme_index)
            
            for key in ["MetacityTheme"]:
                metacity_variant = original_name.replace("Darker", "Dark")
                change_value(key, "%s-%s" % (metacity_variant, color), theme_index)
            
            for key in ["IconTheme"]:
                change_value(key, "%s-%s" % (original_name, color), theme_index)
            
            for key in ["CursorTheme"]:
                change_value(key, "FreedomOS-%s" % color, theme_index)
            
            # Regenerate GTK3 sass
            os.system("cp -R src/Mint-Y/gtk-3.0/sass %s/gtk-3.0/" % theme)
            y_colorize_directory("%s/gtk-3.0/sass" % theme, color)
            os.chdir("%s/gtk-3.0" % theme)
            # os.system("sed -i 's/no-tint/tint/gI' ./sass/gtk.scss")
            # os.system("sed -i 's/no-tint/tint/gI' ./sass/gtk-dark.scss")
            if (variant == "-Dark"):
                os.system("cp sass/gtk-dark.scss sass/gtk.scss")
            elif (variant == "-Darker"):
                os.system("cp sass/gtk-darker.scss sass/gtk.scss")
            else:
                os.system("rm sass/gtk-dark.scss sass/gtk-darker.scss")
            
            os.system("sassc ./sass/gtk.scss gtk.css")
            os.system("rm -rf sass .sass-cache")
            os.chdir(curdir)
            
            # Regenerate Cinnamon sass
            if (variant != "-Darker"):
                # Darker variants have no cinnamon style
                os.system("cp -R src/Mint-Y/cinnamon/sass %s/cinnamon/" % theme)
                os.system("cp -R %s/cinnamon/sass %s/cinnamon/" % (path, theme))
                y_colorize_directory("%s/cinnamon/sass" % theme, color)
                os.chdir("%s/cinnamon" % theme)
                if (variant == "-Dark"):
                    os.system("cp sass/cinnamon-dark.scss sass/cinnamon.scss")
                os.system("sassc ./sass/cinnamon.scss cinnamon.css")
                os.system("rm -rf sass .sass-cache")
            os.chdir(curdir)
            
            # Accent color
            files = []
            files.append(os.path.join(theme, "gtk-2.0", "gtkrc"))
            files.append(os.path.join(theme, "gtk-2.0", "main.rc"))
            files.append(os.path.join(theme, "gtk-2.0", "panel.rc"))
            files.append(os.path.join(theme, "gtk-2.0", "apps.rc"))
            files.append(os.path.join(theme, "gtk-2.0", "menubar-toolbar.rc"))
            for file in files:
                if os.path.exists(file):
                    for accent in Y_HEX_ACCENT1:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': y_hex_colors1[color], 'file': file})
                    for accent in Y_HEX_ACCENT2:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': y_hex_colors2[color], 'file': file})
                    for accent in Y_HEX_ACCENT3:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': y_hex_colors3[color], 'file': file})
                    for accent in Y_HEX_ACCENT4:
                        os.system("sed -i s'/%(accent)s/%(color_accent)s/gI' %(file)s" % {'accent': accent, 'color_accent': y_hex_colors4[color], 'file': file})
            
            # # Remove metacity-theme-3.xml (it doesn't need to be derived since it's using GTK colors, and Cinnamon doesn't want to list it)
            # os.system("rm -f %s" % os.path.join(theme, "metacity-1", "metacity-theme-3.xml"))
            
            directories = []
            directories.append(os.path.join(theme, "cinnamon/common-assets"))
            directories.append(os.path.join(theme, "cinnamon/light-assets"))
            directories.append(os.path.join(theme, "cinnamon/dark-assets"))
            for directory in directories:
                if os.path.exists(directory):
                    y_colorize_directory(directory, color)
            
            # Assets
            os.system("rm -rf %s/gtk-3.0/assets" % theme)
            os.system("rm -rf %s/gtk-2.0/assets" % theme)
            if variant == "-Dark":
                os.system("cp -R %s/gtk-2.0/assets-dark %s/gtk-2.0/assets" % (path, theme))
                os.system("cp -R %s/xfwm4-dark/*.png %s/xfwm4/" % (path, theme))
            else:
                os.system("cp -R %s/gtk-2.0/assets %s/gtk-2.0/assets" % (path, theme))
                os.system("cp -R %s/xfwm4/*.png %s/xfwm4/" % (path, theme))
            os.system("cp -R %s/gtk-3.0/assets %s/gtk-3.0/assets" % (path, theme))
            
            os.system("cp -R files/%s ./usr/share/themes" % theme)

