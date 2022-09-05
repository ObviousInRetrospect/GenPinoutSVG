# GenPinoutSVG

This repository is a fork of https://github.com/stevenj/GenPinoutSVG and Steven Johnson wrote the vast majority of the code in it. ObviousInRetrospect added some minor features that he uses to generate the diagrams for DxCore and megaTinyCore.

This repository contains a program to produce pinout SVG files from a CSV file
source file of pin definitions and other graphical/format commands.

# Changes in this fork
* support for | within a field to split the contents into multiple boxes of the same style.
* CHIP45 command which is identical to box except the result is rotated 45 degrees. This is under development and likley to change in the future. The purpose of this command is to draw a square chip with pins on 4 sides at an angle. That allows all the text to be horizontal
* Automatic sizing of pin boxes (pip install pycairo for it to be accurate). Enabled by setting the width of a box to 0.
* plumbed a W=None default paramater to a few more functions to allow width to be overriden
* pintype of NO_TRIANGLE will suppress the leading triangle for a pin (intended for continuations and legends)
* automatic wrapping of pin lines that go off the page as long as the spacing allows it. warning messages when this happens.
* You can use any of P# (P1...P100), PR#, Pr# for a PINTYPE if you define the box class PNUM. These pin types will render a PNUM containing the relevent number box in place of the circle at the end of a pin. PR# (PR1..PR100) will rotate the box 45 degrees. Pr# will rotate -45.


