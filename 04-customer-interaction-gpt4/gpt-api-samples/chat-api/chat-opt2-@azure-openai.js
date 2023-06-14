const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");
const endpoint = `https://${process.env["AZURE_OPENAI_INSTANCE_NAME"]}.openai.azure.com`;
const apiKey = process.env["AZURE_OPENAI_API_KEY"];

const messages = [
  {
    role: "system",
    content: "You are an AI assistant that helps to classify the sentiment of input text.",
  },
  {
    role: "user",
    content: 'Input text: \n"Great coffee machine\n\nSentiment:',
  },
];

async function main() {
  console.log("== Chat Completions Sample ==");

  const client = new OpenAIClient(
    endpoint,
    new AzureKeyCredential(apiKey)
  );
  const deploymentId = process.env["GPT_MODEL_DEPLOYMENT_NAME"];
  const result = await client.getChatCompletions(deploymentId, messages);

  for (const choice of result.choices) {
    console.log(choice.message);
  }
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});

module.exports = { main };
