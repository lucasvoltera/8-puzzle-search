import cx_Freeze

executables = [cx_Freeze.Executable ( "main.py" )] 

cx_Freeze.setup ( 
   name = "8-puzzle" , 
   options = { "build_exe" : { "packages" : [ "pygame", "pygame_gui" ],
                              "include_files" : [ "utils\FiraCode-Retina.ttf", "utils\FiraCode-Retina.ttf", "theme.json", "utils\matriz.py", "utils\puzzle.py", "utils\constantes.py"]}}, 
   executables = executables
)