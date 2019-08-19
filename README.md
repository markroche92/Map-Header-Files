# Map Header Files
## Background
This repository contains a tool written in Python 3 to assist with projects written in C. Files in the C language are split into two categories: source (.c) and header (.h) files. Any source or header file may include a number of header files via the #include preprocessor directive. 

During the preprocessing step of build,  #include statements are replaced by the content of the file specified within the #include statement. 

A translation unit is a fully preprocessed source file - i.e. all preprocessor operations have been carried out within the source file and all included files. When compiling a project, the number of translation units is equal to the number of source files of the project. 

After preprocessing, the translation units are compiled, and the result is an object file per translation unit. The next step of the software build is the linking step, which combines the object files into a single executable file.

In a large project, there can be hundreds of source and header files. For a number of reasons (e.g. compilation failure, run-time issue or investigating of results from a static code analyser) one may need to understand the network of file inclusion across the project. 

The tool which is stored in this repository helps the user do exactly this. With the help of the [GraphViz](https://pypi.org/project/graphviz/) python library, a visual representation of the network of file inclusion is generated. 

## Using the Tool
### Prerequisites
Python 3.5+ is required to use the GraphViz library. To install, use pip:
```
$ pip install graphviz
```
### Organising Code Files
The tool is currently configured such that:
* all source files are expected within a directory 'source'
* all header files are expected within a directory 'includes'
* 'source' and 'includes' must live in the same directory

When running the tool, the user is expected to provide the relative path to the parent directory

### Running the Tool
The user has the option to analyse all source files, or a specified subset. These can be specified manually over command-line, or within a text file - it is the user's choice.
#### Specify Source Files Manually
To specify source files manually, run as follows:
```
$python main.py path -m file1.c file2.c ... fileN.c
```
* `path` is the relative path from current directory to parent directory of 'source' and 'includes' folder
* `-m` must follow to indicate manual method of specification
* `fileX.c` is a sourcefile name


#### Specify Source Files in Text File
To specify source files in a text file, run as follows:
```
$python main.py path -f textfile.txt
```
* `path` is the relative path from current directory to parent directory of 'source' and 'includes' folder
* `-f` must follow to indicate text file method of specification
* `textfile.txt` is the textfile name

The textfile must be in the current working directory

## Example Output
![](https://github.com/markroche92/Map-Header-Files/blob/master/images/exampleOutput.PNG)
*image generated using [GraphViz](https://pypi.org/project/graphviz/) python library*
