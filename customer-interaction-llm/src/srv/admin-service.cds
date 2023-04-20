using { xxx.cust.int.llm as db  } from '../db/customer-interaction-db';

//@requires_ : 'authenticated-user'
service AdminService {

  entity CustomerInteraction as projection on db.CustomerInteraction actions {
    
    //inoke the llm model, output as json
    //classify the category of the interaction, 
    //summarise the text message into a title less 100 characters to and summary less than 300 characters 
    //extract the structed entities from the text message
    @sap.applicable.path : 'processByllm'
    action processByllm();
    @sap.applicable.path : 'summarise'
    action summarise();
    @sap.applicable.path : 'sentimentAnalyse'
    action sentimentAnalyse();

  };

  entity CustomerInteractionCategory as projection on db.CustomerInteractionCategory;
  entity CustomerInteractionChannel as projection on db.CustomerInteractionChannel;
  entity CustomerInteractionStatus as projection on db.CustomerInteractionStatus;
  entity CustomerInteractionPriority as projection on db.CustomerInteractionPriority;

  entity InboundCustomerMessageType as projection on db.InboundCustomerMessageType;
  entity InboundCustomerMessage as projection on db.InboundCustomerMessage actions {
    action reply();
  };
  entity AudioMessage as projection on db.AudioMessage;

  entity OutboundServiceMessageType as projection on db.OutboundServiceMessageType;
  entity OutboundServiceMessage as projection on db.OutboundServiceMessage;

  entity Contact as projection on db.Contact;
  entity Customer as projection on db.Customer;
}