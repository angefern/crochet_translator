import re
# import sys
import requests 
from bs4 import BeautifulSoup

"""
SKILLS 
- web scraping (beautiful soup)
- regex 
- python 
- edge case handling (prevented partial matches)


NOTE TO SELF 
- "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass" into terminal to temporarily allow reading scripts
- ".\env\Scripts\activate" to enter the virtual environment 

BUGS 
        # deal with plurals !!!!!!!!!!!!!111
        # fix sl st (when there's a space within the term )
        # deal with 1st? (first) -- that's just bad pattern writing tbh.. not my problem 



IMPROVEMENT IDEAS 
-reading from a website / read a whole website 
-web/app interface?
-options for uk/us terms?
-error checking
-enter special stitches for your particular pattern (should be added to the end of the list - so they are chekced for first)
"""



def main(): 
    # get input text
    s= input("Enter your crochet pattern: ")

    # print the converted result
    print("\nTranslated pattern:\n" + convert(s))


def convert(s):
    
    # separate into two functions after 

    # get the website 
    url = "https://www.craftyarncouncil.com/standards/crochet-abbreviations" # save the url as a string
    response = requests.get(url) # returns a requests.Response object
    soup = BeautifulSoup(response.text, 'html.parser') # .text returns the content of the repsonse in unicode

    # pick out the terms we want to use from the webpage 
    terms = {} # create an empty dict 
    for row in soup.find_all('tr'): # find all table rows 
        cols = row.find_all('td') # find all table data cells in each row 
        if len(cols) == 2: # make sure there are two columns (for the term + def)            
            term = cols[0].text.strip().lower()
            definition = cols[1].text.strip().lower()

            if term == "*": # stop when you get to terms and common measurements (only taking the top half of the page basically )
                break
            if term == "ch-": # this particular term isn't v helpful in translating and complicates things 
                continue 
            if term and definition: # only adding non-empty entries 
                #*******here check if term contains "or" and enter two terms with the same def (+++ check if def contains an "or" - then match respectively)
                #*** c
                # could also deal with this using / to avoid duplicate replacing ...
                if "or" in term: 
                    term1, term2 = term.split(" or ")
                    if "or" in definition: 
                        def1, def2 = definition.split(" or ")
                        terms[term1] = def1
                        terms[term2] = def2                       
                    else: 
                        terms[term1] = definition
                        terms[term2] = definition              
                else:       
                    terms[term] = definition

        terms["ss"] = "slip stitch" # not found on this website

    for x in reversed(list(terms)): # checks for complicated variants of a stich before default versions
        # s = s.replace(x, terms[x])
        # s = s.replace(x.title(), terms[x].title()) # replace titlecase versions of the terms 
        # s = s.replace(x.upper(), terms[x].upper()) # replace uppercase versions of the terms 
        
        # for x in s: # find all occurences of the substring in the main string 
        # regex = r"(?:\b|\d+)" + re.escape(x) + r"(?![a-zA-Z])" #the substring is NOT followed by another letter (i.e. it is really only that symbol.... hopefully this works)
        # regex = r"(?![a-zA-Z])" + re.escape(x) + r"(?![a-zA-Z])" #the substring is NOT followed by another letter (i.e. it is really only that symbol.... hopefully this works)
        
        regex = r"\b(\d+)?" + re.escape(x) + r"(?![a-zA-Z])" #the substring is NOT followed by another letter (i.e. it is really only that symbol.... hopefully this works)                regex = r"\b(\d+)?" + re.escape(x) + r"(?![a-zA-Z])" #the substring is NOT followed by another letter (i.e. it is really only that symbol.... hopefully this works)
        # TEST FIXING SL SLT regex = r"(?<![a-zA-Z])(\d+)?" + re.escape(x) + r"(?![a-zA-Z])" #the substring is NOT followed by another letter (i.e. it is really only that symbol.... hopefully this works)                regex = r"\b(\d+)?" + re.escape(x) + r"(?![a-zA-Z])" #the substring is NOT followed by another letter (i.e. it is really only that symbol.... hopefully this works)

        # ensure word boundary, then capture the preceding number if it is there 
        # print(regex)
            #\b checks for word boundary before the substsring, escape makes sure the letters aren't interepreted as escape chaars 

        # s = re.sub(regex, terms[x], s, 0, re.IGNORECASE) 
        s = re.sub(regex, lambda match_obj: (match_obj.group(1) or '') + terms[x], s, 0, re.IGNORECASE | re.MULTILINE) #multiline isn't really needed here

        # pass funcion to re.sub as a replacement (second paramenter) -- function takes match object arg and retunrs the replacement string
        #match_obj.group(1) returns None/False if it didn't capture a number
            # # print(matches)
            # indices = [()
            ## still working on the regex 



    # print(terms)
    for x in terms: 
        print(f"{x}: {terms[x]}")

    return s


if __name__ == "__main__": 
    main()