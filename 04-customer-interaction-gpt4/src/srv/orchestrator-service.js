module.exports = cds.service.impl(async function () {
    // Connect to external services destinations
    //CTC: Destination to the sentiment analysis service
    //BR: Destination to Business Rule Service
    //FSM: Destination to FSM API
    const CTC = await cds.connect.to('CTC');
    const BR = await cds.connect.to('BR');
    const FSM = await cds.connect.to('FSM');

    const {
        CustomerInteraction
    } = this.entities;

    /**
     * Handler of AFTER-EVENT of creating an customer interaction with an inbound customer message
     * [Flow is implemented in Orchestrator Service]
     * 1. Prior to this, CustomerInteraction & InboundCustomerMessage have been created.
     * 2. Details such as ID, sequence, intent will be parsing into this function.
     * 3. BR & FSM destination should be prepared prior.
     * 4. BR: to take in intent (classification) for the required Action.
     * 5. FSM: required Action from above would create a service call in FSM.
     * 6. OutboundServiceMessage: should capture the AutoReply.
     * 
     */
    this.on('handleMessageV2', async req => {
        try {
            //  1. Prior to this, CustomerInteraction & InboundCustomerMessage have been created.
            //  2. Details such as ID, sequence, intent will be parsing into this function.
            //  3. BR & FSM destination should be prepared prior. 
            const BR = await cds.connect.to('BR');
            const FSM = await cds.connect.to('FSM');
            // console.log("Payload in handleMessageV3 as follows: " + JSON.stringify(req.data));
            console.log("In process 1-3...");


            const query = SELECT`title, summary, extRef`.from`CustomerInteraction`.where({ ID: req.data.message.interaction_ID });
            const interaction = await cds.db.run(query);

            console.log(req.data.message);
            console.log(interaction[0].title);
            console.log(interaction[0].summary);

            //  4. BR: to take in intent (classification) for the required Action.
            const classification = req.data.message.intent_code;
            const BR_payload = {
                RuleServiceId: "3a4e53b84c8e4313bc6d7922ade85809",
                RuleServiceRevision: "1",
                Vocabulary: [
                    {
                        Classification: classification
                    }
                ]
            };
            const BR_resp = await BR.post("/rules-service/rest/v2/rule-services", BR_payload);
            const action = BR_resp.Result[0].Route.Action;

            // console.log("In process 4... BR Output as route action follows:");
            // console.log(action);

            //  5. FSM: required Action from above would create a service call in FSM.
            let code = "";
            if (action === "TI-Chatbot") {
                //  this variable is for the classification intent code TI > 
                var messageintent = "Technical Issue";
                const FSM_payload = {
                    leader: null,
                    subject: interaction[0].title,
                    chargeableEfforts: false,
                    project: null,
                    owners: null,
                    objectGroup: null,
                    resolution: null,
                    syncObjectKPIs: null,
                    inactive: false,
                    partOfRecurrenceSeries: null,
                    contact: "D0725AA6243A4470A49C0052232CA898",
                    problemTypeName: null,
                    originCode: "-1",
                    problemTypeCode: null,
                    changelog: null,
                    endDateTime: "2023-12-31T09:00:00Z",
                    priority: (classification.toLocaleLowerCase() === "complaint") ? "HIGH" : "LOW",
                    branches: null,
                    salesOrder: null,
                    dueDateTime: "2023-12-31T22:59:00Z",
                    salesQuotation: null,
                    udfMetaGroups: null,
                    orderReference: null,
                    responsibles: [
                        "14523B3D57424338858CB56BBF120696"
                    ],
                    syncStatus: "IN_CLOUD",
                    statusCode: "-2",
                    businessPartner: "2827EC2EE37540918B0A556A818A3978",
                    projectPhase: null,
                    technicians: [],
                    typeName: "Unplanned",
                    chargeableMileages: false,
                    orgLevel: null,
                    chargeableMaterials: false,
                    statusName: "Ready to plan",
                    orderDateTime: null,
                    chargeableExpenses: false,
                    lastChanged: 1544172897151,
                    durationInMinutes: null,
                    serviceContract: null,
                    createPerson: "14523B3D57424338858CB56BBF120696",
                    externalId: null,
                    groups: null,
                    team: null,
                    typeCode: "-1",
                    // equipments: [
                    //     "3B981A0D8206421393DB124C2430F95E"
                    // ],
                    startDateTime: "2022-12-09T08:00:00Z",
                    location: null,
                    udfValues: null,
                    incident: null,
                    remarks: "Interaction #" + req.data.message.interaction_ID + ". ExtRefNo: " + interaction[0].extRef + ". Sentiment: " + req.data.message.sentiment + ". Intent: " + messageintent + ". Summary: " + interaction[0].summary + ".",
                    originName: "Intelligent Ticket System"
                };
                const headers = {
                    "X-Client-ID": "DemoClient",
                    "X-Client-Version": "1.0",
                    "X-Account-ID": 96388,
                    "X-Company-ID": 108432

                };
                const FSM_resp = await FSM.send("POST", "/ServiceCall/?dtos=ServiceCall.26", FSM_payload, headers);
                code = FSM_resp.data[0].serviceCall.code;

                // console.log("In process 5. FSM Output as Service Call Code follows.");
                // console.log(code);
            }

            // Respond to the requester
            const res = {
                type: classification,
                route: action,
                fsmcode: code
            };
            return res;
        } catch (err) {
            req.error(err.code, err.message);
        }
    });

    /**
     * version 1 of original intelligent ticketing system
     */
    this.on('handleMessage', async req => {
        try {
            // Grab message from payload
            const message = req.data.message;

            // Call CTC classification API passing the received message and retrieve classification
            const CTC_payload = {
                text: message.text
            };
            const CTC_resp = await CTC.post("/do-analysis", CTC_payload);
            const classification = new String(CTC_resp.overall_classification);

            // Call Business Rules API passing the classification and retreive the route
            const BR_payload = {
                RuleServiceId: "3a4e53b84c8e4313bc6d7922ade85808",
                RuleServiceRevision: "1",
                Vocabulary: [
                    {
                        Classification: classification
                    }
                ]
            };
            const BR_resp = await BR.post("/rules-service/rest/v2/rule-services", BR_payload);
            const action = BR_resp.Result[0].Route.Action;

            // If action is "CRM" then a service request must be created
            let code = "";
            if (action === "CRM") {
                const FSM_payload = {
                    leader: null,
                    subject: message.text,
                    chargeableEfforts: false,
                    project: null,
                    owners: null,
                    objectGroup: null,
                    resolution: null,
                    syncObjectKPIs: null,
                    inactive: false,
                    partOfRecurrenceSeries: null,
                    contact: "D0725AA6243A4470A49C0052232CA898",
                    problemTypeName: null,
                    originCode: "-1",
                    problemTypeCode: null,
                    changelog: null,
                    endDateTime: "2023-12-31T09:00:00Z",
                    priority: (classification.toLocaleLowerCase() === "complaint") ? "HIGH" : "LOW",
                    branches: null,
                    salesOrder: null,
                    dueDateTime: "2023-12-31T22:59:00Z",
                    salesQuotation: null,
                    udfMetaGroups: null,
                    orderReference: null,
                    responsibles: [
                        "14523B3D57424338858CB56BBF120696"
                    ],
                    syncStatus: "IN_CLOUD",
                    statusCode: "-2",
                    businessPartner: "8FA7D41CD4C448BF9A27962E9055C141",
                    projectPhase: null,
                    technicians: [],
                    typeName: "Unplanned",
                    chargeableMileages: false,
                    orgLevel: null,
                    chargeableMaterials: false,
                    statusName: "Ready to plan",
                    orderDateTime: null,
                    chargeableExpenses: false,
                    lastChanged: 1544172897151,
                    durationInMinutes: null,
                    serviceContract: null,
                    createPerson: "14523B3D57424338858CB56BBF120696",
                    externalId: null,
                    groups: null,
                    team: null,
                    typeCode: "-1",
                    equipments: [
                        "3B981A0D8206421393DB124C2430F95E"
                    ],
                    startDateTime: "2022-12-09T08:00:00Z",
                    location: null,
                    udfValues: null,
                    incident: null,
                    remarks: null,
                    originName: "Intelligent Ticket System"
                };
                const headers = {
                    "X-Client-ID": "DemoClient",
                    "X-Client-Version": "1.0",
                    "X-Account-ID": 96388,
                    "X-Company-ID": 108432

                };
                const FSM_resp = await FSM.send("POST", "/ServiceCall/?dtos=ServiceCall.26", FSM_payload, headers);
                code = FSM_resp.data[0].serviceCall.code;
            }

            // Configure reply message accourding to route
            const replyMessage = (action === "CRM") ? 'Thank you for reaching out. A service call for your ' + classification.toLocaleLowerCase() + ' with code "' + code + '" has been created in our system. A representative will contact you soon.' : "Thank you for appreciating our service. We hope to keep always satisfying your expectations!";

            // Respond to the requester
            const res = {
                type: classification,
                route: action,
                replyMessage: replyMessage
            };

            return res;
        } catch (err) {
            req.error(err.code, err.message);
        }
    });
});