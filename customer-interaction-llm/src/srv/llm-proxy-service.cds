using {xxx.cust.int.llm as db} from '../db/customer-interaction-db';

service LlmProxyService @(path : '/llm-proxy') {

    type LlmType : Integer enum {
        OpenAI_GPT35     = 0;
        OpenAI_GPT4      = 1;
        AzureOpenAI_GPT4 = 2;
        Google_Bard      = 3;
        Meta_LLaMA       = 4;
        GPTJ             = 5;
    };

    type Command : Integer enum {
        Completions = 0;
        Embedding   = 1;
    };

    type Role : String enum {
        Completions = 'completions';
        Embedding   = 'embedding';
    };

    type CompletionOptions {
        model       : String;
        temperature : Double default 0.8;
    };

    type Entity{
        field: String;
        value: String;
    };

    type CustomerMsgResult
    {
        sentiment: String;
        title: String;
        summary: String;
        entities: array of Entity;
    }

    type CustomerMsgReturnType {
        data : CustomerMsgResult;
        created_at: Integer;
        total_tokens   : Integer;
    };

    //action invokeLLM(role : Role, text : String) returns LlmReplyType;
    //@(path: '/invoke-llm')
    action invokeLLM(use_case : String, text : String) returns CustomerMsgReturnType;
    action sentimentAnalyse(text : String) returns CustomerMsgReturnType;
    action summarise(text : String) returns CustomerMsgReturnType;
    action extractEntities(text : String) returns CustomerMsgReturnType;
    action processCustomerMessage(text: String) returns CustomerMsgReturnType;
}
