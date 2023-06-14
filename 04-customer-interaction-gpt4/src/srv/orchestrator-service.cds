namespace cust.int.srv;

service OrchestratorService @(path: '/int-ticket') {
    type Message : {
        interaction_ID : Integer;
        contact_ID     : Integer;
        inboundTextMsg : LargeString;
        channel_code   : String;
        sequence       : Integer;
        summary        : LargeString;
        sentiment      : String;
        type_code      : String;
        intname        : String;
        intent_code    : String;
    }

    type Result  : {
        type         : String;
        route        : String;
        replyMessage : String;
        fsmcode      : Integer;
    }

    action handleMessage(message : Message)   returns Result;
    action handleMessageV2(message : Message) returns Result;
}
