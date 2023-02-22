# team-tulip-troops

# Team description
Team "Tulip Troops" has four participants and one (non-participating) team lead from the Joint IT Command under the Defence Materiel Organization (DMO) of the Netherlands. The team is part of a large IT-innovation department (KIXS) of the Dutch DoD, and comprises two data scientists and two data engineers.

Team members: 
- Daan Gommers
- Gerben Rook
- Nicolaas Krempel
- Rik Kleine

# Results
Classifying content as misinformation is very important to counter the online onslaught of fake news working to undermine the healthy functioning of democracies. Several approaches have been proposed, such as classifying the text based on writing style, or using graph-based methods to determine fake content based on the spread through social media. We propose a more evidence-based method. Looking beyond the recent hype of ChatGPT, it has become apparent that Large Language Models (LLM) are capable of amazing feats. Many trivial human tasks such as comparing text are now also possible using AI. Therefore, we decided to further explore this technology for its ability to verify any given claim for its credibility, based on objective textual evidence.

More specifically, our solution leverages the power of LLMs to verify a claim based on evidence from open (internet) sources or an on-premise knowledge base. Using AI at every step, the first check whethers a text contains a claim, then compares the claim to search query results, determines the source credibility, and finally returns a weighted credibility score. Moreover, additional information (entities, sentiment) is added to enrich the data. A convenient interactive dashboard is provided for users to work with the created tooling.

We make use of two models from the Hugging Face library:
- For claim/opinion classification, claim verification and source credibility: `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`
- For summarization: `sshleifer/distilbart-cnn-12-6`

Using tweets as examples, an immediate problem that arises is the fact that most tweets do not actually contain fake news, or any claim for that matter. To determine this, we use a zero-shot approach, defined by Hugging Face as follows: "Zero Shot Classification is the task of predicting a class that wasn't seen by the model during training. This method, which leverages a pre-trained language model, can be thought of as an instance of transfer learning which generally refers to using a model trained for one task in a different application than what it was originally trained for. This is particularly useful for situations where the amount of labeled data is small." With this method, we apply the DeBERTa model to classify whether an input text contains an opinion or a claim. If it is an opinion, we deem it as not relevant, since it does not attempt to spread factual misinformation. If a claim is detected, however, our analysis continues. Our custom labels for this classification are: `['claim', 'opinion']`.

![](/docs/claim_opinion.png)

Using the summarization model, we summarize the claim to make sure it does not exceed 50 words. The claim is then used to query Google or ElasticSearch. The first approach relies on open-source internet data, while the second approach allows the user to limit the knowledge base on proprietary data. For the demo, we include the provided Guardian and New York Times articles in ElasticSearch. This could also be applied to NATO information sources. Note that this approach is only reliable up to the latest date that the knowledge base was updated. Searching Google will give the most recent results available.

After collecting the evidence, it is compared with the claim to judge whether it supports or contradicats the claim. For this, we first summarize each piece of evidence, and input it into the DeBERTa model. Our custom labels for this classification are roughly formatted like this: `['<claim> is true', 'not enough information', '<claim> is false']`. If the claim is not supported by the given piece of evidence, the result will be False. Of course, it can be the case that no relevant evidence is found, but only the next best results. Therefore, if the evidence provides no relevant information to verify the claim, the result will be Neutral. If the claim is obviously True, many relevant sources will be returned, and the model will judge the claim as True.

![](/docs/true_false.png)

An important next step is to also determine the credibility of the evidence sources. If a claim is deemed True based on fake news media, this would of course undermine the outcome completely. Having considered white/blacklist methods, we eventually ended up also applying the LLM to this problem, using a zero-shot task defined as `['credible source', 'uncredible source']`. This model is applied to the domain name of the source URL, e.g. 'bbc' or 'infowars'. If a source is uncredible, and states that a claim is True, our model actually reverses the conclusion and gives a negative score.

TODO screenshot van resultaat

Additionally, a possible feature worth mentioning is assessing the country affiliation of a source. Although this is not included in the analysis pipeline, experiments with this concept have yielded impresive results. An example would be assessing whether a source is affiliated with a hostile nation, and changing the credibility score accordingly.

TODO screenshot van resultaat

Finally, some additional information is extracted from the claim, such as entities and emotion. This is added to provide users with quick insights about the content of a claim.

The result of our model pipeline is stored in ElasticSearch and visualized in the dashboard.

![](/docs/dashboard.png)

# Architecture

## Overall architecture
![](/docs/overall_architecture.png)

The application architecture consists of several components that work together to provide a powerful and scalable solution. The frontend is built using Angular, a popular and widely used framework for building web applications. The frontend is responsible for displaying the data and providing an intuitive user interface for interacting with the application.

The backend is implemented using a REST API conforming to the Open API Specification. This API is responsible for receiving requests from the frontend and other external systems, as well as triggering the Python AI Pipeline with the provided claim or Twitter message. The AI Pipeline uses Python to perform the necessary natural language processing tasks and produce the desired results. The results are then stored in ElasticSearch, a distributed search and analytics engine that provides a scalable and flexible datastore for the application.

By utilizing a REST API, the application is highly interoperable and can be easily integrated with other systems. This allows for easy integration with external data sources or other applications that may need to interact with the data stored in ElasticSearch and the AI Pipeline.

Overall, the application architecture is designed to be highly scalable and provide a reliable and flexible solution for processing and analyzing large amounts of natural language data.

## Activity Diagram
![](/docs/activity_diagram.png)
Credibility activity diagram

## Open API Specification for Interoperability
![](/docs/open_api.png)
The backend is implemented using a REST API conforming to the Open API Specification for maximum interoperability.
![](/docs/response.png)
This is a response object from the service analyse (REST API) which can be easily integrated into other information systems.

# Research

## Programming Languages
- Python
- Web (Angular)

## Software / frameworks
- Hugging Face
- FastAPI (OpenAPI specs)
- ElasticSearch

## Explanation
We prefer Python for its rich availability of open source data science libraries. Hugging Face is a very useful package containing powerful (large) language models. Pretrained models proved very applicable to the given challenges. We use ElasticSearch to enable a custom knowledge base to search from, as well as saving the model output. FastAPI is used according to OpenAPI specifications in order to encourage interoperability. 

# Team Stories
TODO

# Additional information
TODO

# Links

- TIDE page: https://tide.act.nato.int/mediawiki/tidepedia/index.php/Team_1099