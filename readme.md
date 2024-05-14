# Bibliometric Analyses on the Reception of Eugen Ehrlich in the German Sociology of Law in the 1970s and 1980s

This notebook contains the code to generate the graphs and figures used in the publication

> Christian Boulanger, "Ehrlich-Rezeption in den 1970er- und 1980er-Jahren: eine digitale Spurensuche", 
in: Marietta Auer, Ralf Seinecke, Eugen Ehrlich - Kontexte und Rezeptionen, Tübingen: Mohr-Siebeck, 2024, S. 389-424.

The figures can be found in the ["docs" subdirectory](./docs/) and are published [here](https://cboulanger.github.io/ehrlich-bibliometrie/). 

The data for the following queries were obtained by querying the Web of Science and OpenAlex databases and by automatic
citation extraction from the full texts of the Zeitschrift für Rechtssoziologie, the Journal of Law and Society, and a 
collection of legal sociology textbooks between 1960 and 1989. It is to be expected that the data from the citation 
extraction will be partially incorrect and incomplete. This is due to the shortcomings of the automated extraction 
at the time of the research. However, these errors should be evenly distributed; results that do not concern individual 
values but express larger trends should be relatively reliable.

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

## Acknowledgements

- Data from the Web of Science and from OpenAlex has been provided by the German Competence Network for Bibliometrics funded by the Federal Ministry of Education and Research (Grant: 16WIK2101A)
- I would like to acknowledge the contribution of student assistants at the Max Planck Institute for Legal History and Legal Theory, in particular Lisa-Marie Esselmann, Daniel Fejzo, and Fabian Reinold, who created training data for the citation extraction model by annotating source texts.


 



