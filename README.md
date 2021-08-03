# Pantzer-Index

No standardized list of printers’ and publishers’ names with their associated STC numbers currently exists. There is, however, an index of printers and publishers produced by Katherine Pantzer for the third volume of the STC. The index entries include the individual or organisation’s name (sometimes with variant spellings), a headnote giving brief biographical details and other information, and then the STC numbers for the books they printed or published, arranged by date. Supplied dates are given in brackets. Further information is included along with the numbers, such as an ‘f.’ denoting it was printed ‘for’ the individual (see STC Vol. III p. xviii for more of these abbreviations). Pantzer’s index was digitized and used as the basis for a dataset that gives standardized printer/publisher names, their STC numbers, dates, and other information that can be integrated with other datasets. 
1.	Scanning and OCR
The 193 pages of the index were scanned at 400 ppi after some experimentation with different sizes and resolutions. These images were OCR’d with ABBYY FineReader. 

2.	Manual cleaning, reformatting, and checking
a.	I spent around 2 days verifying FineReader’s ‘low-confidence characters’ (around 50 per page). These were mostly the characters ‘(A3)’, ‘11’ being mistaken for ‘ll’, and the daggers which mark printer’s dates of death. 
b.	The OCR’d text was then exported into Notepad++, to standardize its formatting and perform another general quality check. I introduced line breaks between each entry, consolidated entries that ran over a page break into one paragraph (removing their ‘continued’ headings), deleted the letter headings, and ensured that each year-group of STC numbers began on a new line. The following global changes were made to correct common OCR errrors:
•	‘Diet. 7’, ’Diet. /’ etc. to ‘Dict. 1’
•	Baseline closing quotation marks to ‘.,’
•	Carats to ‘A’ 
The most recent file with these changes made is ‘Pantzer4.txt’.

3.	Parsing and structuring 
A Jupyter Notebook script (‘Pantzer Index cleaning.ipynb’) processes the text, ultimately producing a Python dictionary that structures each entry into a hierarchy of printer name, headnote, date, STC number, STC ‘attributes’ (the extra information sometimes provided alongside the numbers). See the file ‘dict structures.txt’ for a representation of this. 

The script
•	Makes more global edits, such as replacing all hyphens for em dashes (the OCR distinguished between them inconsistently)
•	Splits the index by entry along the line breaks
•	Extracts the first line (name) as the heading, and splits the rest of the entry by the line-opening year headings using a regex written to account for all possible variations of date format (‘1556:’, but also ‘1556/1557:’, ‘after 1556?’, ‘1556, before:’, ‘1556? —1557’, etc.)
•	Splits each year group along ‘, ‘ (to ensure that this only split numbers and not their attributes, spaces before common attributes such as ‘, f.’ were temporarily removed). 
•	Some numbers are of the abbreviated form ‘—.4’. The script identifies these, and finds the root number in the item before, and replaces the dash with it.
•	Converts square brackets and question marks into ‘supplied’ and ‘queried’ attributes
•	Organises the numbers, attributes, dates, headnotes, and names into a Python dict hierarchy.

4.	Handling number ranges
Many numbers in the STC index are expressed as ranges, which pose a problem for the script, as they get processed as a single item. The output of the script was then processed by another script that separated out these ranges into individual items. Seven Python functions handle different kinds of range expression: integer to integer, decimal to decimal within the same integer, integer to decimal in the same integer, decimal to integer, decimal to decimal in another integer, integer to decimal in a different integer, and ranges that express an ‘a’ version of the text (e.g. ‘1234-1234a’). Other ranges that contain letters will be edited manually. Running this script produces a version of the Pantzer index that gives the maximum number of possible items between each range, even if they don’t exist. So, for instance, ‘1234-1234.5’ evaluates to 1234, 1234.1, 1234.2, 1234.3, 1234.4, and 1234.5, though some of these may not exist as the STC point system begins adding variants at .5. This is not a problem as the dataset is used to import names into a pre-existing list of extant STC numbers. It cannot, however, be used as a dataset of all STC numbers without it being edited down by cross-referencing it with this list. 
