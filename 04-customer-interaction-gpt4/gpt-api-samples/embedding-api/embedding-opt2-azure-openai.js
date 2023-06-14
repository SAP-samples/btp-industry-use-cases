const { Configuration, OpenAIApi} = require('azure-openai');

const endpoint = `https://${process.env["AZURE_OPENAI_INSTANCE_NAME"]}.openai.azure.com`;
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
const deploymentName = process.env["EMBEDDING_MODEL_DEPLOYMENT_NAME"];
const openai = new OpenAIApi(
    new Configuration({
      apiKey: this.apiKey,
      azure: {
        apiKey,
        endpoint,
        deploymentName
      },
    })
  );

(async() => {
    const response = await openai.createEmbedding({
        input: "Techincal issue: The device is not functioning properly, technical assistance is required to repair it, or a replacement part is required"
    });

console.log(response.data.data[0].embedding);
})();