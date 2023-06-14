using { xxx.cust.int.llm as db  } from '../db/customer-interaction-db';

service CustomerService @(path : '/cust') {

  entity CustomerInteraction as projection on db.CustomerInteraction;

  @readonly
  entity CustomerInteractionCategory as projection on db.CustomerInteractionCategory;
  
  @readonly
  entity CustomerInteractionChannel as projection on db.CustomerInteractionChannel;
  
  @readonly
  entity CustomerInteractionStatus as projection on db.CustomerInteractionStatus;
  
  @readonly
  entity CustomerInteractionPriority as projection on db.CustomerInteractionPriority;
  
  @readonly
  entity InboundCustomerMessageType as projection on db.InboundCustomerMessageType;
  
  entity InboundCustomerMessage as projection on db.InboundCustomerMessage;
  entity AudioMessage as projection on db.AudioMessage;
  
  @readonly
  entity OutboundServiceMessage as projection on db.OutboundServiceMessage;
  
  @readonly
  entity OutboundServiceMessageType as projection on db.OutboundServiceMessageType;
}