This program was inspired by [Graphical Datasheets](https://github.com/sparkfun/Graphical_Datasheets)

## How To Use

This is a Python 3 program and has only been tested on V3.6.  It should be
considered the minimum version for bug reports.

1. Create a Python Virtual Environment
2. Install Dependencies with pip
    * docopt
    * svgwrite
    * wand
3. Clone this repository
4. Execute ./GenPinoutSVG.py \<csv file\>

## CSV Input data format

The CSV format is a simple list of drawing commands, at a higher level than raw SVG and targeted to the needs of a graphical pinout datasheet.

The basic format of the CSV file is:

* \n (Carriage Return 0x13) is the Line Ender character
* Fields are separated with , (Comma)
* If you put a comma inside a string, quote it with " (double quote)

Each line of the CSV is a command, with the following general format:

* First Field = Command Name
* Second to Nth Field = Options to the command

There are **TWO** Phases in the drawing process and the commands are divided by phase.  The first phase is the SETUP phase, which defines all the attributes of the page and drawing options, themes.  The Second phase is the DRAW phase and it is triggered by the DRAW command.

DRAW Operations must occur in Draw Phase and Setup operations must occur in Setup phase.

### **SETUP** Phase Commands (Called before the **DRAW** Command)

* **LABEL**, DEFAULT, TYPE, GROUP, \<list of labels for pin attributes\>
  * Defines PIN labels, best as the first command in the file. Aligns with pin data draw commands in draw phase.  Helps create named columns which ease editing in a spreadsheet.
    * DEFAULT - Defines the Default theme
    * TYPE - Pin Type Theme Settings
    * GROUP - Pin Group Theme Settings
    * \<List> - The List of PIN Functions
* **BORDER COLOR**,  default, \<type>, \<group>, \<List of border colors for each label>
  * Defines Theme border color of Pin Type
    * DEFAULT - Default border color, must be specified
    * \<type> - Optional border color for Types
    * \<group> - Optional border color for Pin Groups
    * \<list> - Optional border color for each Pin Label
* **FILL COLOR**, default, \<type>, \<group>, \<List of fill colors for each label>
  * Defines Theme fill color of Pin Type
    * DEFAULT - Default fill color, must be specified
    * \<type> - Optional fill color for Types
    * \<group> - Optional fill color for Pin Groups
    * \<list> - Optional fill color for each Pin Label
* **OPACITY**, default, \<type>, \<group>, \<List of opacities for each label>
  * Theme Opacity Value of Pin Type
    * DEFAULT - Default fill color opacity, must be specified
    * \<type> - Optional fill color opacity for Types
    * \<group> - Optional fill color opacity for Pin Groups
    * \<list> - Optional fill color opacity for each Pin Label
* **FONT** default, \<type>, \<group>, \<List of font names for each label>
  * Theme Font of Pin Type
    * DEFAULT - Default Font, must be specified
    * \<type> - Optional Font for Types
    * \<group> - Optional Font for Pin Groups
    * \<list> - Optional Font for each Pin Label
* **FONT SIZE**, default, \<type>, \<group>, \<List of font sizes for each label>
  * Theme Font Size of Pin Type
    * DEFAULT - Default Font Size, must be specified
    * \<type> - Optional Font Size for Types
    * \<group> - Optional Font Size for Pin Groups
    * \<list> - Optional Font Size for each Pin Label
* **FONT COLOR**, default, \<type>, \<group>, \<List of font colors for each label>
  * Theme Font Color of Pin Type
    * DEFAULT - Default Font Color, must be specified
    * \<type> - Optional Font Color for Types
    * \<group> - Optional Font Color for Pin Groups
    * \<list> - Optional Font Size for each Pin Label
* **FONT SLANT**, default, \<type>, \<group>, \<List of font slants for each label>
  * Theme Font Slant of Pin Type, possible slants are: "normal","italic", "oblique"
    * DEFAULT - Default Font Slant, must be specified
    * \<type> - Optional Font Slant for Types
    * \<group> - Optional Font Slant for Pin Groups
    * \<list> - Optional Font Slant for each Pin Label
* **FONT BOLD**, default, \<type>, \<group>, \<List of font boldness for each label>
  * Theme Font Boldness of Pin Type, possible boldness are: "normal", "bold", "bolder", "lighter", "100", "200", "300", "400", "500", "600", "700", "800", "900"
    * DEFAULT - Default Font Boldness, must be specified
    * \<type> - Optional Font Boldness for Types
    * \<group> - Optional Font Boldness for Pin Groups
    * \<list> - Optional Font Boldness for each Pin Label
* **FONT STRETCH**, default, \<type>, \<group>, \<List of font stretch for each label>
  * Theme Font Stretch of Pin Type, possible stretch are: "normal", "wider", "narrower", "ultra-condensed", "extra-condensed", "condensed", "semi-condensed", "semi-expanded", "expanded", "extra-expanded", "ultra-expanded"
    * DEFAULT - Default Font Stretch, must be specified
    * \<type> - Optional Font Stretch for Types
    * \<group> - Optional Font Stretch for Pin Groups
    * \<list> - Optional Font Stretch for each Pin Label
* **TYPE**, **IO**, Color, Opacity
  * Sets the Color and Opacity IO pin Indicator
    * Color - The Color of the IO Pin Type indicator
    * Opacity - The Opacity of the IO Pin Type indicator
* **TYPE**, **INPUT**, Color, Opacity
  * Sets the Color and Opacity INPUT pin Indicator
    * Color - The Color of the INPUT Pin Type indicator
    * Opacity - The Opacity of the INPUT Pin Type indicator
* **TYPE**, **OUTPUT**, Color, Opacity
  * Sets the Color and Opacity OUTPUT pin Indicator
    * Color - The Color of the OUTPUT Pin Type indicator
    * Opacity - The Opacity of the OUTPUT Pin Type indicator
* **WIRE**, **DIGITAL**, Color, Opacity, Thickness
  * Sets the Color, Opacity and Thickness of Digital Wires
    * Color - The Color of the Digital Wire
    * Opacity - The Opacity of Digital Wire
    * Thickness - The Thickness of a Digital Wire
* **WIRE**, **PWM**, Color, Opacity, Thickness
  * Sets the Color, Opacity and Thickness of PWM Wires
    * Color - The Color of the PWM Wire
    * Opacity - The Opacity of PWM Wire
    * Thickness - The Thickness of a PWM Wire
* **WIRE**, **ANALOG**, Color, Opacity, Thickness
  * Sets the Color, Opacity and Thickness of ANALOG Wires
    * Color - The Color of the ANALOG Wire
    * Opacity - The Opacity of ANALOG Wire
    * Thickness - The Thickness of a ANALOG Wire
* **WIRE**, **HS-ANALOG**, Color, Opacity, Thickness
  * Sets the Color, Opacity and Thickness of High Speed ANALOG Wires
    * Color - The Color of the ANALOG Wire
    * Opacity - The Opacity of ANALOG Wire
    * Thickness - The Thickness of a ANALOG Wire
* **WIRE**, **POWER**, Color, Opacity, Thickness
  * Sets the Color, Opacity and Thickness of POWER Wires
    * Color - The Color of the POWER Wire
    * Opacity - The Opacity of POWER Wire
    * Thickness - The Thickness of a POWER Wire
* **GROUP**, name, Color, Opacity
  * Sets the Name of a Pin group, and the Color and Opacity of the Pin Group Circle.
    * name - The name of the pin group
    * color - The color of the pin group
    * opacity - The opacity of the pin group
* **BOX**, \<Name>, \<Border Color>, \<Border Opacity>, \<Fill Color>, \<Fill Opacity>, \<Linewidth>, \<BoxWidth>, \<BoxHeight>, \<Box Cr X>, \<Box Cr Y>, \<Box Skew>, \<Box Skew Offset>
  * Define a box theme
    * Name - The name of the box theme
    * Border Color - The color of the Border line around the box
    * Border Opacity - Number 0.00-1.00 defines opacity of the border line
    * Fill Color - Fill color of the box
    * Fill Opacity - Opacity of the Fill (0.00-1.00), set to 0 for no fill
    * Line Width - Width of the border line
    * Box Width - Default width of the box
    * Box Height - Default height of the box
    * Box Cr X - Box Corner Radius (X Direction)
    * Box Cr Y - Box Corner Radius (Y Direction)
    * Box Skew - Amount of slant to pu on the box
* **TEXT FONT**, \<Theme Name>, \<Font>, \<Size>, \<Outline Color>, \<Color>, \<slant>, \<bold>, \<stretch>
  * Defines a Font for use by text entries. Text entries can also use a font theme for a labeled pin column
* **PAGE**, "page name"
  * Sets the page size Defaults to A4-L)
    * page name - Name of page, ("A4-P", "A4-L", "A3-P" or "A3-L")
