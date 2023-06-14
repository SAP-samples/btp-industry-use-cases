const axios = require('axios');

const url = `https://${process.env["AZURE_OPENAI_INSTANCE_NAME"]}.openai.azure.com/openai/deployments/${process.env["GPT_MODEL_DEPLOYMENT_NAME"]}/chat/completions?api-version=2023-03-15-preview`;
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
const headers = {
      'Content-Type': 'application/json',
      'api-key': apiKey,
};

const data = {
      messages: [
	{ role: 'system', content: 'You are an AI assistant that helps to classify the sentiment of input text.' },
	{ role: 'user', content: 'Input text: \n"Great coffee machine\n\nSentiment:' }],
	max_tokens: 800,
	temperature: 0.7,
};

axios.post(url, data, { headers })
.then(response => {
      console.log(response.data.choices[0].message);
      //Handle the response here
})
.catch(error => {
     console.error(error);
     //Handle errors here
});
