const axios = require('axios')
const url = `https://${process.env["AZURE_OPENAI_INSTANCE_NAME"]}.openai.azure.com/openai/deployments/${process.env["EMBEDDING_MODEL_DEPLOYMENT_NAME"]}/embeddings?api-version=2022-12-01`;
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
const headers =  {
   'Content-Type': 'application/json',
    'api-key': apiKey,
};

const data = {
    input: "Techincal issue: The device is not functioning properly, technical assistance is required to repair it, or a replacement part is required"
};

axios.post(url, data, {headers})
.then(response => {
    console.log(response.data.data[0].embedding);
    //Handle the response here
})
.catch(error => {
    console.error(error);
    //Handle errors here
});