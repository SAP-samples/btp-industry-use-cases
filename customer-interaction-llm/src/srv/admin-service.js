const cds = require("@sap/cds/lib");
const e = require("express");

module.exports = class AdminService extends cds.ApplicationService {
  init() {
    const {
      CustomerInteraction,
      InboundCustomerMessage,
      InboundCustomerMessageIntent,
      OutboundServiceMessage,
      Contact,
    } = this.entities;

    this.before(["NEW", "CREATE"], [CustomerInteraction, Contact], genid);
    this.before(
      ["NEW", "CREATE"],
      [InboundCustomerMessage, OutboundServiceMessage],
      genseq
    );

    /**
     * Handler of on creating an customer interaction with an inbound customer message
     * 1.invoke the llm-proxy to perform sentiment analysis, text summarisation
     * and entity extraction on the text message on inbound customer message
     * 2.update the sentiment on the InboundCustomerMessage instance.
     * 3.update the title and summary on CustomerInteraction
     */
    this.on(["CREATE"], CustomerInteraction, async (req) => {
      //prepare the default value for CustomerInteraction
      //default status as New if missing
      //default priority as Medium if missing
      if(typeof req.data.status_code === 'undefined' || req.data.status_code.length === 0)
        req.data.status_code = "NW";
      if(typeof req.data.priority_code === 'undefined' || req.data.priority_code.length === 0)
        req.data.priority_code = "M";
      
      req.data.extRef = generateExtRef();

      const inMsgs = req.data.inboundMsgs.map((msg) => msg.inboundTextMsg);
      const inboundText = { text: inMsgs[0] };
      const LlmProxyService = await cds.connect.to("LlmProxyService");

      //Invoke the LLM proxy to process the current inbound customer message.
      const result = await LlmProxyService.processCustomerMessage(inboundText);
      //reflect the summarised title to the inbound customer message
      req.data.summary = result.data.summary;
      req.data.title = result.data.title;
      req.data.inboundMsgs[0].summary = result.data.title;
      if (result.data.sentiment) {
        req.data.inboundMsgs[0].sentiment = result.data.sentiment;
        if (result.data.sentiment === "Positive") {
          //complement
          req.data.inboundMsgs[0].type_code = "CL";
        } else if (result.data.sentiment === "Negative") {
          //complement
          req.data.inboundMsgs[0].type_code = "CM";
        } else {
          //information
          req.data.inboundMsgs[0].type_code = "IN";
        }
      }
      //embedding the text of incoming customer message to vector.
      //and to be stored into IncomingCustomerMessage.vector field
      //will be used for classifying the intents of the text
      const embedding = await LlmProxyService.embedding(inboundText);
      req.data.inboundMsgs[0].embedding = embedding;

      //manual transaction
      cds.tx(async () => {
        await INSERT.into(CustomerInteraction, req.data);
      });

      return req.data;
    });

    /**
     * Handler of on creating an inbound customer message
     * 1.invoke the llm-proxy to perform sentiment analysis,
     * text summarisation and entity extraction
     * 2.update the sentiment on the InboundCustomerMessage instance.
     * 3.update the title and summary on parent object CustomerInteraction
     */
    this.on(["CREATE"], InboundCustomerMessage, async (req) => {
      const inboundTextMsgs = await cds
        .tx(req)
        .run(
          SELECT.from(InboundCustomerMessage)
            .columns("inboundTextMsg")
            .where("interaction_ID=", req.data.interaction_ID)
        );
      let inMsgs = inboundTextMsgs.map((msg) => msg.inboundTextMsg);
      //at this point, the new record hasn't hit the database.
      //so add the new instance of InboundCustomerMessage to the list.
      //sum up all the inbound customer messages, and
      inMsgs.push(req.data.inboundTextMsg);
      const allInboundText = { text: inMsgs.join("\n") };
      const LlmProxyService = await cds.connect.to("LlmProxyService");
      //Invoke the LLM proxy to summarise all the inbound customer messages of the interaction instance.
      //which will be used update the title and summary of CustomerInteraction instance
      const summaryResult = await LlmProxyService.summarise(allInboundText);

      //Invoke the LLM proxy to process the current inbound customer message.
      const result = await LlmProxyService.processCustomerMessage(
        req.data.inboundTextMsg
      );
      //reflect the summarised title to the inbound customer message
      req.data.summary = result.data.title;
      if (result.data.sentiment) {
        req.data.sentiment = result.data.sentiment;
        if (result.data.sentiment === "Positive") {
          //complement
          req.data.type_code = "CL";
        } else if (result.data.sentiment === "Negative") {
          //complement
          req.data.type_code = "CM";
        } else {
          //information
          req.data.type_code = "IN";
        }
      }

      //embedding the text of incoming customer message to vector.
      //and to be stored into IncomingCustomerMessage.vector field
      //will be used for classifying the intents of the text
      const embedding = await LlmProxyService.embedding(
        req.data.inboundTextMsg
      );
      req.data.embedding = embedding;

      //manual transaction
      cds.tx(async () => {
        await UPDATE(CustomerInteraction, req.data.interaction_ID).with({
          title: summaryResult.data.title,
          summary: summaryResult.data.summary,
        });
        await INSERT.into(InboundCustomerMessage, req.data);
      });

      return req.data;
    });

    /**
     * Handler of before creating an inbound customer message intent
     * 1.invoke the llm-proxy to perform embedding on the descr of 
     * inbound customer message intent
     * 2.set the value for embedding field on inbound customer message intent
     */
    this.before(["NEW","CREATE"], InboundCustomerMessageIntent, async (req) => {
      //before NEW triggered by create button on UI.
      //at this moment, only key(code) is available, thus skip embedding
      //when it is POST http call or save from UI, before create will be triggered
      if(typeof req.data.descr === 'undefined')
        return req.data;

      const descr = { text: req.data.descr };
      const LlmProxyService = await cds.connect.to("LlmProxyService");

      //embedding the description text of incoming customer message intent to vector.
      //and to be stored into IncomingCustomerMessageIntent.embedding field
      //will be used for classifying the intents of the inbound customer message
      const embedding = await LlmProxyService.embedding(descr);
      req.data.embedding = embedding;

      return req.data;
    });

    return super.init();
  }
};

/** Generate primary keys for target entity in request */
async function genid(req) {
  const { ID } = await cds
    .tx(req)
    .run(SELECT.one.from(req.target).columns("max(ID) as ID"));
  req.data.ID = ID + 1;
}

async function genseq(req) {
  const { sequence } = await cds
    .tx(req)
    .run(
      SELECT.one
        .from(req.target)
        .columns("max(sequence) as sequence")
        .where({ interaction_ID: req.data.interaction_ID })
    );
  req.data.sequence = sequence + 1;
}

function generateExtRef() {
  const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let result = "";
  for (let i = 0; i < 8; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}