* **DPI**, dpi
  * Sets the dots per inch.
    * dpi - dots per inch on the page (Defaults to 300)
* **DRAW**
  * Starts the Page Draw, Setup commands after this are ignored.  Draw commands before this are ignored.

### **DRAW** Phase Commands (Called before the **DRAW** Command)

* **GOOGLEFONT**, \<link>
  * Embed a link to google web fonts (doesn't work for Inkscape)
* **IMAGE**, name, X, Y, W, H, \<cx>, \<cy>, \<cw>, \<ch>, \<rot>
  * Puts a PNG on the page at the requested location and for the requested size, with an optional crop and rotate.
* **ICON**, name.svg, X,Y,W,H,\<rot>
  * Embeds another SVG inside this one, at the required location and size/rotation. (Used for informational icons)
    * name.svg = svg file name to use
    * X,Y = Top left Origin
    * W/H = Width and Height to display at.
    * rot = Optional angle of rotation to apply
* **ANCHOR**, X, Y
  * Sets Starting point for Pin Attribute display.
    * X - X Coordinate of top left corner of first pin to show
    * Y - Y Coordinate of top left corner of first pin to show
* **PINSET**, Side, Packed, JustifyX, JustifyY, LineStep, PinWidth, GroupWidth, LeaderOffset, Column Gap, LeaderHStep
  * Define a pin list.
    * Side - The side the pins are on.
    * Packed - Pins are listed Packed, or Columnar
    * JustifyX - How text aligns in the X Direction
    * JustifyY - How text aligns vertically
    * LineStep - Step between consecutive lines
    * PinWidth - Width of the pin Indicator
    * GroupWidth - Width of the pin Group Indicator
    * LeaderOffset - Width of Leader Wire
    * Column Gap - Distance between adjacent boxes
    * LeaderHStep - allows the leader to be offset each line for vertical pins.
* **PIN**, \<Wire>, \<TYPE>, \<GROUP>, \<List of Pin attribute  strings>
  * Pin Attributes to print at next pin line.
    * Wire = The Wire Type (POWER/PWM/ANALOG/DIGITAL) Defaults to DIGITAL if not set.
    * TYPE = Pin Type (IO/INPUT/OUTPUT) Defaults to IO if not set.
    * GROUP = Pin Group name. Defaults to un-grouped if not set.
    * List = List of pin functions, in order of defined Labels.
* **PINTEXT**, \<Wire>, \<TYPE>, \<GROUP>, \<theme>, \<label> \<Text>
  * Text to print at next pin line.
    * Wire - The Wire Type (POWER/PWM/ANALOG/DIGITAL) Defaults to DIGITAL if not set.
    * TYPE - Pin Type (IO/INPUT/OUTPUT) Defaults to IO if not set.
    * GROUP - Pin Group. Defaults to un-grouped if not set.
    * Label - First Column Label, prints first column box and this text.  If not present, first column box is not printed at all.
    * theme - Theme to use when printing the text.
    * Text - The message to print
* **BOX**, Theme, X, Y, \<BoxWidth>, \<BoxHeight>, \<X Justify>, \<Y Justify>, \<Text>
  * Draw a box at the required location.
    * Theme - The box theme to draw with.
    * X,Y - The Origin of the box (Top Left corner)
    * Width/Height - Optional, if set override the themes box size
    * X Justify - Optional, define Text justification in box, valid options are "LEFT", "RIGHT", "CENTER", defaults to "CENTER" if not set.
    * Y Justify - Optional, define Text justification in box, valid options are "TOP", "BOTTOM", "CENTER", defaults to "CENTER" if not set.
    * Text - Optional, Text to place inside the box.
* **MESSAGE**, \<X>, \<Y>, \<Line Step>, \<Font>, \<Font Size>, \<X Justify>, \<Y Justify>
  * Text Message Options.  Any missing options use the previously set value, and do not reset.
    * X - Origin of text to print
    * Y - Origin of text to print.
    * Line Step - Distance between lines
    * Font - Font to use
    * Font Size - Optional over-ride of size of font.
    * X Justify - Font alignment in X Direction
    * Y Justify - Font alignment in Y Direction
* **TEXT**, \<edge color>, \<color>, \<Message>, \<NL>
  * Arbitrary Line of Text, using MESSAGE options.
    * edge color - Color of Font Outline
    * color - Color of Font body
    * Message - Text to display
    * NL - If present causes the line to advance to the next line.
* **END MESSAGE**
  * Terminates the previous multi-line message

## License

This code is licensed under GPL-3.  See [GPL-3](gpl-3.0.md) for Details.
