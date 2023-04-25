# Functional Requirements Evaluation 

## Requirements

Identifier   | Competency Question / Natural language sentence                                                                     |Domain 
|-----|-----------------------------------------------------------------------------------------|---------------
HOLY1   |Who is the provider for a given product or technology?                                   | Market   
HOLY2   |In which geographical market is a certain product available?                             | Market   
HOLY3   |Which direct competitors ("rivals") does a company have per continent?                   | Market    
HOLY4   |What revenues does a given product generate per geographic market?                       | Market    
HOLY5   |Who are the major investors per continent?                                               | Market       
HOLY6   |In what kind of projects is a given organization engaged?                                | Market
HOLY7   |What applications are there for a given product?                                         | Technological  
HOLY8   |What is the state of the projects related to a given product type?                       | Technological 
HOLY9   |Which components are used in products converting hydrogen to power?                      | Technological     
HOLY10  |Which substitutes does a given product have?                                             | Technological     
HOLY11  |What projects are related to a given product type or technology?                         | Technological    
HOLY12  |Do product components change over time?                                                  | Technological
HOLY13  |In which type of vehicles are fuel cells used?                                           | Technological         
HOLY14  |What projects are related to a given application type?                                   | Market     
HOLY15  |What is the relation between geographic locations and the number of organizations?       | Market        
HOLY16  |What is the relation between geographic locations and the number of products?            | Market        
HOLY17  |In which countries is a given company present?                                           | Market              
HOLY18  |What patents does a given organization hold?                                             | Technological               



## Test Cases SPARQL Queries

Here we provide formalize the functional ontology requirements through test cases. We including SPARQL queries extracted from the previously listed requirements together with the expected results. 

<details><summary> HOLY1 Who is the provider for a given product or technology?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    select distinct ?product ?organization where { 
        ?organization holy:producesProduct ?product.
        ?product a holy:Product.
        ?organization a org:Organization
    } 
<strong>Expected Answer: </strong> An organisation who is connected to a given product. <em>e.g. Hyzon Motors produces Hyzon hybrid bi-polar plate technology.</em> [(see example)](HOLY1_example_results.csv)
</details>

<details><summary> HOLY2 In which geographical market is a certain product available?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    select distinct ?product ?geo where { 
        ?geo holy:hasProduct ?product.
        ?product a holy:Product.
        ?geo a holy:GeographicMarket.
    } 
<strong>Expected Answer: </strong>A products relation to a geographic region. <em>e.g. Hyzon Class 8 FCEV is available in North America, Australia</em>
</details>

<details><summary> HOLY3 Which direct competitors ("rivals") does a company have per continent?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?continent ?organization ((?organization_type) as ?economic_activity) where {
        ?organization a org:Organization, ?organization_type.
        ?organization holy:participatesIn ?geo.
        ?geo dbo:country ?Country.
        ?Country dbo:continent ?Continent.
        Filter(?organization_type in (holy:EnergySectorOrganization, holy:ManufacturingOrganization))
    } 
<strong>Expected Answer: </strong>List of organisations connected to similar sector in similar geographic areas. <em>e.g. Korea Western Power Co., Ltd. (KOWEPO) participate in the Energy Sector in Asia. </em>
</details>

<details><summary> HOLY4 What revenues does a given product generate per geographic market? </summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?Country ?product ?revenue where {
        ?product a holy:Product;
                holy:productSoldIn ?geo;
                holy:hasIndicator ?revenue.
        ?revenue a holy:Revenue.
        ?geo dbo:country ?Country.
    } 
<strong>Expected Answer: </strong> List of Product with Indicator Revenue filtered by geographic region.
</details>

<details><summary> HOLY5 Who are the major investors per continent? </summary>
<strong>SPARQL Query</strong>

    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?organization ?Continent (count(?investment) as ?qty_investments) where {
        ?organization a org:Organization;
                    holy:hasIndicator ?investment;
                    holy:participatesIn ?geo.
        ?investment a holy:Investment.
        ?geo holy:hasIndicator ?investment.
        ?geo dbo:country ?Country.
        ?Country dbo:continent ?Continent
    } group by ?organization ?Continent
<strong>Expected Answer: </strong> List of organisations by continent and characteristic of investment.
</details>

<details><summary> HOLY6 In what kind of projects is a given organization engaged? </summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX m4i: <http://w3id.org/nfdi4ing/metadata4ing#>
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    select distinct ?organization ?project_type where {
        ?organization m4i:associatesToProject ?project;
                    a org:Organization.
        ?project a ?project_type.
        ?project_type rdfs:subClassOf holy:ObjectiveBasedProject   
    } 
<strong>Expected Answer: </strong> List of projects associated to an organisation.
<em>e.g. Airbus is engaged in Product Development Project ZEROe</em>
</details>

<details><summary> HOLY7 What applications are there for a given product?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    select distinct ?product ?application where { 
        ?product holy:isUsedIn ?application.
        ?product a holy:Product.
        ?application a holy:Application
    } 
