const cds = require("@sap/cds");
const axios = require("axios");
const VCAP_APPLICATION = JSON.parse(process.env.VCAP_APPLICATION);
const llm_api_base_url = VCAP_APPLICATION.llm.api_base_url;

// Init instance of axios which works with llm_api_base_url
const axiosInstance = axios.create({ baseURL: llm_api_base_url });

//Authentication
if (VCAP_APPLICATION.llm.auth_method === "bearer-api-key") {
  //for example, openai
  const authorization = `Bearer ${VCAP_APPLICATION.llm.api_key}`;
  //const organization = VCAP_APPLICATION.llm.organization;
  axiosInstance.defaults.headers.common["Authorization"] = authorization;
  //axiosInstance.defaults.headers.common["OpenAI-Organization"] = organization;
} else if (VCAP_APPLICATION.llm.auth_method === "api-key") {
  //for example, azure openai service
  axiosInstance.defaults.headers.common["api-key"] =
    VCAP_APPLICATION.llm.api_key;
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
});

const invokeLLM = function (use_case, text) {
  //Retrieve the configuration from environment variable process.VCAP_APPLICATION
  //where the use_cases and access to the LLM API are defined
  const target_use_case = VCAP_APPLICATION.use_cases.filter(
    (entry) => entry.name === use_case
  )[0];
  const targetRole = VCAP_APPLICATION.llm.roles.filter(
    (roleEntry) => roleEntry.name === target_use_case.target_role
  )[0];
  const api = VCAP_APPLICATION.llm.api.filter(
    (apiEntry) => apiEntry.name === targetRole.target_api
  )[0];

  //Special process for ' and " in the text
  //Replace all ' with \', " with \"
  text = text.replaceAll("'", "'");
  text = text.replaceAll('"', '"');

  //llm vendor as openai. To be refactored as LlmProvider class for handling vendor-specific API format
  if (VCAP_APPLICATION.llm.vendor === "openai" || VCAP_APPLICATION.llm.vendor === "azure-openai") {
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
            content: `${targetRole.input_indicator}\n${text}\n${targetRole.output_prompt}`,
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

  //const api = VCAP_APPLICATION.llm.api[command]
};
