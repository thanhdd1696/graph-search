import argparse as ap
from Astar import *
from DLS import *

######## RUNNING THE CODE ####################################################
#   You can run this code from terminal by executing the following command
#   python solvepuzzle.py <puzzle> <procedure> <output_file> <flag>
#   for example: python solvepuzzle.py BBWEW A result 0
#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA
###############################################################################


################## YOUR CODE GOES HERE ########################################
def graphsearch(puzzle, flag, procedure_name):
    solution = ''
    print("puzzle: ", puzzle)
    print("Flag: ", flag)
    print("Procedure: ",procedure_name)
    if procedure_name == "DLS":
        bound = 50  # you have to determine its value
        dls = DLS(puzzle)
        n = dls.search(bound, flag)
        solution = n.getPath()
    elif procedure_name == "A":
        astar = Astar(puzzle)
        n = astar.search(flag)
        solution = n.getPath()
    else: 
        print("invalid procedure name")
    return solution

###############################################################################
########### DO NOT CHANGE ANYTHING BELOW ######################################
###############################################################################

def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')
    file_handle.write(solution)

def main():
    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("puzzle_string", help= "comprises a sequence of symbols, can be B, W, E", type= str)
    parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be BK, DLS, A", type=str)
    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)
    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # get all the arguments
    arguments = parser.parse_args()

##############################################################################
# these print statements are here to check if the arguments are correct.
# print("The puzzle is " + arguments.puzzle_string)
# print("The procedure_name is " + arguments.procedure_name)
# print("The output_file_name is " + arguments.output_file_name)
# print("The flag is " + str(arguments.flag))
##############################################################################

    # Extract the required arguments
    puzzle = arguments.puzzle_string
    procedure_name = arguments.procedure_name
    output_file_name = arguments.output_file_name
    flag = arguments.flag

    solution_string = "" # contains solution
    write_flag = 0 # to control access to output file

    # take a decision based upon the procedure name
    if procedure_name == "DLS" or procedure_name == "A":
        solution_string = graphsearch(puzzle, flag, procedure_name)
        write_flag = 1
    else:
        print("invalid procedure name")

    # call function write to file only in case we have a solution
    if write_flag == 1:
        write_to_file(output_file_name, solution_string)

if __name__ == "__main__":
    main()