<strong>Expected Answer: </strong> List of applications associated to a specific product. [(see example)](HOLY7_example_results.csv)
</details>

<details><summary> HOLY8 What is the state of the projects related to a given product type?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    select distinct ((?product_type) as ?type) ((?project_state)as ?stage) (count(?project) as ?qty) where {
        ?project a holy:Project;
                holy:relatesToProduct ?product;
                a ?project_state.
        ?project_state rdfs:subClassOf holy:StateBasedProduct.
        ?product a holy:Product;
                a ?product_type.
    } group by ?product_type ?project_state
<strong>Expected Answer: </strong> List of  Projects  associated to a Product and thier state (planned, ongoing, finished)
</details>

<details><summary> HOLY9 Which components are used in products converting hydrogen to power?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dct: <http://purl.org/dc/terms/>
    select distinct ?product ?component where {
        ?product dct:hasPart ?component;
            a holy:PowerGeneration.    
    } 
<strong>Expected Answer: </strong>
</details>

<details><summary> HOLY10 Which substitutes does a given product have?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dct: <http://purl.org/dc/terms/>
    select distinct ?product ?substitute ?application where {
        ?product holy:isUsedIn ?application;
                a holy:Product.
        ?substitute holy:isUsedIn ?application;
                    a holy:substituteProduct.
    } 
<strong>Expected Answer: </strong> List of products associated to the same applications.
</details>

<details><summary> HOLY11 What projects are related to a given product type?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    select distinct ?product_type ?project where {
        ?project a holy:Project;
                holy:relatesToProduct ?product.
        ?product a holy:Product;
                a ?product_type.
    } 
<strong>Expected Answer: </strong> List of Projects associated to a given product.
</details>



<details><summary> HOLY12 Do product components change over time?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dct: <http://purl.org/dc/terms/>
    select distinct ?product ?component where {
        ?product dct:hasPart ?component;
            a holy:HydrogenProduct.    
    }
<strong>Expected Answer: </strong> List of product components asoccieated to a time stamp.

Requires time component included by timestamping provenance text obtained through OBIE
</details>

<details><summary> HOLY13 In which type of vehicles are fuel cells used?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    select distinct (count(?vehicle_type) as ?qty_vehicles) ?vehicle_type  where { 
        ?product holy:isUsedIn ?application.
        ?product a holy:PolymerElectrolyteMembraneFuelCell.
        ?application a ?vehicle_type.
        ?vehicle_type rdfs:subClassOf holy:Road.
    } group by ?vehicle_type
<strong>Expected Answer: </strong> List of vehicle types employing fuel cells. <em> e.g. Train, Truck, Card, etc.</em>
</details>

<details><summary> HOLY14 What projects are related to a given application type?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    select distinct ?application_type ?project where {
        ?project a holy:Project;
                holy:relatesToApplication ?application.
        ?application a holy:Application;
                    a ?application_type.
    } 
<strong>Expected Answer: </strong>List of Projects associated to entities in a given application class.
</details>


<details><summary> HOLY15 What is the relation between geographic locations and the number of organizations?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?Country (count(?organization) as ?org_qty) where {
        ?organization a org:Organization;
                    holy:participatesIn ?geo.
        ?geo a holy:GeographicMarket;
            dbo:country ?Country
    } group by (?Country)
<strong>Expected Answer: </strong> List of geographic locations in the market with the amount of organizations associated to them.
</details>

<details><summary> HOLY16 What is the relation between geographic locations and the number of products?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?Country (count(?product) as ?prod_qty) where {
        ?product a holy:Product;
                holy:participatesIn ?geo.
        ?geo a holy:GeographicMarket;
            dbo:country ?Country
    } group by (?Country)
<strong>Expected Answer: </strong>
</details>

<details><summary> HOLY17 In which countries is a given company present?</summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX schema: <http://schema.org/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?organization ?geo ?Country  ?Continent where {
        ?organization holy:participatesIn ?geo.
        ?organization a org:Organization.
        ?geo dbo:country ?Country.
        ?Country dbo:continent ?Continent.
    } 
<strong>Expected Answer: </strong> List of geographic locations in the market with the amount of products associated to them.
</details>

<details><summary> HOLY18 What patents does a given organization hold? </summary>
<strong>SPARQL Query</strong>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    select distinct ?organization ?patent where {
        ?organization a org:Organization;
                    holy:hasIndicator ?patent.
        ?patent a holy:Patent.
    } 
<strong>Expected Answer: </strong> List of patents associated to a given Organization
</details>




## Type of SPARQL Queries


HOLY Type        | Explicit Relation  | Inference/Aggregetaion  | LOD     | OBIE    | Total                                                                      
|--------------|--------------------|-------------------------|---------|---------|--------------|
Technological  |         5          |           2             |   0     |    1    |     8                                                               
Market         |         3          |           1             |   6     |    0    |     10         
Total          |         8          |           3             |   6     |    1    |     18
      