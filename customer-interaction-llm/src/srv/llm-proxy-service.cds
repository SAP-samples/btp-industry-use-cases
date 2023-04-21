using { xxx.cust.int.llm as db  } from '../db/customer-interaction-db';

service LlmProxyService @(path : '/llm-proxy') {
    action sentimentAnalyse (text: String);

    type LlmType : Integer enum {
        OpenAI_GPT35 = 0;
        OpenAI_GPT4 = 1;
        AzureOpenAI_GPT4 = 2;
        Google_Bard = 3;
        Meta_LLaMA = 4;
        GPTJ = 5;
    }

    type Command : Integer enum {
        Completions = 0;
        Embedding = 1; 
    }

    type CompletionOptions {
        model : String;
        temperature : Double default 0.8;        
    }

    type LlmReplyType {
        role : String;
        content: String;
    }
    action invokeLLM(command: Command, text: String) returns LlmReplyType;
}