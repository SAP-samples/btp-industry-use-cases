using {xxx.cust.int.llm as db} from '../db/customer-interaction-db';

//@requires_ : 'authenticated-user'
service AdminService {

  entity CustomerInteraction          as projection on db.CustomerInteraction {
    *,
    messages : Composition of many MessageThread on messages.interactionID = ID

  //inoke the llm model, output as json
  //classify the category of the interaction,
  //summarise the text message into a title less 100 characters to and summary less than 300 characters
  //extract the structed entities from the text message
  // @sap.applicable.path : 'processByllm'
  // action processByllm();
  // @sap.applicable.path : 'summarise'
  // action summarise();
  // @sap.applicable.path : 'sentimentAnalyse'
  // action sentimentAnalyse();
  };

  //Normalise the InboundCustomerMessage and OutboundServiceMessage as MessageThread
  //for showing communication history of the customer interaction in timeline.
  entity MessageThread                as
      select
        interaction.ID            as interactionID,
        interaction.customer.name as customer,
        interaction.customer.ID   as customerID,
        inboundTextMsg            as message,
        contact.name              as name,
        'Inbound'                 as direction : String(10),
        sentiment,
        summary,
        intent.name               as intent,
        createdAt
      from InboundCustomerMessage
    union
      select
        interaction.ID            as interactionID,
        interaction.customer.name as customer,
        interaction.customer.ID as customerID,
        outboundTextMsg as message,
        processedBy     as name,
        'Outbound' as direction:String(10),
        'N/A' as sentiment,
        type.name as summary,
        replyTo.intent.name as intent,
        createdAt
      from OutboundServiceMessage;

  entity CustomerInteractionCategory  as projection on db.CustomerInteractionCategory;
  entity CustomerInteractionChannel   as projection on db.CustomerInteractionChannel;
  entity CustomerInteractionStatus    as projection on db.CustomerInteractionStatus;
  entity CustomerInteractionPriority  as projection on db.CustomerInteractionPriority;
  entity InboundCustomerMessageType   as projection on db.InboundCustomerMessageType;
  entity InboundCustomerMessageIntent as projection on db.InboundCustomerMessageIntent;

  entity InboundCustomerMessage       as projection on db.InboundCustomerMessage {
    *,
    intent.name as intname @(title: '{i18n>intname}')
  } actions {
    action reply();
  };

  entity AudioMessage                 as projection on db.AudioMessage;
  entity OutboundServiceMessageType   as projection on db.OutboundServiceMessageType;
  entity OutboundServiceMessage       as projection on db.OutboundServiceMessage;
  entity Contact                      as projection on db.Contact;
  entity Customer                     as projection on db.Customer;
}
