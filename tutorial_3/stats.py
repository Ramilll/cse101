def average(numlist):
    """Return average of list of numbers"""
    return (sum(numlist) / len(numlist)).__round__(2)

def string_floats_to_list(string_floats):
    """Return a list from the string of floats string_floats."""
    return [float(x) for x in string_floats.split()]

def student_data(data_string):
    """Compute (name, results) tuple from the string data_string."""
    login_name, string_floats = data_string.split(" ", 1)
    return login_name, string_floats_to_list(string_floats)

def tuple_to_string(name, results):
    """Return string from (name, results) tuple"""
    return name + " " +  " ".join([str(result) for result in results])

def read_student_data(filename):
    """Return list of student data from file"""
    with open (filename, "r") as f:
        return [student_data(line) for line in f]

def extract_averages(filename):
    """Return list of name and average for each line in file"""
    return [(name, average(results)) for name, results in read_student_data(filename)]

def discard_scores(numlist):
    """Filter numlist: construct a new list from numlist with
    the first two, and then the lowest two, scores discarded.
    """
    numlist = numlist[2:]
    numlist.remove(min(numlist))
    numlist.remove(min(numlist))
    return numlist

def summary_per_student(infilename, outfilename):
    """Create summaries per student from the input file 
    and write the summaries to the output file.
    """
    data = read_student_data(infilename)
    with open(outfilename, "w") as f:
        summed_scores = []
        for name, results in data:
            results = discard_scores(results)
            f.write(tuple_to_string(name, results) + " sum: " + str(sum(results).__round__(2)) + "\n")
            summed_scores.append(sum(results))
        f.write("total average: " + str(average(summed_scores)) + "\n")

def summary_per_tutorial(infilename, outfilename):
    """Create summaries per student from infile and write to outfile.
Now we want to create summaries for each tutorial. For each tutorial, we write to an output file a line containing the name of the tutorial together with its average, minimum, and maximum scores.

Since this is a French school, the tutorials are named TD1, TD2, TD3, etc (“TD” meaning travaux dirigés).

Note that no scores are to be removed from the information; we want the complete picture here. As usual, we use round on our floats before displaying them, to show (at most) 2 digits after the decimal point. The file must end with a newline character \n.

Write a function summary_per_tutorial which accomplishes this. Here’s a start:
"""
    data = read_student_data(infilename)
    with open(outfilename, "w") as file:
        tds_data = []
        for i, (name, results) in enumerate(data):
            if i == 0:
                for result in results:
                    tds_data.append([result])
            else:
                for j, result in enumerate(results):
                    tds_data[j].append(result)
        for i, td_data in enumerate(tds_data):
            file.write("TD" + str(i + 1) + ": average: " + str(average(td_data).__round__(2)) + " min: " + str(min(td_data)) + " max: " + str(max(td_data)) + "\n")
    


            