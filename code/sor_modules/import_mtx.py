"""
import_mtx.py

This module contains 2 functions:

  - import_mtx(); and
  - get_mtx_b().

import_mtx() takes 1 input:

  - filename - A string containing the path to an input file

import_mtx() reads in an .mtx file and builds CSR vectors from it using the
scipy.io.mmread() function.

Returns 3 numpy arrays in CSR format, val, col and rowStart.

get_mtx_b() aims to import or generate a b vector. It gives the user the
option to specify a b vector, randomly generate one, or quit. If the user
elects to import a file, the function checks if the file exists and if it is
of the correct file length, in which case it is imported.

If the user elects to generate a random array, one is generated using the
maximum and minimum values of the input matrix as upper and lower bounds.

get_mtx_b() returns a 1 dimensional numpy array.

Requirements: numpy, scipy.io, get_filename, write_output

"""

from sor_modules import get_filename, write_output
import numpy as np
import scipy.io


def import_mtx(filename, output_filename):
    try:
        # Import matrix
        A = scipy.io.mmread(filename)

        # Reformat matrix to CSR
        A = A.tocsr()

        # Set val to the CSR data
        val = A.data

        # Set val to the CSR indices
        col = A.indices

        # Set rowStart to the CSR row indices
        rowStart = A.indptr

        # Return val, col and rowStart vectors
        return val, col, rowStart
    except:
        write_output.output_text_file(output_filename, "Cannot Proceed")
        exit("Unable to import the .mtx file. Please check it and try again")


def get_mtx_b(val, rowStart, output_filename, rand_b=False):

    # Initialize vector b
    vector_b = np.array([])

    # While the b vector is empty
    while vector_b.size == 0:
        if rand_b == True:
            if min(val)!= max(val):
                vector_b = np.random.randint(min(val), max(val), rowStart.size - 1)
                continue
            else:
                vector_b = np.ones(rowStart.size - 1) * min(val)
                continue

        # If the user wants to provide a file name:
        if input('Would you like to enter a file containing a vector b? '
                 '[y/n]: ').upper() == 'Y':
            # Set the file name
            b_filename = input('Please enter the filename: ')

            # If the file exists:
            if get_filename.check_file_exists(b_filename):
                # Try to open the file into a numpy array
                try:
                    vector_b = np.genfromtxt(b_filename, max_rows=1)
                # If it doesn't work, let the user know and exit
                except:
                    write_output.output_text_file(output_filename, "Cannot "
                                                                   "Proceed")
                    exit("Error in importing the file. Please check that all "
                          "values are floats and there is no other "
                          "information in the file.")

                # If the number of entries in b is not the same as the number
                # of rows in the matrix
                if vector_b.size != rowStart - 1:
                    # If the user wants to try again
                    if input("That vector has the wrong dimensions, "
                             "%d instead of %d. Would you like to try again?"
                             " [y/n]: " %
                             (vector_b.size, rowStart - 1)).upper() == 'Y':
                        # Restart loop
                        continue
                    # If the user doesn't want to try again
                    else:
                        # Exit
                        exit("User exit. No output file created.")
            # If the file doesn't exist
            else:
                # If the user wants to try again:
                if input("I can't find that file. Would you like to try "
                         "again? [y/n]: ").upper() == 'Y':
                    # Restart loop
                    continue
                # If the user does not want to try again
                else:
                    # Exit
                    exit("User exit. No output file created.")
        # If the user doesn't want to enter a file name
        else:
            # If the user wants to generate a random vector:
            if input('Would you like to use a random vector? '
                     '[y/n]: ').upper() == 'Y':
                # Create a random vector_b based on maximum and minimum
                # values of A
                vector_b = np.random.randint(min(val), max(val),
                                             rowStart.size - 1)
            # If not, ask to exit
            else:
                # If user elects to exit
                if input('Would you like to exit? [y/n]: ').upper() == 'Y':
                    # Exit
                    exit("User exit. No output file created.")
                # Otherwise, restart loop
                else:
                    # Restart loop
                    continue

    # Return b
    return vector_b
