# Bibliometric Analyses on the Reception of Eugen Ehrlich in the German Sociology of Law in the 1970s and 1980s

This notebook contains the code to generate the graphs and figures used in the publication

Christian Boulanger, "Ehrlich-Rezeption in den 1970er- und 1980er-Jahren: eine digitale Spurensuche", 
in: Marietta Auer, Ralf Seinecke, Eugen Ehrlich - Kontexte und Rezeptionen, Tübingen: Mohr-Siebeck, 2024.

The data for the following queries were obtained by querying the Web of Science and OpenAlex databases as well as
automatic citation extraction from the full texts of the Zeitschrift für Rechtssoziologie, the Journal of Law and 
Society and a collection of legal sociology textbooks between 1960 and 1989. The data of citation extraction is 
partially erroneous and incomplete due to the current deficiencies automated extraction. However, these errors 
should be evenly distributed. Therefore, results that do not concern individual values but express larger trends, 
should  be generally reliable.

## Requirements & Configuration

- You'll need a Neo4J server >= v4.4 
- For the Jupyter Notebook, install the required python modules with `(pip|conda) install py2neo python-dotenv pandas pyvis`
- In order to generate screenshots from the interactive HTML visualizations, you need to install the Playwright library:
  https://playwright.dev/python/docs/intro
- Rename `.env.dist` and adapt the values to fit your local environment

## Data

- Data from OpenAlex as well as the data obtained from machine extraction can be found in the `data` subdirectory as
  data dumps which can be imported into the Neo4J Graph database v4.4.
- The data obtained from the Web of Science cannot be shared due to legal reasons. 
- The same applies to the fulltexts of the ZfRsoz and the JLS, which you will have to download and convert to text 
files yourself, if you want to run the corpus analyses. 



 



