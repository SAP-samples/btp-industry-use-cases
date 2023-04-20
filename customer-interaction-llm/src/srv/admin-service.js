const cds = require("@sap/cds/lib");
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

    // this.before(["NEW", "CREATE"], InboundCustomerMessage, async (req) => {
    //   const { sequence } = await cds
    //     .tx(req)
    //     .run(
    //       SELECT.one
    //         .from(InboundCustomerMessage)
    //         .columns("max(sequence) as sequence")
    //         .where("interaction_ID=", req.data.interaction_ID)
    //     );
    //   req.data.sequence = sequence + 1;
    // });

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
