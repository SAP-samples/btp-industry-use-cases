# AI-driven Public Urban Transport Optimization

Below you can find a summary of the use case description. For the full explanation, please, refer to the two blog posts published in the SAP Community:

https://blogs.sap.com/2023/07/31/ai-driven-public-urban-transport-optimization-introduction-architecture/
https://blogs.sap.com/2023/07/19/ai-driven-public-urban-transport-optimization-implementation-deep-dive/

## Description

**The Urban Public Transport Industry**

The urban public transportation industry refers to the sector involved in moving people from one location to another. In terms of people transportation, it includes various modes such as buses, trains, subways, and others. The industry’s primary goal is to provide safe, efficient, and reliable transportation services.

Here are some key facts about the urbanization trends world-wide:
- Overall, more people in the world lives in urban than in rural setting since 2010. In 2020, 56.2 percent of the world population was urban. Around 75% of the EU citizens are living in the cities.
- The urban transport has impact to the society and the environment. For example, in the US public transportation is having 84% less carbon emission compared to by using regular cars. The electric and hybrid buses count is constantly growing and now around 80% if then is leading to clean technology. The overall consumption of the gasoline in the US is reduced by 6 billion gallon each year by using the public transport
- The traffic congestion and inefficient transport systems still persist, and, for example, they account for 24% of GHG emissions in the European cities. This is due to high population density of our cities that is also destinated to increase, since the movement from rural areas to cities never stopped.
- Public transportation continues to be one of the safest modes of travel. Safe travel is a high priority of public transportation systems, state, and local governments.

**The challenge of public mobility**

The public transport systems are far from being efficient and well planned, resulting in several issues that we experience every day. Let’s see, what are the major challenges in the industry. Among the most common issues we can recognize:

- Long detouring distance
- Improper departure frequency setting
- Crowded travel during rush hours
- Poor passenger comfort in vehicles
  
Some other issues are emerging with the city expansion, for example it is possible to notice:

- Unreasonable layout of public transport lines
- Insufficient public transport infrastructures
- Insufficient number of stations
- Long waiting times
  
The main challenge for the transportation industry is to continuously improve the transportation service in the city, capture each anomaly and react in the real-time.

The urban public transport is a very complex scenario that can be described with accuracy only considering data coming from several data sources, often delivered in real-time. We can mention some of them. For example, the service timetables, the vehicle location, all the unstructured data posted by the users on social media. The only possibility to deal with so many and complex data is to drop the classic approaches and turn to AI.


## Solution Architecture

In our use case we are imaging to play the role of a SAP partner who is engaged by a public transport operator in the city of London who need to build an AI-driven solution on top of SAP BTP to optimize the bus service he operates.

The scenario of the public transport is usually very complicated and it can be described only by acquiring different types of data from many data sources, endogenous or exogenous to the enterprise. So, here data is the foundation and for this reason we have conceived the architecture depicted below where we have designed a performant data orchestration with SAP Data Intelligence and we have foreseen a suitable data persistency layer based on SAP Datasphere (which relies on SAP HANA Cloud DB and HANA Data Lake) that will feed AI algorithms for the timetable optimization in SAP AI Core. The consumption of data and insights from AI is performed in SAP Analytics Cloud.

<p align="center">
<img src="https://blogs.sap.com/wp-content/uploads/2023/07/architecture-4.png" alt="drawing" width="700"/>
</p>

Please, notice that the vehicle use in the transportation companies are managed by the SAP Digital Vehicle Hub, which contributed to the final data model as well with master and transaction data related to the vehicle management.

The stories deployed in the SAP Analytics Cloud are exposed in the SAP Build Work Zone, Standard Edition. The Work Zone is the final end-user interface, where the role-based access helps to assign the right access for each user.


**Prototyped components**

For this use case we protoyped only some components of the solution to give some inspiration. In particular, we prototyped the following items:

- Data ingestion and orchestration for the London bus service

  - Data ingestion pipelines with SAP Data Intelligence
  - Data tiering with SAP Data Intelligence
  - Integration of SAP Digital Vehicle Hub
    
- Harmonization and modeling of the London bus service data

  - Harmonizing and modeling data with SAP Datasphere graphical & SQL views
  - Harmonizing data SAP Datasphere Analytic Models

- Visualizing insights from data for the London bus service
  
  - Monitoring tools for the urban public transport use case


## How to use the material

In this repository we are providing the material relative to the prototyped components. In order to repduce in your landscape what we did, please, follow the instructions provided in each folder in the order proposed below.

File or Folder | Purpose
---------|----------
[01-data-ingestion-and-orchestration](./01-data-ingestion-and-orchestration) | Material to implement the data ingestion and orchestration for the London bus service
[02-data-harmonization-and-modeling](./02-data-harmonization-and-modeling/) | Material to perform the harmonization and modeling of the London bus service data
[03-visualize-insights-from-data-and-AI](./03-visualize-insights-from-data-and-AI/) | Material to build a SAC story for the urban public transport use case
[development](./development) | Jupyter notebook to test some Python code then used in the prototype.


## How to obtain support

[Create an issue](https://github.com/SAP-samples/btp-industry-use-cases/issues) in this repository if you find a bug or have questions about the content.
 
For additional support, [ask a question in SAP Community](https://answers.sap.com/questions/ask.html).


## License
Copyright (c) 2023 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](../LICENSE) file.
