namespace cust.int.srv;

type Message : {
    text: String;
    intent: String;
}

type Result : {
    type : String;
    route : String;
    replyMessage : String;
}

service OrchestratorService @( path: '/int-ticket' ) {
    action handleMessage( message : Message ) returns Result;
    action handleMessageV2( message : Message ) returns Result;
}