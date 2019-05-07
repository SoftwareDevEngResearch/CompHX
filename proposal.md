# Tommy Moore Project Proposal

The proposed work for this project consists of comparing the capabilities of  different compact heat exchanger designs. The purpose of this project is to support a proposed research project (pending approval by mid April) to design a compact heat exchanger for experimental loops that will be placed in the Versitale Test Reacter. Due to the expected heat rate inside of the experimental loop and the space available for heat exchange, the proposed heat exchanger must work very efficiently. To assist in the design of this heat exchanger, the different designs are analytically analyzed first before moving on to more complex analyses (CFD and experimental).

The software being proposed for this project will  read in the initial and boundary conditions for the heat exchanger as well as other design parameters. These values will then be used to compute the hot and cold side temperatures as well as the heat flux that heat exchanger removes from the system. The two design concepts being considered are a fin design and a shell and tube design. Each design will be analyzed for optimal fin spacing/tube diamater, number of tubes/fins, and length of fins as appropriate. Results will be tablated numerically as well as graphically. The main goal is to determine the optimal design (number of tubes, diameter, fin spacing, etc.) for each design concept and document the heat removal for each design. Heat exchanger performance will be computed using the analysis methods outlined in Incropera and Dewitt [1].

Though this code is being proposed for the application of a specific project, the goal is that it can be used to analyze any compact heat exchanger that utilizes a tube and shell or a fin design. This tool could be used by anyone that has a system with specified boundary conditions and desires to know the optimal spacing for their heat exchanger design. 

An additional goal of this project is to get a better understanding of batch scripting. On top of the script that computes the optimal conditions for the two heat exchangers considered, a script will be written where a group of physical layouts for the heat exchanger is specified and the corresponding thermal performance will be detailed for each case. These results will also be collected both graphically and numerically.

The codes written for this project will need to use numpy and matplotlib for math functions and graphing, respectively. Additionally, I hope to investigate some more advanced graphing packages to better visualize the results. This could include movies, contour plots, or other such figures. This software would also benefit from testing of the analytic solution, so a package such as unitest could be very useful. 

Depending on the time these features take to implement, more advanced functionality could also be implemented. This could include a graphical user interface, more advanced heat exchanger designs, or the development of input libraries to speed up run times. 

## References
1. Incropera, F. P., & DeWitt, D. P. (2002). Fundamentals of heat and mass transfer. New York: J. Wiley.
