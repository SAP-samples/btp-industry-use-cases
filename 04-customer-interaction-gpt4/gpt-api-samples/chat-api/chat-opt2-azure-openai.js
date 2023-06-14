const { Configuration, OpenAIApi } = require("azure-openai");
const endpoint = `https://${process.env["AZURE_OPENAI_INSTANCE_NAME"]}.openai.azure.com`;
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
const deploymentName = process.env["GPT_MODEL_DEPLOYMENT_NAME"];

const openai = new OpenAIApi(
  new Configuration({
    apiKey: this.apiKey,
    azure: {
      apiKey: apiKey,
      endpoint: endpoint,
      deploymentName: deploymentName,
    },
  })
);

(async () => {
  const completion = await openai.createChatCompletion({
    messages: [
      {
        role: "system",
        content:
          "You are an AI assistant that helps to classify the sentiment of input text.",
      },
      {
        role: "user",
        content: 'Input text: \n"Great coffee machine\n\nSentiment:',
      },
    ],
  });

  console.log(completion.data.choices[0].message);
})();
