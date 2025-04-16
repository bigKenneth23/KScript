KScript:

    KScript is a lightweight mathmatical scripting language!

    Requirements:

        With the correct files installed, the interpreter can be used quickly and efficiently, following suit 
        of languages like python in which no set-up is required for the program itself. The only requirements
        for KScript to function are as follows:

        Python interpreter:
            A python interpreter must be installed on your device in order for the KScript interpreter to run.
            This WILL change when KScript is at a more stable version and the interpreter is ready to be compiled
            into it's own standalone program.

        File structure:
            Inside of your chosen folder, you must have 4 files grouped together, 3 of which are irreplaceable.

            The structure MUST match the following:

                KScript (Main folder)

                    FileReader.py -> This file contains the Reader class which is responsible for reading the 
                    written KScript code and converts it into lines before handing it to the interpreter.

                    Interpreter.py -> This file contains the interpreter processor, the variable array and the
                    custom function array classes necessary for parsing and executing the passed lines.

                    main.py -> This is the main file that groups the interpreter and the reader together, this 
                    is the file that will be executed in order to interpret the KScript code.

                    console.txt -> This is the file that will contain the written code, if this file is not present
                    or is deleted, a new one CAN be created in its place. The name "console.txt" only has relevance
                    in the "Reader" class, this can be changed simply by finding the path passed in to the reader 
                    object and altering it to your new KScript file path (relative to the main file).

                    **NOTE**: The console path is found within "main.py".
                    