const { OpenAIEmbeddings } = require( "langchain/embeddings/openai");

const instanceName = process.env["AZURE_OPENAI_INSTANCE_NAME"];
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
const deploymentName = process.env["EMBEDDING_MODEL_DEPLOYMENT_NAME"];

const embeddings = new OpenAIEmbeddings( {
    azureOpenAIApiKey: apiKey, 
    azureOpenAIApiInstanceName: instanceName, 
    azureOpenAIApiDeploymentName: deploymentName, 
    azureOpenAIApiVersion: '2022-12-01', 
});

(async() => {
    const res = await embeddings.embedQuery(
        "Techincal issue: The device is not functioning properly, technical assistance is required to repair it, or a replacement part is required"
    );

    console.log(res)
})();