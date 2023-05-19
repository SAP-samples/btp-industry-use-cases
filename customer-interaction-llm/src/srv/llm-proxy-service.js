const cds = require("@sap/cds");
const axios = require("axios");
//load configuration of llm api access, prompts and use_cases.
const config = require("./config.json");
const llm_api_base_url = config.llm.api_base_url;

// Init instance of axios which works with llm_api_base_url
const axiosInstance = axios.create({ baseURL: llm_api_base_url });

//Authentication
//api_key or user_name/password etc credential must be configured in and loaded from 
//process env variables:
//process.env.api_key
if (config.llm.auth_method === "bearer-api-key") {
  //for example, openai
  const authorization = `Bearer ${process.env.api_key}`;
  //const organization = config.llm.organization;
  axiosInstance.defaults.headers.common["Authorization"] = authorization;
  //axiosInstance.defaults.headers.common["OpenAI-Organization"] = organization;
} else if (config.llm.auth_method === "api-key") {
  //for example, azure openai service
  axiosInstance.defaults.headers.common["api-key"] =
  process.env.api_key;
}

//here is the service implementation
module.exports = cds.service.impl(async function () {
  /**
   * A generic API to invoke LLM API and turn it into your custom REST API
   * Output as JSON
   */
  this.on("invokeLLM", async (req) => {
    const { use_case, text } = req.data;

    const result = await invokeLLM(use_case, text);
    return result;
  });

  /**
   * Prompt Engineering
   * Turning the LLM next word completion API into a REST API of sentiment analysis
   * Output as JSON
   */
  this.on("sentimentAnalyse", async (req) => {
    const { text } = req.data;

    const result = await invokeLLM("sentiment-analysis", text);
    return result;
  });

  /**
   * Prompt Engineering
   * Turning the LLM next word completion API into a REST API of
   * summarising a input text into a title(<=100 characters) and a summary (<=300 characters)
   * Output as JSON
   */
  this.on("summarise", async (req) => {
    const { text } = req.data;

    const result = await invokeLLM("text-summarisation", text);
    return result;
  });

  /**
   * Prompt Engineering
   * Turning the LLM next word completion API into a REST API of
   * extracting a list of entities(customer_no, product_name, order_no etc.) from a input text
   * Output as JSON
   */
  this.on("extractEntities", async (req) => {
    const { text } = req.data;

    const result = await invokeLLM("entity-extraction", text);
    return result;
  });

  /**
   * Prompt Engineering
   * Turning the LLM next word completion API into a custom REST API of
   * processing customer text message including
   * 1.Sentiment Analysis
   * 2.Text Summarisation
   * 3.Entities Extraction
   * Output as JSON
   */
  this.on("processCustomerMessage", async (req) => {
    const { text } = req.data;

    const result = await invokeLLM("customer-message-process", text);
    return result;
  });

  /**
   * Embedding
   * API Proxy of LLM embedding API to embed the input text into vector
   * Output as Vector string
   */
  this.on("embedding", async (req) => {
    const { text } = req.data;

    const result = await invokeLLM("words-embedding", text);
    return result;
  });

  /**
   * Zero-shot classification
   * API Proxy of LLM embedding API to embed the input text into vector
   * Output the customer message category as string based on cosine similarity
   */
    this.on("zeroShotClassification", async (req) => {
      const { inputVector } = req.data;
  
      const embedding = await invokeLLM("words-embedding", inputVector);
      //get intent embedding from db
      const query= SELECT `name,embedding` .from `InboundCustomerMessageIntent`;
      const intents = await cds.db.run (query);
      //const intentsString= JSON.stringify(intents)
      console.log(intents);
      const intent = await similaritySearch(embedding, intents);
      return intent;
    });


});

