const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");
const endpoint = `https://${process.env["AZURE_OPENAI_INSTANCE_NAME"]}.openai.azure.com`;
const apiKey = process.env["AZURE_OPENAI_API_KEY"];

const input = [
  "Techincal issue: The device is not functioning properly, technical assistance is required to repair it, or a replacement part is required"
];

async function main() {
  console.log("== Embedding Sample ==");

  const client = new OpenAIClient(
    endpoint,
    new AzureKeyCredential(apiKey)
  );
  const deploymentId = process.env["EMBEDDING_MODEL_DEPLOYMENT_NAME"];
  const result = await client.getEmbeddings(deploymentId, input);

  for (const item of result.data) {
    console.log(item.embedding);
  }
  //console.log (result.data[0].embedding);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});

module.exports = { main };
