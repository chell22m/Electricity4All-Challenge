#Electricity4All-Challenge README - updated after deadline

I discovered this cool challenge at the UN Unite Ideas webiste on May 13th, 2016 - just two days before the deadline of May 15th, 2016 - and decided to give it a try.
With no prior knowledge of Visual Basic, I went through the code line by line adding my own comments to better understand the algorithm.
I managed to get a working solution submitted before the deadline. However, the documentation in the 'offcial' README is a little lacking.
Thus, I'm adding an updated README here for any visitors..

Further information on the challenge can be found here: https://unite.un.org/ideas/content/electricity4all-python-challenge

###(a) Description of the code

The original algorithm written in VBA found whether settlement locations should conect to a grid or an off-grid technology for their
electrical uses. The algorithm used a naive approach of a double for loop to loop over all the electrified posts in the outer loop
and all the un-electrified posts in the inner loop, before comparing if they were close in distance.

This proposed solution uses the Locality-Sensitive Hashing for Finding Nearest Neighbors Algorithm to solve the problem. The algorithm
only retrives the closest neighbors fullfiling the distance criteria for the un-electrified posts in the inner loop using a 2D Hash Map.
This speeds up the algorithm significantly.

###(b) instructions on how the program works and how to use it:

Please run the algorithm.py in a terminal with the related txt file, which really are csv files. 

```
$ python algorithm.py 
Please enter the scenario filename: scenarios/scenarioLow2.csv
Processing scenario file:  scenarios/scenarioLow2.csv
Elapsed time: 14.6737229824
```
*Also note that as of now the output.txt
file is overwritten so please copy before rerunning a new scenario. This is also listed under known issues.*

#####More information on the different files used during the run:
- **GIS_Input.txt** - constant location, population, and distance boundary data used by algorithm.py. This can be edited as well.
- **scenario1.txt** - Example input file - one possible scenario - there are multiple scenarios also generated in this format under the
scenarios folder.
- **output.txt** - the generated output file with the GIS input data also added for reference. The second row below the title lists the
sum of all the electrical statuses for each distance and population boundary condition.

###(c) Code running time, the RAM and the processor specifications of the computer used to run the code.

- Running time: 15.1933588982 seconds for the 40,000 entries
- Machine: Mac OS X Version 10.7.5
- Processor: 2.4 GHz Intel Core i5
- RAM: 4 GB 1333 MHz DDR3

###(d) Known issues

1. The csv files generated from Excel have the odd new line character (^M) - which causes issues with the input parser so please
remove them either using:
  - dos2unix
or:
  - perl -pi -e 's/\r\n|\n|\r/\n/g'   <input_file>
  
  source (http://stackoverflow.com/a/14155400)
  
2. As of now, please ensure that there are no empty lines, such as this: ",,,,," - anywhere in the file. But, note that this string
is fine: "0,,,,,". This is a bug and will be fixed.

3. The input and output files are listed as .txt but they really are .csv files. I chose to keep them comma separated so that they are
easy to view in Excel, which I'm guessing is preferred by the challenge committee as the original code was embedded in Excel and written
in VBA.

###(e) Improvements for the future

1. While coding up the solution, I initially used csv reader to parse in the input data. However, writing the output data was slightly
more challenging to update only one column for every boundary condition. Thus, after a little research I found out about pandas and
used this module to write the output. If I could start over, I would probably use pandas to read in the file as well - this would
most likely make it easier to generate different types of input file as well.

2. The current solution also overwrites the output.txt file for every scenario input file - this will need to be fixed.

3. The code was written in a very short time period - but it was written with reusability in mind so the different functions can be
imported to other modules without relying on any other functions. The prompt is only shown if the code is run stand-alone.

4. Following the point above, this would make unit testing these functions much easier. Also, unittests must be written for this.

5. There are several TODO stubs that need to be finished.

###(f) Credit

- For more information on LSH: https://www.slaney.org/malcolm/yahoo/Slaney2008-LSHTutorial.pdf
- Good intro to pandas: http://pandas.pydata.org/pandas-docs/stable/10min.html
- Documentation used to understand VBA: https://msdn.microsoft.com/en-us/library/sh9ywfdk.aspx
