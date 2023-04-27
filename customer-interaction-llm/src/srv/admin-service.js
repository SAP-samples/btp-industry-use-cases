const cds = require("@sap/cds/lib");
const e = require("express");

module.exports = class AdminService extends cds.ApplicationService {
  init() {
    const {
      CustomerInteraction,
      InboundCustomerMessage,
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
      let inMsgs = inboundTextMsgs.map(msg => msg.inboundTextMsg);
      inMsgs.push(req.data.inboundTextMsg);
      const text = { text: inMsgs.join("\n") };
      const LlmProxyService = await cds.connect.to("LlmProxyService");
      const result = await LlmProxyService.processCustomerMessage(text);
      const embedding = await LlmProxyService.embedding(text);
      req.data.vector = embedding;
      cds.tx (async ()=>{
        await UPDATE(CustomerInteraction, req.data.interaction_ID).with({
          title: result.data.title,
          summary: result.data.summary
        })
        await INSERT.into(InboundCustomerMessage, req.data);
      });

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
