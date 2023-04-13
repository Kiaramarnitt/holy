# Ontology Maintenance Guidelines

For the further development of HOLY, a maintenance plan has been developed which aims to continually evaluate the structure and accuracy of the ontology as well as provide feedback regarding areas of high potential for future growth endeavors. 

To do this, a [questionnaire](https://docs.google.com/forms/d/e/1FAIpQLSdN_JHk7BZ8_kjKnyAEIAPdALV5_qNRH9tDI_bt88si3CkQGQ/viewform?usp=sf_link) consisting of fixed, mostly open-ended questions has been created and will be publicly available to allow for external input about the current state of the hydrogen market. Submissions will be regularly reviewed and taken into account regarding changes for further versions of HOLY.

## Entity Deprecation Strategy

Following [MIRO](https://github.com/owlcs/miro/blob/master/miro.md) guidelines, classes are moved to owl:DeprecatedClass and labeled with an annotation property when deemed obsolete. No class is deleted.

## Versioning Policy 

In maintaining this ontology, the versioning policy introduced by [OBO Foundry](https://obofoundry.org/id-policy.html) is followed:

Versions are named by a date in the following format: YYYY-MM-DD. For a given version of an ontology, the ontology should be accessible at the following URL, where idspace; is replaced by the IDSPACE in lower case

