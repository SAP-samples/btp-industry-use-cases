const cds = require("@sap/cds");
const axios = require("axios");
const VCAP_APPLICATION = JSON.parse(process.env.VCAP_APPLICATION);
const llm_api_base_url = VCAP_APPLICATION.llm.api_base_url;

// Init instance of axios which works with llm_api_base_url
const axiosInstance = axios.create({ baseURL: llm_api_base_url });

const authorization = `Bearer ${VCAP_APPLICATION.llm.api_key}`;
const organization = VCAP_APPLICATION.llm.organization;
axiosInstance.defaults.headers.common["Authorization"] = authorization;
//axiosInstance.defaults.headers.common["OpenAI-Organization"] = organization;

const createSession = async () => {
  console.log("Creating session");

  const authorization = `Bearer ${VCAP_APPLICATION.llm.api_key}`;
  const organization = VCAP_APPLICATION.llm.organization;
  axiosInstance.defaults.headers.common["Authorization"] = authorization;
  //axiosInstance.defaults.headers.common["OpenAI-Organization"] = organization;

  //Setup the cookie
  let context = {};
  context.authorization = authorization;
  context.organization = organization;
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
//here are the service handlers
module.exports = cds.service.impl(async function () {
  this.on("invokeLLM", async (req) => {
    const { command, text } = req.data;

    const result = await invokeLLM(command, text);
    return result.choices[0].message;

  });
});

const invokeLLM = function (command, text) {
  const api = VCAP_APPLICATION.llm.api[command]
  return new Promise(function (resolve, reject) {
    axiosInstance
      .request({
        url: api.api_path,
        method: "POST",
        data: {
          model: api.model,
          messages: [{ role: "user", content: `${text}` }],
        },
      })
      .then((res) => {
        console.log(res.data.choices[0].message);
        resolve(res.data);
      })
      .catch((err) => {
        reject(err);
      });
  });
};
