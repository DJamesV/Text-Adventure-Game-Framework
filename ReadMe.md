# Test Adventure Game Framework - Most Noticeably used in Almost-Gone


### How the System works
Story-play is node-based and works by exploring places (or scenes, which are simple places desgined for single use and only as a vessel for story). When you explore, you enter a **list**. That list is the story to play. The list contains object(s) which are of different classes.
The classes used are:
* **Display** - used for displaying text. Fun features, such as indents, smart new lines, color, and speaker-based color built in! (To utilize indents and smart new lines, define any needed paramaters and then use :t: for tab and :n: for new line, with your indent paramater automatically applied).
* **Conditional** - used for conditional aspeccts of the story. Depends on conditions to play certain lists. Still a work in progress as of yet.
* **Choice** - used when a choice is required. The choice is printed based on input, with custom display messages allowed for each item. All input is sanity checked against the allowed range. Will be integrated with SubPlaces more fully
* **Flag** - used for in-dictionary switching. When a string is returned by a **Switch**, it searches for a **Flag** with that string as the name.
* **Switch** - used for switching to other **Subplaces**, **Places**, **Routes**, **Flags**, and **more**. SubPlaces are currently still under development.
* **Lull** - used for slowing down the story experience
* **List** - used for multi-level listing (it returns a list to play through, makes things a little more readable)

### Note
Please note some of the file structure is a little bit cluttered. This project is quickly going from garden to architecture, so will change, but may or may not be delayed as I anticipate I will both rewrite the system in Rust (I plan on keeping the Python version) and change the story input method based on the input of Rotri Salvatore (@DreadbotReporter7) who is currently writing a text adventure game using this framework.
