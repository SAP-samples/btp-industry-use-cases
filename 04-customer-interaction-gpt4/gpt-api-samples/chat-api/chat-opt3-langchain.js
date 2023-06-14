const { ChatOpenAI } = require("langchain/chat_models/openai");
const { HumanChatMessage, SystemChatMessage } = require("langchain/schema");

const chat = new ChatOpenAI({
  azureOpenAIApiKey: "AZURE_OPENAI_API_KEY",
  azureOpenAIApiInstanceName: "AZURE_OPENAI_INSTANCE_NAME",
  azureOpenAIApiDeploymentName: "GPT_MODEL_DEPLOYMENT_NAME",
  azureOpenAIApiVersion: "2023-03-15-preview",
  temperature: 0.7,
});

(async () => {
  const response = await chat.call([
    new SystemChatMessage(
      "You are an AI assistant that helps to classify the sentiment of input text."
    ),
    new HumanChatMessage("Input text:\nGreat coffee machine\nSentiment:"),
  ]);

  console.log(response);
})();
