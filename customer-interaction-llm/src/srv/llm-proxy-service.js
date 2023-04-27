const cds = require("@sap/cds");
const axios = require("axios");
const VCAP_APPLICATION = JSON.parse(process.env.VCAP_APPLICATION);
const llm_api_base_url = VCAP_APPLICATION.llm.api_base_url;

// Init instance of axios which works with llm_api_base_url
const axiosInstance = axios.create({ baseURL: llm_api_base_url });

const authorization = `Bearer ${VCAP_APPLICATION.llm.api_key}`;
//const organization = VCAP_APPLICATION.llm.organization;
axiosInstance.defaults.headers.common["Authorization"] = authorization;
//axiosInstance.defaults.headers.common["OpenAI-Organization"] = organization;

const createSession = async () => {
  console.log("Creating session");

  const authorization = `Bearer ${VCAP_APPLICATION.llm.api_key}`;
  //const organization = VCAP_APPLICATION.llm.organization;
  axiosInstance.defaults.headers.common["Authorization"] = authorization;
  //axiosInstance.defaults.headers.common["OpenAI-Organization"] = organization;

  //Setup the cookie
  let context = {};
  context.authorization = authorization;
  //context.organization = organization;
  return context; // return Promise<cookie> cause func is async
};

let isGetActiveSessionRequest = false;
let requestQueue = [];
const callRequestsFromQueue = (context) => {
  requestQueue.forEach((sub) => sub(context));
};
const addRequestToQueue = (sub) => {
  requestQueue.push(sub);
};
const clearQueue = () => {
  requestQueue = [];
};
//register axios interceptor which handles responses errors

axiosInstance.interceptors.response.use(null, (error) => {
  console.error(error.message);
  const { response = {}, config: sourceConfig } = error;
  // check if request failed cause Unauthorized or forbidden
  if (response.status === 408) {
    console.log(
      "The error is due to time out. \nWe'll create a new session and retry the request."
    );
    // if this request is first we set isGetActiveSessionRequest flag to true and run createSession
    if (!isGetActiveSessionRequest) {
      isGetActiveSessionRequest = true;
      createSession()
        .then((context) => {
          // when createSession resolve with cookie value we run all request from queue with new cookie
          isGetActiveSessionRequest = false;
          callRequestsFromQueue(context);
          clearQueue(); // and clean queue
        })
        .catch((e) => {
          isGetActiveSessionRequest = false; // Very important!
          console.error("Create session error: %s", e.message);
          clearQueue();
        });
    }
    // and while isGetActiveSessionRequest equal true we create and return new promise
    const retryRequest = new Promise((resolve) => {
      // we push new function to queue
      addRequestToQueue((context) => {
        // function takes one param 'cookie'
        console.log(
          "Retry with new session context %s request to %s",
          sourceConfig.method,
          sourceConfig.url
        );
        //******************************************************************************************/
        // Option 1: Setup the required headers: cookie,token and authorization, reintialise
        // an request with axios(sourceConfig)
        //******************************************************************************************/

        sourceConfig.headers.Authorization = context.authorization;
        sourceConfig.headers["OpenAI-Organization"] = context.organization;
        //resolve(axios(sourceConfig)); // and resolve promise with axios request by old config with cookie
        // we resolve exactly axios request - NOT axiosInstance request cause it could call recursion
        //******************************************************************************************/
        // Option 2: Retry the request with axiosInstance with initialized session context
        // Since the new session has been created, the session context has been initialized to axioInstance
        // the easiest way is to retry the request with axiosInstance and the original request config-sourceConfig
        // It might cause endless recursion if it is due to wrong credentials.
        // Therefore, please assure the correct credentials, otherwise, you may think of implement the
        // maximum retries.
        //******************************************************************************************/
        resolve(axiosInstance.request(sourceConfig));
      });
    });
    return retryRequest;
  } else {
    // if error is not related with Unauthorized we reject promise
    return Promise.reject(error);
  }
});

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
  if (VCAP_APPLICATION.llm.vendor === "openai") {
    //completions API
    if (api.name === "completions") {
      //completions api
      let messages = [{ role: "user", content: `${text}` }];
      //chat api
      if (api.api_path.endsWith("/chat/completions")) {
        messages = [
          {
            role: "system",
            content: `${targetRole.system_prompt}`,
          },
          {
            role: "user",
            content: `${targetRole.input_indicator}\n${text}\n${targetRole.output_prompt}`,
          }
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
      let data = { model: api.model, input: text };

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
