# Knowledge Acquisition: Semantic Layer
In the development of HOLY, semantic-lexical relationships have been defined using varied methods based on the scope and class. Nevertheless, there was a tendency to employ manual methods when developing the current version of the Hydrogen Ontology. Automatic methods were implemented where reasonable, and a thesaurus was used as a tool in manual definition. Manual methods include the identification, definition, and verification of words and their relationships as well as using in-person research (articles, website, etc.) and expert involvement and analysis of data sources by humans. 

For example, the “Product” layer used a nearly completely manual approach to identify labels, keywords, connected words, and synonyms. This manual approach included internet searches, using dictionaries and lexica for identification as well as manually searching databases and verifying findings by cross-checking or consulting the domain expert. 

The “Organization” layer used primarily manual methods in researching hydrogen-related companies when building the structure and identifying words which indicate connections within the hydrogen market. Even automatically acquired words within test runs of the NLP Model have been checked manually for accuracy and quality of use.

The “Application” layer used a mainly manual approach with the assistance of a thesaurus. Based on the goal of providing a general and broad range of possible applications for hydrogen technologies, a thesaurus was used to find even more words which are associated to otherwise manually acquired ones. However, as in other classes, the relation and hierarchical structure was created using manual methods. Manual methods I this instance included the cross-checking of articles and lexica concerning the connection to different fuel cell technologies.

The “Geographic market” layer followed a completely automatic approach by importing Linked Open Data; specifically imported were sections of the DBpedia ontology. After researching the DBpedia ontology, the stored information concerning locations was seemed sufficient to integrate them into HOLY.

The “Project” layer used wholly manual methods. This is because project abbreviations and names do not always show a clear connection to the topic of hydrogen. Manual methods involved the manual search for hydrogen-related projects and the examination of hydrogen project databases.

The “Indicator” layer used manual methods, but with less depth than the previous classes. This was due to limitations of the scope of HOLY.

Ultimately, it can be said that automatic methods have been used in situations when the results can’t be doubted. For the core of the ontology and hydrogen definitions, solely manual methods have been implemented. For general terms, a thesaurus helped in the research of words accompanied by manual verification.

Manual methods have been used for:
-	Literature research
-	Conducting interviews with experts (knowledge exchange)
-	Research for possibilities of information extraction
-	Prioritizing knowledge
-	Vocabulary research
-	Literature review

A thesaurus has been used for:
-	Assisting in keyword search (just search/acquisition, the final identification of relevance by review was done manually)

Automatic methods have solely been used for:
-	Semantic relations concerning location data for the class “Geographic Market” (words, synonyms, related terms – e.g., Germany connected to European Union connected to Western Hemisphere) have been derived from the DBpedia Ontology

It should be noted that during the development of HOLY, available breakthrough tools such as Chat GPT have not been applied for knowledge acquisition. However, the use of such models is considered as a possible tool for brainstorming new keywords for future expansion of the ontology.
