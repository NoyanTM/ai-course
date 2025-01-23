# Task 5 - Report

## Requirements
- https://moodle.astanait.edu.kz/mod/assign/view.php?id=163845
- Develop software and model for analyzing / identification of stylistic / stylometry characteristics and the authorship
  - Get familiar with the methods and algorithms used in stylometry (e.g. word frequency analysis, N-grams, machine learning models).
  - Data input: Implement the ability to load texts (in TXT, DOCX, PDF formats).
  - Text preprocessing: Removing stop words, lemmatization, tokenization.
  - Feature extraction: The program should extract stylistic characteristics: Frequency of use of words and phrases. Average sentence length. Number of unique words. Use of grammatical constructions.
  - Author identification: Create a machine learning model that classifies text by author using a training sample of texts by famous authors.
  - Software functionality: Graphical interface or console application for working with texts. Visualization of stylistic characteristics (e.g. histograms of word frequencies). Ability to test the model on new texts.
  - Program testing: Test the program on texts from known sources (e.g., works of classical literature). Evaluate the accuracy of authorship determination.
Application examples:
- Literary studies: Analysis of the authorship of works, for example, proving that Shakespeare's plays were written by himself and not by another author.
- Forensics: Using text analysis to identify the author of anonymous threats, letters, or posts.
- Cybersecurity: Attribution of cyberattacks based on the analysis of the text of phishing letters or malware.
- Social media research: Identification of users or groups creating a certain type of content.

## Solution
- Installation:
  - python3 -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt
- Dataset example:
  - https://archive.ics.uci.edu/dataset/217/reuter+50+50
