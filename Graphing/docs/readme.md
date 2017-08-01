# GraphQL and AUT Air New Zealand R & D Project

## What is the project
---
The project looks at making data more accessible for chatbots and future applications through the powers of GraphQL, Web Scraping and Serverless Applications.

---

Oscar and internal chatbots provide an interesting angle for digital communication with existing and soon to be built infrastructure. The goal of faster communication has the  potential to lead to more information flowing between different kinds of consumers of Air New Zealand. The AUT project team is looking to display and learn new tech.

### The System
---

The system has three major features that allow for an increasing sourcing of information, additional supplies of well structure light data describing one of Air New Zealands most important discussion points, locations. As well as more noveau approach to provide event information as people are traveling.
  <dl>
<dt>Features</dt>
<dd>- Web Scraping Scripts</dt>
<dd>- DynamoDB store of knowledge</dt>
<dd>- Serverless GraphQL interface</dt>

### Web & API Scraping Scripts
At the time of writing we have tackled and learnt BeautifulSoup, requests and python to pull and loop over html plus json elements. We are using APIs such as facebook, eventfindas, eventbrite.
The main websites we have been targeting for this have been: Wikipedia, which we have been using to draw information around Continents, Countries, Cities and Towns. Tourism New Zealand for interesting tourism information and events. and  we are also looking at using geonames and maxmind to gain more information on cities and countries. 
We believe this is within our capabilites and will look to find more relevant data as we progress.
We will deploy most of our scripts to AWS Lambda and to look to have them run at different rates to keep their  information updated. 
Aswell as errorchecking to notify when unexpected events occur with the web and database data.

### DynamoDB
 We plan on using AWS DynamoDB to store the information we collect as it is extremely cheap and scalable. It is also is a noSQL database meaning the information we gather and communicate will mostly never leave a json readable key value data scheme.
 
 ### GraphQL
 The interesting front of our application. To quickly prime people who are new to this application, it is an application query language designed by facebook in 2012 and open-sourced in 2015.
 It allows data to be retrieved minimally and quickly,what do we mean by this?
 You ask for the data you need in the body of your query and you then receive it.
 It achieves a similar end product to REST transfering state of resources as well as the ability to design your data layer around all of your user interfaces.
 One of it's big advantages is the way it interacts with user interfaces.
