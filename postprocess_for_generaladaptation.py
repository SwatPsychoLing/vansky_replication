#Graph showing adaptation (decrease in surprisal)
#Include all sentences, and show average surprisal
#across sentences or word by word surprisal across
#whole thing
#Rather than selecting just the critical regions,
#look at either:
###All regions
###Sentence position - going from 1 to 120 (across
  #all 16 lists)
#Include filler sentences as well (probably learning
#something about the fillers and just not the critical
#sentences)
#Graph: sentence position (as independent var) and average
#surprisal across sentence (dependent var), with 16 data
#points for each
#Also want to show mean and std bar error
#Goal: show that it’s learning something, just not what
#we want ; stronger evidence that it’s a failure to
#replicate (post-processing is working)

##want to read in all the separate csv results
##for each sentence (1 to 120), add sentence position
    #of list
##at a given sentence position (1 to 120, dependent var)
    #add 16 data points - one for each list
    #each data point is avg sentence surprisal
    #for sentence at the position

import argparse
import pandas as pd

###### USER DEFINED: DIRECTORY OF ORIGINAL AND RESULTS FILES
directory_og = 'fj-original/'   ##directory of the original sentence files - complete w conditions
directory_res = 'fj-try3-output/'  ##directory of the processed output files
results_file = ''
original_file = ''


def main():
    global results_file, original_file
    ##setting up expected command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('list_name', type=lambda x:validate_list(parser, x))
    parser.add_argument('processed_filename')  ##where the processed output will be saved
    args = parser.parse_args()

    ##--LOAD RESULTS INTO DATAFRAME--##
    ##get columns of data fram from heading of results file
    columns = results_file.readline().strip("\n").split(" ")
    ##get the data from the results file
    line_reslst = []  ##list containing all results from file
        #each index corresponds to a word presented in that order
    #for each line in the results file
    for l in results_file.readlines():
        if(l[0] == '='):  ##reached end of data
            break
        else:  ##otherwise add next data point to list of lines
            l_listified = l.strip("\n").split(" ")  #turn line into list
            line_reslst.append(l_listified)

    data = pd.DataFrame(line_reslst, columns=columns)  #create dataframe of results list

    ##writing output##
    ##then write out to processed file in csv format
    inf = open(args.processed_filename, 'a')
    ##write lists in csv format
    ##WANT HEADINGS: list, sentid (critical), condition, order, word, sentpos, region (3/0), surp
    heading = "list,sentid,avgsurp\n"   ##get proper heading from column names
    list = args.list_name.split(".")[0]
    if(args.list_name == "ListA1.adapting"):  ##only write heading for first list; NOTE: hardcoded!
        file_output = heading  ##concatenate all info to write into file at end
    else:
        file_output = ""
    ##go through results file
    ##record sentence position
    curr_sentence_pos = 0
    ##start keeping track of average surprisal for this sentence
    curr_surprisal_total = 0
    curr_num_words = 0
    ##when new sentence position reached (onto next sentence)
        #add datapoint to output to file: sentence position + avg surprisal
    ##go through rows in data_region dataframe
    for row_num, row in data.iterrows():

        if int(row['sentid']) > curr_sentence_pos:  ##if reached next sentence
            ##get avg surprisal
            avg_pos_surp = curr_surprisal_total / float(curr_num_words)
            ##add to file output
            file_output += str(list) + "," + str(curr_sentence_pos) + "," + str(avg_pos_surp) + "\n"
            ##update all counter vars
            curr_sentence_pos = int(row['sentid'])
            curr_surprisal_total = float(row['surp'])
            curr_num_words = 1
        else:  ##word in current sentence
            curr_surprisal_total += float(row['surp'])
            curr_num_words += 1
    ##write out final sentence
    ##get avg surprisal
    avg_pos_surp = curr_surprisal_total / float(curr_num_words)
    ##add to file output
    file_output += str(list) + "," + str(curr_sentence_pos) + "," + str(avg_pos_surp) + "\n"

    inf.write(file_output)
    ##close files
    inf.close()
    results_file.close()
    original_file.close()


def validate_list(parser, listname):
    """
    given parser and name of current list
    opens and returns the results and original file for list
    using directories global vars
    """
    if (valid_ogfile(listname) and valid_resfile(listname)):
        return listname
    else:
        parser.error("Filename error: %s" % listname)

def valid_ogfile(listname):
    """
    given name of file
    assigns global original file (opened)
    returns false if unable to open file
    """
    global original_file, directory_og
    listname = listname.split(".")[0]  #get rid of adapting or notadapting
    try:
        original_file = open(directory_og+listname+".csv", "r")
        return True
    except:
        return False

def valid_resfile(listname):
    """
    given name of list
    assigns global results file (opened)
    returns false if unable to open file
    """
    global results_file, directory_res
    try:
        results_file = open(directory_res+listname+".output", "r")
        return True
    except:
        return False


###################################################################
# BELOW FUNCTION IS PROVIDED FROM VANSKY REPLICATION INSTRUCTIONS #
###################################################################
def add_regionnums(row):
    if row['condition'] == 'ambig' and row['sentpos'] in ('7','8','9'):
        #ambiguous critical region starts with word 7
        return(3)
    elif row['condition'] == 'unambig' and row['sentpos'] in ('9','10','11'):
        #unambiguous critical region starts with word 9
        return(3)
    else:
        return(0)

#######
main()
