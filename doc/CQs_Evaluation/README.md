# Competency Questions Evaluation


Num   | Competency Questions                                                                    |Type of CQ     
|-----|-----------------------------------------------------------------------------------------|---------------
CQ1   |Who is the provider for a given product or technology?                                   | Market   
CQ2   |In which geographical market is a certain product available?                             | Market   
CQ3   |Which direct competitors ("rivals") does a company have per continent?                   | Market    
CQ4   |What revenues does a given product generate per geographic market?                       | Market    
CQ5   |Who are the major investors per continent?                                               | Market       
CQ6   |In what kind of projects is a given organization engaged?                                | Market
CQ7   |What applications are there for a given product?                                         | Technological  
CQ8   |What is the state of the projects related to a given product type?                       | Technological 
CQ9   |Which components are used in products converting hydrogen to power?                      | Technological     
CQ10  |Which substitutes does a given product have?                                             | Technological     
CQ11  |What projects are related to a given product type or technology?                         | Technological    
CQ12  |Do product components change over time?                                                  | Technological
CQ13  |In which type of vehicles are fuel cells used?                                           | Technological         
CQ14  |What projects are related to a given application type?                                   | Market     
CQ15  |What is the relation between geographic locations and the number of organizations?       | Market        
CQ16  |What is the relation between geographic locations and the number of products?            | Market        
CQ17  |In which countries is a given company present?                                           | Market              
CQ18  |What patents does a given organization hold?                                             | Technological               



## SPARQL Queries

Here we provide example queries to answer the previously-listed competency questions with the HOLY ontology.

<details><summary> CQ1 Who is the provider for a given product or technology?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    select distinct ?product ?organization where { 
        ?organization holy:producesProduct ?product.
        ?product a holy:Product.
        ?organization a org:Organization
    } 
</details>

<details><summary> CQ2 In which geographical market is a certain product available?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    select distinct ?product ?geo where { 
        ?geo holy:hasProduct ?product.
        ?product a holy:Product.
        ?geo a holy:GeographicMarket.
    }
</details>

<details><summary> CQ3 Which direct competitors ("rivals") does a company have per continent?</summary>

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
</details>

<details><summary> CQ4 What revenues does a given product generate per geographic market? </summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?Country ?product ?revenue where {
        ?product a holy:Product;
                holy:productSoldIn ?geo;
                holy:hasIndicator ?revenue.
        ?revenue a holy:Revenue.
        ?geo dbo:country ?Country.
    }
</details>

<details><summary> CQ5 Who are the major investors per continent? </summary>

    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?organization ?Continent (count(?investment) as ?qty_investments) where {
        ?organization a org:Organization;
                    holy:hasIndicator ?investment;
                    holy:participatesIn ?geo.
        ?geo dbo:country ?Country.
        ?Country dbo:continent ?Continent
    } group by ?organization ?Continent
</details>

<details><summary> CQ6 In what kind of projects is a given organization engaged? </summary>

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
</details>

<details><summary> CQ7 What applications are there for a given product?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    select distinct ?product ?application where { 
        ?product holy:isUsedIn ?application.
        ?product a holy:Product.
        ?application a holy:Application
    } 
</details>

<details><summary> CQ8 What is the state of the projects related to a given product type?</summary>

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
</details>

<details><summary> CQ9 Which components are used in products converting hydrogen to power?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dct: <http://purl.org/dc/terms/>
    select distinct ?product ?component where {
        ?product dct:hasPart ?component;
            a holy:PowerGeneration.    
    }
</details>

<details><summary> CQ10 Which substitutes does a given product have?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dct: <http://purl.org/dc/terms/>
    select distinct ?product ?substitute ?application where {
        ?products holy:isUsedIn ?application;
                a holy:Product.
        ?substitute holy:isUsedIn ?application;
                    a holy:substituteProuct.
    }
</details>

<details><summary> CQ11 What projects are related to a given product type?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    select distinct ?product_type ?project where {
        ?project a holy:Project;
                holy:relatesToProduct ?product.
        ?product a holy:Product;
                a ?product_type.
    }
</details>



<details><summary> CQ12 Do product components change over time?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dct: <http://purl.org/dc/terms/>
    select distinct ?product ?component where {
        ?product dct:hasPart ?component;
            a holy:HydrogenProduct.    
    }

*Requires time component included by timestamping provenance text obtained through OBIE*
</details>

<details><summary> CQ13 What projects are related to a given application type?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    select distinct ?application_type ?project where {
        ?project a holy:Project;
                holy:relatesToApplication ?application.
        ?application a holy:Application;
                    a ?application_type.
    }
</details>


<details><summary> CQ14 In which type of vehicles are fuel cells used?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    select distinct (count(?vehicle_type) as ?qty_vehicles) ?vehicle_type  where { 
        ?product holy:isUsedIn ?application.
        ?product a holy:PolymerElectrolyteMembraneFuelCell.
        ?application a ?vehicle_type.
        ?vehicle_type rdfs:subClassOf holy:Road.
    } group by ?vehicle_type
</details>


<details><summary> CQ15 What is the relation between geographic locations and the number of organizations?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?Country (count(?organization) as ?org_qty) where {
        ?organization a org:Organization;
                    holy:participatesIn ?geo.
        ?geo a holy:GeographicMarket;
            dbo:country ?Country
    } group by (?Country)
</details>

<details><summary> CQ16 What is the relation between geographic locations and the number of products?</summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    select distinct ?Country (count(?product) as ?prod_qty) where {
        ?product a holy:Product;
                holy:participatesIn ?geo.
        ?geo a holy:GeographicMarket;
            dbo:country ?Country
    } group by (?Country)
</details>

<details><summary> CQ17 In which countries is a given company present?</summary>

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
</details>

<details><summary> CQ18 What patents does a given organization hold? </summary>

    PREFIX holy: <http://purl.org/holy/ns#>
    PREFIX org: <http://www.w3.org/ns/org#>
    select distinct ?organization ?patent where {
        ?organization a org:Organization;
                    holy:hasIndicator ?patent.
        ?patent a holy:Patent.
    }
</details>




## Type of SPARQL Queries


CQ Type        | Explicit Relation  | Inference/Aggregetaion  | LOD     | OBIE    | Total                                                                      
|--------------|--------------------|-------------------------|---------|---------|--------------|
Technological  |         5          |           2             |   0     |    1    |     8                                                               
Market         |         3          |           1             |   6     |    0    |     10         
Total          |         8          |           3             |   6     |    1    |     18
      