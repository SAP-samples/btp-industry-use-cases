namespace int.ticket.srv;

type Message : {
    text: String;
}

type Result : {
    type : String;
    route : String;
    replyMessage : String;
}

service IntTicketService @( path: '/int-ticket' ) {
    action handleMessage( message : Message ) returns Result;
}
