# ****************************************
#
#
# TODOS
# - Look up papers on malware classification
# - How many threads a Malware process spawned (possibility)
# - How many of each type of system call was made (could try transforming this like e^(#calls) or something)
# - N-Grams (count # of times see a sequence [do for all possible sequences])
# - # processes created
# - which DLL files its opening
# - filetype being opened
# - Search the Malware classes online to see what they do: ex. http://www.mcafee.com/threat-intelligence/malware/default.aspx?id=136491
# TODO: Write a program that prints out the average feature vector for each class, according to the
#       featues we defined here
# -impersonate_user system call looks sketch
# -autoexec.bat calls? (Swizzor)
# Number of files created [create_file] (Swizzor?)
# ****************************************
import os
from collections import Counter
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import numpy as np
from scipy import sparse


## Here are two example feature-functions. They each take an xml.etree.ElementTree object,
# (i.e., the result of parsing an xml file) and returns a dictionary mapping
# feature-names to numeric values.
## TODO: modify these functions, and/or add new ones.
def first_last_system_call_feats(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'first_call-x' to 1 if x was the first system call
      made, and 'last_call-y' to 1 if y was the last system call made.
      (in other words, it returns a dictionary indicating what the first and
      last system calls made by an executable were.)
    """
    c = Counter()
    in_all_section = False
    first = True # is this the first system call
    last_call = None # keep track of last call we've seen
    for el in tree.iter():
        # ignore everything outside the "all_section" element
        if el.tag == "all_section" and not in_all_section:
            in_all_section = True
        elif el.tag == "all_section" and in_all_section:
            in_all_section = False
        elif in_all_section:
            if first:
                c["first_call-"+el.tag] = 1
                first = False
            last_call = el.tag  # update last call seen

    # finally, mark last call seen
    c["last_call-"+last_call] = 1
    return c

def system_call_count_feats(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'num_system_calls' to the number of system_calls
      made by an executable (summed over all processes)
    """
    c = Counter()
    in_all_section = False
    for el in tree.iter():
        # ignore everything outside the "all_section" element
        if el.tag == "all_section" and not in_all_section:
            in_all_section = True
        elif el.tag == "all_section" and in_all_section:
            in_all_section = False
        elif in_all_section:
            c['num_system_calls'] += 1
    return c



# **********************************
#
# OUR FEATURES
#
# **********************************
def num_system_call_feats(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'first_call-x' to 1 if x was the first system call
      made, and 'last_call-y' to 1 if y was the last system call made.
      (in other words, it returns a dictionary indicating what the first and
      last system calls made by an executable were.)
    """
    c = Counter()
    in_all_section = False
    first = True # is this the first system call
    last_call = None # keep track of last call we've seen
    for el in tree.iter():
        # ignore everything outside the "all_section" element
        if el.tag == "all_section" and not in_all_section:
            in_all_section = True
        elif el.tag == "all_section" and in_all_section:
            in_all_section = False
        elif in_all_section:
            c["num_call-"+el.tag] += 1

    return c

def num_ngram_system_calls(n):
    def f(tree):
        c = Counter()
        in_all_section = False
        cur_ngram = []
        for el in tree.iter():
            # ignore everything outside the "all_section" element
            if el.tag == "all_section" and not in_all_section:
                in_all_section = True
            elif el.tag == "all_section" and in_all_section:
                in_all_section = False
            elif in_all_section:
                cur_ngram.append(el.tag)
                if len(cur_ngram) == n:
                    c["num_ngram_call-"+"-".join(cur_ngram)] += 1
                    cur_ngram.pop(0)
        return c
    return f




def num_start_term_reason_feats(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'first_call-x' to 1 if x was the first system call
      made, and 'last_call-y' to 1 if y was the last system call made.
      (in other words, it returns a dictionary indicating what the first and
      last system calls made by an executable were.)
    """
    c = Counter()
    for el in tree.iter():
        if el.tag == "process":
            startreason = el.attrib['startreason']
            termreason = el.attrib['terminationreason']
            c['num_s_reason-' + startreason] += 1
            c['num_t_reason-' + termreason] += 1

    return c

def username_feats(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'first_call-x' to 1 if x was the first system call
      made, and 'last_call-y' to 1 if y was the last system call made.
      (in other words, it returns a dictionary indicating what the first and
      last system calls made by an executable were.)
    """
    c = Counter()
    for el in tree.iter():
        if el.tag == "process":
            if 'username' in el.attrib:
                username = el.attrib['username']
                c['username-' + username] = 1
    return c

def weird_sequence_in_filename(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'first_call-x' to 1 if x was the first system call
      made, and 'last_call-y' to 1 if y was the last system call made.
      (in other words, it returns a dictionary indicating what the first and
      last system calls made by an executable were.)
    """
    c = Counter()
    for el in tree.iter():
        if el.tag == "process":
            if 'filename' in el.attrib:
                filename = el.attrib['filename']
                if "&#x7E;" in filename:
                    c['weird_in_filename'] = 1

    return c

def windows_commands_in_filename(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'first_call-x' to 1 if x was the first system call
      made, and 'last_call-y' to 1 if y was the last system call made.
      (in other words, it returns a dictionary indicating what the first and
      last system calls made by an executable were.)
    """
    c = Counter()
    win_commands = ["del ", "ping ", " nul"]
    for el in tree.iter():
        if el.tag == "process":
            if 'filename' in el.attrib:
                filename = el.attrib['filename']
                for cm in win_commands:
                    if cm in filename:
                        c['win_command_in_filename'] = 1
                        return c

    return c


def num_processes(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'first_call-x' to 1 if x was the first system call
      made, and 'last_call-y' to 1 if y was the last system call made.
      (in other words, it returns a dictionary indicating what the first and
      last system calls made by an executable were.)
    """
    c = Counter()
    in_processes = False
    for el in tree.iter():
        if el.tag == "processes" and not in_processes:
            in_processes = True
        elif el.tag == "processes" and in_processes:
            in_processes = False
        elif in_processes and el.tag == "process":   
            c["num_processes"] += 1
    return c
 
def num_threads(tree):
    """
    arguments:
      tree is an xml.etree.ElementTree object
    returns:
      a dictionary mapping 'first_call-x' to 1 if x was the first system call
      made, and 'last_call-y' to 1 if y was the last system call made.
      (in other words, it returns a dictionary indicating what the first and
      last system calls made by an executable were.)
    """
    c = Counter()
    for el in tree.iter():
       if el.tag == "thread":   
           c["num_threads"] += 1
    return c

def convert_to_secs(t):
    # Expects time in format 00:00.00
    min, sec = t.split(':')
    out = float(min)*60 + float(sec)
    return out

def total_runtime(tree):
    out = {}
    runtime = 0
    for el in tree.iter():
        if el.tag == "process":
            # Make sure this isn't a </process> tag or something
            if "starttime" in el.attrib:
                starttime = convert_to_secs(el.attrib['starttime'])
                endtime = convert_to_secs(el.attrib['terminationtime'])
                runtime += (endtime - starttime)
    out['runtime'] = runtime
    return out


ALL_FEATURES = [num_ngram_system_calls(3), num_system_call_feats, num_start_term_reason_feats,
                num_processes, num_threads, total_runtime,
                windows_commands_in_filename,
                username_feats]
