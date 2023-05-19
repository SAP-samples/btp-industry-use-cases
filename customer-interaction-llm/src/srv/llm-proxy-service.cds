using {xxx.cust.int.llm as db} from '../db/customer-interaction-db';

service LlmProxyService @(path : '/llm-proxy') {

    //type defintion for an extracted entity
    type Entity{
        field: String;
        value: String;
    };

    //type defintion for an process result of a customer text message
    type CustomerMsgResult
    {
        sentiment: String;
        title: String;
        summary: String;
        entities: array of Entity;
    }

    //type defintion for the final result of an process result of a customer text message
    type CustomerMsgReturnType {
        data : CustomerMsgResult;
        created_at: Integer;
        total_tokens   : Integer;
    };

    //type defintion for the final result of an process result of a customer text message
    type intentType {
        name : String;
        embedding: LargeString;
    };

    /**
     * A generic API to invoke LLM API and turn it into your custom REST API
     * Output as JSON
     */
    action invokeLLM(use_case : String, text : String) returns CustomerMsgReturnType;

    /**
     * Prompt Engineering
     * Turning the LLM next word completion API into a REST API of sentiment analysis 
     * Output as JSON
     */
    action sentimentAnalyse(text : String) returns CustomerMsgReturnType;

    /**
     * Prompt Engineering
     * Turning the LLM next word completion API into a REST API of 
     * summarising a input text into a title(<=100 characters) and a summary (<=300 characters)
     * Output as JSON
     */
    action summarise(text : String) returns CustomerMsgReturnType;

    /**
     * Prompt Engineering
     * Turning the LLM next word completion API into a REST API of 
     * extracting a list of entities(customer_no, product_name, order_no etc.) from a input text
     * Output as JSON
     */
    action extractEntities(text : String) returns CustomerMsgReturnType;

    /**
     * Prompt Engineering
     * Turning the LLM next word completion API into a custom REST API of 
     * processing customer text message including
     * 1.Sentiment Analysis
     * 2.Text Summarisation
     * 3.Entities Extraction
     * Output as JSON
     */
    action processCustomerMessage(text: String) returns CustomerMsgReturnType;

    action embedding(text: String) returns LargeString;

    //Actions and functions to classify a customer message based on intent with openAI embeddings
    action similaritySearch(inputVector: LargeString) returns String;
    action zeroShotClassification(inputVector: LargeString) returns String;
    function dot(vec1:array of Double, vec2:array of Double) returns Double;
    function norm(vec:array of Double) returns Double;
    function cosineSimilarity(vec1:LargeString, vec2:LargeString ) returns Double;
    function similaritySearch(inputVector: LargeString, intents: array of intentType ) returns String;

}
