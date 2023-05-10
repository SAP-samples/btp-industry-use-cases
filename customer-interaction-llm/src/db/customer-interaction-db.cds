using { sap, managed } from '@sap/cds/common';
namespace xxx.cust.int.llm;

/**
 * A customer interaction records any interaction between customer and service provider, 
 * its purpose is to address the customer's needs,answer questions, provide support, and help them with their concerns. 
 * A customer interaction could be in-person conversations, phone calls, emails,
 * live chat, social media interactions, and more. 
 * A customer interaction could be triggered through
 * -customer leave a product review on the website 
 * -customer express feedback and concern about the product or service 
 *  on social modia(twitter,fb,ins,linkedin etc) 
 * -customer has a question about the product udate or their online order status, 
 *  then create an inquiry through Q&A chatbot on instant messaging(whatsapp,messenger,wechat etc.)
 * -customer request support about troubleshooting
 */
entity CustomerInteraction : managed {
  key ID : Integer;
  extRef : String(8);
  category : Association to CustomerInteractionCategory;
  originChannel : Association to CustomerInteractionChannel;
  status : Association to CustomerInteractionStatus;
  priority : Association to CustomerInteractionPriority;
  title : String(100);
  summary : String(300);
  tags :  String(100);
  inboundMsgs : Composition of many InboundCustomerMessage on inboundMsgs.interaction = $self;
  outboundMsgs : Composition of many OutboundServiceMessage on outboundMsgs.interaction = $self;
}

/**
 * It is used to categorise the purpose of customer interaction, 
 * such as Product Review, Customer Feedback, Q&A, Support etc.
 */
entity CustomerInteractionCategory {
  key code : String(3);
  name : String(30);
}

/**
 * the channel of customer interaction, such as social medias(twitter, face book,instgram,linkedin etc.), 
 * website, email, instant messaging(slack, whatsapp, wechat etc. ), phone call, in-person conversation etc
 */
entity CustomerInteractionChannel {
  key code : String(3);
  name : String(30);
}

/**
 * the status of a customer interaction, such as 
 * New, In-Process, Author Action, Solution Provided, Closed, Re-Opened and Confirmed
 */
entity CustomerInteractionStatus {
  key code : String(2);
  name : String(20);
}

/**
 * the priority of a customer interaction, such as 
 * Low, Medium, High, Very High 
 */
entity CustomerInteractionPriority {
  key code : String(1);
  name : String(10);
}

/**
 * An inbound customer message record the message received from customers via multiple channels
 */
entity InboundCustomerMessage : managed {
  key sequence : Integer default 1;
  key interaction : Association to CustomerInteraction;
  contact : Association to Contact;
  sentiment : String(10);
  type : Association to InboundCustomerMessageType;
  topic : Association to InboundCustomerMessageTopic;
  customer : Association to Customer;
  language : String(10);
  inboundTextMsg : String(2000);
  embedding : LargeString; //embedding vector of inboundTextMsg
  audio : Association to AudioMessage;
  summary : String(200);
  channel : Association to CustomerInteractionChannel;
  outboundServiceMsg : Association to many OutboundServiceMessage on outboundServiceMsg.replyTo = $self;
}

entity Contact {
  key ID : Integer;
  name : String(100);
  phoneNo : String(20);
  
  email: String(50);
  facebook: String(100);
  instagram: String(100);
  whatsapp: String(20);
  linkedin: String(100);
  twitter: String(100);
  slack: String(100);
  wechat: String(50);
  customer : Association to Customer;
}

entity Customer {
  key ID : String(10);
  name : String(100);
  contacts : Association to many Contact on contacts.customer = $self;
}

/**
 * The category of customer message could be 
 * Complaint,Complement,Request
 */
entity InboundCustomerMessageType {
  key code : String(2);
  name : String(20);
}

/**
 * The main topics about customer message could be 
 * Product Information: Customers may reach out to request information about a specific appliance, such as its features, specifications, and pricing.
 * Product Review: Customers may be seeking advice on which appliance would best suit their needs or fit their kitchen space.
 * Technical Support: Customers may need help troubleshooting issues with their appliance, such as a malfunctioning part or error message.
 * Installation and Setup: Customers may need guidance on how to properly install and set up their appliance, whether it's a refrigerator, dishwasher, or oven.
 * Maintenance and Cleaning: Customers may have questions about how to properly maintain and clean their appliance to ensure it runs efficiently and lasts longer.
 * Replacement Parts: Customers may need assistance in finding and ordering replacement parts for their appliance, such as a new filter or bulb.
 * Warranty Information: Customers may need to inquire about their warranty coverage or make a claim for a repair or replacement.
 * Order Status and Shipping: Customers may have questions about the status of their order or need assistance with shipping and delivery.
 * Return and Refund Inquiries: Customers may need to initiate a return or request a refund for an appliance that does not meet their expectations.
 * Feedback and Suggestions: Customers may want to provide feedback or suggestions for improving the appliance or the vendor's service.
 */
entity InboundCustomerMessageTopic {
  key code : String(2);
  name : String(50);
  descr : String(1000);
  embedding: LargeString;
}

/**
 * An audio message from customer as part of a CustomerMessage instance,
 * which is recorded from phone call with customer in call center
 */
entity AudioMessage : managed {
  key ID : Integer;
  key inboundCustomerMsg : Association to InboundCustomerMessage;
  audioData : LargeBinary;
}

/**
 * An outbound service message is in response to an inbound customer message.
 */
entity OutboundServiceMessage : managed {
  key sequence : Integer;
  key interaction : Association to CustomerInteraction;
  type : Association to OutboundServiceMessageType;
  outboundTextMsg : String(2000);
  processedBy : String(100);
  remark : String(200);
  replyTo : Association to InboundCustomerMessage;
}

/**
 * The types of an outbound service message: 
 * Auto Reply, Q&A Virtual Assistant, Generated Answer by RPA Bot, Answer by Human Agent, Internal Memo etc.
 */
entity OutboundServiceMessageType {
  key code : String(2);
  name : String(50);
}