const invokeLLM = function (use_case, text) {
  //Retrieve the configuration from environment variable process.VCAP_APPLICATION
  //where the use_cases and access to the LLM API are defined
  const target_use_case = config.use_cases.filter(
    (entry) => entry.name === use_case
  )[0];
  const targetRole = config.llm.roles.filter(
    (roleEntry) => roleEntry.name === target_use_case.target_role
  )[0];
  const api = config.llm.api.filter(
    (apiEntry) => apiEntry.name === targetRole.target_api
  )[0];

  //Special process for ' and " in the text
  //Replace all ' with \', " with \"
  text = text.replaceAll("'", "'");
  text = text.replaceAll('"', '"');

  //llm vendor as openai. To be refactored as LlmProvider class for handling vendor-specific API format
  if (config.llm.vendor === "openai" || config.llm.vendor === "azure-openai") {
    //completions API
    if (api.name === "completions") {
      //set default completions api for davinci-text series model
      let messages = [{ role: "user", content: `${text}` }];
      //chat api is recommended GPT-3.5-Turbo onward
      if (api.api_path.includes("/chat/completions")) {
        messages = [
          {
            role: "system",
            content: `${targetRole.system_prompt}`,
          },
          {
            role: "user",
            content: `${targetRole.input_indicator}\n${text}\n${targetRole.output_indicator}`,
          },
        ];
      }
      return new Promise(function (resolve, reject) {
        axiosInstance
          .request({
            url: api.api_path,
            method: "POST",
            data: {
              model: api.model,
              messages: messages,
            },
          })
          .then((res) => {
            console.log(res.data);
            const message = res.data.choices[0].message;
            const replyText = message.content.replace(/\n/g, " ");
            console.debug(replyText);
            let result = {};
            result.data = JSON.parse(replyText);
            result.created_at = res.data.created;
            result.total_tokens = res.data.usage.total_tokens;
            console.debug(result);
            resolve(result);
            //resolve(res.data);
          })
          .catch((err) => {
            reject(err);
          });
      });
    } else if (api.name === "embeddings") {
      //per best practice, https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/embeddings?tabs=console#replace-newlines-with-a-single-space
      //Replace newlines with a single space
      let data = { model: api.model, input: text.replaceAll("\n", " ") };

      return new Promise(function (resolve, reject) {
        axiosInstance
          .request({
            url: api.api_path,
            method: "POST",
            data: data,
          })
          .then((res) => {
            console.log(res.data);
            const result = res.data.data[0].embedding.toString();
            resolve(`[${result}]`);
          })
          .catch((err) => {
            reject(err);
          });
      });
    }
  }

  //const api = config.llm.api[command]
};

// Scalar product between two vectors
const dot= function (vec1, vec2){
  var length = Math.min(vec1.length, vec2.length);
  var dotprod = 0;
  for (var i = 0; i < length; i++) {
    dotprod += vec1[i] * vec2[i];
  }
  return dotprod;
}
// Norm of a vector
const norm= function (vec){
  var N = Math.sqrt(dot(vec, vec));
  return N;
}
// Cosine similarity between two embeddings vectors
const cosineSimilarity = function(vec1, vec2)  {
  var cosim = dot(vec1, vec2) / (norm(vec1) * norm(vec2));
  return cosim;
};
const convertEmbedding= function(intent){


};
// Function to associate the embedding of an input message to the closest message Intent category
const similaritySearch = function(inputVector, intents) {
  
  //converting embeddings in LargeString format in array of doubles
  inputVector = inputVector.replace(/'/g, '"') 
  inputVector = JSON.parse(inputVector)

  //compute cosine similarities
  const similarities = new Map(intents.map( element =>  { return [element.name,
    embedding=cosineSimilarity(inputVector, JSON.parse(element.embedding.replace(/'/g, '"'))) ]; }),    
  );

  console.log(similarities);

  //Take max similarity
  var max_key=null;
  var max_value=0.;

  similarities.forEach( (v,k) =>  { 
    if( v > max_value){
      max_value=v;
      max_key=k;
    }
  });
    
  console.log(max_key);
  console.log(max_value);

  return max_key
};
